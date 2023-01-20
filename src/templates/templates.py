import math
import heapq
import random
from time import time
from typing import Tuple
from copy import deepcopy
import dictdatabase as ddb
from models.road import Road
from abc import abstractmethod
from models.navigation import navigation
from scipy.spatial import distance
from models.control import control
from templates.models import Template, Vehicle
from models.new_control import new_draw
from templates.visitor import NodeVisitor
from models.draw_control import draw_control
from templates.models import CurveEdge, Edge, IntersectionNode, Map, RoadEdge
     

class BasicMapBuilder:

    def __init__(self):
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

    def __build_roads(self, start, end, inN, outN, width):
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
                lambda_=0,
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
                lambda_=0,
                start=(x1, y1),
                end=(x0, y0)
            )
            self.map.lanes.append(lane)
            road.lanes.append(lane_id)

            x0, y0 = x0 + nX, y0 + nY
            x1, y1 = x1 + nX, y1 + nY

            self.map.intersections[start].input_lanes.append(lane_id)
            self.map.intersections[end].out_lanes.append(lane_id)
            self.map.extremes_lanes.append(lane_id)

        self.map.roads.append(road)

    def __build_intersections(self):

        for x, y in self.map.intersections:
            follows = {}
            i = 0
            for in_lane_id in self.map.intersections[(x, y)].input_lanes:
                for out_lane_id in self.map.intersections[(x, y)].out_lanes:

                    # print(f'{(x,y)}')

                    road_in: Edge = self.map.lanes[in_lane_id]
                    road_out: Edge = self.map.lanes[out_lane_id]

                    # check if road_in and road_out are in the same road
                    if abs(BasicMapBuilder.__calculate_angle(road_in) - 
                    BasicMapBuilder.__calculate_angle(road_out)) < 5 or \
                    (abs(BasicMapBuilder.__calculate_angle(road_in) - \
                    BasicMapBuilder.__calculate_angle(road_out)) > 177.5 and \
                    abs(BasicMapBuilder.__calculate_angle(road_in) - \
                    BasicMapBuilder.__calculate_angle(road_out)) < 182.5):
                        # print(
                            # f'PARALLEL: {(road_in.start, road_in.end)} -- {(road_out.start, road_out.end)}')
                        continue

                    # turning left
                    if abs(BasicMapBuilder.__calculate_angle(road_in) - \
                    BasicMapBuilder.__calculate_angle(road_out)) > 185:
                        continue

                    # print(f'connect {road_in.end} to {road_out.start}')
                    # print(road_in.start, road_in.end,
                        # road_out.start, road_out.end)
                    curve_pt = BasicMapBuilder.__calculate_curve_point(road_in, road_out)
                    # print(f'curve at {curve_pt}')
                    curve = CurveEdge(
                        input_lane_id=in_lane_id,
                        output_lane_id=out_lane_id,
                        curve_point=curve_pt
                    )
                    curve_id = len(self.map.curves)
                    self.map.curves.append(curve)

                    try:
                        self.map.extremes_lanes.remove(out_lane_id)
                    except:
                        print(f'road_out_id {out_lane_id} not in extremeRoads')

                    angle = BasicMapBuilder.__calculate_angle(road_in)

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
                        follows[angle] += [(
                            self.map.curves[curve_id].input_lane_id,
                            self.map.curves[curve_id].output_lane_id, i) 
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

    def __calculate_angle(road_in: Road) -> float:
        x0, y0 = road_in.start
        x1, y1 = road_in.end

        if (x0**2 + y0**2) > (x1**2 + y1**2):
            tmp = x0, y0
            x0, y0 = x1, y1
            x1, y1 = tmp

        # print(f'x0: {x0}, y0: {y0}, x1: {x1}, y1: {y1}')

        co = y1 - y0
        ca = x1 - x0

        if ca == 0 and co != 0:
            return 90.0

        h = (co**2 + ca**2)**0.5
        
        # print(f'co: {co}, ca: {ca}, h: {h}')
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

    def __calculate_curve_point(road_a: Road, road_b: Road):
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


class GridMapBuilder(BasicMapBuilder):

    def __init__(self, 
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
        super().__init__()

        self.center_point = center_point
        self.len_roads = len_roads
        self.lower_limit_x = lower_limit_x
        self.lower_limit_y = lower_limit_y
        self.upper_limit_x = upper_limit_x
        self.upper_limit_y = upper_limit_y
        self.in_roads = in_roads
        self.out_roads = out_roads
        self.map.width_roads = width_roads

        self.__recalculate_limits()

    def build_map(self) -> Map:

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
                    and self.__is_valid(pt):
                    
                    pt0 = (vX, vY)
                    pt1 = pt
        
                    if (pt0[0]**2 + pt0[1]**2)**0.5 > (pt1[0]**2 + pt1[1]**2)**0.5:
                        pt0 = pt
                        pt1 = (vX, vY)

                    if ((pt0[0] <= self.lower_limit_x or pt0[0] >= self.upper_limit_x) and \
                        (pt1[0] <= self.lower_limit_x or pt1[0] >= self.upper_limit_x)) or \
                       ((pt0[1] <= self.lower_limit_y or pt0[1] >= self.upper_limit_y) and \
                        (pt1[1] <= self.lower_limit_y or pt1[1] >= self.upper_limit_y)): 
                        continue

                    self._BasicMapBuilder__build_roads(
                        pt0, pt1, self.in_roads, self.out_roads, self.map.width_roads)
                    
                    heapq.heappush(stack, pt)
                    edges.add((pt0, pt1))

        self._BasicMapBuilder__build_intersections()

        # add the frequency of vehicles in each road
        for road in self.map.roads:
            for i in road.lanes:
                self.map.lanes[i].lambda_ = random.uniform(0, 0.15)
                # print(f'\n{self.map.lanes[i]}\n')


        return deepcopy(self.map) , edges
    
    def __recalculate_limits(self):
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
            else:
                x += self.len_roads
                X -= self.len_roads
                y += self.len_roads
                Y -= self.len_roads
            
            self.lower_limit_x = x
            self.lower_limit_y = y
            self.upper_limit_x = X
            self.upper_limit_y = Y

    def __is_valid(self, pt):
            return pt[0] >= self.lower_limit_x and \
                pt[0] <= self.upper_limit_x and \
                pt[1] >= self.lower_limit_y and \
                pt[1] <= self.upper_limit_y


import heapq
from sys import maxsize

def get_nearest_lane(map: Map, start, end):
    return random.choice( 
        [ lane 
            for lane in map.intersections[start].out_lanes
                for lane2 in map.intersections[end].input_lanes
                    if lane == lane2
        ]
    )

def floyd_warshall(map: Map, edges: set) -> tuple[dict, list]:
    visited = dict()

    for x, y in map.intersections:
        for (x0, y0), (x1, y1) in edges:
            if (x0, y0) == (x, y) and (x1, y1) not in visited:
                visited[(x1, y1)] = len(visited)
            if (x1, y1) == (x, y) and (x0, y0) not in visited:
                visited[(x0, y0)] = len(visited)

    paths = [[[] for _ in range(len(visited))]      for _ in range(len(visited))]
    costs = [[maxsize for _ in range(len(visited))] for _ in range(len(visited))]

    (x0, y0), (x1, y1) = [t for t in iter(edges)][0]
    len_roads = distance.euclidean((x0, y0), (x1, y1))

    for (x0, y0), (x1, y1) in edges:
        i = visited[(x0, y0)]
        j = visited[(x1, y1)]
        costs[i][j] = len_roads
        paths[i][j] = [get_nearest_lane(map, (x0, y0), (x1, y1))]

    for i in range(len(visited)):
        costs[i][i] = 0

    for k in range(len(visited)):
        for i in range(len(visited)):
            for j in range(len(visited)):
                if costs[i][k] + costs[k][j] < costs[i][j]:
                    costs[i][j] = costs[i][k] + costs[k][j]
                    paths[i][j] = paths[i][k] + paths[k][j]

    return visited, costs, paths

class VehicleGeneration:

    def __init__(self, map: Map, edges: set):
        visited, matrix, paths = floyd_warshall(map, edges)
        self.visited = visited
        self.matrix = matrix
        self.edges = edges
        self.paths = paths
        self.map = map

    def generate_cars_round(self, dt, time) -> list[Vehicle]:
        cars = []

        for lane_id in self.map.extremes_lanes:
            lane = self.map.lanes[lane_id]

            r = random.random()
            if r > navigation._navigation__poisson(lane.lambda_, dt, 1):
                continue

            # get nearest point of `lane.start`
            best = (maxsize, (0,0))
            for x, y in self.visited.keys():
                if distance.euclidean(lane.start, (x, y)) < best[0]:
                    best = (distance.euclidean(lane.start, (x, y)), (x, y))

            u = self.visited[best[1]]
            v = u
            while u == v:
                v = random.randint(0, len(self.visited)-1)

            # get path from U to V intersection node
            print(f"u: {u} == v: {v} == path: {len(self.paths[u])}")
            path = self.paths[u][v]
            print('!!!')
            print(path)
            car: Vehicle = Vehicle(path=path, start=time)
            cars.append(car)

        return cars

    def generate_cars(self, time_generation = 10, step_size = 0.014) -> list[Vehicle]:
        cars = []
        current = 0

        while current  < time_generation:
            cars += self.generate_cars_round(step_size, current)
            current += step_size

        cars = [car for car in cars if len(car.path) > 0]

        return cars


class TemplateIO:

    def __init__(self, builder: BasicMapBuilder):
        self.builder = builder

    def generate_template(self, name: str):

        s = ddb.at(name)
        if not s.exists():
            map, edges = self.builder.build_map()            
            cars = VehicleGeneration(map, edges).generate_cars()
            temp = Template(map=map, vehicles=cars)

            s.create(
                NodeVisitor().visit(temp)
            )

    def load_template(self, name: str):
        s = ddb.at(name)
        if s.exists():
            json = s.read()
            draw = new_draw()
            ctrl = draw.ctrl

            # add roads
            for lane in json['map']['lanes']:
                ctrl.AddRoad(
                    road_init_point=lane['start'],
                    road_end_point=lane['end'],
                    lambda_=lane['lambda_'],
                )

            # add connections between roads            
            for curve in json['map']['curves']:
                ctrl.connect_roads(
                    road_1_id=curve['input_lane_id'],
                    road_2_id=curve['output_lane_id'],
                    curve_point=curve['curve_point']
                )
            
            # create intersections
            for x in json['map']['intersections']:
                for y in json['map']['intersections'][x]:
                    follows = json['map']['intersections'][x][y]['follows']
                    follows = [ tuple(f) for f in follows ] 
                    ctrl.CreateCorner(follows)

            # add extremes roads
            ctrl.AddExtremeRoads(json['map']['extremes_lanes'])

            ctrl.speed = 5

            cars = []
            for car in json['vehicles']:
                print(car)
                path, start = car['path'], car['start']
                start, car = ctrl.AddRoutedVehicle(path, start)
                cars.append((start, car))

            return draw, cars
