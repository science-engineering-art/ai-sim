from pyexpat import model
from matplotlib.hatch import HorizontalHatch
from models.control import control
from models.genetic_algorithm_marcos import *
from models.simulation import Simulation, Simulation_test_3



simulation = Simulation_test_3()
MAX_ITERATIONS = 10
genetic_algorithm(simulation, 100, 15, 100, 10)



# print(ctrl.corners[0].turns)    
# ctrl = new_simulation()
# print(ctrl.GetDimension())
# t1 = 100
# t2 = 400
# ctrl.SetConfiguration([t1,t2,t2,t2,t1,t2,t2,t2,t1,t2,t2,t2,t1,t2,t2])
# # ctrl.Start(it_amount= 10000, draw=False)
# ctrl.Start(it_amount= 10000, draw=True)

# to_print_1 = []
# to_print_2 = []
# for road_id in range(len(ctrl.road_max_queue)):
#     if not ctrl.is_curve[road_id]:
#         to_print_1.append(ctrl.road_max_queue[road_id])
#         to_print_2.append(ctrl.road_average_time_take_cars[road_id])
# print(to_print_1)
# print(to_print_2)
