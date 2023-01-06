
from collections import deque
from multiprocessing.sharedctypes import copy
from queue import Queue
from time import sleep, time
from tokenize import Intnumber
from typing import Deque
from xml.etree.ElementTree import Comment
from scipy.spatial import distance
from sympy import rot_axis1
from models.corner import corner
from models.vehicle import Vehicle
from models.road import Road
import random
from copy import deepcopy
from models.painting import *
from pygame.locals import *
from pygame import gfxdraw
import pygame
import math

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

        self.roads = []
        self.road_index = {}  # store the index of each road in roads list
        self.running = True
        self.vehicles = []
        self.corners = []
        self.curves = {}  # stores for each connection the road conforming its curve
        self.is_curve = []  # Determines wheter a road represents a curve/auxiliar road
        self.extremeRoads = []  # roads who start at the edge of the map

        # random vehicles templates
        self.basic_vehicles = [
            Vehicle(x=0, length=1.22, width=1, color=(30, 255, 255),
                    v_max=33.3, a_max=2.89, b_max=9.25),
            # Vehicle(x=0, length= 1.22, width = 1, color=(30, 255,255), v_max = 80, a_max=2.89, b_max=9.25),
            # Vehicle(x=0, length= 3, width = 1.5, color=(255, 30,255), v_max = 30, a_max=2.9, b_max=3),
            # Vehicle(x=0, length= 2, width = 0.85, color=(255, 255,30), v_max = 40, a_max=2.2, b_max=4),
            # Vehicle(x=0, length= 2.5, width = 1.2, color=(118,181,197), v_max = 65, a_max=4.9, b_max=1.5),
            # Vehicle(x=0, length= 2.5, width = 1.2, color=(135,62,35), v_max = 50, a_max=2.9, b_max=2.5),
        ]

        # fitness prperties
        self.road_max_queue = []
        self.road_car_entrance_queue = []
        self.road_total_amount_cars = []
        self.road_total_time_take_cars = []
        self.road_average_time_take_cars = []

        self.__dict__.update(kwargs)

    def NewRandomVehicle(self):
        '''Creates a random vehicle with probability prob'''

        from math import e, factorial

        def poisson(Lambda: float, t: float, x: int):
            Lambda *= t
            return Lambda**x * (e**(-Lambda)) / factorial(x)

        cars = []
        roads_id = []

        for road_id in self.extremeRoads:
            road: Road = self.roads[road_id]

            r = random.random()
            if r > poisson(road.lambda_, self.dt, 1):
                continue

            # select uniformly the vehicle template (i.e. color, length, speed)
            car: Vehicle = deepcopy(random.choice(self.basic_vehicles))
            road.vehicles.append(car)
            cars.append(car)
            roads_id.append(road_id)

        return cars, roads_id

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

            _, roads_id = self.NewRandomVehicle()  # generates a new random vehicle
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
                if draw:
                    Painting.draw_road(screen, road, GRAY)  # repaint it
                # if it has a semaphore in red...
                if type(road.end_conn) == corner and not road.end_conn.CanIPass(road_id):
                    # add a 'semaphore car' to vehicles
                    road.vehicles.appendleft(
                        Vehicle(road.length, 3, 1, color=RED, v=0))
                # update the state of each vehicle in the road
                self.UpdateRoad(road)

            for road in self.roads:
                for car in road.vehicles:
                    if draw:
                        # repaint all the cars
                        Painting.draw_vehicle(screen, road, car)

                if len(road.vehicles) > 0 and road.vehicles[0].color == RED:
                    self.road_max_queue[self.roads.index(road)] = max(self.road_max_queue[self.roads.index(road)],
                                                                      len(road.vehicles))  # fitness.................................
                    road.vehicles.popleft()  # remove all the semaphores in red

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

    def UpdateRoad(self, road):
        
        road_id = self.roads.index(road)
        
        delete_amout = 0  # amount of of cars that move to other roads
        for i in range(len(road.vehicles)):
            car = road.vehicles[i]
            lead = None
            if i != 0:
                lead = road.vehicles[i - 1]
            if car.color != RED:  # be careful do not update the semaphore car
                car.update(dt=self.dt, lead=lead)
            if car.x > road.length:  # if the car position is out of the road
                delete_amout += 1  # remove the car from this road
                self.NextRoad(car, road)  # and add it in the next one

        red = road.vehicles.popleft() if len(
            road.vehicles) > 0 and road.vehicles[0].color == RED else None
        
        self.road_total_time_take_cars[road_id] += self.dt * len(road.vehicles)
            
            
        for i in range(delete_amout):  # remove the cars moving out from the road
            road.vehicles.popleft()

            if len(self.road_car_entrance_queue[road_id]) > 0:
                # fitness.................................
                self.road_total_amount_cars[road_id] += 1
                # self.road_total_time_take_cars[road_id] += self.it_number + \
                    # 1 - self.road_car_entrance_queue[road_id][0]
                # fitness.................................
                self.road_car_entrance_queue[road_id].pop(0)

        if red != None:
            road.vehicles.appendleft(red)

    def NextRoad(self, vehicle: Vehicle, road: Road):

        if not road.end_conn:  # if nothing is associated with the end of the road
            return  # means the road end in the edge of the map

        vehicle.x = 0
        if type(road.end_conn) == Road:  # if the road is followed by other road
            # simply add the vehicle to that road
            road.end_conn.vehicles.append(vehicle)
            next_road_id = self.roads.index(road.end_conn)
            # fitness.................................
            self.road_car_entrance_queue[next_road_id].append(self.it_number)
            return road.end_conn

        # in other case the road ends in a cornen, in which case we uniformily random select
        # the next road from the corner that can be reached from the current one
        next_road_id = random.choice(
            road.end_conn.follow[self.road_index[road]])

        # if the road is in a corner it may have a curve associated
        next_road_curve_id = self.curves[(
            self.road_index[road], next_road_id)][0]
        next_road: Road = self.roads[next_road_curve_id]
        next_road.vehicles.append(vehicle)
        # fitness.................................
        self.road_car_entrance_queue[next_road_curve_id].append(self.it_number)
        return next_road

    def AddRoad(self, road_init_point, road_end_point, lambda_ = 1/50):
        '''Adds a nex road to the simulation'''

        road = Road(road_init_point, road_end_point, lambda_)
        road_id = len(self.roads)
        self.roads.append(road)
        self.is_curve.append(False)
        self.road_index[road] = road_id
        return road_id

    def connect_roads(self, road_1_id, road_2_id, curve_point):
        '''connects to roads with a curve using an external point to create the curve
        and return the indexes of the curve's sub-roads'''

        road_1: Road = self.roads[road_1_id]
        road_2: Road = self.roads[road_2_id]
        road_locations = [
            *Road.get_curve_road(road_1.end, road_2.start, curve_point)]
        roads_2 = [Road(r_loc[0], r_loc[1]) for r_loc in road_locations]

        # the next road of each road of the curve is assigned
        for i in range(0, len(road_locations) - 1):
            roads_2[i].end_conn = roads_2[i+1]
        roads_2[len(road_locations) - 1].end_conn = road_2

        # compute indexes
        return_val = []
        for road in roads_2:
            self.road_index[road] = len(self.roads)
            return_val.append(len(self.roads))
            self.roads.append(road)
            self.is_curve.append(True)

        # assign to each follow pair, the first sub-road of the corresponding curve
        self.curves[(road_1_id, road_2_id)] = return_val

        return return_val

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
