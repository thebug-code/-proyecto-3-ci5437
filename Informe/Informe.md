#
### CI5437 - Inteligencia Artificial 1
##### Prof. Carlos Infante
# Proyecto 3: CNF-SAT
Por Oliver Bueno, Alejandro Meneses

## Presentación del problema
En este proyecto se centra en la organización eficiente de un torneo, en donde se busca la asignación eficiente de fechas y horas para los juegos de un torneo. Frente a un conjunto de reglas y restricciones de tiempo, buscando garantizar que cada equipo juegue el número adecuado de partidos, tanto de local como de visitante, y que todos los juegos se programen de manera justa y dentro de un período específico.

Para abordar este problema, se recurre a la lógica proposicional y solucionadores SAT. Se han modelado y traducido las reglas del torneo a formato DISMAC CNF, de tal forma que el solucionador SAT puede procesarlo, lo que nos permite explorar los posibles horarios y encontrar uno que cumpla con todas las condiciones impuestas.

## Modelado de las restriciones
Para establecer las restriciones se establece la variable M con los sub-índices l(local), v(visitante), d(día), h(hora), en donde se establecen los siguientes domininios para los sub-índices:

- Dom l: Son todos los posibles equipos.
- Dom v: Son todos los posibles equipos.
- Dom d: Son todas las posibles fechas desde el día inicial, hasta el día final
- Dom h: Son todoas las posible horas en punto en las que puede empezar un juego, esto es, si la hora de inicio es 07:30:00 y la hora de culminación de la jornada es 14:00:00, el dominio de las horas para los encuentros es {08:00:00, 10:00:00, 12:00:00}. El dominio contiene la primera hora en punto más cercana al inicio y se va incrementando cada dos horas hasta la última hora válida.

Cada restricción se modela de la siguiente forma:

- Todos los juegos deben empezar en horas "en punto": Esto esta contemplado por la definicíon de la variable M, dado por el dominio del sub-índice h.
- Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas: Esto esta contemplado por la definicíon de la variable M, dado por el dominio del sub-índice d.
- Todos los juegos deben ocurrir entre un rango de horas especificado: Esto esta contemplado por la definicíon de la variable M, dado por el dominio del sub-índice h.
- Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos: Se definen las siguientes cláusulas lógicas

  
  $(\neg M_{l,v,d,h} \lor \neg M_{l,v,d+1,h})$   Para los partidos como local
  
  $(\neg M_{v,l,d,h} \lor \neg M_{v,l,d+1,h})$   Para los partidos como visitante

- Un participante puede jugar a lo sumo una vez por día: Se definen las siguiente cláusula lógica

  $(\neg M_{l,v,d,h} \lor \neg M_{l,v',d,h'})$ con $h != h' $

- Dos juegos no pueden ocurrir al mismo tiempo: Se definen las siguiente cláusula lógica

  $(\neg M_{l,v,d,h} \lor \neg M_{l',v',d,h})$ con $(l,v) != (l', v') $

- Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales": Se definen las siguientes cláusulas lógicas

  - Todos los participantes juegan como "locales" una vez contra los otros participantes.
  
    $(\forall d,h | M_{l,v,d,h})$ donde el equipo l juega como local contra el equipo v. Esto cláusula asegura que se juegue al  
    menos una vez.

    $(\neg M_{l,v,d',h'} \lor \neg M_{l,v,d',h'})$ con $(d, h) != (d', h') $ Esta cláusula asegura que se jueguen exactamente una vez.

  - Todos los participantes juegan como "visitantes" una vez contra los otros participantes.
 
    $(\forall d,h | M_{v,l,d,h})$ donde el equipo l juega como visitante contra el equipo v. Esto cláusula asegura que se juegue al  
    menos una vez.

    $(\neg M_{v,l,d',h'} \lor \neg M_{v,l,d',h'})$ con $(d, h) != (d', h') $ Esta cláusula asegura que se jueguen exactamente una vez.
  
## Especificaciones de la implementación
Para la implementación de la solución se uso python como lenguaje y Glucose como solucionar SAT. A continuación se detallan los archivos y sus funciones.

- read_json: contiene las funciones para leer archivos.json con las especificaciones de torneos, además contiene funciones que retornan cada dia del torneo y las horas especificas en las que se puede jugar cada encuentro, las cuales son necesarias para establecer las variables.

- traductor_cnf: contiene la clase "TraductorCNF" la cual se encarga de generar todos los posibles encuentros, realizando un producto cruz, guardando dichos encuentros en un diccionario, a los cuales se les da como claves números enteros, los cuales son las variables para la cnf. Además contiene las funciones que para establecer las clausulas de cada una de las restricciones como fueron definidas en la sección anterior, también contiene las funciones para traducir las clausulas al formato Dismac y para traducir las salidas que retorne el SAT-solver a formato .ics.

- utils: contiene las funciones necesarias para ejecutar el SAT-solver Glucose.

- main: contiene el cliente principal para la ejecuación de las tareas del programa.

## Pruebas y resultados
Se realizarón un total 10 pruebas, las cuales fueron aumentando de dificultad progresivamnete, siendo proporcional con el número de equipos, el número de horas, y el número de días a continuación se muestra una tabla con los valores usados y los resultados.

| Nº Equipos | Horas | Días | Variables  | Clausulas     | Tiempo (s) |
|------------|-------|------|------------|---------------|------------|
| 4          | 4     | 6    | 168        | 5604          | 0.008594   |
| 4          | 4     | 31   | 744        | 43620         | 0.037973   |
| 4          | 6     | 61   | 2196       | 288138        | 0.411798   |
| 5          | 6     | 61   | 3660       | 538430        | 0.753633   |
| 5          | 8     | 61   | 4880       | 944180        | 1.505926   |
| 6          | 8     | 61   | 5490       | 900435        | 1.293759   |
| 8          | 8     | 61   | 10248      | 2057972       | 3.201675   |
| 8          | 8     | 76   | 12768      | 2853032       | 4.806860   |
| 10         | 8     | 76   | 20520      | 5423310       | 4.115944   |
| 14         | 10    | 76   | 69160      | 37159122      | 29.88765   |

Las pruebas se realizarón en un equipocon la siguientes especificaciones:
- Procesador: i5 12600k, 3,7 GHZ, 16 hilos.
- Memoria Ram: 16 GB, Ddr5 4800 MHz.

## Conclusiones
Dados los resultados anterirores, se observa que al modificar los sub-índices de la variable, cambia la complegidad del problema, lo que ocasiona multiples resultados.

Al aumentar alguno de los valores de los sub-índice el problema aumenta, esto se ve reflejado en la cantidad de variables que se genera, y esto concuerda, ya que los dominios para efectuar producto cruz para obtener la variables para el SAT-solver aumenta. Por otro lado al aumentar el número de variables, tambien aumenta el número de clausulas del cnf.

Además se observan que los tiempos van en aumento y esto se produce a que cada proceso (generar las variables, generar las clausulas, resolver el cnf) aumenta de complegidad ya que tienen un mayor dominio que abarcar.

El problema hasta las pruebas que fueron abordas resulto eficiente, pero se puede notar que al aumentar un poco las variables, el programa aumenta significativamente el tiempo para resolverlo, lo cual deja como conclusión que para un número elevado de equipos en un torneo de larga duración, resolver rl problema usando CNF-SAT puede resultar ineficiente.
