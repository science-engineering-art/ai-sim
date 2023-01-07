

from audioop import reverse
from cmath import sqrt
from distutils.dir_util import remove_tree
from heapq import heappop, heappush
from numpy import Inf
from pygame import init
from sklearn.metrics import euclidean_distances
# from models.new_control import new_cControl
from models.road import Road

class A_star:
    
    def SetDraw(setdraw):
        global draw
        draw = setdraw
    
    def euclidean_distance(ctrl, next_road_id, end_road_id):
        init_point = ctrl.roads[next_road_id].end
        end_point = ctrl.roads[end_road_id].start
        return sqrt((end_point[1] - init_point[1])**2 + (end_point[0] - init_point[0])**2).real
    
    def my_herusistic(ctrl, next_road_id, end_road_id):
        return A_star.euclidean_distance(ctrl, next_road_id, end_road_id)
        
    def real_distance(ctrl, init_road_id, last_road_id, next_road_id):
        return ctrl.roads[next_road_id].length
        
    def find_shortest_path(ctrl, init_road_id : Road, end_road_id : Road, g_increment = real_distance, h = euclidean_distance):
        
        init_road = ctrl.roads[init_road_id]
        end_road = ctrl.roads[end_road_id]
        queue = []
        
        p = [-1 for _ in range(len(ctrl.roads))]
        f = [Inf for _ in range(len(ctrl.roads))]
        f[init_road_id] = h(ctrl, init_road_id, end_road_id)
        heappush(queue, (f[init_road_id], init_road_id))    
        
        while len(queue) > 0:
            d, road_id = heappop(queue)
            road : Road = ctrl.roads[road_id]
            if road_id == end_road_id:
                break
            if not road.end_conn:
                continue
            for next_road_id in road.end_conn.follow[road_id]:
                increment = g_increment(ctrl, init_road_id, road_id, next_road_id)
                h_val = h(ctrl, next_road_id, end_road_id)
                if f[next_road_id] <= d + increment + h_val:
                    continue
                p[next_road_id] = road_id
                f[next_road_id] = d + increment + h_val
                heappush(queue, (f[next_road_id], next_road_id))
                
        path = []
        road_id = end_road_id
        while road_id != init_road_id:
            path.append(road_id)
            road_id = p[road_id]
            
        path.append(road_id)
        path.reverse()
        
        return path
            
            
    def my_g_increment_function(ctrl, init_road_id, current_road_id, next_road_id):
        car = ctrl.AddRoutedVehicle(current_road_id, next_road_id)
        car.color = (255, 255, 255)
        if draw != None:
            return draw.ObserveVehicle(car, len(car.path))
        else:
            return ctrl.ObserveVehicle(car, len(car.path))
        