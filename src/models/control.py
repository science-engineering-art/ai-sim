
from vehicle import Vehicle
from road import Road
import random
from copy import deepcopy

from pygame.locals import *
from pygame import gfxdraw
import pygame


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (127, 127, 127)


class control:
    def __init__(self):
        self.roads = []
        self.road_index = {}
        self.running = True
        self.vehicles = []
        self.corners = []
        self.extremeRoads = []
        
        self.basic_vehicles = [Vehicle(x=0, length= 14, width = 7)]
        
    def NewRandomVehicle(self, cant = 1):
        
        for _ in range(cant):
            car : Vehicle = deepcopy(random.choice(self.basic_vehicles))
            road : Road = random.choice(self.extremeRoads)
            road.vehicles.append(car)
        
    def Start(self):
        pygame.init()
        screen = pygame.display.set_mode((1400,800))
        pygame.display.update()


        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                # running = False
                # car.stopped = False
            print(event)
        
            
            pygame.display.update()
        
    def NextRoad(self, vehicle, road):
        if not road.end:
            return
        
        vehicle.x = 0
        if type(road.end) == Road:
            road.end.vechicles.append(vehicle)
            return road.end
        
        next_road_id = random.choice(road.end.follow[self.road_index[road]])
        next_road : Road = self.roads[next_road_id]
        next_road.vehicles.append(vehicle)
        return next_road
        