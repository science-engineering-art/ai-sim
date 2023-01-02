from pyexpat import model
from matplotlib.hatch import HorizontalHatch
from models.control import control
from models.genetic_algorithm_marcos import *
from models.simulation import Simulation, Simulation_test_3



simulation = Simulation_test_3()
MAX_ITERATIONS = 10
genetic_algorithm(simulation, pop_size=10, number_of_turns=15, maximum_waiting_time=100, 
                  average_passing_time=5,speed = 20, obs_time=5, max_iterations= 50)


