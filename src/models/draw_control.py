
from functools import reduce
from multiprocessing.sharedctypes import copy
from ntpath import join
from time import  time
from tokenize import Intnumber
from typing import Deque
from xml.etree.ElementTree import Comment

from h11 import ConnectionClosed
from matplotlib.colors import LightSource
from pandas import concat
from sklearn.preprocessing import scale
from models.connection_road import connection_road
from models.control import control
from models.corner import corner
from models.navigation import navigation
from models.vehicle import Vehicle
from models.road import Road
import random
from copy import deepcopy
from models.painting import *
from pygame.locals import *
import pygame
from math import e, factorial

RED = (255, 0, 0)
BLUE = (0, 255, 255)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (225, 225, 225)

# relaciones:
# vehiculo.length/calle 4m/300m
# vehiculo.vmax/calle 80-120km/h/300m = 22.2-33.3m/s/300m
# vehiculo.a_max/vmax 1/11.5
# vehiculo.b_max/vmax 1/3.60

class draw_control():
    '''class made to control hall the simulation over the map'''
    def __init__(self, **kwargs):


        self.ctrl = control()
        self.ctrl.curve_steps = 1
        self.__dict__.update(kwargs)

    def Start(self, observation_time=-1, it_amount=-1):
        '''method to begin the simulation'''

        ctrl = self.ctrl
        pygame.init()
        screen = pygame.display.set_mode((1400, 800))
        pygame.display.update()

        self.it_number = 0
        init_time = time()
        while (self.it_number < it_amount or it_amount == -1) and (time() - init_time < observation_time or observation_time == -1):

            t1 = time()  # measures time complexity

            self.ctrl.UpdateAll()
            
            screen.fill(LIGHT_GRAY)  # repaint the background

            for event in pygame.event.get():  # check if exiting
                if event.type == QUIT:
                    pygame.quit()

            self.DrawAllRoads( screen)
            self.DrawAllRoadsCars( screen)
            
            pygame.display.update()

            ctrl.dt = (time() - t1) * ctrl.speed
            self.it_number += 1

    def DrawAllRoads(self, screen):
        for road in self.ctrl.roads:
            Painting.draw_road(screen, road, GRAY)  # repaint it
                
        for c_road in self.ctrl.c_roads:
            for road in c_road.roads:
                Painting.draw_road(screen, road, GRAY)  # repaint it
                
    def DrawAllRoadsCars(self, screen):
        
        for road in self.ctrl.roads:
            ligth = []
            if type(road.end_conn) == corner and not road.end_conn.CanIPass(self.ctrl.road_index[road]):
                ligth.append(Vehicle(
                road.length, 3, 1, color=RED, v=0, stopped=True))
            elif type(road.end_conn) == corner and road.end_conn.light_controled:
                ligth.append(Vehicle(
                road.length, 3, 1, color=GREEN, v=0, stopped=True))
            for car in road.vehicles + ligth:
                # repaint all the cars
                Painting.draw_vehicle(screen, road, car)

        for c_road in self.ctrl.c_roads:
            for road in c_road.roads:
                for car in road.vehicles:
                    # repaint all the cars
                    Painting.draw_vehicle(screen, road, car)
