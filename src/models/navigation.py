import heapq
import random
from copy import deepcopy
from math import e, factorial
from collections import deque
from models.vehicle import Vehicle

class navigation():
    
    def __init__(self, ctrl):
        self.cars = []
        self.fixed_vehicles = []
        self. ctrl = ctrl

    def NewRandomVehicle(self, time=-1):
        '''Creates a random vehicle with probability prob'''

        cars = []
        roads_id = []

        for road_id in self.ctrl.extremeRoads:
            road = self.ctrl.roads[road_id]

            r = random.random()
            if r > navigation.__poisson(road.lambda_, self.ctrl.dt, 1):
                continue

            # select uniformly the vehicle template (i.e. color, length, speed)
            car: Vehicle = deepcopy(random.choice(self.ctrl.basic_vehicles))
            
            if len(road.vehicles) > 0 and road.vehicles[len(road.vehicles) - 1].x < car.length:
                continue
            road.vehicles.append(car)
            car.path = [road_id]; car.current_road_in_path = 0
            self.cars.append(car)
            cars.append(car)
            roads_id.append(road_id)

        # print(self.fixed_vehicles, self.cars)

        # new_fv = []
        # if len(self.fixed_vehicles) == 0 or self.fixed_vehicles[0][0] > time: 
        #     return cars, roads_id
        # print(f'\n\nTIME: {time} < {self.fixed_vehicles[0][0]}  <<<====>>>  {self.fixed_vehicles}\n\n')

        # while len(self.fixed_vehicles) > 0 and self.fixed_vehicles[0][0] <= time:
        #     _, vehicle = heapq.heappop(self.fixed_vehicles)

        #     road = self.ctrl.roads[vehicle.path[0]]
        #     l = len(road.vehicles)
        #     if l == 0 or (road.vehicles[l - 1].x < road.vehicles[l - 1].length): 
        #         road.vehicles.append(vehicle)
        #         self.cars.append(vehicle)
        #         cars.append(vehicle)
        #         roads_id.append(vehicle.path[0])
        #     else: new_fv.append(vehicle)
        
        return cars, roads_id

    def NextRoad(self, vehicle: Vehicle):


        road_id = vehicle.path[vehicle.current_road_in_path]
        ctrl = self.ctrl
        road = ctrl.roads[road_id]
    
        if not road.end_conn:  # if nothing is associated with the end of the road
            return  # means the road end in the edge of the map
        
        if vehicle.current_road_in_path < len(vehicle.path) - 1:
            next_road_id =  vehicle.path[vehicle.current_road_in_path + 1]
        else:
            # we select the next corner road that can be reached from the current one, 
            # taking into account the flow of cars on each of these roads
            next_road_id = random.choices(
                population=road.end_conn.follow[ctrl.road_index[road]], 
                weights=[navigation.__poisson(ctrl.roads[i].lambda_, ctrl.dt, 1) 
                    for i in road.end_conn.follow[ctrl.road_index[road]]],
                k = 1)[0]

            vehicle.path.append(next_road_id)

        next_road_connec  = ctrl.our_connection[(road_id, next_road_id)]
        return next_road_connec
    
    def __poisson(Lambda: float, t: float, x: int):
        if t == 0:
            t = 1e-8
        Lambda *= t
        return Lambda**x * (e**(-Lambda)) / factorial(x)
