
class corner:

    '''class to simulate the concept of a corner 
    (i.e. a point where more than two roads converge)'''

    def __init__(self, light_controled = False):
        
        self.current_turn = -1 #indicate which road has the green light 
        self.light_controled = light_controled #indiates wether ther is a semaphore in the corner
        self.numberOfTurns = 0  #indicate the amount of turns the green light passes throw
        self.time_tick = 0 #used to decided when to change the lights
        self.intermediate_time = 100 #period of time where everyone is in red 
        self.turns = [] #the position i stores which follow pair has the green light 
        self.times = [] #indicates the duration of each turn
        self.myturn = {} #store for each follow pair its turn number (inverse to self.turns)
        self.IncomingRoads = [] #stores the roads that end at the corner
        self.OutgoingRoads = [] #stores the roads that star at the corner
        self.follow = {} #stores for each road that end at corner which
                        #roads may follow it 


    def tick(self, t = 1):
        '''increments the time count and change the ligths if needed.
        (the turns sucession is -1, 0, -2, 1, 2, -3 ...., where the
        negatives indicate everyone is in red)
        '''
        if not self.light_controled:
            return
        self.time_tick += t
        if self.current_turn < 0:
            if self.time_tick == self.intermediate_time:
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
        '''Add the in_road, if it hasn't been added before'''
        for in_road in roads:
            if not self.IncomingRoads.__contains__(in_road):
                self.IncomingRoads.append(in_road)
                self.follow[in_road] = []


    def addOutgoingRoads(self, roads):
        '''Add the out_road, if it hasn't been added before'''
        for out_road in roads:
            if not self.OutgoingRoads.__contains__(out_road):
                self.OutgoingRoads.append(out_road)


    def addFollow(self, in_road, out_road, order = None, displace = False, time = 400):
        '''Add a follow pair, i.e. a  pair of (in_road, out_road) indicating 
        a car can move from in_road to out_road. 
        The parameter order is used to indicate its turn in the semaphore.
        The parameter displace is used, if order was given, to indicate if we want 
        to simultaneously give green light to this pair and the ones that had this turn before. In
        case of negative the turns of the rest of the pairs follow this one (they are displaced)
        The parameter time indicates the amount of time (ticks) this pait turn last (is green)'''
        
        self.addIncomingRoads([in_road])
        self.addOutgoingRoads([out_road])
        self.follow[in_road].append(out_road)
        
        if self.light_controled:
            if  order != None:
                # print(order + 1 - self.numberOfTurns)
                self.turns.extend([] for _ in range(max(0, order + 1 - self.numberOfTurns)))
                self.times.extend(time for _ in range(max(0, order + 1 - self.numberOfTurns)))
                if displace:
                    self.turns.append([])
                    self.times.append(0)
                    for pos in range(order, self.numberOfTurns):
                        self.turns[pos + 1] = self.turns[pos]
                        self.times[pos + 1] = self.times[pos]
                    self.turns[order] = [(in_road, out_road)]
                    self.times[order] = time
                else:
                    self.turns[order].append((in_road, out_road))
                self.numberOfTurns += max(0, order + 1 - self.numberOfTurns)
                self.myturn[(in_road, out_road)] = order
                        
            else:
                self.times.append(time)
                self.numberOfTurns+=1
                self.turns.append([(in_road, out_road)])
                self.myturn[(in_road, out_road)] = self.numberOfTurns - 1


    def addFollows(self, in_roads, out_roads, order = None, displace = False, time = 1000):
        '''adds all the possible pair between in and out roads, as follow pairs'''
        if order == None:
            order = self.numberOfTurns
        
        for in_road in in_roads:
            for out_road in out_roads:
                if out_roads == out_roads[0]:
                    self.addFollow(in_road, out_road, order, displace, time)
                else:
                    self.addFollow(in_road, out_road, order)


    def CanIPass(self, in_road):
        '''If ask if a road has the green light. 
        It condiderate that the cars in a road can simultaneously with
        the same green light move to all the follow roads corresponding
        to the current one but this is a behavior that we whish to improve.'''
        
        return self.current_turn == self.myturn[(in_road, self.follow[in_road][0])] 
