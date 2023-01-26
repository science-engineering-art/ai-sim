
# Traffic-lights

Para resolver las depenencias del proyecto ejecute el siguiente comando.

```shell
pip install -r requeriments.txt 
```


Para probar el algoritmo evolutivo usado con la simulacion ejecute alguno de los siguientes dos comandos.

```shell
make test3_evol
make test5_evol
```

Para ajustar los parámetros se debe entrar a los archivos de código `test3_evolutionary_algorithm .py` y `test5_evolutionary_algorithm`.

Para probar como se veria la simulacion ajuste los parametros de tiempo de ejecucion pasados al metodo Start(observation_time o it_amount) y de speed en el objeto ctrl (correspondiente a la velocidad de la simulacion), en `test_3_simulation.py`, `test_4.py`, `test_5.py` o `test_6.py`. Tenga en cuenta que el mapa de `test_4.py` es algo grande y los precalculos asociados pueden tomar varios minutos, pero esto es solo la primera vez que lo ejecuta en su computadora. El `test_5` es el que se uso para probar el algoritmo genetico exhaustivamente.

```shell
make test3
make test4
make test5
make test6
```

`test3_a_star_length.py` contiene una ejemplo del uso de una version de A_star para calcular la menor distancia de una calle a otra teniendo como heurisitica la distancia en linea recta. 

`test3_a_star_time` contiene una version de A_star para calcular el menor tiempo de una calle a otra teniendo teniendo como heurisitica (h) la distancia en linea recta. Lo interesante de esto es que para medir el tiempo lo que se hace es ponerse a correr una simulacion, y se insertan varios carros a tomar todas las rutas posibles para obtener sus tiempos de llegada (los valores de g en f = g + h)

`test3_a_star_time_dijkstra` es similar al anterior pero usamos para calcular la heuristica un Dijkstra partiendo de la calle final, hasta todas las otras calles, calculando un aproximado de tiempo teniendo en cuenta la longitud de las calles y los tiempos de cada semaforos.

Puede observar como se comportan estos algoritmos haciendo uso de 
```shell
make test3_time
make test3_time_dijkstra
```