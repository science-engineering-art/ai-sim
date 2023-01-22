from math import sqrt
from heapq import heappop, heappush
from sys import maxsize as Inf
from models.road import Road

class A_star:
    
    def SetDraw(setdraw):
        global draw
        draw = setdraw
    
    def euclidean_distance(ctrl, next_road_id, end_road_id, v = None):
        init_point = ctrl.roads[next_road_id].end
        end_point = ctrl.roads[end_road_id].start
        return sqrt((end_point[1] - init_point[1])**2 + (end_point[0] - init_point[0])**2).real
    
    def my_herusistic(ctrl, next_road_id, end_road_id, v = None):
        return A_star.euclidean_distance(ctrl, next_road_id, end_road_id)
        
    def real_distance(ctrl, init_road_id, last_road_id, next_road_id):
        return ctrl.roads[next_road_id].length
        
    def find_shortest_path(ctrl, init_road_id : Road, end_road_id : Road, g_increment = real_distance, h = euclidean_distance):
        
        queue = []
        
        p = [-1 for _ in range(len(ctrl.roads))]
        f = [Inf for _ in range(len(ctrl.roads))]
        f[init_road_id] = g_increment(ctrl, init_road_id, init_road_id, init_road_id) + h(ctrl, init_road_id, end_road_id)
        heappush(queue, (f[init_road_id], init_road_id))    
        
        while len(queue) > 0:
            d, road_id = heappop(queue)
            road : Road = ctrl.roads[road_id]
            if road_id == end_road_id:
                break
            if not road.end_conn:
                continue
            for next_road_id in road.end_conn.follow[road_id]:
                increment = g_increment(ctrl, init_road_id, next_road_id, next_road_id)
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
    
    def CalculateIncrements(ctrl, road, road_id):
        cars = []
        for next_road_id in road.end_conn.follow[road_id]:
            car = ctrl.AddRoutedVehicle(next_road_id, next_road_id)
            car.color = (255, 255, 255)
            cars.append(car)
        if draw != None:
            return draw.ObserveVehicles(cars)
        else:
            return ctrl.ObserveVehicles(cars)
                
    def dijkstra_base_heuristic(ctrl, next_road_id, end_road_id, d):
        return d[next_road_id]
        
    def find_shortest_path_parallel(ctrl, init_road_id : Road, end_road_id : Road, g_increment = real_distance, h = euclidean_distance):
        
        dddd = A_star.Dikjstra(ctrl,end_road_id)
        
        queue = []
        
        p = [-1 for _ in range(len(ctrl.roads))]
        f = [Inf for _ in range(len(ctrl.roads))]
        f[init_road_id] = g_increment(ctrl, init_road_id, init_road_id, init_road_id) + h(ctrl, init_road_id, end_road_id, dddd)
        heappush(queue, (f[init_road_id], init_road_id))    
        
        while len(queue) > 0:
            d, road_id = heappop(queue)
            print(road_id)
            road : Road = ctrl.roads[road_id]
            if road_id == end_road_id:
                break
            if not road.end_conn:
                continue
            increments = A_star.CalculateIncrements(ctrl, road, road_id)
            for i in range(len(road.end_conn.follow[road_id])):
                next_road_id = road.end_conn.follow[road_id][i]
                h_val = h(ctrl, next_road_id, end_road_id, dddd)
                if f[next_road_id] <= d + increments[i] + h_val:
                    continue
                p[next_road_id] = road_id
                f[next_road_id] = d + increments[i] + h_val
                heappush(queue, (f[next_road_id], next_road_id))
                
        path = []
        road_id = end_road_id
        while road_id != init_road_id:
            path.append(road_id)
            road_id = p[road_id]
            
        path.append(road_id)
        path.reverse()
        
        return path
    
    def Dikjstra(ctrl, end_road_id : Road):
        
        queue = []
        f = [Inf for _ in range(len(ctrl.roads))]
        visited = [False for _ in range(len(ctrl.roads))]
        start_conn = [None for _ in range(len(ctrl.roads))] 
        inverse_conn = {}
        
        end_road = ctrl.roads[end_road_id]
        f[end_road_id] = end_road.length / ctrl.basic_vehicles[0].v_max
        heappush(queue, (f[end_road_id], end_road_id))    
        
        for corner in ctrl.corners:
            inverse_conn[corner] = {}
            for road_id in corner.OutgoingRoads:
                start_conn[road_id] = corner
                inverse_conn[corner][road_id] = []
            for road_id in corner.IncomingRoads:
                for out_road in corner.follow[road_id]:
                    inverse_conn[corner][out_road].append(road_id)
        
        while len(queue) > 0:
            d, road_id = heappop(queue)
            if visited[road_id]:
                continue
            
            if not start_conn[road_id]:
                continue
            
            for next_road_id in inverse_conn[start_conn[road_id]][road_id]:
                c =  ctrl.roads[next_road_id].length / ctrl.basic_vehicles[0].v_max
                f_val = start_conn[road_id].times[start_conn[road_id].myturns[(next_road_id, road_id)][0]]+ c
                if f[next_road_id] <= d + f_val:
                    continue
                f[next_road_id] = d + f_val
                heappush(queue, (f[next_road_id], next_road_id))
                
        return f