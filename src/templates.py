import math
import heapq
from typing import Any, Dict, List, Tuple
from models.road import Road
from abc import abstractmethod
from scipy.spatial import distance
from models.control import control
from pydantic import BaseModel
import dictdatabase as ddb


class BaseNode:...


class Edge(BaseModel, BaseNode):
    id: int
    start: Tuple[float, float]
    end: Tuple[float, float]


class RoadEdge(BaseModel, BaseNode):
    lanes: List[int]


class CurveEdge(BaseModel, BaseNode):
    input_lane_id: int
    output_lane_id: int
    curve_point: Tuple[float, float]


class IntersectionNode(BaseModel, BaseNode):
    input_lanes: List[int]
    out_lanes: List[int]
    follows: List[Tuple[int, int, int]]


class Map(BaseModel, BaseNode):
    width_roads: float
    lanes: List[Edge]
    roads: List[RoadEdge]
    intersections: Dict[Tuple[float,float], IntersectionNode] 
    curves: List[CurveEdge]
    extremes_lanes: List[int] 
    

def iter_fields(node: 'NodeVisitor'):
    for field in node.__dict__:
        try: 
            yield field, getattr(node, field)
        except:...


class NodeVisitor:
    """
        JSON Serializer
    """
    def visit(self, node: 'NodeVisitor'):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node: 'NodeVisitor'):
        json = {}

        for key, value in iter_fields(node):
           
            if isinstance(value, list):
                json[key] = []
                for item in value:
                    if isinstance(item, BaseNode):
                        json[key].append(self.visit(item))
                    else:
                        json[key].append(item)
            
            elif isinstance(value, dict):
                if key not in json:
                    json[key] = {}
                for kw, item in value.items():
                    if isinstance(item, BaseNode):
                        if isinstance(kw, tuple):
                            x, y = kw
                            x, y = f"{x}", f"{y}"
                            if x not in json[key]:
                                json[key][x] = {}
                            if y not in json[key][x]:
                                json[key][x][y] = {}
                            json[key][x][y] = self.visit(item)
                        else:
                            json[key][kw] = self.visit(item)
            
            elif isinstance(value, BaseNode):
                json = {}
                for kw, item in iter_fields(value):
                    json[kw] = item
            
            else:
                json[key] = value

        return json


def calculate_angle(road_in: Road) -> float:
    x0, y0 = road_in.start
    x1, y1 = road_in.end

    if (x0**2 + y0**2) > (x1**2 + y1**2):
        tmp = x0, y0
        x0, y0 = x1, y1
        x1, y1 = tmp

    print(f'x0: {x0}, y0: {y0}, x1: {x1}, y1: {y1}')

    co = y1 - y0
    ca = x1 - x0

    if ca == 0 and co != 0:
        return 90.0

    h = (co**2 + ca**2)**0.5
    
    print(f'co: {co}, ca: {ca}, h: {h}')
    try: 
        angle = math.acos((co**2 + ca**2 - h**2) / (2 * co * ca))
        angle = math.degrees(angle)
    except:
        print('error 1')

    try: 
        angle = math.acos((co**2 + h**2 - ca**2) / (2 * co * h))
        angle = math.degrees(angle)
    except:
        print('error 2')

    try:
        angle = math.acos((h**2 + ca**2 - co**2) / (2 * h * ca))
        angle = math.degrees(angle)
    except:
        print('error 3')

    return angle


def calculate_curve_point(road_a: Road, road_b: Road):
    '''calculates the point where the curve should be created'''
    xa_0, ya_0 = road_a.start
    xa_1, ya_1 = road_a.end
    xb_0, yb_0 = road_b.start
    xb_1, yb_1 = road_b.end

    try:
        m_a = (ya_1 - ya_0) / (xa_1 - xa_0)
    except ZeroDivisionError:
        ...

    try:
        m_b = (yb_1 - yb_0) / (xb_1 - xb_0)
    except ZeroDivisionError:
        ...

    n_a = 0
    if xa_1 - xa_0 == 0:
        x = xa_0
        m_a = 0
    elif xb_1 - xb_0 == 0:
        x = xb_0
        m_a = 0
    else:
        n_a = ya_0 - xa_0*m_a
        n_b = yb_0 - xb_0*m_b
        x = (n_b - n_a) / (m_a - m_b)

    y = 0
    if ya_1 - ya_0 == 0:
        y = ya_0
    elif yb_1 - yb_0 == 0:
        y = yb_0
    else:
        y = m_a * x + n_a

    return (x, y) 


