from pydantic import BaseModel
from typing import Dict, List, Tuple


class BaseNode(BaseModel):...


class Edge(BaseNode):
    lambda_: float
    start: Tuple[float, float]
    end: Tuple[float, float]


class RoadEdge(BaseNode):
    lanes: List[int]


class CurveEdge(BaseNode):
    input_lane_id: int
    output_lane_id: int
    curve_point: Tuple[float, float]


class IntersectionNode(BaseNode):
    input_lanes: List[int]
    out_lanes: List[int]
    follows: List[Tuple[int, int, int]]


class Map(BaseNode):
    width_roads: float
    lanes: List[Edge]
    roads: List[RoadEdge]
    intersections: Dict[Tuple[float,float], IntersectionNode] 
    curves: List[CurveEdge]
    extremes_lanes: List[int] 


class Vehicle(BaseNode):
    path: List[int]
    start: float


class Template(BaseNode):
    map: Map
    vehicles: List[Vehicle]
