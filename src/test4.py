from templates.templates import GridMapBuilder, TemplateIO

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

temp = TemplateIO(temp)
temp.generate_template('map4')
draw, cars = temp.load_template('map4')
draw.Start(observation_time=5)
print(cars)
draw.ObserveVehicles(cars)