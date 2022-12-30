from models.control import control

ctrl = control()

ctrl.build_roads((700,400), (1380,400), 1, 1, 150)
ctrl.build_roads((700,10) , (700,400) , 1, 1, 150)
ctrl.build_roads((10,400) , (700,400) , 1, 1, 150)
ctrl.build_roads((700,400), (700,790) , 1, 1, 150)
ctrl.build_intersections()

ctrl.Start(it_amount=100000)
