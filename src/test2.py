
from templates.templates import GridMapBuilder, TemplateIO

temp = GridMapBuilder(
    center_point=(700,400), 
    len_roads=200, 
    lower_limit_x=480, 
    lower_limit_y=0, 
    upper_limit_x=920, 
    upper_limit_y=800, 
    in_roads=2,
    out_roads=2, 
    width_roads=4
)

temp = TemplateIO(temp)
temp.generate_template('map2')
draw, _ = temp.load_template('map2')
draw.Start(it_amount=100000)
