from typing import List, Tuple


class Road:
    def __init__(self, start:Tuple[int,int], end: Tuple[int,int]):
        self.start = start
        self.end = end

    @property
    def get_rect(self):
        x0,y0 = self.start
        x1,_ = self.end
        return (x0, y0, x1-x0, 10)
