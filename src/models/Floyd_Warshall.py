
from this import d
from numpy import Inf
from models.road import Road
import dictdatabase as ddb

st_distances_matrix = {}
st_path_matrix = {}
big = True

def GetPathsMatrix(ctrl):
    
    global st_path_matrix
    
    if st_path_matrix.get(ctrl.name):
       return  st_path_matrix[ctrl.name]
    
    if big:
        s = ddb.at('Floyd_Warshall_' + ctrl.name)
        if s.exists():
            json = s.read()
            st_path_matrix[ctrl.name] = json['matrix']
            return st_path_matrix[ctrl.name]
        
    #setting intial values
    path_matrix = [[[] for road_to in range(len(ctrl.roads))] for road_in in range(len(ctrl.roads))]
    parents_matrix = [[None for road_to in range(len(ctrl.roads))] for road_in in range(len(ctrl.roads))]
    distances_matrix = [[Inf for road_to in range(len(ctrl.roads))] for road_in in range(len(ctrl.roads))]
    
    for road_from_id in range(len(ctrl.roads)):
        distances_matrix[road_from_id][road_from_id] = 0
                
    for road_from_id in range(len(ctrl.roads)):
        road_from = ctrl.roads[road_from_id]
        for road_to_id in range(len(ctrl.roads)):
            if road_from.end_conn and road_to_id in road_from.end_conn.follow[road_from_id]:
                distances_matrix[road_from_id][road_to_id] = road_from.length
                parents_matrix[road_from_id][road_to_id] = road_from_id
                 
    for road_max_id in range(len(ctrl.roads)):
        print(road_max_id)
        for road_from_id in range(len(ctrl.roads)):
            for road_to_id in range(len(ctrl.roads)):
                if distances_matrix[road_from_id][road_max_id] + distances_matrix[road_max_id][road_to_id] < \
                                                                    distances_matrix[road_from_id][road_to_id]:
                    distances_matrix[road_from_id][road_to_id] = distances_matrix[road_from_id][road_max_id] \
                        + distances_matrix[road_max_id][road_to_id]
                    parents_matrix[road_from_id][road_to_id] = parents_matrix[road_max_id][road_to_id]
    
    
    #addind last road length to the length of the path    
    for road_from_id in range(len(ctrl.roads)):
        for road_to_id in range(len(ctrl.roads)):
            if distances_matrix[road_from_id][road_to_id] < Inf:
                distances_matrix[road_from_id][road_to_id] +=ctrl.roads[road_to_id].length

    for road_from_id in range(len(ctrl.roads)):
        for road_to_id in range(len(ctrl.roads)):
            if distances_matrix[road_from_id][road_to_id] >= Inf:
                continue
            road_middle = road_to_id
            path_matrix[road_from_id][road_to_id].append(road_middle)
            while road_middle != road_from_id:
                road_middle = parents_matrix[road_from_id][road_middle]
                path_matrix[road_from_id][road_to_id].append(road_middle)
            path_matrix[road_from_id][road_to_id].reverse()

    st_distances_matrix[ctrl.name] = distances_matrix
    st_path_matrix[ctrl.name] = path_matrix
    
    if big:
        s.create({
            'matrix' :  st_path_matrix[ctrl.name]}
        )
    
    return path_matrix

def GetPath(ctrl, road_from_id, road_to_id):
    path_matrix = GetPathsMatrix(ctrl)
    return path_matrix[road_from_id][road_to_id]