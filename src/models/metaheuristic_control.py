
from functools import reduce
from multiprocessing.sharedctypes import copy
from ntpath import join
from time import  time
from tokenize import Intnumber
from typing import Deque
from xml.etree.ElementTree import Comment

from h11 import ConnectionClosed
from pandas import concat
from sklearn.preprocessing import scale
from models.connection_road import connection_road
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

class control:
    '''class made to control hall the simulation over the map'''
    def __init__(self, **kwargs):

        self.speed = 5  # how many simulation second will pass for every real life second
        # time step in each iteration of while cycle in Start
        self.dt = self.speed * (1/300)

        self.scale = 300
        self.roads_width = 1
        self.roads = []
        self.c_roads = []
        self.our_connection = {}
        self.road_index = {}  # store the index of each road in roads list
        self.running = True
        self.vehicles = []
        self.corners = []
        self.extremeRoads = []  # roads who start at the edge of the map

        # random vehicles templates
        self.basic_vehicles = [
            Vehicle(x=0, length=4*self.scale/300, width=self.roads_width,
                    color=(30, 255, 255), b_max = 9.25*self.scale / 300,
                    v_max=29.8*self.scale/300, a_max=2.89*self.scale/300),
            Vehicle(x=0, length=3.5*self.scale/300, width=self.roads_width,
                    color=(255, 30,255), b_max = 10.25*self.scale / 300,
                    v_max=28.3*self.scale/300, a_max=2.5*self.scale/300),
            Vehicle(x=0, length=4.2*self.scale/300, width=self.roads_width,
                    color=(255, 255,30), b_max = 12.25*self.scale / 300,
                    v_max=22.2*self.scale/300, a_max=2*self.scale/300),
            Vehicle(x=0, length=4.5*self.scale/300, width=self.roads_width,
                    color=(118,181,197), b_max = 8.9*self.scale / 300,
                    v_max=33.3*self.scale/300, a_max=3.1*self.scale/300),
            Vehicle(x=0, length=2.7*self.scale/300, width=self.roads_width,
                    color=(135,62,35), b_max = 8.5*self.scale / 300,
                    v_max=22.7*self.scale/300, a_max=3.3*self.scale/300)
        ]
         
        self.nav = navigation(self)

        # fitness properties
        self.road_max_queue = []
        self.road_car_entrance_queue = []
        self.road_total_amount_cars = []
        self.road_total_time_take_cars = []
        self.road_average_time_take_cars = []

        self.__dict__.update(kwargs)


    def AddExtremeRoads(self, roads, lambdas=None):
        '''establish the extreme roads'''
        for i in range(len(roads)):
            road_id = roads[i]
            if lambdas != None:
                self.roads[road_id].lambda_ = lambdas[i]
            self.extremeRoads.append(road_id)

    def Start(self, observation_time=-1, it_amount=-1, draw=True):
        '''method to begin the simulation'''
        if draw:
            pygame.init()
            screen = pygame.display.set_mode((1400, 800))
            pygame.display.update()

        # presetting the fitness properties
        for road in self.roads:
            self.road_max_queue.append(0)
            self.road_total_amount_cars.append(0)
            self.road_total_time_take_cars.append(0)
            self.road_car_entrance_queue.append([])
        self.it_number = 1

        init_time = time()
        while (self.it_number < it_amount or it_amount == -1) and (time() - init_time < observation_time or observation_time == -1):

            t1 = time()  # measures time complexity

            for corn in self.corners:
                corn.tick(self.dt)  # increments the time of each semaphore

            if draw:
                screen.fill(LIGHT_GRAY)  # repaint the background

            _, roads_id = self.nav.NewRandomVehicle()  # generates a new random vehicle
            if len(roads_id) > 0:
                for road_id in roads_id:
                    # fitness.................................
                    self.road_car_entrance_queue[road_id].append(
                        self.it_number)

            if draw:
                for event in pygame.event.get():  # check if exiting
                    if event.type == QUIT:
                        pygame.quit()

            for road_id in range(len(self.roads)):  # for each road....
                road = self.roads[road_id]
                # if it has a semaphore in red...
                if type(road.end_conn) == corner and not road.end_conn.CanIPass(road_id):
                    # add a 'semaphore car' to vehicles
                    road.vehicles.appendleft(
                        Vehicle(road.length, 3, 1, color=RED, v=0, stopped = True))
                # update the state of each vehicle in the road
                self.UpdateRoad(road)

            self.UpdateConnectionRoads()
            
            self.DrawAllRoads(draw, screen)
            self.DrawAllRoadsCars(draw, screen)
            
            if draw:
                pygame.display.update()

            # print(self.dt)
            self.dt = (time() - t1) * self.speed
            self.it_number += 1

        # fitness.................................
        for road_id in range(len(self.roads)):
            c = 0
            t = 0
            for i in range(len(self.roads[road_id].vehicles)):
                c += 1
            self.road_total_time_take_cars[road_id] += self.dt * c
            self.road_total_amount_cars[road_id] += c
            self.road_average_time_take_cars.append(((self.road_total_time_take_cars[road_id])
                                                     / (self.road_total_amount_cars[road_id]) if self.road_total_amount_cars[road_id] != 0 else 0))

    def DrawAllRoads(self, draw, screen):
        for road in self.roads:
            if draw:
                Painting.draw_road(screen, road, GRAY)  # repaint it
                
        for c_road in self.c_roads:
            for road in c_road.roads:
                if draw:
                    Painting.draw_road(screen, road, GRAY)  # repaint it
    def DrawAllRoadsCars(self, draw, screen):
    
        for road in self.roads:
            for car in road.vehicles:
                if draw:
                    # repaint all the cars
                    Painting.draw_vehicle(screen, road, car)

            if len(road.vehicles) > 0 and road.vehicles[0].color == RED:
                self.road_max_queue[self.roads.index(road)] = max(self.road_max_queue[self.roads.index(road)],
                                                                len(road.vehicles))  # fitness.................................
                road.vehicles.popleft()  # remove all the semaphores in red
        for c_road in self.c_roads:
            for road in c_road.roads:
                for car in road.vehicles:
                    if draw:
                        # repaint all the cars
                        Painting.draw_vehicle(screen, road, car)

            

    def UpdateConnectionRoads(self):
        for c_road in self.c_roads:
            c_road:connection_road
            for i in range(len(c_road.roads)):
                road = c_road.roads[i]
                self.UpdateAllVehiclesInRoad(road)
                
                red = road.vehicles.popleft() if len(
                                    road.vehicles) > 0 and road.vehicles[0].color == RED else None
                while len(road.vehicles) > 0:
                    vehicle = road.vehicles[0]
                    if vehicle.x <= road.length:
                        break
                    
                    road.vehicles.popleft()
                    vehicle.x = 0
                    to = c_road.to_road
                    if i != len(c_road.roads) - 1:
                        to = c_road.roads[i + 1]
                    to.vehicles.append(vehicle)
                    
                if red != None:
                    road.vehicles.appendleft(red)

    
    def UpdateAllVehiclesInRoad(self, road):
        for i in range(len(road.vehicles)):
            vehicle = road.vehicles[i]
            lead = None
            if i != 0:
                lead = road.vehicles[i - 1]
            vehicle.update(dt=self.dt, lead=lead)
            

    def UpdateRoad(self, road):
        
        road_id = self.roads.index(road)
        
        self.UpdateAllVehiclesInRoad(road)
        
        red = road.vehicles.popleft() if len(
            road.vehicles) > 0 and road.vehicles[0].color == RED else None
        while len(road.vehicles) > 0:
            vehicle = road.vehicles[0]
            if vehicle.x <= road.length:
                break
            
            road.vehicles.popleft()
            vehicle.x = 0
            self.nav.NextRoad(vehicle, road)
            
        # fitness.................................
        self.road_total_time_take_cars[road_id] += self.dt * len(road.vehicles)
        if len(self.road_car_entrance_queue[road_id]) > 0:
            self.road_total_amount_cars[road_id] += 1
            self.road_car_entrance_queue[road_id].pop(0)
        if red != None:
            road.vehicles.appendleft(red)


    def AddRoad(self, road_init_point, road_end_point, lambda_ = 1/50):
        '''Adds a nex road to the simulation'''

        road = Road(road_init_point, road_end_point, lambda_)
        road_id = len(self.roads)
        self.roads.append(road)
        self.road_index[road] = road_id
        return road_id

    def connect_roads(self, road_1_id, road_2_id, curve_point):
        '''connects to roads with a curve using an external point to create the curve
        and return the indexes of the curve's sub-roads'''


        road_1: Road = self.roads[road_1_id]
        road_2: Road = self.roads[road_2_id]
        
        
        c_road = connection_road(road_1, road_2, curve_point)
        self.c_roads.append(c_road)
        
        self.our_connection[(road_1_id, road_2_id)] = c_road
        
        return len(self.c_roads) - 1 #return the position/id

    def CreateCorner(self, follows):
        '''Create a new corner given a list of follow pairs'''

        corn = corner(light_controled=True)
        self.corners.append(corn)

        for follow in follows:
            if len(follow) > 2:
                corn.addFollow(follow[0], follow[1], order=follow[2])
            else:
                corn.addFollow(follow[0], follow)
            self.roads[follow[0]].end_conn = corn

    def GetDimension(self):
        dimension = 0
        for corner in self.corners:
            dimension += (corner.numberOfTurns + 1)

        return dimension

    def SetConfiguration(self, individual):
        pos = 0
        for corner in self.corners:
            corner.time_tick = individual[pos]
            pos+=1
            for i in range(corner.numberOfTurns):
                corner.times[i] = individual[pos]
                pos += 1
