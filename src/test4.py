from models.control import control
from templates.templates import GridMap

template = GridMap(
    center_point=(700, 400), 
    len_roads=92, 
    lower_limit_x=0,
    lower_limit_y= 0, 
    upper_limit_x= 1400,
    upper_limit_y= 800,
    in_roads= 2,
    out_roads= 2,
    width_roads= 4
)
template.generate_template('map4')
ctrl: control = template.load_template('map4')
ctrl.Start(observation_time=10, draw=False)