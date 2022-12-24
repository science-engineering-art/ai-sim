import pygame
from pygame import gfxdraw
from pygame.locals import *
from pyparsing import python_style_comment

from models.road import Road
from models.vehicle import Vehicle

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

pygame.init()
screen = pygame.display.set_mode((1400,800))
pygame.display.update()
roads = []

def draw_road(screen, road : Road, color):
    x, y = road.start
    l = road.length
    h = 10
    
    d_x = lambda v1,v2 : (v1*l*road.angle_cos + v2*h*road.angle_sin)/2
    d_y = lambda v1,v2 : (v1*l*road.angle_sin - v2*h*road.angle_cos)/2
    vertices = [(x + d_x(v1,v2), y + d_y(v1,v2)) for v1,v2 in [(0,-1), (0,1), (2,1), (2,-1)]]

    gfxdraw.filled_polygon(screen, vertices, color)

def draw_vehicle(scree, vehicle : Vehicle, color):
    l = vehicle.length
    h = vehicle.width
    road : Road = roads[vehicle.path[vehicle.current_road]]
    road_x, road_y = road.start
    x = road_x + road.angle_cos * vehicle.x
    y = road_y + road.angle_sin * vehicle.x
    
    d_x = lambda v1,v2 : (v1*l*road.angle_cos + v2*h*road.angle_sin)/2
    d_y = lambda v1,v2 : (v1*l*road.angle_sin - v2*h*road.angle_cos)/2
   
    vertices = [(x + d_x(v1, v2), y + d_y(v1, v2)) for v1,v2 in [(0,-1), (0,1), (2,1), (2,-1)]]
    
    gfxdraw.filled_polygon(screen, vertices, color)

def createRoads(pair_point_list):
    
    roads = []
    for x, y in pair_point_list:
        roads.append(Road(x,y))
        
    return roads
    

pos_x, pos_y, end_y, start_x, curv = 700, 400, 900, 0, 40

road_locations = [
    ((start_x, pos_y),(pos_x, pos_y)),
    ((pos_x + curv, pos_y + curv), (pos_x + curv, end_y)),
    *Road.get_curve_road    ((pos_x, pos_y), (pos_x + curv, pos_y + curv),  ( pos_x + curv, pos_y))
]

# road_locations = [
#     ((0,400),(700,400)),
#     ((710,410),(710,900)),
#     ((pos_x,start_y),(pos_x, pos_y)),
#     ((pos_x + curv, pos_y + curv), (end_x, pos_y + curv)),
#     # Road((700,400),(1400,400))
#     *Road.get_curve_road((700,400), (710,410), (710, 400))
#     *Road.get_curve_road((pos_x + curv, pos_y + curv), (pos_x, pos_y), ( pos_x + curv, pos_y))
# ]

roads = [Road(x,y) for x,y in road_locations]

car = Vehicle(0, 401, 14,7, [0,1,2,3,4])

# car.stopped = True
# vehicles = [
#     car,
#     Vehicle(0,401,14,7),
#     Vehicle(0,401,14,7)
# ]

running = True
count = 0
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            # running = False
            # car.stopped = False
        print(event)
    
    screen.fill((220,220,220))
    
    for road in roads:
        draw_road(screen,road, GRAY)
    
    draw_vehicle(screen, car, BLUE)
    
    # vehicles[0].update()
    # gfxdraw.box(screen, vehicles[0].get_rect, BLUE)
    # for i in range(1, len(vehicles)):
    #     vehicles[i].update(1/60, vehicles[i-1])
    #     gfxdraw.box(screen, vehicles[i].get_rect, BLUE)
    
    pygame.display.update()

pygame.quit()
