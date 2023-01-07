from matplotlib.hatch import HorizontalHatch
from sklearn.utils import all_estimators
from models.A_star import A_star
from models.control import control
from models.draw_control import draw_control
from models.new_control import new_control, new_draw
from models.simulation import Simulation_test_3

pos_x = [100, 450, 800, 1150]
pos_y = [100, 300, 500, 700]
h_diff = 20
v_diff = 20
road_width = 10
draw = new_draw()
draw.ctrl = new_control()
ctrl = draw.ctrl

AB = ctrl.AddRoad((pos_x[0], pos_y[2]), (pos_x[1], pos_y[2]), 0.0138)
LJ = ctrl.AddRoad((pos_x[0], pos_y[1]), (pos_x[1], pos_y[1]), 0.01305)
BA = ctrl.AddRoad((pos_x[1], pos_y[2] - road_width), (pos_x[0], pos_y[2] - road_width), 0.00972)

BC = ctrl.AddRoad((pos_x[1] + h_diff, pos_y[2]), (pos_x[2], pos_y[2]), 0.00916)
CB = ctrl.AddRoad((pos_x[2], pos_y[2] - road_width), (pos_x[1] + h_diff, pos_y[2] - road_width), 0.0075)

JI = ctrl.AddRoad((pos_x[1] + h_diff, pos_y[1]), (pos_x[2], pos_y[1]), 0.004)
IJ = ctrl.AddRoad((pos_x[2], pos_y[1] - road_width), (pos_x[1] + h_diff, pos_y[1] - road_width), 0.0125)

CD = ctrl.AddRoad((pos_x[2] + h_diff, pos_y[2]), (pos_x[3], pos_y[2]), 0.00305)
DC = ctrl.AddRoad((pos_x[3], pos_y[2] - road_width), (pos_x[2] + h_diff, pos_y[2] - road_width), 0.006)
IG = ctrl.AddRoad((pos_x[2] + h_diff, pos_y[1]), (pos_x[3], pos_y[1]), 0.02361)

KJ = ctrl.AddRoad((pos_x[1] + h_diff / 2, pos_y[0]), (pos_x[1] + h_diff / 2, pos_y[1] - v_diff), 0.014)
JB = ctrl.AddRoad((pos_x[1] + h_diff / 2, pos_y[1] + v_diff / 2), (pos_x[1] + h_diff / 2, pos_y[2] - v_diff), 0.01916)
BE = ctrl.AddRoad((pos_x[1] + h_diff / 2, pos_y[2] + v_diff / 2), (pos_x[1] + h_diff / 2, pos_y[3]), 0.0227)

IH = ctrl.AddRoad((pos_x[2] + h_diff / 2, pos_y[1] - v_diff), (pos_x[2] + h_diff / 2, pos_y[0]), 0.0025)
CI = ctrl.AddRoad((pos_x[2] + h_diff / 2, pos_y[2] - v_diff), (pos_x[2] + h_diff / 2, pos_y[1] + v_diff / 2), 0.0205)
FC = ctrl.AddRoad((pos_x[2] + h_diff / 2, pos_y[3]), (pos_x[2] + h_diff / 2, pos_y[2] + v_diff / 2), 0.018)

normal = 1/50
factor = 20
ctrl.AddExtremeRoads([AB, DC, FC, KJ, LJ], [normal * factor, normal * factor, normal, normal, normal])

#curvas desde la izquiera
ctrl.connect_roads(AB, BE, (pos_x[1] + h_diff / 2, pos_y[2]))
ctrl.connect_roads(LJ, JB, (pos_x[1] + h_diff / 2, pos_y[1]))
ctrl.connect_roads(BC, CI, (pos_x[2] + h_diff / 2, pos_y[2]))
ctrl.connect_roads(JI, IH, (pos_x[2] + h_diff / 2, pos_y[1]))

#curvas desde arriba
ctrl.connect_roads(KJ, JI, (pos_x[1] + h_diff / 2, pos_y[1]))
ctrl.connect_roads(JB, BA, (pos_x[1] + h_diff / 2, pos_y[2] - road_width))
ctrl.connect_roads(JB, BC, (pos_x[1] + h_diff / 2, pos_y[2]))

#curvas desde abajo
ctrl.connect_roads(FC, CD, (pos_x[2] + h_diff / 2, pos_y[2]))
ctrl.connect_roads(FC, CB, (pos_x[2] + h_diff / 2, pos_y[2] - road_width))
ctrl.connect_roads(CI, IG, (pos_x[2] + h_diff / 2, pos_y[1]))
ctrl.connect_roads(CI, IJ, (pos_x[2] + h_diff / 2, pos_y[1] - road_width))

