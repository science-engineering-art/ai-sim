from typing import Tuple
from numpy import sqrt

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (127, 127, 127)

class Vehicle:

    def __init__(self, x, length, width, path = [], color = BLUE, **kwargs):
        # dimensions
        self.color = color
        self.x = x
        self.length = length
        self.width = width
        
        self.path = path
        self.v = 0
        self.v_max = 16.67
        self.v = self.v_max * 3/4
        self.a = 0
        self.a_max = 1.44
        self.b_max = 4.61

        self.s0 = 4
        self.T = 1

        self.__dict__.update(kwargs)

    def update(self, dt = 1/60, lead: 'Vehicle' = None):
        
        if self.v + self.a * dt < 0:
            self.x -= 1/2*self.v**2/self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt**2 /2

        alpha = 0
        if lead: 
            delta_x = lead.x - self.x - lead.length
            delta_v = self.v - lead.v
            alpha = (self.s0 + max(0, self.v*self.T + self.v*delta_v/(2*sqrt(self.a_max*self.b_max)))) / delta_x

        self.a = self.a_max * (1 - (self.v/self.v_max)**4 - alpha**2)
