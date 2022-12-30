
import pygame
from pygame import gfxdraw
from models.road import Road
from models.vehicle import Vehicle
import random
from copy import deepcopy


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)


class Painting:
    def draw_road(screen, road : Road, color):
        x, y = road.start
        l = road.length
        h = 1
        
        d_x = lambda v1,v2 : (v1*l*road.angle_cos + v2*h*road.angle_sin)/2
        d_y = lambda v1,v2 : (v1*l*road.angle_sin - v2*h*road.angle_cos)/2
        vertices = [(x + d_x(v1,v2), y + d_y(v1,v2)) for v1,v2 in [(0,-1), (0,1), (2,1), (2,-1)]]

        gfxdraw.filled_polygon(screen, vertices, color)

    def draw_vehicle(screen, road, vehicle : Vehicle):
        color = vehicle.color
        l = -vehicle.length
        h = vehicle.width
        # road : Road = roads[vehicle.path[vehicle.current_road]]
        road_x, road_y = road.start
        x = road_x + road.angle_cos * vehicle.x
        y = road_y + road.angle_sin * vehicle.x
        
        d_x = lambda v1,v2 : (v1*l*road.angle_cos + v2*h*road.angle_sin)/2
        d_y = lambda v1,v2 : (v1*l*road.angle_sin - v2*h*road.angle_cos)/2
    
        vertices = [(x + d_x(v1, v2), y + d_y(v1, v2)) for v1,v2 in [(0,-1), (0,1), (2,1), (2,-1)]]
        
        gfxdraw.filled_polygon(screen, vertices, color)