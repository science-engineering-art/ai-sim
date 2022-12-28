import pygame
import osmnx as ox
from map import Map

# Ciudad Deportiva, Havana, Cuba
point = (23.1021, -82.3936)
G = ox.graph_from_point(point, dist=1000, retain_all=True, simplify=True, network_type='drive')
G = ox.project_graph(G)


from map import keep_map, load_map
keep_map(G)
streets = load_map()


RED = (255, 0, 0)
BLUE = (0, 0, 20)
GRAY = (150,150,150)
WHITE = (255, 255, 255)

inc = 0.8

m = Map(1400, 800, lng=inc*2555299.469922482, lat=inc*356731.10053785384, i_zoom=0.1)

last_x = -1
last_y = -1

while True:

    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                m.inc_zoom()
            elif event.button == 5: 
                m.dec_zoom()

        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1: 
                if last_x == last_y == -1:
                    last_x, last_y = event.pos
                else:
                    m.x += (event.pos[0] - last_x)/2
                    m.y += (event.pos[1] - last_y)/2
                    last_x, last_y = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                last_x = last_y = -1
        
        m.fill(WHITE)

        for st in streets:
            try:
                m.draw_road(st, inc, GRAY)
            except:
                pass

        m.update()
