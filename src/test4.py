import heapq
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


def is_valid(pt):
    return pt[0] >= 0 and pt[0] <= 1400 and pt[1] >= 0 and pt[1] <= 800


while len(stack) > 0:
    
    vX, vY = heapq.heappop(stack)
    pts = [(vX + 100, vY), (vX - 100, vY), (vX, vY + 100), (vX, vY - 100)]

    for pt in pts:
        if ((vX, vY), pt) not in edges and (pt, (vX, vY)) not in edges \
            and is_valid(pt):

            pt0 = (vX, vY)
            pt1 = pt
            
            if (pt0[0]**2 + pt0[1]**2)**0.5 > (pt1[0]**2 + pt1[1]**2)**0.5:
                pt0 = pt
                pt1 = (vX, vY)
            
            ctrl.build_roads(pt0, pt1, 1, 1, 4)
            heapq.heappush(stack, pt)
            edges.add((pt0, pt1))


ctrl.build_intersections()

# print(ctrl.extremeRoads)
ctrl.Start(it_amount=1000, draw=True)