class BasicTemplate:

    def __init__(self, ctrl: control):
        self.ctrl = ctrl
        self.map = Map(
            width_roads=0,
            lanes=[],
            roads=[],
            intersections={},
            curves=[],
            extremes_lanes=[]
        )

    @abstractmethod
    def build_map(self) -> Map:
        pass

    def generate_template(self, name: str):
        self.build_map()

        s = ddb.at(name)
        if not s.exists():
            s.create(
                NodeVisitor().visit(self.map)
            )

    def build_roads(self, start, end, inN, outN, width):
        x0, y0 = start
        x1, y1 = end

        if x0**2 + y0**2 > x1**2 + y1**2:
            x0, y0 = end
            x1, y1 = start

        vX, vY = x1-x0, y1-y0
        nX, nY = vY, -vX

        # normalize
        n = (nX**2 + nY**2)**0.5
        nX, nY = width/n*nX, width/n*nY

        n = (vX**2 + vY**2)**0.5
        x0, y0 = x0 + vX * width / n, y0 + vY * width / n
        x1, y1 = x1 - vX * width / n, y1 - vY * width / n

        n = int((inN + outN) / 2)
        rX, rY = n * -nX, n * -nY

        if (inN + outN) % 2 == 0:
            rX, rY = rX + nX / 2, rY + nY / 2

        x0, y0 = x0 + rX, y0 + rY
        x1, y1 = x1 + rX, y1 + rY

        if start not in self.map.intersections:
            self.map.intersections[start] = IntersectionNode(
                input_lanes=[],
                out_lanes=[],
                follows=[]
            )
        if end not in self.map.intersections:
            self.map.intersections[end] = IntersectionNode(
                input_lanes=[],
                out_lanes=[],
                follows=[]
            )
        if start not in self.map.intersections:
            self.map.intersections[start] = IntersectionNode(
                input_lanes=[],
                out_lanes=[],
                follows=[]
            )
        if end not in self.map.intersections:
            self.map.intersections[end] = IntersectionNode(
                input_lanes=[],
                out_lanes=[],
                follows=[]
            )

        road = RoadEdge(
            lanes=[]
        )

        for _ in range(inN):
            # create road
            lane_id = len(self.map.lanes)
            lane = Edge(
                id=lane_id,
                start=(x0, y0),
                end=(x1, y1)
            )
            self.map.lanes.append(lane)
            road.lanes.append(lane_id)

            x0, y0 = x0 + nX, y0 + nY
            x1, y1 = x1 + nX, y1 + nY

            self.map.intersections[end].input_lanes.append(lane_id)
            self.map.intersections[start].out_lanes.append(lane_id)
            self.map.extremes_lanes.append(lane_id)

        for _ in range(outN):
            # create road
            lane_id = len(self.map.lanes)
            lane = Edge(
                id=lane_id,
                start=(x0, y0),
                end=(x1, y1)
            )
            self.map.lanes.append(lane)
            road.lanes.append(lane_id)

            x0, y0 = x0 + nX, y0 + nY
            x1, y1 = x1 + nX, y1 + nY

            self.map.intersections[start].input_lanes.append(lane_id)
            self.map.intersections[end].out_lanes.append(lane_id)
            self.map.extremes_lanes.append(lane_id)

        self.map.roads.append(road)

    def build_intersections(self):

        for x, y in self.map.intersections:
            follows = {}
            i = 0
            for in_lane_id in self.map.intersections[(x, y)].input_lanes:
                for out_lane_id in self.map.intersections[(x, y)].out_lanes:

                    print(f'{(x,y)}')

                    road_in: Edge = self.map.lanes[in_lane_id]
                    road_out: Edge = self.map.lanes[out_lane_id]

                    # check if road_in and road_out are parallel
                    if distance.euclidean(road_in.start, road_out.end) == \
                       distance.euclidean(road_in.end, road_out.start):
                        print(
                            f'PARALLEL: {(road_in.start, road_in.end)} -- {(road_out.start, road_out.end)}')
                        continue

                    x0, y0 = road_in.start[0] - \
                        road_in.end[0], road_in.start[1] - road_in.end[1]
                    x1, y1 = road_out.end[0] - \
                        road_out.start[0], road_out.end[1] - road_out.start[1]
                    sim = (x0 * x1 + y0 * y1) / \
                        ((x0**2 + y0**2)**0.5 * (x1**2 + y1**2)**0.5)

                    # check if road_in and road_out are the same road
                    if sim == 1 or sim == -1:
                        continue

                    print(f'connect {road_in.end} to {road_out.start}')
                    print(road_in.start, road_in.end,
                          road_out.start, road_out.end)
                    curve_pt = calculate_curve_point(road_in, road_out)
                    print(f'curve at {curve_pt}')
                    curve = CurveEdge(
                        input_lane_id=in_lane_id,
                        output_lane_id=out_lane_id,
                        curve_point=curve_pt
                    )
                    curve_id = len(self.map.curves)
                    self.map.curves.append(curve)
                    # self.ctrl.connect_roads(road_in_id, road_out_id, curve_pt)

                    try:
                        self.map.extremes_lanes.remove(out_lane_id)
                    except:
                        print(f'road_out_id {out_lane_id} not in extremeRoads')

                    angle = calculate_angle(road_in)

                    if i not in follows:
                        follows[i] = []

                    follows[i].append((angle, curve_id))
                i += 1

            tmp = follows
            follows = {}

            for i in tmp:
                angle, _ = tmp[i][0]

                for j in tmp:
                    if i == j: continue
                    
                    angle2, _ = tmp[j][0]

                    if angle > 180 and angle2 < 180:
                        angle %= 180
                    if angle < 180 and angle2 > 180:
                        angle2 %= 180                    
                    
                    if abs(angle - angle2) < 1e-8:
                        if angle not in follows:
                            follows[angle] = []
                        follows[angle] += [(curve_id, i) 
                            for _, curve_id in tmp[j]]

                if angle not in follows:
                    follows[angle] = []
                follows[angle] += [(
                    self.map.curves[curve_id].input_lane_id,
                    self.map.curves[curve_id].output_lane_id, i) 
                    for _, curve_id in tmp[i]]
            
            tmp = follows
            follows = []
            for _, tuples in tmp.items():
                follows += tuples

            if len(follows) > 0:
                self.map.intersections[(x, y)].follows = follows            


