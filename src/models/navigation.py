import random
from copy import deepcopy
from math import e
from models.Floyd_Warshall import GetPath
from models.vehicle import Vehicle
from models.Floyd_Warshall import st_distances_matrix
from models.Floyd_Warshall import st_path_matrix

class navigation():
    '''class that simulates a navigation system installed in a car (actually interconnected
    between al cars, because is the same for all of them) that decide the routes of the cars.'''
    
    def __init__(self, ctrl):
        self.cars = []
        self.fixed_vehicles = []
        self. ctrl = ctrl

    def NewRandomVehicle(self, fixed_direction = True):
        '''Inserts a new vehicle into the simulation'''

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
            if fixed_direction:
                car.path = self.GenerateRandomPath(road_id); car.current_road_in_path = 0
            else:
                car.path = [road_id]; car.current_road_in_path = 0
            self.cars.append(car)
            cars.append(car)
            roads_id.append(road_id)
            
        new_fv = []
        for vehicle in self.fixed_vehicles:
            road = self.ctrl.roads[vehicle.path[0]]
            l = len(road.vehicles)
            if l == 0 or (road.vehicles[l - 1].x < road.vehicles[l - 1].length): 
                road.vehicles.append(vehicle)
                self.cars.append(vehicle)
                cars.append(vehicle)
                roads_id.append(vehicle.path[0])
            else: new_fv.append(vehicle)
        self.fixed_vehicles = new_fv    
        
        return cars, roads_id
    
    def GenerateRandomPath(self, road_from_id):

        road_to_id = random.choice(range(len(self.ctrl.roads)))
        path = GetPath(self.ctrl, road_from_id, road_to_id)
        while path == []:
            road_to_id = random.choice(range(len(self.ctrl.roads)))
            path = GetPath(self.ctrl, road_from_id, road_to_id)
        return path
            

    #careful when using, this method can return None
    def NextRoad(self, vehicle: Vehicle):
        road_id = vehicle.path[vehicle.current_road_in_path]
        ctrl = self.ctrl
        road = ctrl.roads[road_id]
    
        if not road.end_conn:  # if nothing is associated with the end of the road
            return  # means the road end in the edge of the map
        
        next_road_id = None
        if vehicle.current_road_in_path < len(vehicle.path) - 1:
            next_road_id =  vehicle.path[vehicle.current_road_in_path + 1]
            
        pp = st_distances_matrix
        dd = st_path_matrix
        next_road_connec  = ctrl.our_connection.get((road_id, next_road_id))
        return next_road_connec
    
    def __poisson(Lambda: float, t: float, x: int):
        if t == 0:
            t = 1e-8
        Lambda *= t
        return 1.0 -  (e**(-Lambda)) 
