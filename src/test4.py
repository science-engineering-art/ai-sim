from models.control import control
from templates.templates import GridMap

template = GridMap((700, 400), 92, 300, 200, 1100, 600, 2, 2, 4)
ctrl: control = template.generate_template('map4')
ctrl.Start(observation_time=120, draw=True)