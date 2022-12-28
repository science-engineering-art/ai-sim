from typing import List, Tuple
from window import Window
from pygame import gfxdraw
from road import Road
from shapely.geometry import LineString


def build_rect( 
        start: Tuple[float,float], 
        end: Tuple[float,float],
        width: float = 3
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

    rect = [(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
    rect = [(x - nX * width / 2, y - nY * width / 2) for x, y in rect]

    return rect


class Map(Window):

    def __init__(self, width, height, **kwargs):
        super().__init__(width, height, **kwargs) 

    def draw_road(self, st: LineString, inc: float, color: tuple):
        last = None
        for c in st.__geo_interface__['coordinates']:
            c = (inc*c[0], inc*c[1])
            if last == None:
                last = (c[0] - self.lat,c[1] - self.lng)
                continue
            
            lat = c[0] - self.lat
            lng = c[1] - self.lng

            pts = build_rect(last, (lat, lng))

            gfxdraw.filled_polygon(self.screen, [
                (self.x + lat * self.zoom, self.y + lng * self.zoom)
                for lat, lng in pts
            ], color)


import dictdatabase as ddb
from networkx import MultiDiGraph

def keep_map(map: MultiDiGraph, path: str = 'map.geojson'):

    s = ddb.at(path)

    if not s.exists():
        streets = []

        for _, _, data in map.edges(data=True):
            try:
                if data['osmid'] in streets:
                    continue
                streets.append(data['geometry'].__geo_interface__)
            except: ...

        s.create({
            'type': 'FeatureCollection',
            'features': streets
        })
            
def load_map(path: str = 'map.geojson'):

    s = ddb.at(path)

    if not s.exists():
        return None

    return [LineString(ft['coordinates']) for ft in s.read()['features']]
