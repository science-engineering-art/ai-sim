from typing import List, Tuple
from shapely.geometry import MultiPolygon, Polygon, LineString


def build_rect( 
        start: Tuple[float,float], 
        end: Tuple[float,float],
        width: float = 3
    ) -> List[Tuple[float,float]]:
    
    x0, y0 = start
    x1, y1 = end

    if x0**2 + y0**2 > x1**2 + y1**2:
        x0, y0 = end
        x1, y1 = start

    # vector from start to end
    vX, vY = x1 - x0, y1 - y0   
    # normal vector
    nX, nY = -vY, vX

    # normalize
    n = (nX**2 + nY**2)**0.5
    nX, nY = width/n * nX, width/n * nY

    # third vector
    x2, y2 = x1 + nX, y1 + nY
    # fourth vector
    x3, y3 = x0 + nX, y0 + nY

    rect = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
    rect = [(x - nX * width / 2, y - nY * width / 2) for x, y in rect]

    return rect

def build_polygon(line: LineString):
    
    last = None
    for c in line.__geo_interface__['coordinates']:
        if last == None:
            last = c
            continue
    
        pts = build_rect(last, c)




class Car:...


class Road(MultiPolygon): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Lane(Polygon):
    def __init__(self, line: LineString):
        build_polygon(line)

        self.cars = List[Tuple[float, Car]]


def create_curve_road_points(init_point, end_point, inclination_point, steps = 15):
    points = []
    
    for i in range(steps + 1):
        t = i/steps
        x = init_point[0] * (1-t)**2 + 2 * (1-t) * t * inclination_point[0] + t**2 * end_point[0]
        y = init_point[1] * (1-t)**2 + 2 * (1-t) * t * inclination_point[1] + t**2 * end_point[1]
        points.append((x,y))   
    
    return points


def get_curve_road(init_point, end_point, inclination_point, steps = 15):
    points = create_curve_road_points(init_point, end_point, inclination_point, steps)
    
    roads = []
    for i in range(len(points) - 1):
        roads.append((points[i], points[i+1]))
        
    return roads 