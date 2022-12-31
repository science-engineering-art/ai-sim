from matplotlib.hatch import HorizontalHatch
from models.control import control
from models.genetic_algorithm import *
from models.simulation import Simulation, Simulation_test_3



# evaluates an individual in the simulation returning queue size in relation to waiting time
def eval_individual_in_simulation(individual):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(individual)
    print(individual)
    ctrl.Start(it_amount = 10000, draw=False)
    fitness_val = -1
    for road_id in range(len(ctrl.road_max_queue)):
        if not ctrl.is_curve[road_id]:
            fitness_val = max(fitness_val, ctrl.road_average_time_take_cars[road_id]) #we use the max between average time a car takes in every semaphore
    return -fitness_val #I use the opposite value because we wish to diminish the time it takes for the cars


# gives a fitness value to each individual of the population
def fitness(population):
    fitness = []
    for individual in population:
        fitness.append(eval_individual_in_simulation(individual))
    return fitness

# main method of the genetic algorithm
def genetic_algorithm(pop_size, number_of_turns, maximum_waiting_time, average_passing_time):
    # init
    population = [init_population(
        pop_size, number_of_turns, maximum_waiting_time, average_passing_time)]

    # generation number
    i = 0

    # best solution found
    best_solution = ([], -Inf)  # (solution, fitness value)

    while i < MAX_ITERATIONS:
        print(f'Iteration {i} DONE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # TODO: get fitness of each individual in population
        fitness_vals = fitness(population[i])

        # saves the solution with the greatest fitness in the current generation if it is better that the stored
        # in best solution
        max_f = max(fitness_vals)
        if max_f > best_solution[1]:
            best_solution = (population[i][fitness_vals.index(max_f)], max_f)

        # gets best solutions to create new population with cromosomes in binary
        best_solutions, parents = select_parents(
            encode_population(population[i]), fitness_vals)

        # TODO: manage population size

        new_population = []
        # storing parents (best solutions in the current generation) for the next
        new_population += best_solutions
        # crossovering parents
        new_population += xover(parents[0], parents[1])
        # mutating some individuals
        mutate(new_population, 0)

        # sets cromosomes back to decimal
        new_population = decode_population(new_population)

        population.append(new_population)
        i += 1

    return best_solution[0]

simulation = Simulation_test_3()
MAX_ITERATIONS = 10
genetic_algorithm(4, 15, 1000, 10)



# print(ctrl.corners[0].turns)    
# ctrl = new_simulation()
# print(ctrl.GetDimension())
# t1 = 100
# t2 = 400
# ctrl.SetConfiguration([t1,t2,t2,t2,t1,t2,t2,t2,t1,t2,t2,t2,t1,t2,t2])
# # ctrl.Start(it_amount= 10000, draw=False)
# ctrl.Start(it_amount= 10000, draw=True)

# to_print_1 = []
# to_print_2 = []
# for road_id in range(len(ctrl.road_max_queue)):
#     if not ctrl.is_curve[road_id]:
#         to_print_1.append(ctrl.road_max_queue[road_id])
#         to_print_2.append(ctrl.road_average_time_take_cars[road_id])
# print(to_print_1)
# print(to_print_2)
