from models.control import control
from templates import GridMap


ctrl = control()


template = GridMap(ctrl, (700, 400), 92, 300, 200, 1100, 600, 2, 2, 4)
template.generate_map()
ctrl.Start(observation_time=120, draw=True)


# to_print_1 = []
# to_print_2 = []
# for road_id in range(len(ctrl.road_max_queue)):
#     if not ctrl.is_curve[road_id]:
#         to_print_1.append(ctrl.road_max_queue[road_id])
#         to_print_2.append(ctrl.road_average_time_take_cars[road_id] * ctrl.dt)
# print(to_print_1)
# print(to_print_2)
# print( time() - t)
