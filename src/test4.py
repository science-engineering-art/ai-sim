import random
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
draw = temp.load_template('map4')

ctrl = draw.ctrl

ctrl.speed = 40
cars = []

ok = True
while ok:
    try:
        road_start_id = ctrl.extremeRoads[0]
        road_end_id   = random.randint(1, len(ctrl.roads))
        print(f"\n\nINITIAL POINT: {road_start_id} TARGET: {road_end_id}\n\n")
        prior, car = ctrl.AddRoutedVehicle(road_start_id, road_end_id, random.uniform(0, 5))
        ok = False
    except:...

car.color = (255,255,255)
cars.append((prior, car))

draw.Start(observation_time=20)
draw.ObserveVehicles(cars)
