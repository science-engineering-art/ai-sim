from models.control import control
from templates import GridMap


ctrl = control()


template = GridMap(ctrl, (700, 400), 92, 300, 200, 1100, 600, 2, 2, 4)
template.generate_map()
