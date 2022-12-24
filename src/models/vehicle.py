from typing import Tuple
from numpy import sqrt

class Vehicle:

    def __init__(self, x, y, length, width, path = []):
        # dimensions
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        
        self.current_road = 0
        self.path = path
        self.v = 0
        self.v_max = 60
        self.a = 0
        self.a_max = 2.5
        self.b_max = 4.61

        self.s0 = 4
        self.T = 1

        self.stopped = False

    @property
    def get_rect(self) -> Tuple[int,int,int,int]:
        return (self.x, self.y, self.length, self.width)

    def update(self, dt = 1/160, lead: 'Vehicle' = None):
        
        if self.stopped: return

        if self.v + self.a * dt < 0:
            self.x -= 1/2*self.v**2/self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt**2 /2

        alpha = 0
        if lead: 
            delta_x = lead.x - self.x - self.length
            delta_v = self.v - lead.v
            alpha = (self.s0 + max(0, self.v*self.T + self.v*delta_v/(2*sqrt(self.a_max*self.b_max)))) / delta_x

        self.a = self.a_max * (1 - (self.v/self.v_max)**4 - alpha**2)
        
