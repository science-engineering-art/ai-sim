from templates.templates import GridMapBuilder

temp = GridMapBuilder(center_point=(700,400), 
    len_roads=92, lower_limit_x=10, 
    lower_limit_y=10, upper_limit_x=1380, 
    upper_limit_y=790, in_roads=1,
    out_roads=1, width_roads=10
)

temp.generate_template('map1')
ctrl = temp.load_template('map1')
ctrl.Start(it_amount=100000)