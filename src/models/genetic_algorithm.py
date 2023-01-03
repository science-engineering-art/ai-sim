import random
import os
import sys
from numpy import Inf

from sklearn import cross_decomposition

from models.control import control

MAX_ITERATIONS = 100

EVAL_INDIVIDUAL_IN_SIMULATION_MAX_AVERAGE = 0
EVAL_INDIVIDUAL_IN_SIMULATION_TOTAL = 1
EVAL_INDIVIDUAL_IN_SIMULATION_WEIGTHED_MEAN = 2

GET_WEIGHTS_FIT_PROPORTIONAL = 0
GET_WEIGHTS_BY_RANKING = 1

MULTIPOINT_XOVER = 0
INTERMEDIATE_XOVER = 1
GEOMETRIC_XOVER = 2

# gets k random indexes in a list
def get_random_indexes(input_list, k=-1):
    if k < 0:
        k = random.randint(1, len(input_list))
    return list(set(random.choices(range(len(input_list)),
                                   k=k)))


# initialites the population with random values between the average passing time (time that takes a car to cross a road)
# and the maximum waiting time
# each individual contains a list with the green times of each turn (disjoint semaphores in the intersection)
def init_population(pop_size, number_of_turns, maximum_waiting_time, average_passing_time):
    population_set = []

    for i in range(pop_size):
        individual = []
        for j in range(number_of_turns):
            individual.append(random.randint(
                average_passing_time, maximum_waiting_time))

        population_set.append(individual)

    return population_set

# mutates k individuals according to the mutation probability of replace a gen by a random
# valid number
def mutate_random(population_set, mutation_probability, maximum_waiting_time, average_passing_time):
    for individual in population_set:
        for i in range(len(individual)):
            r = random.random()
            if r < mutation_probability:
                individual[i] = random.randint(
                    average_passing_time, maximum_waiting_time)
    return population_set


def get_weights_fit_proportional(pop_len, order, fitness_set):
    
    total = sum(fitness_set)
    weigths = [x/total for x in fitness_set]
    return weigths

def get_weights_by_ranking(pop_len, order, fitness_set, s = 1.8):
    
    weights = [0 for _ in range(pop_len)]
    for i in range(pop_len):
        weights[order[i]] = (2 - s)/pop_len + (2*(i)*(s-1)
                                               )/(pop_len * (pop_len - 1))
    return weights


# Assign to each individual a probability of being a parent based on weight_method criteria.
# Then the two arrays of parents are selected randomly from the population according to the
# probabilities assigned. It is considered here that the new population must be equally large
# to the current one, that the best_amount best individual will prevale and that each couple
# of parents produce two children.
def select_parents(population_set, fitness_set, bests_amount=2, weight_method = GET_WEIGHTS_BY_RANKING):

    pop_len = len(population_set)
    parents_amount = (pop_len - bests_amount)//2
    if (pop_len - bests_amount) % 2 != 0:
        parents_amount += 1
        bests_amount -= 1

    order = sorted(range(pop_len), key=lambda i: fitness_set[i])
    
    weight_methods = (get_weights_fit_proportional, get_weights_by_ranking)
    weights = weight_methods[weight_method](pop_len, order, fitness_set)

    parents = [[], []]
    parents_a_indexes = random.choices(population=range(
        pop_len), k=parents_amount, weights=weights)
    for p_a in parents_a_indexes:
        record = weights[p_a]
        weights[p_a] = 0
        parents[1].append(random.choices(
            population=population_set, k=1, weights=weights)[0])
        weights[p_a] = record
    parents[0] = [population_set[parents_a_indexes[i]]
                  for i in range(parents_amount)]

    bests = [population_set[order[pop_len - i]]
             for i in range(1, bests_amount + 1)]  # two best parents
    return bests, parents

# random crossover points are selected and the alternating segments of the individuals are swapped to get new offsprings.
def multipoint_xover(parent_a, parent_b, p=1):
    offsprings = [[], []]

    last = (0, parent_a)  # point, parent

    points = get_random_indexes(parent_a if len(
        parent_a) <= len(parent_b) else parent_b, p)
    points.sort()

    for i in points:
        offsprings[0] += last[1][last[0]:i]
        offsprings[1] += parent_b[last[0]                                  
            :i] if last[1] == parent_a else parent_a[last[0]:i]
        last = (i, parent_b if last[1] == parent_a else parent_a)
    offsprings[0] += last[1][last[0]:]
    offsprings[1] += parent_b[last[0]                              
        :] if last[1] == parent_a else parent_a[last[0]:]

    return offsprings


def intermediate_xover(parent_a, parent_b, alpha=0.5):

    return [[int(alpha * parent_a[i] + (1 - alpha) * parent_b[i]) for i in range(len(parent_a))], random.choice([parent_a, parent_b])]


def geometric_xover(parent_a, parent_b):

    return [[int((parent_a[i] * parent_b[i]) ** 0.5) for i in range(len(parent_a))], random.choice([parent_a, parent_b])]


# performs crossover (of individuals or cromosomes) between parents
def xover(parent_a, parent_b, xover_method = MULTIPOINT_XOVER):
    crossover_methods = [multipoint_xover, intermediate_xover, geometric_xover]
    new_population = []
    for i in range(len(parent_a)):
        new_population += crossover_methods[xover_method](parent_a[i], parent_b[i])
    return new_population

# evaluates an individual in the simulation returning queue size in relation to waiting time


def eval_individual_in_simulation_max_average(simulation, individual, speed, obs_time):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(individual)
    ctrl.speed = speed
    ctrl.Start(observation_time=obs_time, draw=False)
    fitness_val =-1
    for road_id in range(len(ctrl.roads)):
        if not ctrl.is_curve[road_id]:
            # We use the max between average time a car takes in every semaphore
            fitness_val = max(
                fitness_val, ctrl.road_average_time_take_cars[road_id])
            
    # We use the opposite value because we wish to diminish the time it takes for the cars
    return -fitness_val

