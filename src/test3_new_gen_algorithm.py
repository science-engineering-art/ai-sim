from pyexpat import model
from matplotlib.hatch import HorizontalHatch
from models.control import control
from models.genetic_algorithm_marcos import *
from models.simulation import Simulation, Simulation_test_3



simulation = Simulation_test_3()
MAX_ITERATIONS = 10
genetic_algorithm(simulation, 20, 15, 100, 5, max_iterations= 20)


