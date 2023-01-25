
from queue import PriorityQueue
from traceback import print_tb
from kiwisolver import DuplicateEditVariable
from matplotlib.backend_bases import ToolContainerBase
from numpy import Inf
import models.simulation

import dictdatabase as ddb

simulation = models.simulation.Simulation_test_5()


def get_bests(number_of_test, amount = 20):

    ddb.config.storage_directory = '../tests/_all_json/'
    s = ddb.at(f'test_{number_of_test}')
    json = s.read()
    
    bests = PriorityQueue()
    
    for i in range(49):
        fitness = json[str(i)]['fitness']
        for j in range(30):
            if fitness[j] < -20:
                bests.put((-fitness[j],i,j))
     
    b = []
    for i in range(amount):
        _, i, j = bests.get()
        b.append((i,j))
    return b
                
        
        
def get_fit_with_similars(json, best):
    fit = 0
    cant = 0
    for i in range(50):
        for j in range(30):
            to_compare = json[str(i)]['population'][j]
            diff = 0
            for idx in range(len(best)):
                if best[idx] != to_compare[idx]:
                    diff+=1
                if diff > 3:
                    break
            if diff <= 3:
                print('h')
                fit += json[str(i)]['fitness'][j]
                cant += 1
    fit = fit/cant
    return fit
    
def obtain_solutions_to_compare(number_of_test):
    ddb.config.storage_directory = '../tests/_all_json/'
    
    s = ddb.at(f'test_{number_of_test}')
    json = s.read()
    fitness = json['0']['fitness']
    min_fit = min(fitness)
    pos = fitness.index(min_fit)
    worst = json['0']['population'][pos]
    
    
    indxs = get_bests(number_of_test)
    for w in range(30):
        indxs.append((49,w))
        
    best_best = []
    mx_fit = -Inf
    for ii, jj in indxs:
        best = json[str(ii)]['population'][jj]
        fit = get_fit_with_similars(json, best)
        print(fit)
        if fit > mx_fit:
            mx_fit = fit
            best_best = best
            print('w', w)
        print('done')
    print(mx_fit)
    
    # best_best = []
    # print(Inf - 2)
    # mx_fit = -Inf
    # for w in range(0,50):
    #     if json[str(w)].get('best_solution'):
    #         best = json[str(w)]['best_solution']['vector']
    #         fit = get_fit_with_similars(json, best)
    #         print(fit > mx_fit)
    #         if fit > mx_fit and fit < -20:
    #             mx_fit = fit
    #             best_best = best
    #             print('w', w)
    #         print('done')
            
    # for w in range(30):
    #     best = json['49']['population'][w]
    #     fit = get_fit_with_similars(json, best)
    #     if fit > mx_fit:
    #         mx_fit = fit
    #         best_best = best
    #         print('w', w)
    #     print('done')
    

    # fitness = json['49']['fitness']
    # max_fit = max(fitness)
    # pos = fitness.index(max_fit)
    # best = json['49']['population'][pos]
    
    # best = json['0']['best_solution']['vector']
    # for i in range(50):
    #     if json[str(i)].get('best_solution'):
    #         best = json[str(i)]['best_solution']['vector']
    
    return worst, best_best

def obatain_results(vector, numer_of_times = 5, obs_time = 10):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(vector)
    ctrl.speed = 30
    average_per_road = [0 for i in range(len(ctrl.roads))]
    total_time_take_cars = 0
    for _ in range(numer_of_times):
        ctrl.Start(observation_time=obs_time)
        
        total_time_take_cars += sum(ctrl.road_total_time_take_cars) / numer_of_times
        for i in range(len(ctrl.roads)):
            average_per_road[i] += ctrl.road_average_time_take_cars[i]/numer_of_times
        
        ctrl = simulation.get_new_control_object()
        print('here')
    
    average_per_road = [average_per_road[i] for i in sorted(range(len(average_per_road)), \
                        key = lambda x : ctrl.roads[x].lambda_, reverse=True)]
    
    return average_per_road, total_time_take_cars
    
a = obatain_results(obtain_solutions_to_compare(1)[1], numer_of_times=5) #best
b = obatain_results(obtain_solutions_to_compare(1)[0], numer_of_times=5) #worts
print([(a[0][i], b[0][i]) for i in range(len(a[0]))])
print(a[1], b[1])