
from numpy import Inf
# from models.control import control
from models.road import Road


st_distances_matrix = {}
st_path_matrix = {}


def GetPathsMatrix(ctrl ):
    
    if st_path_matrix.get(ctrl):
       return  st_path_matrix[ctrl]
   
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
                # path_matrix[road_from_id][road_to_id] = [road_from_id]
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
                    # path_matrix[road_from_id][road_to_id] = path_matrix[road_from_id][road_max_id] + \
                        # path_matrix[road_max_id][road_to_id]
                    parents_matrix[road_from_id][road_to_id] = parents_matrix[road_max_id][road_to_id]
    
    
    #addind last road length to the length of the path    
    for road_from_id in range(len(ctrl.roads)):
        for road_to_id in range(len(ctrl.roads)):
            if distances_matrix[road_from_id][road_to_id] < Inf:
                distances_matrix[road_from_id][road_to_id] +=ctrl.roads[road_to_id].length
                # path_matrix[road_from_id][road_to_id].append(road_to_id)

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

    st_distances_matrix[ctrl] = distances_matrix
    st_path_matrix[ctrl] = path_matrix
    
    return path_matrix

def GetPath(ctrl, road_from_id, road_to_id):
    path_matrix = GetPathsMatrix(ctrl)
    return path_matrix[road_from_id][road_to_id]