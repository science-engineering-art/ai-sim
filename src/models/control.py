from functools import reduce
from multiprocessing.sharedctypes import copy
from ntpath import join
from time import time
from tokenize import Intnumber
from typing import Deque
from xml.etree.ElementTree import Comment

from h11 import ConnectionClosed
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
                    color=(30, 255, 255), b_max=9.25*self.scale / 300,
                    v_max=29.8*self.scale/300, a_max=2.89*self.scale/300),
            Vehicle(x=0, length=3.5*self.scale/300, width=self.roads_width,
                    color=(255, 30, 255), b_max=10.25*self.scale / 300,
                    v_max=28.3*self.scale/300, a_max=2.5*self.scale/300),
            Vehicle(x=0, length=4.2*self.scale/300, width=self.roads_width,
                    color=(255, 255, 30), b_max=12.25*self.scale / 300,
                    v_max=22.2*self.scale/300, a_max=2*self.scale/300),
            Vehicle(x=0, length=4.5*self.scale/300, width=self.roads_width,
                    color=(118, 181, 197), b_max=8.9*self.scale / 300,
                    v_max=33.3*self.scale/300, a_max=3.1*self.scale/300),
            Vehicle(x=0, length=2.7*self.scale/300, width=self.roads_width,
                    color=(135, 62, 35), b_max=8.5*self.scale / 300,
                    v_max=22.7*self.scale/300, a_max=3.3*self.scale/300)
        ]

        self.nav = navigation(self)

        self.__dict__.update(kwargs)

    def AddExtremeRoads(self, roads, lambdas=None):
        '''establish the extreme roads'''
        for i in range(len(roads)):
            road_id = roads[i]
            if lambdas != None:
                self.roads[road_id].lambda_ = lambdas[i]
            self.extremeRoads.append(road_id)

    def Start(self, observation_time=-1, it_amount=-1):
        '''method to begin the simulation'''
        self.it_number = 0
        init_time = time()
        while (self.it_number < it_amount or it_amount == -1) and (time() - init_time < observation_time or observation_time == -1):
            t1 = time()  # measures time complexity
            self.UpdateAll()
            self.dt = (time() - t1) * self.speed
            self.it_number += 1
            

    def UpdateAll(self, time):

        def CleanRedLights():
            for road in self.roads:
                if len(road.vehicles) > 0 and road.vehicles[0].color == RED:
                    road.vehicles.pop(0)  # remove all the semaphores in red

        CleanRedLights()

        for corn in self.corners:
            corn.tick(self.dt)  # increments the time of each semaphore

        self.nav.NewRandomVehicle(time=time)  # generates a new random vehicle

        for road_id in range(len(self.roads)):  # for each road....
            road = self.roads[road_id]
            if type(road.end_conn) == corner and not road.end_conn.CanIPass(road_id):
                road.vehicles.insert(0, Vehicle(
                    road.length, 3, 1, color=RED, v=0, stopped=True))
            self.UpdateRoad(road)

        self.UpdateConnectionRoads()

    def UpdateConnectionRoads(self):
        for c_road in self.c_roads:
            c_road: connection_road
            for i in range(len(c_road.roads)):
                road = c_road.roads[i]
                self.UpdateAllVehiclesInRoad(road)

                red = road.vehicles.pop(0) if len(
                    road.vehicles) > 0 and road.vehicles[0].color == RED else None
                while len(road.vehicles) > 0:
                    vehicle = road.vehicles[0]
                    if vehicle.x <= road.length:
                        break

                    road.vehicles.pop(0)
                    vehicle.x = 0
                    to = c_road.to_road
                    if i != len(c_road.roads) - 1:
                        to = c_road.roads[i + 1]
                    else:
                        vehicle.current_road_in_path += 1
                    to.vehicles.append(vehicle)

                if red != None:
                    road.vehicles.insert(0, red)

    def UpdateAllVehiclesInRoad(self, road):
        for i in range(len(road.vehicles)):
            vehicle = road.vehicles[i]
            lead = None
            if i != 0:
                lead = road.vehicles[i - 1]
            vehicle.update(dt=self.dt, lead=lead)

    def UpdateRoad(self, road):

        self.UpdateAllVehiclesInRoad(road)

        red = road.vehicles.pop(0) if len(
            road.vehicles) > 0 and road.vehicles[0].color == RED else None

        if len(road.vehicles) > 0 and self.VehicleCanTurn(road.vehicles[0], road):
            road.vehicles[0].stopped = False

        while len(road.vehicles) > 0:
            vehicle = road.vehicles[0]
            if vehicle.x <= road.length or vehicle.stopped:
                break

            next_road_connec: connection_road = self.nav.NextRoad(vehicle)
            if self.VehicleCanTurn(vehicle, road):
                road.vehicles.pop(0)
                if next_road_connec:
                    vehicle.x = 0
                    next_road_connec.roads[0].vehicles.append(vehicle)
            else:
                vehicle.stopped = True

        if red != None:
            road.vehicles.insert(0, red)

    def VehicleCanTurn(self, vehicle, road):
        next_road_connec: connection_road = self.nav.NextRoad(vehicle)
        if not next_road_connec:
            return True
        to_road = next_road_connec.to_road
        if not (len(to_road.vehicles) == 0 or to_road.vehicles[len(to_road.vehicles) - 1].x >=
                to_road.vehicles[len(to_road.vehicles) - 1].length):
            return False
        
        to_road_id = self.road_index[to_road]
        for road_in in road.end_conn.preceed[to_road_id]:
            conn_r = self.our_connection[(road_in, to_road_id)]
            for road in conn_r.roads:
                if len(road.vehicles) > 0:
                    return False
                
        return True
            

    def AddRoad(self, road_init_point, road_end_point, lambda_=1/50):
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

        return len(self.c_roads) - 1  # return the position/id

    def CreateCorner(self, follows, ligth_controled = True):
        '''Create a new corner given a list of follow pairs'''

        corn = corner(light_controled=ligth_controled)
        self.corners.append(corn)

        for follow in follows:
            if len(follow) > 2:
                corn.addFollow(follow[0], follow[1], order=follow[2])
            else:
                corn.addFollow(follow[0], follow)
            self.roads[follow[0]].end_conn = corn
