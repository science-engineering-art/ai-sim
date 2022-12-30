
from multiprocessing.sharedctypes import copy
from turtle import _Screen

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
from scipy.spatial import distance


RED = (255, 0, 0)
BLUE = (0, 255, 255)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)
LIGHT_GRAY = (225,225,225)


class control:
    '''class made to control hall the simulation over the map'''


    def __init__(self):
        self.roads = []
        self.road_index = {}#store the index of each road in roads list
        self.running = True
        self.vehicles = []
        self.corners = []
        self.curves = {} #stores for each connection the road conforming its curve
        self.extremeRoads = [] #roads who start at the edge of the map
        
        #random vehicles templates
        self.basic_vehicles = [Vehicle(x=0, length= 3, width = 1, color=(10,255,255))]

        # coordinates - roads
        self.coord_roads_in  = {}
        self.coord_roads_out = {}


    def NewRandomVehicle(self, prob = 1/1000, cant = 1):
        '''Creates a random vehicle with probability prob'''
        
        r = random.random()
        if r > prob:
            return
        
        for _ in range(cant):
            #select uniformly the vehicle template (i.e. color, length, speed)
            car : Vehicle = deepcopy(random.choice(self.basic_vehicles))
            #select uniformly the vehicle start road from the extreme ones
            road : Road = self.roads[random.choice(self.extremeRoads)]
            road.vehicles.append(car)


    def AddExtremeRoads(self,roads):
        '''establish the extreme roads'''
        for road_id in roads:
            self.extremeRoads.append(road_id)


    def Start(self):
        '''method to begin the simulation'''
        pygame.init()
        screen = pygame.display.set_mode((1400,800))
        pygame.display.update()

        while self.running:
            
            for corn in self.corners:
                corn.tick() #increments the time of each semaphore
            
            screen.fill(LIGHT_GRAY) #repaint the background
            
            self.NewRandomVehicle() #generates a new random vehicle
            
            for event in pygame.event.get(): #check if exiting
                if event.type == QUIT:
                    pygame.quit()
        
            for road in self.roads: #for each road....
                Painting.draw_road(screen, road, GRAY) #repaint it 
                if type(road.end_conn) == corner and not road.end_conn.CanIPass(self.road_index[road]): #if it has a semaphore in red...
                    road.vehicles.insert(0, Vehicle(road.length, 3, 9, color = RED)) #add a 'semaphore car' to vehicles
                self.UpdateRoad(road) #update the state of each vehicle in the road
            
            for road in self.roads:
                for car in road.vehicles:
                    Painting.draw_vehicle(screen, road, car) #repaint all the cars
                    
                if len(road.vehicles) > 0 and road.vehicles[0].color == RED:
                    road.vehicles.__delitem__(0) #remove all the semaphores in red
            
            pygame.display.update()


    def UpdateRoad(self, road):
        delete_list = [0 for _ in range(len(road.vehicles))] #list of cars that move to other roads
        for i in range(len(road.vehicles)):
            car = road.vehicles[i]
            lead = None
            if i != 0:
                lead = road.vehicles[i - 1]
            if car.color != RED: #be careful do not update the semaphore car
                car.update(lead = lead)
            if car.x > road.length: #if the car position is out of the road
                delete_list[i] = 1  #remove the car from this road
                self.NextRoad(car, road) #and add it in the next one
        
        for i in range(len(delete_list)):   #remove the cars moving out from the road
            if delete_list[i] == 1:
                road.vehicles.__delitem__(i)
            
          
    def NextRoad(self, vehicle: Vehicle, road : Road):
        
        if not road.end_conn: #if nothing is associated with the end of the road
            return  #means the road end in the edge of the map

        vehicle.x = 0
        if type(road.end_conn) == Road: #if the road is followed by other road
            road.end_conn.vehicles.append(vehicle) #simply add the vehicle to that road
            return road.end_conn    
        
        #in other case the road ends in a cornen, in which case we uniformily random select
        #the next road from the corner that can be reached from the current one
        next_road_id = random.choice(road.end_conn.follow[self.road_index[road]])
        
        #if the road is in a corner it may have a curve associated
        next_road_curve_id = self.curves[(self.road_index[road],next_road_id )][0]
        next_road : Road = self.roads[next_road_curve_id]
        next_road.vehicles.append(vehicle)
        return next_road
    

    def AddRoad(self, road_init_point, road_end_point):
        '''Adds a nex road to the simulation'''
        
        road = Road(road_init_point, road_end_point)
        road_id = len(self.roads)
        self.roads.append(road)
        self.road_index[road] = road_id
        return road_id


    def build_roads(self, start, end, inN, outN, width):
        x0, y0 = start
        x1, y1 = end

        if x0**2 + y0**2 > x1**2 + y1**2:
            x0, y0 = end
            x1, y1 = start

        vX, vY = x1-x0, y1-y0
        nX, nY = vY, -vX

        #normalize
        n = (nX**2 + nY**2)**0.5
        nX, nY = width/n*nX, width/n*nY 

        n = (inN + outN) / 2
        rX, rY = n * -nX, n * -nY

        if (inN + outN) % 2 == 0:
            rX, rY = rX + width/2 * nX, rY + width/2 *nY

        x0, y0 = start
        x1, y1 = end

        x0, y0 = x0 + rX, y0 + rY
        x1, y1 = x1 + rX, y1 + rY

        if start not in self.coord_roads_in:
            self.coord_roads_in[start] = []
        if end not in self.coord_roads_in:
            self.coord_roads_in[end] = []
        if start not in self.coord_roads_out:
            self.coord_roads_out[start] = []
        if end not in self.coord_roads_out:
            self.coord_roads_out[end] = []

        for _ in range(outN):
            id = self.AddRoad((x1, y1), (x0, y0))
            x0, y0 = x0 + nX, y0 + nY
            x1, y1 = x1 + nX, y1 + nY 
            self.coord_roads_in[start].append(id)
            self.coord_roads_out[end].append(id)

        for _ in range(inN):
            id = self.AddRoad((x0, y0), (x1, y1))
            x0, y0 = x0 + nX, y0 + nY
            x1, y1 = x1 + nX, y1 + nY 
            self.coord_roads_in[end].append(id)
            self.coord_roads_out[start].append(id)


    def build_intersections(self):
 
        for x, y in self.coord_roads_in:
            for road_out_id in self.coord_roads_out[(x,y)]:
                
                road_in_id = self.coord_roads_in[(x,y)][0]
                road_in: Road = self.roads[road_in_id]
                road_out: Road = self.roads[road_out_id]

                # check if road_in and road_out are in the same avenue
                if distance.euclidean(road_in.start, road_out.start) == \
                    distance.euclidean(road_in.end, road_out.end):
                    continue

                if road_in.end == (x,y):
                    x0, y0 = road_in.start
                    x1, y1 = road_in.end
                    vX, vY = x1-x0, y1-y0
                    
                    n = (vX**2 + vY**2)**0.5
                    vX, vY = vX/n, vY/n
                    
                    road_in.end = x - vX, y - vY
                
                if road_out.start == (x,y):
                    x0, y0 = road_out.start
                    x1, y1 = road_out.end
                    vX, vY = x1-x0, y1-y0
                    
                    n = (vX**2 + vY**2)**0.5
                    vX, vY = vX/n, vY/n
                    
                    road_out.start = x + vX, y + vY
                
                self.connect_roads(road_in_id, road_out_id, (x,y))
                

    def connect_roads(self, road_1_id, road_2_id, curve_point):    
        '''connects to roads with a curve using an external point to create the curve
        and return the indexes of the curve's sub-roads'''
        
        road_1 : Road = self.roads[road_1_id]
        road_2 : Road = self.roads[road_2_id]
        road_locations = [*Road.get_curve_road(road_1.end, road_2.start, curve_point)]
        roads_2 = [Road(r_loc[0], r_loc[1]) for r_loc in road_locations]
        
        #the next road of each road of the curve is assigned
        for i in range(0, len(road_locations) - 1):
            roads_2[i].end_conn = roads_2[i+1]
        roads_2[len(road_locations) - 1].end_conn = road_2
        
        
        #compute indexes
        return_val = []    
        for road in roads_2:
            self.road_index[road] = len(self.roads)
            return_val.append(len(self.roads))
            self.roads.append(road)
           
        #assign to each follow pair, the first sub-road of the corresponding curve
        self.curves[(road_1_id, road_2_id)] = return_val
            
        return return_val


    def CreateCorner(self, follows):
        '''Create a new corner given a list of follow pairs'''
        
        corn = corner(light_controled=True)
        self.corners.append(corn)
        
        for follow in follows:
            if len(follow) > 2:
                corn.addFollow(follow[0], follow[1], order = follow[2])
            else:
                corn.addFollow(follow[0], follow)
            self.roads[follow[0]].end_conn = corn