#curvas desde la derecha
ctrl.connect_roads(DC, CI, (pos_x[2] + h_diff / 2, pos_y[2] - road_width))
ctrl.connect_roads(CB, BE, (pos_x[1] + h_diff / 2, pos_y[2] - road_width))
ctrl.connect_roads(IJ, JB, (pos_x[1] + h_diff / 2, pos_y[1] - road_width))

#uniones rectas hortizontales
ctrl.connect_roads(AB, BC, (pos_x[1], pos_y[2]))
ctrl.connect_roads(LJ, JI, (pos_x[1], pos_y[1]))
ctrl.connect_roads(JI, IG, (pos_x[2], pos_y[1]))
ctrl.connect_roads(BC, CD, (pos_x[2], pos_y[2]))
ctrl.connect_roads(CB, BA, (pos_x[1], pos_y[2] - road_width))
ctrl.connect_roads(DC, CB, (pos_x[2], pos_y[2] - road_width))

#uniones rectas verticales
ctrl.connect_roads(KJ, JB, (pos_x[1] + h_diff / 2, pos_y[1]))
ctrl.connect_roads(JB, BE, (pos_x[1] + h_diff / 2, pos_y[2]))
ctrl.connect_roads(CI, IH, (pos_x[2] + h_diff / 2, pos_y[1]))
ctrl.connect_roads(FC, CI, (pos_x[2] + h_diff / 2, pos_y[2]))


ctrl.CreateCorner([(AB, BE, 0), (AB, BC, 0),\
    (CB, BE, 1), (CB, BA, 1),\
    (JB, BC, 2), (JB, BA, 2), (JB, BE, 2)])

ctrl.CreateCorner([(BC, CD, 0), (BC, CI, 0),\
    (DC, CI, 1), (DC, CB, 1),\
    (FC, CD, 2), (FC, CB, 2), (FC, CI, 2)])

ctrl.CreateCorner([(LJ, JI, 0), (LJ, JB, 0),\
    (IJ, JB, 1),\
    (KJ, JI, 2), (KJ, JB, 2)])

ctrl.CreateCorner([(JI, IG, 0), (JI, IH, 0),\
    (CI, IH, 1), (CI, IG, 1), (CI, IJ, 1)])
    

t1 = 0
t2 = 30
# ctrl.SetConfiguration([t2 for _ in range(11)])
# ctrl.SetConfiguration([81, 67, 7, 43, 25, 20, 53, 48, 85, 83, 29])
# ctrl.SetConfiguration([19, 89, 27, 44, 4, 38, 11, 40, 11, 10, 52, 56, 59, 27, 59]    )

rr = [AB, BA, BE, BC, CB, CD, DC, FC, CI, IG, IH, IJ, JI, KJ, LJ, JB]
print(ctrl.roads[AB].length)
ctrl.speed = 20

# p = A_star.find_shortest_path(ctrl, init_road_id=BC, end_road_id=BE)
# print(p)
# for x in p:
#     print(rr.index(x))

draw.Start(observation_time = 1)
A_star.SetDraw(draw)
print(A_star.find_shortest_path(ctrl,AB,IG,g_increment=A_star.my_g_increment_function))

# car = ctrl.AddRoutedVehicle(AB, IG)

# print(car.path)
# draw.ObserveVehicle(car, len(car.path))

to_print_1 = []
to_print_2 = []
to_print_3 = []
to_print_4 = []

# my_roads = []
# str_rr = ['AB', 'BA', 'BE', 'BC', 'CB', 'CD', 'DC','FC', 'CI', 'IG', 'IH', 'IJ', 'JI', 'KJ', 'LJ', 'JB']
# for i in range(16):
#     road_id = rr[i]
#     to_print_1.append(f'{str_rr[i]} : {ctrl.road_max_queue[road_id]}')
#     to_print_2.append(f'{str_rr[i]} : {ctrl.road_average_time_take_cars[road_id]}')
#     to_print_3.append(f'{str_rr[i]} : {ctrl.road_total_time_take_cars[road_id]}')
#     to_print_4.append(f'{str_rr[i]} : {ctrl.road_average_time_take_cars[road_id] * ctrl.road_total_amount_cars[road_id]**2}')


# print('max queue')
# print(to_print_1)
# print('ave time')
# print(to_print_2)
# print('total time')
# print('total time')
# print(to_print_3)
# print('new fitt')
# print(to_print_4)