def eval_individual_in_simulation_total(simulation, individual, speed, obs_time):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(individual)
    ctrl.speed = speed
    ctrl.Start(observation_time=obs_time, draw=False)
    fitness_val = 0
    for road_id in range(len(ctrl.roads)):
        if not ctrl.is_curve[road_id]:
            fitness_val += ctrl.road_total_time_take_cars[road_id]
    
    # We use the opposite value because we wish to diminish the time it takes for the cars
    return -fitness_val

def eval_individual_in_simulation_weigthed_mean(simulation, individual, speed, obs_time):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(individual)
    ctrl.speed = speed
    ctrl.Start(observation_time=obs_time, draw=False)
    fitness_val = 0
    sumsq = 0
    for road_id in range(len(ctrl.roads)):
        if not ctrl.is_curve[road_id]:
            fitness_val += ctrl.road_average_time_take_cars[road_id] * ctrl.road_total_amount_cars[road_id]**2
            sumsq += ctrl.road_total_amount_cars[road_id]**2
   
    # We use the opposite value because we wish to diminish the time it takes for the cars
    return -fitness_val / sumsq



# gives a fitness value to each individual of the population
def fitness(simulation, population, speed, obs_time, eval_method = EVAL_INDIVIDUAL_IN_SIMULATION_TOTAL):
    fitness = []
    
    eval = [eval_individual_in_simulation_max_average, eval_individual_in_simulation_total, eval_individual_in_simulation_weigthed_mean ]
    for individual in population:
        fitness.append(eval[eval_method](
            simulation, individual, speed, obs_time))
    return fitness


# main method of the genetic algorithm
def genetic_algorithm(simulation, pop_size, number_of_turns, maximum_waiting_time, average_passing_time, 
                      speed, obs_time, max_iterations=100, xover_method = MULTIPOINT_XOVER,
                      weight_method = GET_WEIGHTS_BY_RANKING, eval_method = EVAL_INDIVIDUAL_IN_SIMULATION_TOTAL):
    # init
    population = init_population(
        pop_size, number_of_turns, maximum_waiting_time, average_passing_time)

    # generation number
    i = 0

    # best solution found
    best_solution = ([], -Inf)  # (solution, fitness value)

    f = test_storage_init(max_iterations, pop_size, number_of_turns, maximum_waiting_time, average_passing_time, 
                          speed, xover_method, weight_method, eval_method, obs_time)

    while i < max_iterations:
        
        fitness_vals = fitness(simulation, population, speed, obs_time, eval_method = eval_method)
        test_storage_iteration(f, population, fitness_vals, i)
        
        print(fitness_vals)

        # saves the solution with the greatest fitness in the current generation if it is better that the stored
        # in best solution
        max_f = max(fitness_vals)
        if max_f > best_solution[1]:
            best_solution = (population[fitness_vals.index(max_f)], max_f)
            f.write(f'Better solution FOUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! \n')
            f.write(f'best solution: {best_solution} \n\n')

        print(
            f'Iteration {i} DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        # gets best solutions to create new population with cromosomes in binary
        bests, parents = select_parents(population, fitness_vals, weight_method=weight_method)

        new_population = []
        # storing parents (best solutions in the current generation) for the next
        new_population += bests
        # crossovering parents
        new_population += xover(parents[0], parents[1], xover_method = xover_method)
        # mutating some individuals
        new_population = mutate_random(
            new_population, 1/number_of_turns, maximum_waiting_time, average_passing_time)

        population = new_population
        i += 1

    f.write(f"Genetic algorithm ENDED!!!!!!!!!! \n")
    f.write(f'Final solution: {best_solution}')
    f.close()
    
    return best_solution[0]

def test_storage_iteration(f, population, fitness_vals, i):
    
    f.write(f"Generation {i} \n\n")
    f.write(f"Population: \n")
    for individual in population:
        f.write(f"{individual} \n")
        print(individual)
    f.write(f"\n")
    f.write(f"fitness: {fitness_vals} \n\n")
    
    f.write(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Best Solution of this population: \n')
    j = fitness_vals.index(max(fitness_vals))
    f.write(f'{population[j]}')
    f.write(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!With a fitness of : \n')
    f.write(f'{fitness_vals[j]}\n\n')

def test_storage_init(max_iterations, pop_size, number_of_turns, maximum_waiting_time, average_passing_time, speed, xover_method, weight_method, eval_method, obs_time):
    
    tests_path = os.path.dirname(__file__)
    if sys.platform.startswith('win'):
        tests_path = tests_path.replace('src\\models', 'tests\\')
    else:
        tests_path = tests_path.replace('src/models', 'tests/')

    file_name = f'test_{max_iterations}_{pop_size}_{number_of_turns}_{maximum_waiting_time}_{average_passing_time}_{speed}'
    ls = os.listdir(tests_path)
    print(ls)

    test_number = 0
    for file in ls:
        if file.startswith(file_name):
            test_number += 1

    if test_number != 0:
        file_name += f'_({test_number})'
    file_name += '.txt'

    print(file_name)

    f = open(tests_path + file_name, "w")

    f.write(f"xover_method: {xover_method} \n\n")
    f.write(f"weight_method: {weight_method} \n\n")
    f.write(f"eval_method: {eval_method} \n\n")
    f.write(f"MAX_ITERATIONS: {max_iterations} \n\n")
    f.write(f"SPEED: {speed} \n\n")
    f.write(f"OBSERVATION_TIME: {obs_time} \n\n")
    
    return f