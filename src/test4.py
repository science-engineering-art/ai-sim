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

ctrl.build_roads((700,400), (1380,400), 1, 1, 10)
ctrl.build_roads((700,10)  , (700,400) , 1, 1, 10)
ctrl.build_roads((10,400)  , (700,400) , 1, 1, 10)
ctrl.build_roads((700,400), (700,790) , 1, 1, 10)
ctrl.build_intersections()

# for road in ctrl.roads:
#     print(road.start, road.end)

ctrl.Start()

# mask = set()
# mask.add((700,400))
# stack = [(700,400)]


# def is_valid(pt):
#     return pt[0] >= 0 and pt[0] <= 1400 and pt[1] >= 0 and pt[1] <= 800


# while len(stack) > 0:
    
#     vX, vY = heapq.heappop(stack)
#     pts = [(vX + 100, vY), (vX - 100, vY), (vX, vY + 100), (vX, vY - 100)]

#     for pt in pts:
#         if pt not in mask and is_valid(pt):
#             road_id = ctrl.AddRoad((vX,vY), pt)
#             heapq.heappush(stack, pt)
#             mask.add(pt)


# print(mask)

# pos_x, pos_y, end_y, start_x, curv = 700, 410, 900, 0, 5
# road_WC_id = ctrl.AddRoad((start_x, pos_y), (pos_x, pos_y))
# road_CW_id = ctrl.AddRoad((pos_x, pos_y - 10), (start_x, pos_y- 10))
# road_CS_id = ctrl.AddRoad((pos_x + curv, pos_y + curv), (pos_x + curv, end_y))
# road_curWCS_ids = ctrl.connect_roads(road_WC_id, road_CS_id, (pos_x + curv, pos_y))


# pos_x, pos_y, end_y, start_x, curv = 720, 400, 200, 1400, -5
# road_EC_id = ctrl.AddRoad((start_x, pos_y), (pos_x, pos_y))
# road_CE_id = ctrl.AddRoad((pos_x, pos_y + 10), (start_x, pos_y + 10))
# road_CN_id = ctrl.AddRoad((pos_x + curv, pos_y + curv), (pos_x + curv, end_y))


# road_curvECN_ids = ctrl.connect_roads(road_EC_id, road_CN_id, (pos_x + curv, pos_y))
# road_curvECW_ids = ctrl.connect_roads(road_EC_id, road_CW_id, (pos_x, pos_y))
# road_curvWCE_ids = ctrl.connect_roads(road_WC_id, road_CE_id, (pos_x, pos_y + 10))
# road_curvWCN_ids = ctrl.connect_roads(road_WC_id, road_CN_id, (pos_x - curv, pos_y))
# road_curvECS_ids = ctrl.connect_roads(road_EC_id, road_CS_id, (pos_x + curv, pos_y))


# curv_x = -5; curv_y = -5; 
# road_NE_id = ctrl.AddRoad((pos_x, end_y + curv_y), (start_x, end_y + curv_y))
# road_curvCNE_ids = ctrl.connect_roads(road_CN_id, road_NE_id, (pos_x + curv_x, end_y + curv_y))


# ctrl.AddExtremeRoads([road_WC_id, road_EC_id])
# ctrl.CreateCorner([(road_WC_id, road_CS_id, 0), (road_EC_id, road_CN_id, 1), (road_EC_id, road_CW_id, 1),\
#     (road_WC_id, road_CN_id, 0), (road_EC_id, road_CS_id,1), (road_WC_id, road_CE_id, 0)])
# ctrl.roads[road_CN_id].end_conn = ctrl.roads[road_NE_id]
# ctrl.curves[(road_NE_id, road_NE_id)] = road_curvCNE_ids
# ctrl.Start()
