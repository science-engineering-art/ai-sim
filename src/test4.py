
from templates.templates import GridMapBuilder, TemplateIO
import models.Floyd_Warshall

temp = GridMapBuilder(
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

models.Floyd_Warshall.big = True
temp = TemplateIO(temp)
temp.generate_template('map4')
draw, cars = temp.load_template('map4')
draw.ctrl.scale = 150
draw.ctrl.name = 'map4'
# draw.ctrl.speed = 20 
draw.Start(observation_time=5000)