class GridMap(BasicTemplate):

    def __init__(self, 
        ctrl: control, 
        center_point: Tuple[float, float], 
        len_roads: float, 
        lower_limit_x: float = 0, 
        lower_limit_y: float = 0, 
        upper_limit_x: float = 1400, 
        upper_limit_y: float = 800,
        in_roads: int = 2,
        out_roads: int = 2,
        width_roads: float = 0.5
    ):
        super().__init__(ctrl)
        self.center_point = center_point
        self.len_roads = len_roads
        self.lower_limit_x = lower_limit_x
        self.lower_limit_y = lower_limit_y
        self.upper_limit_x = upper_limit_x
        self.upper_limit_y = upper_limit_y
        self.in_roads = in_roads
        self.out_roads = out_roads
        self.width_roads = width_roads
        self.recalculate_limits()

    def is_valid(self, pt):
        return pt[0] >= self.lower_limit_x and \
               pt[0] <= self.upper_limit_x and \
               pt[1] >= self.lower_limit_y and \
               pt[1] <= self.upper_limit_y

    def recalculate_limits(self):
        x, y = self.center_point
        X, Y = self.center_point

        while x > self.lower_limit_x or \
              y > self.lower_limit_y or \
              X < self.upper_limit_x or \
              Y < self.upper_limit_y:
            if x > self.lower_limit_x: x -= self.len_roads
            if y > self.lower_limit_y: y -= self.len_roads
            if X < self.upper_limit_x: X += self.len_roads
            if Y < self.upper_limit_y: Y += self.len_roads
            print(x, y, X, Y)
            print(x > self.lower_limit_x) 
            print(y > self.lower_limit_y)
            print(X < self.upper_limit_x)
            print(Y < self.upper_limit_y)
        else:
            x += self.len_roads
            X -= self.len_roads
            y += self.len_roads
            Y -= self.len_roads
        
        self.lower_limit_x = x
        self.lower_limit_y = y
        self.upper_limit_x = X
        self.upper_limit_y = Y

    def build_map(self):

        edges = set()
        stack = [self.center_point]

        while len(stack) > 0:
            
            vX, vY = heapq.heappop(stack)
            pts = [
                (vX + self.len_roads, vY), 
                (vX - self.len_roads, vY), 
                (vX, vY + self.len_roads), 
                (vX, vY - self.len_roads)
            ]

            for pt in pts:
                if ((vX, vY), pt) not in edges and (pt, (vX, vY)) not in edges \
                    and self.is_valid(pt):

                    pt0 = (vX, vY)
                    pt1 = pt
        
                    if (pt0[0]**2 + pt0[1]**2)**0.5 > (pt1[0]**2 + pt1[1]**2)**0.5:
                        pt0 = pt
                        pt1 = (vX, vY)

                    if  ((pt0[0] <= self.lower_limit_x or pt0[0] >= self.upper_limit_x) and (pt1[0] <= self.lower_limit_x or pt1[0] >= self.upper_limit_x)) or \
                        ((pt0[1] <= self.lower_limit_y or pt0[1] >= self.upper_limit_y) and (pt1[1] <= self.lower_limit_y or pt1[1] >= self.upper_limit_y)): 
                        continue

                    self.build_roads(pt0, pt1, self.in_roads, self.out_roads, self.width_roads)
                    heapq.heappush(stack, pt)
                    edges.add((pt0, pt1))

        self.build_intersections()

        self.ctrl.speed = 10
        for er in self.ctrl.extremeRoads: #adjusting generation rate
            self.ctrl.roads[er].Lambda = 1/150

