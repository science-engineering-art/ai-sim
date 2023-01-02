from pyexpat import model
from matplotlib.hatch import HorizontalHatch
from models.control import control
import models.genetic_algorithm_marcos as gam
import models.genetic_algorithm as ga
from models.simulation import Simulation, Simulation_test_3


simulation = Simulation_test_3()

pop_size = 5
number_of_turns = 15
maximum_waiting_time = 90
average_passing_time = 3
speed = 20
obs_time = 1
max_iterations = 10
gam.genetic_algorithm(simulation, pop_size, number_of_turns,
                      maximum_waiting_time, average_passing_time, speed, obs_time, max_iterations)
# ga.genetic_algorithm(simulation, pop_size, number_of_turns, maximum_waiting_time, average_passing_time)
