
from queue import PriorityQueue
from kiwisolver import DuplicateEditVariable
import models.simulation

import dictdatabase as ddb


    
    
simulation = models.simulation.Simulation_test_5()
def obtain_solutions_to_compare(number_of_test):
    ddb.config.storage_directory = '../../tests/_all_json/'
    
    s = ddb.at(f'test_{number_of_test}')
    json = s.read()
    fitness = json['0']['fitness']
    min_fit = min(fitness)
    pos = fitness.index(min_fit)
    worst = json['0']['population'][pos]
    
    best = json['0']['best_solution']['vector']
    for i in range(50):
        if json[str(i)].get('best_solution'):
            best = json[str(i)]['best_solution']['vector']
    
    return worst, best

def obatain_results(vector, numer_of_times = 5, obs_time = 10):
    ctrl = simulation.get_new_control_object()
    ctrl.SetConfiguration(vector)
    ctrl.speed = 30
    average_per_road = [0 for i in range(len(ctrl.roads))]
    total_time_take_cars = 0
    for _ in range(numer_of_times):
        ctrl.Start(observation_time=obs_time)
        
        total_time_take_cars += sum(ctrl.total_time_take_cars) / numer_of_times
        for i in range(len(ctrl.roads)):
            average_per_road[i] += ctrl.road_average_time_take_cars[i]/numer_of_times
        
        ctrl = simulation.get_new_control_object()
        
    return average_per_road, total_time_take_cars
    
print(obatain_results(obtain_solutions_to_compare(2)[1]))
print(obatain_results(obtain_solutions_to_compare(2)[0]))