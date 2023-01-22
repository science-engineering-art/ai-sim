from time import time
from models.control import control
from models.painting import *
from pygame.locals import *


RED = (255, 0, 0)
BLUE = (0, 255, 255)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (225, 225, 225)


class metaeh_control(control):
    '''class made to control hall the simulation over the map'''

    def __init__(self, **kwargs):

        super().__init__()

        # fitness properties
        self.road_total_amount_cars = []
        self.road_total_time_take_cars = []
        self.road_average_time_take_cars = []
        self.ref_car = []

        self.__dict__.update(kwargs)

    def Start(self, observation_time=-1, it_amount=-1):
        '''method to begin the simulation'''

        self.preprocess_fitness_properties()
        self.it_number = 0
        init_time = time()
        while (self.it_number < it_amount or it_amount == -1) and (time() - init_time < observation_time or observation_time == -1):
            t1 = time()  # measures time complexity
            self.UpdateAll()
            self.UpdateFitnessProp()
            t2 = time()
            self.dt = (t2 - t1) * self.speed
            self.it_number += 1
        self.posprocess_fitness_properties()

    def preprocess_fitness_properties(self):
        for _ in range(len(self.roads)):
            self.road_total_amount_cars.append(0)
            self.road_total_time_take_cars.append(0)
            self.road_average_time_take_cars.append(0)
            self.ref_car.append(None)

    def posprocess_fitness_properties(self):
        for road_id in range(len(self.roads)):
            self.road_average_time_take_cars[road_id] = self.road_total_time_take_cars[road_id] /            \
                self.road_total_amount_cars[road_id] if self.road_total_amount_cars[road_id] != 0  \
                else 0

    def UpdateFitnessProp(self):
        for road_id in range(len(self.roads)):
            road = self.roads[road_id]
            self.road_total_time_take_cars[road_id] += self.dt * \
                len(road.vehicles)
            for pos in range(len(road.vehicles)):
                vehicle = road.vehicles[len(road.vehicles) - pos - 1]
                if vehicle.mark == road_id:
                    # vehicle.mark = None
                    break
                self.road_total_amount_cars[road_id] += 1
            if len(road.vehicles) > 0:
                road.vehicles[len(road.vehicles) - 1].mark = road_id
                self.ref_car[road_id] = road.vehicles[len(road.vehicles) - 1]

    def GetDimension(self):
        dimension = 0
        for corner in self.corners:
            dimension += (corner.numberOfTurns + 1)

        return dimension

    def SetConfiguration(self, individual, shync=True):
        pos = 0
        for corner in self.corners:
            corner.time_tick = individual[pos]
            pos += 1
            for i in range(corner.numberOfTurns):
                corner.times[i] = individual[pos]
                pos += 1
