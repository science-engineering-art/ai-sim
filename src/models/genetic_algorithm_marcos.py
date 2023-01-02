import random
from numpy import Inf, sort

MAX_ITERATIONS = 10000


# gets k random indexes in a list
def get_random_indexes(input_list, k=-1):
    if k < 0:
        k = random.randint(1, len(input_list))
    return list(set(random.choices(range(len(input_list)),
                                   k=k)))



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
    mutated_ind = []
    indexes = get_random_indexes(individual)
    for i in range(len(individual)):
        if i in indexes:
            cromosome = list(individual[i])
            for j in get_random_indexes(cromosome):
                cromosome[j] = '0' if cromosome[j] == '1' else '1'
            individual[i] = "".join(cromosome)
        mutated_ind.append(individual[i])
    return mutated_ind

# mutates k individuals according to the mutation rate required (%)
def mutate(encoded_pop_set, mutation_rate):
    mutated_pop = []
    indexes = get_random_indexes(encoded_pop_set, k=int(
        mutation_rate*len(encoded_pop_set)))
    for i in range(len(encoded_pop_set)):
        if i in indexes:
            mutated_pop.append(mutate_individual(encoded_pop_set[i]))
        else:
            mutated_pop.append(encoded_pop_set[i])
    return mutated_pop


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
    
    return [int(alpha * parent_a[i] + (1 - alpha) * parent_b[i]) for i in range(len(parent_a))]

def geometric_xover(parent_a, parent_b):
    
    return [int((parent_a[i] * parent_b[i]) ** 0.5) for i in range(len(parent_a))]


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
    population = init_population(
        pop_size, number_of_turns, maximum_waiting_time, average_passing_time)

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
            best_solution = (population[fitness.index(max_f)], max_f)

        # gets best solutions to create new population with cromosomes in binary
        bests, parents = select_parents_ranked(population, fitness)

        new_population = []
         # storing parents (best solutions in the current generation) for the next
        new_population += bests
        # crossovering parents
        new_population += xover(parents[0], parents[1])
        # mutating some individuals
        new_population = mutate(new_population)

        # sets cromosomes back to decimal
        new_population = decode_population(new_population)

        population = new_population
        i += 1

    return best_solution[0]


# pop = [[1, 4, 5, 10], [11, 5, 2, 1], [
#     5, 8, 4, 15], [3, 2, 54, 1], [7, 8, 23, 5]]
# fitness = [1, 9, 5, 8, 90]
# bin_p = encode_population(pop)
# print(bin_p)
# print(mutate(bin_p, 0.5))
# # print(bin_p)
# # print(get_random_indexes([1, 2, 3, 4, 5], 1))
# print(multipoint_xover("100", "202"))

# print(select_parents(pop, fitness))

# # a = [1, -9, -90, 3, 2]
# # print(a.index(min(a)))
# # a.remove(a[a.index(min(a))])
# # print(a)

# print(cromosome_xover(bin_p[0], bin_p[1]))
