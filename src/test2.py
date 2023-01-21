from templates.templates import GridMapBuilder, TemplateIO

temp = GridMapBuilder(
    center_point=(700,400), 
    len_roads=200, 
    lower_limit_x=300, 
    lower_limit_y=0, 
    upper_limit_x=1100, 
    upper_limit_y=800, 
    in_roads=1,
    out_roads=1, 
    width_roads=10
)
temp = TemplateIO(temp)
temp.generate_template('map2')
draw, _ = temp.load_template('map2')
draw.Start(it_amount=100000)
