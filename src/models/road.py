from ctypes import create_unicode_buffer
from typing import List, Tuple
from venv import create
from scipy.spatial import distance


class Road:
    def __init__(self, start:Tuple[int,int], end: Tuple[int,int]):
        self.start = start
        self.end = end
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        self.vehicles = []
        self.end_conn = None

    @property
    def get_rect(self):
        x0,y0 = self.start
        x1,_ = self.end
        return (x0, y0, x1-x0, 10)
    
    def get_curve_road(init_point, end_point, inclination_point, steps = 15):
        points = Road.create_curve_road_points(init_point, end_point, inclination_point, steps)
        
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
            
    

