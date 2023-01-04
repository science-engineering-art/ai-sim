from pydantic import BaseModel
from typing import Dict, List, Tuple


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
