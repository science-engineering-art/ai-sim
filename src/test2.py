from templates import GridMap

temp = GridMap(center_point=(700,400), 
    len_roads=600, lower_limit_x=10, 
    lower_limit_y=10, upper_limit_x=1380, 
    upper_limit_y=790, in_roads=1,
    out_roads=1, width_roads=150
)

temp.build_roads((700,400), (1380,400), 1, 1, 150)
temp.build_roads((700,10) , (700,400) , 1, 1, 150)
temp.build_roads((10,400) , (700,400) , 1, 1, 150)
temp.build_roads((700,400), (700,790) , 1, 1, 150)
temp.build_intersections()

temp.generate_template('map2')

ctrl = temp.load_template('map2')
ctrl.Start(it_amount=100000)
