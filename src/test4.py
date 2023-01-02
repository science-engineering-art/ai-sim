import heapq
from time import time
from models.control import control
from models.road import Road


# class MultiLane:

#     def __init__(self, start, end, inN, outN, width):
#         self.roads = []
#         self.__build_roads(start, end, inN, outN, width)

#     def __build_roads(self, start, end, inN, outN, width):        
#         x0, y0 = start
#         x1, y1 = end

#         if x0**2 + y0**2 > x1**2 + y1**2:
#             x0, y0 = end
#             x1, y1 = start

#         vX, vY = x1-x0, y1-y0
#         nX, nY = vY, -vX

#         #normalize
#         n = (nX**2 + nY**2)**0.5
#         nX, nY = width/n*nX, width/n*nY 

#         n = (inN + outN) / 2
#         rX, rY = n * -nX, n * -nY

#         if (inN + outN) % 2 == 0:
#             rX, rY = rX + width/2 * nX, rY + width/2 *nY

#         start = start[0] + rX, start[1] + rY
#         end   = end[0] + rX, end[1] + rY

#         for _ in range(outN):
#             self.roads.append(Road(end, start))
#             start = start[0] + nX, start[1] + nY
#             end   = end[0] + nX  , end[1] + nY 

#         for _ in range(inN):
#             self.roads.append(Road(start, end))
#             start = start[0] + nX, start[1] + nY
#             end   = end[0] + nX  , end[1] + nY 

ctrl = control()


edges = set()
stack = [(700,400)]
len_roads = 92

def is_valid(pt):
    return pt[0] >= 0 and pt[0] <= 1400 and pt[1] >= 0 and pt[1] <= 800

def calculate_limits(center_pt, len_roads):
    x, y = center_pt
    X, Y = center_pt

    while x > 0 or y > 0 or X < 1400 or Y < 800:
        if x > 0: x -= len_roads
        if X < 1400: X += len_roads
        if y > 0: y -= len_roads
        if Y < 800: Y += len_roads
    else:
        x += len_roads
        X -= len_roads
        y += len_roads
        Y -= len_roads
    
    return x, X, y, Y

x, X, y, Y = calculate_limits((700, 400), len_roads)

while len(stack) > 0:
    
    vX, vY = heapq.heappop(stack)
    pts = [(vX + len_roads, vY), (vX - len_roads, vY), (vX, vY + len_roads), (vX, vY - len_roads)]

    for pt in pts:
        if ((vX, vY), pt) not in edges and (pt, (vX, vY)) not in edges \
            and is_valid(pt):

            pt0 = (vX, vY)
            pt1 = pt
            
            if (pt0[0]**2 + pt0[1]**2)**0.5 > (pt1[0]**2 + pt1[1]**2)**0.5:
                pt0 = pt
                pt1 = (vX, vY)
            
            if (pt0[0] == pt1[0] and (pt0[0] == x or pt0[0] == X)) or \
                (pt0[1] == pt1[1] and (pt0[1] == y or pt0[1] == Y)): 
                continue

            ctrl.build_roads(pt0, pt1, 1, 1, 4)
            heapq.heappush(stack, pt)
            edges.add((pt0, pt1))


ctrl.build_intersections()
print(ctrl.extremeRoads)
# for road in ctrl.roads:
#     if not ctrl.is_curve[ctrl.roads.index(road)]:
#         print(road.length)
# print(ctrl.extremeRoads)
t = time()
ctrl.speed = 10
for er in ctrl.extremeRoads: #adjusting generation rate
    ctrl.roads[er].Lambda = 1/150
ctrl.Start(observation_time=120, draw=True)

to_print_1 = []
to_print_2 = []
for road_id in range(len(ctrl.road_max_queue)):
    if not ctrl.is_curve[road_id]:
        to_print_1.append(ctrl.road_max_queue[road_id])
        to_print_2.append(ctrl.road_average_time_take_cars[road_id] * ctrl.dt)
print(to_print_1)
print(to_print_2)
print( time() - t)
