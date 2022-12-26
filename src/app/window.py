
import pygame
from pygame import gfxdraw
from pygame.locals import *


class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.zoom = 1
        self.x = self.y = 0

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

    def inc_zoom(self):
        self.zoom += 0.001

    def dec_zoom(self):
        self.zoom -= 0.001
        self.zoom = max(0, self.zoom)

    def draw_polygon(self, points, color):
        gfxdraw.filled_polygon(self.screen, [
            (self.x + pt[0] *  self.zoom, self.y + pt[1] * self.zoom)
            for pt in points], color)

    def fill(self, color):
        self.screen.fill(color)

    def update(self):
        pygame.display.update()
