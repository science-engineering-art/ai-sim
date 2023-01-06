



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

        def poisson(Lambda: float, t: float, x: int):
            Lambda *= t
            return Lambda**x * (e**(-Lambda)) / factorial(x)

        cars = []
        roads_id = []

        for road_id in self.ctrl.extremeRoads:
            road: Road = self.ctrl.roads[road_id]

            r = random.random()
            if r > poisson(road.lambda_, self.ctrl.dt, 1):
                continue

            # select uniformly the vehicle template (i.e. color, length, speed)
            car: Vehicle = deepcopy(random.choice(self.ctrl.basic_vehicles))
            road.vehicles.append(car)
            self.cars.append(car)
            cars.append(car)
            roads_id.append(road_id)

        return cars, roads_id
        
