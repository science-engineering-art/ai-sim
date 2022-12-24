
from typing import List

from sympy import false
from models.road import Road


class corner():
    

    
    def __init__(self, light_controled = False):
        
        self.current_turn = -1
        self.numberOfTurns = 0
        self.turns = []
        self.times = []
        self.myturn = {}
        self.light_controled = light_controled
        self.IncomingRoads = []
        self.OutgoingRoads = []
        self.follow = {}
    
    def addIncomingRoads(self, roads):
        self.IncomingRoads.extend(roads)
        for road in roads:
            self.follow[road] = []
        
    def addOutgoingRoads(self, roads):
        self.OutgoingRoads.extend(roads)
        
    def addFollow(self, in_road, out_road, order = None, displace = False, time = 10):
        self.follow[in_road].append(out_road)
        
        if self.light_controled:
            if order:
                if displace:
                    self.turns.append([])
                    self.times.append(0)
                    for pos in range(order, self.numberOfTurns):
                        self.turns[pos + 1] = self.turns[pos]
                        self.times[pos + 1] = self.times[pos]
                    self.turns[order] = [(in_road, out_road)]
                    self.times[order] = time
                    self.numberOfTurns +=1
                else:
                    self.turns[order].append((in_road, out_road))
                self.myturn[(in_road, out_road)] = order
                        
            else:
                self.times[self.numberOfTurns] = self.default_time
                self.times[self.numberOfTurns] = time
                self.numberOfTurns+=1
                self.turns.append([(in_road, out_road)])
                self.myturn[(in_road, out_road)] = self.numberOfTurns - 1
        
    def addFollows(self, in_roads, out_roads, order = None, displace = 0):
        
        if order == None:
            order = self.numberOfTurns
        
        for in_road in in_roads:
            for out_road in out_roads:
                if out_roads == out_roads[0]:
                    self.addFollow(in_road, out_road, order, displace)
                else:
                    self.addFollow(in_road, out_road, order)
    
    @property
    def CanIPass(self, in_road, out_road):
        
        return self.current_turn == self.myturn[(in_road, out_road)] 
        