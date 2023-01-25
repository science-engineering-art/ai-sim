
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
            if fitness[j] < -10:
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
            if diff <= 3 and json[str(i)]['fitness'][j] < -20:
                fit += json[str(i)]['fitness'][j]
                cant += 1
    fit = fit/cant if cant != 0 else -Inf
    return fit
    
def obtain_solutions_to_compare(number_of_test):
    
    ddb.config.storage_directory = '../tests/_all_json/'
    s = ddb.at(f'test_{number_of_test}')
    json = s.read()
    
    fitness = json['0']['fitness']
    min_fit = min(fitness)
    pos = fitness.index(min_fit)
    any = json['0']['population'][pos]
    
    
    indxs = get_bests(number_of_test)
    for w in range(30):
        indxs.append((49,w))
        
    mx_fit = -Inf
    best_best = []
    for ii, jj in indxs:
        best = json[str(ii)]['population'][jj]
        fit = get_fit_with_similars(json, best)
        if fit > mx_fit:
            mx_fit = fit
            best_best = best
            print('w', w)
    
    return (any, best_best)

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
    
    average_per_road = [average_per_road[i] for i in sorted(range(len(average_per_road)), \
                        key = lambda x : ctrl.roads[x].lambda_, reverse=True)]
    
    return average_per_road, total_time_take_cars, sum(average_per_road)/len(average_per_road)

name = 'other_results4'
ddb.config.storage_directory = '../ddb_storage/'
s = ddb.at(name)
if not s.exists():
    s.create({'results' : {}})
for i in range(42,54):
    any, best = obtain_solutions_to_compare(i)
    ave_b, total_b, sum_ave_b = obatain_results(best, numer_of_times = 5)
    ave, total, sum_ave = obatain_results(any, numer_of_times = 5)
    ddb.config.storage_directory = '../ddb_storage/'
    with ddb.at(name, key = 'results').session() as (session, results):
        results[str(i)] = {'average_per_road_b' : ave_b, 'total_time_take_cars_b' : total_b,  'average_all_roads_b' : sum_ave_b, \
                          'average_per_road' : ave, 'total_time_take_cars' : total,  'average_all_roads' : sum_ave  }
        session.write()