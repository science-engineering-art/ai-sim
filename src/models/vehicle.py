from typing import Tuple
from numpy import sqrt

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

class Vehicle:

    def __init__(self, x, length, width, path = [], color = BLUE):
        # dimensions
        self.color = color
        self.x = x
        self.length = length
        self.width = width
        
        self.current_road = 0
        self.path = path
        self.v = 0
        self.v_max = 60
        self.v = self.v_max
        self.a = 0
        self.a_max = 2.5
        # self.a_max = 50
        self.b_max = 4.61
        # self.b_max = 46.1

        self.s0 = 4
        self.T = 1

        self.stopped = False

    def update(self, dt = 1/60, lead: 'Vehicle' = None):
        
        if self.stopped: return
        # if self.stopped: 
        #     self.a = -self.b_max*self.v/self.v_max

        if self.v + self.a * dt < 0:
            self.x -= 1/2*self.v**2/self.a
            self.v = 0
        else:
            self.x += self.v * dt + self.a * dt**2 /2
            self.v += self.a * dt

        alpha = 0
        if lead: 
            delta_x = lead.x - self.x - self.length
            delta_v = self.v - lead.v
            alpha = (self.s0 + max(0, self.v*self.T + self.v*delta_v/(2*sqrt(self.a_max*self.b_max)))) / delta_x

        self.a = self.a_max * (1 - (self.v/self.v_max)**4 - alpha**2)
