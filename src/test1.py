from models.control import control
from templates import GridMap

ctrl = control()

temp = GridMap(ctrl, (700,400), 
    len_roads=600, lower_limit_x=10, 
    lower_limit_y=10, upper_limit_x=1380, 
    upper_limit_y=790, in_roads=1,
    out_roads=1, width_roads=150
)

temp.generate_template('map2')

print(temp.map)

ctrl.Start(it_amount=100000)