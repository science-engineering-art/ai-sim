
# ai-sim

Para probar el algoritmo evolutivo usado con la simulacion ajuste los parametros en test3_evolutionary_algorithm.py
y ejecute el mismo

Para probar como se veria la simulacion ajuste los parametros de tiempo de ejecucion y speed en test_3_simulation.py.

test3_a_star_length.py contiene una version de A_star para calcular la menor distancia de una calle a otra teniendo como heurisitica la distancia en linea recta

test3_a_star_time contiene una version de A_star para calcular el menor tiempo de una calle a otra teniendo teniendo como heurisitica (h) la distancia en linea recta. Lo interesante de esto es que para medir el tiempo lo que se hace es ponerse a correr una simulacion, y poniendo varios carros a tomar todas las rutas posibles para tener los tiempos de llegada (los valores de g en f = g + h)

test3_a_star_time es similar al anterior pero usamos para calcular la heuristica un Dijkstra partiendo de la calle final, hasta todas las otras calles, calculando un aproximado de timempo teniendo en cuenta la longitud de las calles y los tiempos de cada semaforos.
