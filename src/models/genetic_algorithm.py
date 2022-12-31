import random
from numpy import Inf

MAX_ITERATIONS = 10000


# gets k random indexes in a list
def get_random_indexes(input_list, k=-1):
    if k < 0:
        k = random.randint(1, len(input_list))
    return list(set(random.choices(range(len(input_list)),
                                   k=k)))


# converts each cromosome from int to binary
def encode_population(population_set):
    encoded_population_set = []
    for individual in population_set:
        encoded_population_set.append([bin(i)[2:] for i in individual])
    return encoded_population_set


# converts each cromosome from binary to int
def decode_population(population_set):
    decoded_population_set = []
    for individual in population_set:
        decoded_population_set.append([int(i, 2) for i in individual])
    return decoded_population_set


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

            # individual.append(random.randint(average_passing_time, maximum_waiting_time),  # green time
            #                   random.randint(average_passing_time, maximum_waiting_time))  # red time

        population_set.append(individual)

    return population_set


# evaluates an individual in the simulation returning queue size in relation to waiting time
def eval_individual_in_simulation():
    pass


# gives a fitness value to each individual of the population
def fitness():
    pass


# to mutate an individual (encoded) it randomly takes k indexes in n cromosomes (also random)
# and changes '1's to '0's and '0's to '1's in them
def mutate_individual(individual):
    for i in get_random_indexes(individual):
        cromosome = list(individual[i])
        for j in get_random_indexes(cromosome):
            cromosome[j] = '0' if cromosome[j] == '1' else '1'
        individual[i] = "".join(cromosome)


# mutates k individuals according to the mutation rate required (%)
def mutate(encoded_pop_set, mutation_rate):
    for i in get_random_indexes(encoded_pop_set, k=int(
            mutation_rate*len(encoded_pop_set))):
        mutate_individual(encoded_pop_set[i])


# selects the individuals from the current population whose fitness value is greater than the average fitness value
# then, it separates them into two lists equally sized (if the number of individuals chosen is not even,
# the minimum of them is removed)
def select_parents(population_set, fitness_set):
    avg = 0
    for fitness in fitness_set:
        avg += fitness
    avg = avg / len(fitness_set)

    parents = []
    parents_fitness = []
    for i in range(len(population_set)):
        if fitness_set[i] >= avg:
            parents.append(population_set[i])
            parents_fitness.append(fitness_set[i])
            
    #patch to guarantee parents len is at least two
    if len(parents) == 1:
        if fitness_set[0] >= avg:
            parents.append(population_set[1])
            parents_fitness.append(fitness_set[1])
        else:
            parents.append(population_set[0])
            parents_fitness.append(fitness_set[0])

    if len(parents) % 2 != 0:
        i = parents_fitness.index(min(parents_fitness))
        parents.remove(parents[i])
        parents_fitness.remove(parents_fitness[i])
    return parents, [parents[0:len(parents)//2], parents[len(parents)//2:]]


# random crossover points are selected and the alternating segments of the individuals are swapped to get new offsprings.
def multipoint_xover(parent_a, parent_b, p=1):
    offsprings = [[], []]

    last = (0, parent_a)  # point, parent

    points = get_random_indexes(parent_a if len(
        parent_a) <= len(parent_b) else parent_b, p)
    points.sort()

    for i in points:
        offsprings[0] += last[1][last[0]:i]
        offsprings[1] += parent_b[last[0]:i] if last[1] == parent_a else parent_a[last[0]:i]
        last = (i, parent_b if last[1] == parent_a else parent_a)
    offsprings[0] += last[1][last[0]:]
    offsprings[1] += parent_b[last[0]:] if last[1] == parent_a else parent_a[last[0]:]

    return offsprings


# it uses multi point crossover as described above, but this time with cromosomes instead of individuals
def cromosome_xover(individual_a, individual_b):
    pass


# performs crossover (of individuals or cromosomes) between parents
def xover(parent_a, parent_b):
    # TODO: decide when to xover cromosomes and when individuals
    new_population = []
    for i in range(len(parent_a)):
        new_population += multipoint_xover(parent_a[i], parent_b[i])
    return new_population


# algorithm stops after a fixed number of iterations
def stop_criterion(i):
    return i >= MAX_ITERATIONS


# main method of the genetic algorithm
def genetic_algorithm(pop_size, number_of_turns, maximum_waiting_time, average_passing_time):
    # init
    population = [init_population(
        pop_size, number_of_turns, maximum_waiting_time, average_passing_time)]

    # generation number
    i = 0

    # best solution found
    best_solution = ([], -Inf)  # (solution, fitness value)

    while not stop_criterion(i):
        # TODO: get fitness of each individual in population
        fitness = []

        # saves the solution with the greatest fitness in the current generation if it is better that the stored
        # in best solution
        max_f = max(fitness)
        if max_f > best_solution[1]:
            best_solution = (population[i][fitness.index(max_f)], max_f)

        # gets best solutions to create new population with cromosomes in binary
        best_solutions, parents = select_parents(
            encode_population(population[i]), fitness)

        # TODO: manage population size

        new_population = []
        # storing parents (best solutions in the current generation) for the next
        new_population += best_solutions
        # crossovering parents
        new_population += xover(parents[0], parents[1])
        # mutating some individuals
        mutate(new_population)

        # sets cromosomes back to decimal
        new_population = decode_population(new_population)

        population.append(new_population)
        i += 1

    return best_solution[0]

# pop = [[1, 4, 5, 10], [11, 5, 2, 1], [5, 8, 4, 15]]
# bin_p = encode_population(pop)
# print(bin_p)
# mutate(bin_p, 0.5)
# print(bin_p)
# print(get_random_indexes([1, 2, 3, 4, 5], 1))
# print(multipoint_xover("1111", "2222"))


# a = [1, -9, -90, 3, 2]
# print(a.index(min(a)))
# a.remove(a[a.index(min(a))])
# print(a)
