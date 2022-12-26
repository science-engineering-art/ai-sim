# import osmnx as ox
# from shapely.geometry import LineString

# # Get the graph of the city of Berlin
# G = ox.graph_from_place('Havana, Cuba', network_type='drive')


# for n in G.nodes(data=True):
#     print(n)

# s = dict()
# types = set()
# i = 0


# for u, v, k, data in G.edges(keys=True, data=True):
#     try:
#         if data['name'] not in s:
#             s[data['name']] = [(u,v,data)]
#         else:
#             s[data['name']].append((u,v,data))
#     except:
#         pass
#     try:
#         if type(data['geometry']) not in types:
#             types.add(type(data['geometry']))
#         else:
#             i += 1
#     except:
#         pass


# for u, v, data in s['Domínguez']:
#     try:
#         print(u, v, data)
#         print()
#         road: LineString = data['geometry']
#         print(road.centroid)
#         print(road.xy)
#         print(road)
#         print()
#     except:
#         pass

# print(len(G.nodes()), len(G.edges()))


import pygame
from window import Window 


RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200,200,200)


w = Window(1400, 800)
w.zoom = 0.2
x0 = 700
y0 = 400
inc = 3
last_x = -1
last_y = -1

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                w.inc_zoom()
            elif event.button == 5: 
                w.dec_zoom()


        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1: 

                if last_x == last_y == -1:
                    last_x, last_y = event.pos
                else:
                    w.x += (event.pos[0] - last_x)/2
                    w.y += (event.pos[1] - last_y)/2
                    last_x, last_y = event.pos


        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                last_x = last_y = -1
        
        w.fill(GRAY)
        w.draw_polygon([(x0, y0), (x0+inc, y0), (x0+inc, y0+inc), (x0, y0+inc)], RED)
        w.update()
