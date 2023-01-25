

from models.road import Road


class connection_road():
    ''' Class to create the connection between two roads, used for drawing a curve smoothly'''
    
    def __init__(self, road_1, road_2, curve_point, steps = 15):
        
        road_locations = []
        if steps != 0:
            road_locations.extend([
                *connection_road.get_curve_road(road_1.end, road_2.start, curve_point, steps)])
        
        self.roads = [Road(r_loc[0], r_loc[1]) for r_loc in road_locations] + [road_2]
        self.from_road = road_1
        self.to_road = road_2
        
    def CarsTurning(self):
        for road in self.roads:
            if len(road.vehicles):
                return True
        return False

    def get_curve_road(init_point, end_point, inclination_point, steps = 15):
        points = connection_road.create_curve_road_points(init_point, end_point, inclination_point, steps)
    
        roads = []
        for i in range(len(points) - 1):
            roads.append((points[i], points[i+1]))
            
        return roads
    
    def create_curve_road_points(init_point, end_point, inclination_point, steps = 15):
        points = []
        
        for i in range(steps + 1):
            t = i/steps
            x = init_point[0] * (1-t)**2 + 2 * (1-t) * t * inclination_point[0] + t**2 * end_point[0]
            y = init_point[1] * (1-t)**2 + 2 * (1-t) * t * inclination_point[1] + t**2 * end_point[1]
            points.append((x,y))   
        
        return points
 