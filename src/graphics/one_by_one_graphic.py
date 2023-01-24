import os
import numpy as np
import dictdatabase as ddb
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from graphic_info import get_graphic_info

os.chdir('../../tests')

s = ddb.at('graphic_info')
if not s.exists():
    os.system('python convert.py')
    info = get_graphic_info()
    s.create(info)

json = s.read()
test_number  = [i for i in range(50)]

_colors = colors.ColorConverter().colors

for i, (_, _color) in enumerate(_colors.items()):
    if i == 50: break

    min_fitness_list = [min for min, _, _ in json[f'{i}']['mins']]
    max_fitness_list = [max for max, _, _ in json[f'{i}']['maxs']]

    # plotting line
    plt.plot(test_number, min_fitness_list, color=_color)
    # plotting the points
    for j in range(50):
        fit = min_fitness_list[j]
        plt.plot(j, fit, marker='o',
                color='orange' if fit < -1 and fit > -20 else 'gray' if fit < -1 else 'red')

    # plotting line
    plt.plot(test_number, max_fitness_list, color=_color)
    # plotting the points
    for j in range(50):
        fit = max_fitness_list[j]
        plt.plot(j, fit, marker='o',
                color='orange' if fit < -1 and fit > -20 else 'gray' if fit < -1 else 'red')

    # naming the x axis
    plt.xlabel('Test')
    # naming the y axis
    plt.ylabel('Fitness de la solución final')

    # giving a title to my graph
    plt.title('Resultados obtenidos')

    plt.xticks(np.arange(0, 50, 1.0))

    # function to show the plot
    plt.savefig(f'graphic_{i}')

    plt.clf()
