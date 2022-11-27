import queue
from pygame import Rect
from typing import List, Tuple


class Road(Rect):

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
