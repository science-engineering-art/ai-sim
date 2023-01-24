from typing import Tuple
from scipy.spatial import distance


class Road:

    def __init__(self, start:Tuple[int,int], end: Tuple[int,int], lambda_: float = 1/50, **args):
        self.start = start
        self.end = end
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1]-self.start[1]) / self.length
        self.angle_cos = (self.end[0]-self.start[0]) / self.length
        self.vehicles = []
        
        self.start_conn = None #it may be another road or a corner
        self.end_conn = None #it may be another road or a corner
        
        # default value of amount of vehicle transiting per second 
        self.lambda_ = lambda_ # which is equivalent of 72 veh/h
        self.__dict__.update(args)

   