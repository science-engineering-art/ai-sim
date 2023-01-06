import random
from copy import deepcopy
from math import e, factorial
from collections import deque
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
            car.path = [road]; car.current_road_in_path = 0
            self.cars.append(car)
            cars.append(car)
            roads_id.append(road_id)

        return cars, roads_id
    
    def NextRoad(self, vehicle: Vehicle):

        road = vehicle.path[vehicle.current_road_in_path]
    
        if not road.end_conn:  # if nothing is associated with the end of the road
            return  # means the road end in the edge of the map
        
        ctrl = self.ctrl
        road_id = ctrl.road_index[road]
        
        if vehicle.current_road_in_path < len(vehicle.path) - 1:
            next_road_id =  ctrl.road_index[vehicle.path[vehicle.current_road_in_path + 1]]
        else:
            # we select the next corner road that can be reached from the current one, 
            # taking into account the flow of cars on each of these roads

            next_road_id = random.choices(
                population=road.end_conn.follow[ctrl.road_index[road]], 
                weights=[navigation.__poisson(ctrl.roads[i].lambda_, ctrl.dt, 1) 
                    for i in road.end_conn.follow[ctrl.road_index[road]]],
                k = 1)[0]
                        
            # maxx_id = (-1, -1)
            # reordered_options = deepcopy(road.end_conn.follow[ctrl.road_index[road]])
            # random.shuffle(reordered_options)
            # for i in reordered_options:
            #     _, prob = maxx_id
            #     if prob < ctrl.roads[i].lambda_:  # if the probability is higher than the previous one
            #         maxx_id = (i, ctrl.roads[i].lambda_)
            #     if random.random() < navigation.__poisson(ctrl.roads[i].lambda_, ctrl.dt, 1):
            #         next_road_id = i
            #         # _break = True
            #         # print(f'!!!!!!!!!!!!!!!\n break:{_break} BREAK\n!!!!!!!!!!!!!!!')
            #         break
            # else:
            #     # by default we select the one that is most likely to occur
            #     # print(f'!!!!!!!!!!!!!!!\nbreak:{_break} DEFAULT\n!!!!!!!!!!!!!!!')
            #     next_road_id = maxx_id[0]

            vehicle.path.append(ctrl.roads[next_road_id])

        next_road_connec  = ctrl.our_connection[(road_id, next_road_id)]
        return next_road_connec
    
    def __poisson(Lambda: float, t: float, x: int):
        Lambda *= t
        return Lambda**x * (e**(-Lambda)) / factorial(x)
