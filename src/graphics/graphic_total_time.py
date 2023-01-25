
import dictdatabase as ddb
import matplotlib.pyplot as plt
import numpy as np

ddb.config.storage_directory = '../../ddb_storage/'
name = 'all_results'
s = ddb.at(name)
json = s.read()['results']

tota_time_take_cars = []
tota_time_take_cars_b = []
for i in range(1,54):
    tota_time_take_cars.append(json[str(i)]['total_time_take_cars'])
    tota_time_take_cars_b.append(json[str(i)]['total_time_take_cars_b'])
    
    
# plotting line
plt.plot(range(1,54), tota_time_take_cars, color='gray')
# plotting the points
for j in range(1, 54):
    fit = tota_time_take_cars[j - 1]
    plt.plot(j, fit, marker='o',
            color='blue')

# plotting line
plt.plot(range(1,54), tota_time_take_cars_b, color='gray')
# plotting the points
for j in range(1, 54):
    fit = tota_time_take_cars_b[j - 1]
    plt.plot(j, fit, marker='o',
            color='orange' if fit < -1 and fit > -20 else 'gray' if fit < -1 else 'red')

# naming the x axis
plt.xlabel('Test')
# naming the y axis
plt.ylabel('Tiempo total (s)')

# giving a title to my graph
plt.title('Total de tiempo que toma a los carros')

plt.xticks(np.arange(1, 54, 3))

# function to show the plot
plt.savefig(f'graphic_{i}')

plt.clf()