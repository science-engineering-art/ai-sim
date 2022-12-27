
from multiprocessing.sharedctypes import copy
from turtle import _Screen

import typing
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


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (127, 127, 127)
LIGHT_GRAY = (220,220,220)

class control:
    def __init__(self):
        self.roads = []
        self.road_index = {}
        self.running = True
        self.vehicles = []
        self.corners = []
        self.curves = {}
        self.extremeRoads = []
        
        self.basic_vehicles = [Vehicle(x=0, length= 14, width = 7)]
        
    def NewRandomVehicle(self, prob = 1/1000, cant = 1):
        
        r = random.random()
        if r > prob:
            return
        
        for _ in range(cant):
            car : Vehicle = deepcopy(random.choice(self.basic_vehicles))
            road : Road = self.roads[random.choice(self.extremeRoads)]
            road.vehicles.append(car)
    
    def AddExtremeRoads(self,roads):
        for road_id in roads:
            self.extremeRoads.append(road_id)
    
    def Start(self):
        pygame.init()
        screen = pygame.display.set_mode((1400,800))
        pygame.display.update()


        while self.running:
            
            for corn in self.corners:
                corn.tick()
            screen.fill(LIGHT_GRAY)
            
            
            self.NewRandomVehicle()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                # running = False
                # car.stopped = False
            # print(event)
        
            for road in self.roads:
                Painting.draw_road(screen, road, GRAY)
                # print(road, type(road.end_conn))
                if type(road.end_conn) == corner and not road.end_conn.CanIPass(self.road_index[road]):
                    road.vehicles.insert(0, Vehicle(road.length, 3, 9, color = RED))
                self.UpdateRoad(road)
            
            for road in self.roads:
                for car in road.vehicles:
                    Painting.draw_vehicle(screen, road, car)
                    
                if len(road.vehicles) > 0 and road.vehicles[0].color == RED:
                    road.vehicles.__delitem__(0)
            
            pygame.display.update()
      
    def UpdateRoad(self, road):
        delete_list = [0 for _ in range(len(road.vehicles))]
        for i in range(len(road.vehicles)):
            car = road.vehicles[i]
            lead = None
            if i != 0:
                lead = road.vehicles[i - 1]
            if car.color != RED:
                car.update(lead = lead)
            if car.x > road.length:
                delete_list[i] = 1
                self.NextRoad(car, road)
        
        for i in range(len(delete_list)):
            if delete_list[i] == 1:
                print(i)
                road.vehicles.__delitem__(i)
            
        
          
    def NextRoad(self, vehicle: Vehicle, road : Road):
        print('here: ', self.road_index[road], road.end_conn)
        if not road.end_conn:
            return
        
        vehicle.x = 0
        if type(road.end_conn) == Road:
            road.end_conn.vehicles.append(vehicle)
            return road.end_conn
        
        print(road.end_conn.follow[self.road_index[road]])
        next_road_id = random.choice(road.end_conn.follow[self.road_index[road]])
        next_road_curve_id = self.curves[(self.road_index[road],next_road_id )][0]
        next_road : Road = self.roads[next_road_curve_id]
        next_road.vehicles.append(vehicle)
        return next_road
    
    def AddRoad(self, road_init_point, road_end_point):
        
        road = Road(road_init_point, road_end_point)
        road_id = len(self.roads)
        self.roads.append(road)
        self.road_index[road] = road_id
        return road_id
     
    def connect_roads(self, road_1_id, road_2_id, curve_point):    
        
        road_1 : Road = self.roads[road_1_id]
        road_2 : Road = self.roads[road_2_id]
        road_locations = [*Road.get_curve_road(road_1.end, road_2.start, curve_point)]
        roads_2 = [Road(r_loc[0], r_loc[1]) for r_loc in road_locations]
        for i in range(0, len(road_locations) - 1):
            roads_2[i].end_conn = roads_2[i+1]
        
        return_val = []    
        roads_2[len(road_locations) - 1].end_conn = road_2
        for road in roads_2:
            self.road_index[road] = len(self.roads)
            return_val.append(len(self.roads))
            self.roads.append(road)
           
        self.curves[(road_1_id, road_2_id)] = return_val
            
        return return_val
    
    def CreateCorner(self, follows):
        corn = corner(light_controled=True)
        self.corners.append(corn)
        
        for follow in follows:
            corn.addFollow(follow[0], follow[1])
            self.roads[follow[0]].end_conn = corn

        
    

        
        
        
        
        