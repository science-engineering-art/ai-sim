



from collections import deque
from copy import deepcopy
from math import e, factorial
import random
from pygame import init
from models.road import Road
from models.vehicle import Vehicle

class navigation():
    
    def __init__(self, ctrl):
        self.cars = []
        self. ctrl = ctrl
    
    def NewRandomVehicle(self):
        '''Creates a random vehicle with probability prob'''

        cars = []
        roads_id = []

        for road_id in self.ctrl.extremeRoads:
            road = self.ctrl.roads[road_id]

            r = random.random()
            if r > navigation.__poisson(road.lambda_, self.ctrl.dt, 1):
                continue

            s = deque()
            # select uniformly the vehicle template (i.e. color, length, speed)
            car: Vehicle = deepcopy(random.choice(self.ctrl.basic_vehicles))
            
            if len(road.vehicles) > 0 and road.vehicles[len(road.vehicles) - 1].x < car.length:
                continue
            road.vehicles.append(car)
            self.cars.append(car)
            cars.append(car)
            roads_id.append(road_id)

        return cars, roads_id
    
    def NextRoad(self, vehicle: Vehicle, road: Road):
    
        if not road.end_conn:  # if nothing is associated with the end of the road
            return  # means the road end in the edge of the map
        ctrl = self.ctrl
        # we select the next corner road that can be reached from the current one, 
        # taking into account the flow of cars on each of these roads
        maxx_id = (-1, -1)
        reordered_options = deepcopy(road.end_conn.follow[ctrl.road_index[road]])
        random.shuffle(reordered_options)
        _break = False
        for i in reordered_options:
            _, prob = maxx_id
            if prob < ctrl.roads[i].lambda_:  # if the probability is higher than the previous one
                maxx_id = (i, ctrl.roads[i].lambda_)
            if random.random() < navigation.__poisson(ctrl.roads[i].lambda_, ctrl.dt, 1):
                next_road_id = i
                _break = True
                print(f'!!!!!!!!!!!!!!!\n break:{_break} BREAK\n!!!!!!!!!!!!!!!')
                break
        else:
            # by default we select the one that is most likely to occur
            print(f'!!!!!!!!!!!!!!!\nbreak:{_break} DEFAULT\n!!!!!!!!!!!!!!!')
            next_road_id = maxx_id[0]

        road_id = ctrl.roads.index(road)
        next_road_connec: ctrl.connection_road = ctrl.our_connection[(road_id, next_road_id)]
        next_road_connec.roads[0].vehicles.append(vehicle)
        
        return next_road_connec
    
    def __poisson(Lambda: float, t: float, x: int):
        Lambda *= t
        return Lambda**x * (e**(-Lambda)) / factorial(x)
