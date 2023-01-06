

from models.road import Road


class connection_road():
    
    def __init__(self, road_1, road_2, curve_point):
        
        road_locations = [
            *connection_road.get_curve_road(road_1.end, road_2.start, curve_point)]
        
        self.roads = [Road(r_loc[0], r_loc[1]) for r_loc in road_locations]

        # the next road of each road of the curve is assigned
        for i in range(0, len(road_locations) - 1):
            self.roads[i].end_conn = self.roads[i+1]
        
    
    
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
 