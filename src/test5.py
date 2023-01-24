
from templates.templates import GridMapBuilder, TemplateIO
import models.Floyd_Warshall
import dictdatabase as ddb

temp = GridMapBuilder(
    center_point=(700, 400), 
    len_roads=100, 
    lower_limit_x=0,
    lower_limit_y= 0, 
    upper_limit_x= 1400,
    upper_limit_y= 800,
    in_roads= 2,
    out_roads= 2,
    width_roads= 4
)


ddb.config.storage_directory = '../tests/marcos_1_tests/ddb_storage'
s = ddb.at('test_1')
json = s.read()
config = json['0']['best_solution']['vector']
for i in range(49):
    if json[str(i)].get('best_solution'):
        config = json[str(i)]['best_solution']['vector']
        


models.Floyd_Warshall.big = True
temp = TemplateIO(temp)
temp.generate_template('map5')
draw, cars = temp.load_template('map5')
draw.ctrl.scale = 150
draw.ctrl.name = 'map5'
draw.ctrl.speed = 30 

draw.ctrl.SetConfiguration(config)
draw.Start(observation_time=10)
