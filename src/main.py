import pygame
from pygame import gfxdraw
from pygame.locals import *

from models.vehicle import Vehicle
from models.road import Road

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

pygame.init()
screen = pygame.display.set_mode((1400,800))
pygame.display.update()

roads = [
    Road(0,400,1400,10),
    Road(700,400,10,100)
]
car = Vehicle(650, 401, 14,7)
car.stopped = True
vehicles = [
    car,
    Vehicle(60,401, 14,7),
    Vehicle(40,401,14,7)
]
running = True
count = 0
while running:
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        print(event)
    
    screen.fill((220,220,220))
    
    for road in roads:
        gfxdraw.box(screen, road, GRAY)
    
    vehicles[0].update()
    gfxdraw.box(screen, vehicles[0].get_rect, BLUE)
    for i in range(1, len(vehicles)):
        vehicles[i].update(1/60, vehicles[i-1])
        gfxdraw.box(screen, vehicles[i].get_rect, BLUE)
    
    pygame.display.update()
        

pygame.quit()
