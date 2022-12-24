import pygame
from pygame import gfxdraw
from pygame.locals import *
from pyparsing import python_style_comment

from models.corner import corner
from models.corner import corner
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

def draw_vehicle(screen, vehicle : Vehicle, color):
    l = -vehicle.length
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
    

pos_x, pos_y, end_y, start_x, curv = 700, 400, 900, 0, 5

road_locations = [
    ((start_x, pos_y),(pos_x, pos_y)),
    ((pos_x + curv, pos_y + curv), (pos_x + curv, end_y)),
    *Road.get_curve_road((pos_x, pos_y), (pos_x + curv, pos_y + curv),  ( pos_x + curv, pos_y)),
    
]

pos_x, pos_y, end_y, start_x, curv = 710, 400, 0, 1400, -5
road_locations.extend([
    ((start_x, pos_y),(pos_x, pos_y)),
    ((pos_x + curv, pos_y + curv), (pos_x + curv, end_y)),
    *Road.get_curve_road((pos_x, pos_y), (pos_x + curv, pos_y + curv),  ( pos_x + curv, pos_y)),
])

corn = corner(light_controled=True)
corn.addIncomingRoads([0,17])
corn.addOutgoingRoads([1,18])
corn.addFollow(17,18)
corn.addFollow(0,1)

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

car = Vehicle(100, 401, 14,7, [0, *range(2,17), 1])
# car2 = Vehicle(0, 401, 14,7, [0, *range(2,17), 1])
# car2.v = 20
# car2.a = 100

# car.stopped = True
vehicles = [
    car,
    Vehicle(0,401,14,7,[0, *range(2,17), 1]),
    Vehicle(0,401,14,7, [0, *range(2,17), 1]),
    Vehicle(0,401,14,7, [0, *range(2,17), 1]),
    Vehicle(0,401,14,7, [0, *range(2,17), 1]),
    Vehicle(0,401,14,7, [0, *range(2,17), 1]),
    Vehicle(0,401,14,7, [0, *range(2,17), 1])
]

vehicles2 = [
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
    Vehicle(0,401,14,7,[17, *range(19, 32), 18]),
]

toDelete = []
running = True
count = 0
# print(corn.times)
# print(corn.myturn[(0,1)])
# print(corn.myturn[(17,18)])
# print(corn.numberOfTurns)

while running:
    # break    
    corn.tick()
    # print(corn.current_turn)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            # running = False
            # car.stopped = False
        print(event)
    
    screen.fill((220,220,220))
    
    for road in roads:
        draw_road(screen,road, GRAY)
    
    
    # gfxdraw.box(screen, vehicles[0].get_rect, BLUE)
    for i in range(0, len(vehicles)):
        car2 = vehicles[i]
        
        if i != 0: 
            car2.update(lead=vehicles[i-1])
        else:
            car2.update()
        
        if car2.x > roads[car2.path[car2.current_road]].length:
            if car2.current_road == len(car2.path) - 1:
                toDelete.append(car2)
            else:
                x1, x2 = car2.path[car2.current_road], car2.path[car2.current_road] + 1
                print(x1,x2, corn.myturn.get((x1,x2)))
                if corn.myturn.get((x1,x2)) != None:
                    print(corn.myturn[(x1,x2)])
                if corn.myturn.get((x1,x2)) == None or corn.CanIPass(x1,x2):
                    car2.stopped = False
                    car2.current_road+=1
                    car2.x = 0
                else:
                    car2.stopped = True
                    
            
    for car2 in toDelete:
        vehicles.remove(car2)
    toDelete = []
    
    for i in range(0, len(vehicles)):
        car2 = vehicles[i]
        draw_vehicle(screen, car2, BLUE)
        
    for i in range(0, len(vehicles2)):
        car2 = vehicles2[i]
        
        if i != 0: 
            car2.update(lead=vehicles2[i-1])
        else:
            car2.update()
        
        if car2.x > roads[car2.path[car2.current_road]].length:
            if car2.current_road == len(car2.path) - 1:
                toDelete.append(car2)
            else:
                x1, x2 = car2.path[car2.current_road], car2.path[car2.current_road] + 1
                print(x1,x2, corn.myturn.get((x1,x2)))
                if corn.myturn.get((x1,x2)) != None:
                    print(corn.myturn[(x1,x2)])
                if corn.myturn.get((x1,x2)) == None or corn.CanIPass(x1,x2):
                    car2.stopped = False
                    car2.current_road+=1
                    car2.x = 0
                else:
                    car2.stopped = True
            
    for car2 in toDelete:
        vehicles2.remove(car2)
    toDelete = []
    
    for i in range(0, len(vehicles2)):
        car2 = vehicles2[i]
        draw_vehicle(screen, car2, BLUE)
    
    pygame.display.update()

# pygame.quit()
