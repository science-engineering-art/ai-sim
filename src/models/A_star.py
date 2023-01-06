

from audioop import reverse
from cmath import sqrt
from distutils.dir_util import remove_tree
from heapq import heappop, heappush
from numpy import Inf
from pygame import init
from sklearn.metrics import euclidean_distances
from models.road import Road

class A_star:
    
    def euclidean_distance(init_point, end_point):
        return sqrt((end_point[1] - init_point[1])**2 + (end_point[0] - init_point[0])**2).real
        
    def find_shortest_path(ctrl, init_road_id : Road, end_road_id : Road, h = euclidean_distance):
        
        init_road = ctrl.roads[init_road_id]
        end_road = ctrl.roads[end_road_id]
        queue = []
        p = [-1 for _ in range(len(ctrl.roads))]
        f = [Inf for _ in range(len(ctrl.roads))]
        f[init_road_id] = h(end_road.end, init_road.start)
        heappush(queue, (f[init_road_id], init_road_id))    
        while len(queue) > 0:
            d, road_id = heappop(queue)
            road : Road = ctrl.roads[road_id]
            if road_id == end_road_id:
                break
            if not road.end_conn:
                continue
            for next_road_id in road.end_conn.follow[road_id]:
                next_road = ctrl.roads[next_road_id]
                if f[next_road_id] <= d + next_road.length + h(next_road.end, end_road.start):
                    continue
                p[next_road_id] = road_id
                f[next_road_id] = d + next_road.length + h(next_road.end, end_road.start)
                heappush(queue, (f[next_road_id], next_road_id))
                
        path = []
        road_id = end_road_id
        while road_id != init_road_id:
            path.append(road_id)
            road_id = p[road_id]
        path.append(road_id)
        path.reverse()
        return path
            
    