
from typing import List

from sympy import false
# from road import Road


class corner():
    
    def __init__(self, light_controled = False):
        
        self.current_turn = -1
        self.numberOfTurns = 0
        self.time_tick = 0
        self.intermediate_time = 1000
        self.turns = []
        self.times = []
        self.myturn = {}
        self.light_controled = light_controled
        self.IncomingRoads = []
        self.OutgoingRoads = []
        self.follow = {}
    
    def tick(self, t = 1):
        self.time_tick += t
        if self.current_turn < 0 and self.time_tick == self.intermediate_time:
            self.time_tick = 0
            self.current_turn  = -self.current_turn - 1
        elif self.times[self.current_turn] == self.time_tick:
            self.time_tick = 0
            self.current_turn += 1
            if self.current_turn == self.numberOfTurns:
                self.current_turn = -1
            else:
                self.current_turn = -self.current_turn - 1
            
            
    
    def addIncomingRoads(self, roads):
        
        for in_road in roads:
            if not self.IncomingRoads.__contains__(in_road):
                self.IncomingRoads.append(in_road)
                self.follow[in_road] = []
            
    def addOutgoingRoads(self, roads):
        for out_road in roads:
            if not self.OutgoingRoads.__contains__(out_road):
                self.OutgoingRoads.append(out_road)
        
    def addFollow(self, in_road, out_road, order = None, displace = False, time = 4000):
        
        
        self.addIncomingRoads([in_road])
        self.addOutgoingRoads([out_road])
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
                self.times.append(time)
                self.numberOfTurns+=1
                self.turns.append([(in_road, out_road)])
                self.myturn[(in_road, out_road)] = self.numberOfTurns - 1
        
    def addFollows(self, in_roads, out_roads, order = None, displace = False, time = 1000):
        
        if order == None:
            order = self.numberOfTurns
        
        for in_road in in_roads:
            for out_road in out_roads:
                if out_roads == out_roads[0]:
                    self.addFollow(in_road, out_road, order, displace, time)
                else:
                    self.addFollow(in_road, out_road, order)
    
    def CanIPass(self, in_road):
        
        # print(in_road, self.follow[in_road])
        return self.current_turn == self.myturn[(in_road, self.follow[in_road][0])] 
        
    # def CanIPass(self, in_road, out_road):
        
    #     return self.current_turn == self.myturn[(in_road, out_road)] 
        