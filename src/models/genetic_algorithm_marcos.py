import random
from numpy import Inf, sort



MAX_ITERATIONS = 100
    

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
                individual[i] = random.randint(average_passing_time, maximum_waiting_time)
    return population_set

# Assign to each individual a probability of being a parent based on the ranking based on fitness.
# Then the two arrays of parents are selected randomly from the population according to the
# probabilities assigned. It is considered here that the new population must be equally large
# to the current one, that the best_amount best individual will prevale and that each couple
# of parents produce two children. 
def select_parents_ranked(population_set, fitness_set, bests_amount = 2, s = 1.8):
    
    pop_len = len(population_set)
    parents_amount = (pop_len - bests_amount)//2
    if (pop_len - bests_amount) % 2 != 0: 
        parents_amount += 1
        bests_amount -= 1
    
    order = sorted(range(pop_len), key = lambda i: fitness_set[i])
    weights = [0 for _ in range(pop_len)]
    for i in range(pop_len):
        weights[order[i]] =  (2 - s)/pop_len + (2*(i)*(s-1))/(pop_len * (pop_len - 1))

    parents = [[], []]
    parents_a_indexes = random.choices(population=range(pop_len),k=parents_amount, weights=weights)
    for p_a in parents_a_indexes:
        record = weights[p_a]
        weights[p_a] = 0
        parents[1].append(random.choices(population=population_set,k=1, weights=weights)[0])
        weights[p_a] = record
    parents[0] = [population_set[parents_a_indexes[i]] for i in range(parents_amount)]
    
    bests = [population_set[order[pop_len - i]] for i in range(1, bests_amount + 1)] #two best parents
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

def intermediate_xover(parent_a, parent_b, alpha = 0.5):
    
    return [[int(alpha * parent_a[i] + (1 - alpha) * parent_b[i]) for i in range(len(parent_a))]]

def geometric_xover(parent_a, parent_b):
    
    return [[int((parent_a[i] * parent_b[i]) ** 0.5) for i in range(len(parent_a))]]


# performs crossover (of individuals or cromosomes) between parents
def xover(parent_a, parent_b):
    new_population = []
    for i in range(len(parent_a)):
        new_population += multipoint_xover(parent_a[i], parent_b[i])
    return new_population

# evaluates an individual in the simulation returning queue size in relation to waiting time
def eval_individual_in_simulation(simulation, individual):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(individual)
    ctrl.speed = 10
    print(individual)
    ctrl.Start(observation_time = 5, draw=False)
    fitness_val = -1
    for road_id in range(len(ctrl.roads)):
        if not ctrl.is_curve[road_id]:
            fitness_val = max(fitness_val, ctrl.road_average_time_take_cars[road_id]) #we use the max between average time a car takes in every semaphore
    return -fitness_val * ctrl.dt #I use the opposite value because we wish to diminish the time it takes for the cars


# gives a fitness value to each individual of the population
def fitness(simulation, population):
    fitness = []
    for individual in population:
        fitness.append(eval_individual_in_simulation(simulation, individual))
    return fitness

# algorithm stops after a fixed number of iterations
def stop_criterion(i):
    return i >= MAX_ITERATIONS

# main method of the genetic algorithm
def genetic_algorithm(simulation, pop_size, number_of_turns, maximum_waiting_time, average_passing_time, max_iterations = 100):
    # init
    population = init_population(
        pop_size, number_of_turns, maximum_waiting_time, average_passing_time)

    # generation number
    i = 0

    # best solution found
    best_solution = ([], -Inf)  # (solution, fitness value)

    while i < max_iterations:
        fitness_vals = fitness(simulation, population)
        
        print(f'Iteration {i} DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # for individual in population:
        #     print(individual)
        print(fitness_vals)
        print(f'Best Solution found:{best_solution[1]} !!!!!')

        # saves the solution with the greatest fitness in the current generation if it is better that the stored
        # in best solution
        max_f = max(fitness_vals)
        if max_f > best_solution[1]:
            best_solution = (population[fitness_vals.index(max_f)], max_f)

        # gets best solutions to create new population with cromosomes in binary
        bests, parents = select_parents_ranked(population, fitness_vals)

        new_population = []
        # storing parents (best solutions in the current generation) for the next
        new_population += bests
        # crossovering parents
        new_population += xover(parents[0], parents[1])
        # mutating some individuals
        new_population = mutate_random(new_population, 1/number_of_turns, maximum_waiting_time, average_passing_time)

        population = new_population
        i += 1

    return best_solution[0]

