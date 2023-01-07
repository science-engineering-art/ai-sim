from copy import deepcopy
import random
from time import time
from turtle import speed

import pygame 
from models.A_star import A_star
from models.control import LIGHT_GRAY, control
from msilib.schema import Control
from models.draw_control import draw_control

from models.vehicle import Vehicle


class new_control(control):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def ObserveVehicle(self, vehicle : Vehicle, path_length):
        
        self.it_number = 0
        init_time = time()
        while vehicle.current_road_in_path < path_length - 1:
            self.UpdateAll()
        return (time() - init_time) * self.speed
        
        
    def AddRoutedVehicle(self, from_road_id, to_road_id):
        path = A_star.find_shortest_path(self, from_road_id, to_road_id)
        car: Vehicle = deepcopy(random.choice(self.basic_vehicles))
        car.path = path; car.current_road_in_path = 0
        
        self.nav.fixed_vehicles.append(car)
        
        return car
    
class new_draw(draw_control):
    def ObserveVehicle(self, vehicle : Vehicle, path_length):
        
        ctrl = self.ctrl
        pygame.init()
        screen = pygame.display.set_mode((1400, 800))
        pygame.display.update()
        
        self.it_number = 0
        init_time = time()
        while vehicle.current_road_in_path < path_length - 1:
            # print(vehicle.current_road_in_path)
            t1 = time()  # measures time complexity
            ctrl.UpdateAll()
            screen.fill(LIGHT_GRAY)  # repaint the background
            for event in pygame.event.get():  # check if exiting
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.DrawAllRoads( screen)
            self.DrawAllRoadsCars( screen)
            
            pygame.display.update()
        return (time() - init_time) * ctrl.speed

        
        
        
    