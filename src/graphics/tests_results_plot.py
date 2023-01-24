# importing the required module
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

tests_path = os.path.dirname(__file__)
if sys.platform.startswith('win'):
    tests_path = tests_path.replace('src', 'tests\\')
else:
    tests_path = tests_path.replace('src', 'tests/')
print(tests_path)

# y axis values
fitness_list = []
for i in range(50):
    with open(f"{tests_path}test_50_30_199_90_3_30_({i}).txt", "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline().decode()
        last_line = last_line.replace("Final solution: ", "")
        if True:
            fitness = eval(f"{last_line}[1]")
            print(fitness)
        else:
            fitness = 1
            print(fitness)
        fitness_list.append(fitness)

print(fitness_list[49])
# x axis values
test_number = [i for i in range(50)]

# plotting line
plt.plot(test_number, fitness_list, color='gray')

# plotting the points
for i in range(50):
    fit = fitness_list[i]
    plt.plot(i, fit, marker='o',
             color='orange' if fit < -1 and fit > -20 else 'limegreen' if fit < -1 else 'red')

# naming the x axis
plt.xlabel('Test')
# naming the y axis
plt.ylabel('Fitness de la solución final')

# giving a title to my graph
plt.title('Resultados obtenidos')

plt.xticks(np.arange(0, 50, 1.0))

# function to show the plot
plt.show()
