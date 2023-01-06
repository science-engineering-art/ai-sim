



from copy import deepcopy
import random 
from models.A_star import A_star
from models.control import control
from msilib.schema import Control

from models.vehicle import Vehicle


class new_control(control):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    # def UpdateAll(self):
    #     super().UpdateAll(self)
        
        
    def AddRoutedVehicle(self, from_road_id, to_road_id):
        path = A_star.find_shortest_path(self, from_road_id, to_road_id)
        car: Vehicle = deepcopy(random.choice(self.basic_vehicles))
        car.path = path; car.current_road_in_path = 0
        
        self.nav.fixed_vehicles.append(car)
        
        
        
    