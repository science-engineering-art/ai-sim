from pyexpat import model
from matplotlib.hatch import HorizontalHatch
from models.control import control
import models.genetic_algorithm_marcos as gam
# import models.genetic_algorithm as ga
from models.simulation import Simulation, Simulation_test_3


EVAL_INDIVIDUAL_IN_SIMULATION_MAX_AVERAGE = 0
EVAL_INDIVIDUAL_IN_SIMULATION_TOTAL = 1
EVAL_INDIVIDUAL_IN_SIMULATION_WEIGTHED_MEAN = 2

MULTIPOINT_XOVER = 0
INTERMEDIATE_XOVER = 1
GEOMETRIC_XOVER = 2

GET_WEIGHTS_FIT_PROPORTIONAL = 0
GET_WEIGHTS_BY_RANKING = 1

simulation = Simulation_test_3()

pop_size = 10
number_of_turns = simulation.get_new_control_object().GetDimension()
maximum_waiting_time = 90
average_passing_time = 3
speed = 20
obs_time = 1
max_iterations = 100

gam.genetic_algorithm(simulation, pop_size, number_of_turns,
                      maximum_waiting_time, average_passing_time, speed, obs_time, max_iterations,
                      eval_method=EVAL_INDIVIDUAL_IN_SIMULATION_TOTAL, weight_method=GET_WEIGHTS_BY_RANKING, xover_method=MULTIPOINT_XOVER)
