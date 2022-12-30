from typing import List, Tuple
from pygame import gfxdraw
from models.road import Road
from models.vehicle import Vehicle


class Painting:

    def build_rect( 
        start: Tuple[float,float], 
        end: Tuple[float,float],
        width: float = 1
    ) -> List[Tuple[float,float]]:

        x0, y0 = start
        x1, y1 = end

        if x0**2 + y0**2 > x1**2 + y1**2:
            x0, y0 = end
            x1, y1 = start

        # vector from start to end
        vX, vY = x1 - x0, y1 - y0   
        # normal vector
        nX, nY = -vY, vX

        # normalize
        n = (nX**2 + nY**2)**0.5
        nX, nY = width/n * nX, width/n * nY

        # third vector
        x2, y2 = x1 + nX, y1 + nY
        # fourth vector
        x3, y3 = x0 + nX, y0 + nY

        return [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]


    def draw_road(screen, road : Road, color):
        vertices = Painting.build_rect(road.start, road.end, 1.5)
        # window.draw_polygon(vertices, color)
        gfxdraw.filled_polygon(screen, vertices, color)


    def draw_vehicle(screen, road: Road, vehicle : Vehicle):

        x0, y0 = road.start
        x1, y1 = road.end

        if x0**2 + y0**2 > x1**2 + y1**2:
            x0, y0 = road.end
            x1, y1 = road.start

        # vector from start to end
        vX, vY = x1 - x0, y1 - y0
        n = (vX**2 + vY**2)**0.5

        x0, y0 = road.start
        x1, y1 = road.end
        
        sX, sY = x0 + vehicle.x/n * vX, y0 + vehicle.x/n * vY
        eX, eY = x0 + (vehicle.x - vehicle.length)/n * vX, y0 + (vehicle.x - vehicle.length)/n * vY

        vertices = Painting.build_rect((sX,sY), (eX, eY), 1)
        gfxdraw.filled_polygon(screen, vertices, vehicle.color)
        # window.draw_polygon(vertices, (255, 0, 255))
