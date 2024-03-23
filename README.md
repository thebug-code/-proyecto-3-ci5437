## README

### **Descripción del proyecto**

Este proyecto implementa un sistema para la planificación de torneos deportivos, utilizando técnicas de satisfacción de restricciones (SAT) y el solver Glucose. El sistema toma como entrada un archivo JSON con la configuración del torneo y genera un archivo iCalendar (.ics) con la programación de los juegos.

### **Problema a resolver**

El problema consiste en encontrar una asignación de fechas y horas para los juegos de un torneo, satisfaciendo las siguientes restricciones:

* Cada participante debe jugar dos veces con cada uno de los demás, una vez como local y otra como visitante.
* No pueden ocurrir dos juegos al mismo tiempo.
* Un participante puede jugar como máximo un juego por día.
* Un participante no puede jugar como visitante en dos días consecutivos, ni como local dos días seguidos.
* Todos los juegos deben empezar en horas en punto.
* Los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas.
* Los juegos deben ocurrir dentro de un rango de horas específico.
* Todos los juegos tienen una duración de dos horas.

### **Solución**

El sistema se compone de tres módulos:

1. **Traductor a CNF:** Este módulo convierte la configuración del torneo en formato JSON a una fórmula booleana en formato DIMACS CNF.
2. **Solver SAT:** El solver Glucose se utiliza para encontrar una solución satisfactoria a la fórmula booleana.
3. **Traductor a iCalendar:** Este módulo convierte la solución del solver SAT a un archivo iCalendar con la programación de los juegos.

### **Requisitos Previos**

Para ejecutar este proyecto, necesitarás tener instalado Python y C++.

### **Configuración del Entorno**

Antes de comenzar, es recomendable configurar un entorno virtual para manejar las dependencias. Puedes hacerlo con el siguiente comando:

```bash
python -m venv venv
source venv/bin/activate
```

Una vez activado el entorno virtual, instala las dependencias necesarias con:

```bash
pip install -r requirements.txt
```

### **Compilación de Glucose**

Para compilar el SAT solver Glucose, utiliza el siguiente comando:

```bash
./CompileGlucosaSATSolver.sh
```

## Ejecución del Programa

Para iniciar el proceso de asignación de fechas y horas de los juegos, ejecuta el programa principal con:

```bash
python main.py <nombre_archivo>
```

Donde `<nombre_archivo>` es el nombre del archivo JSON de entrada con la configuración del torneo.
