# Planificador de torneos deportivos con SAT: de JSON a iCalendar

## **Descripción del proyecto**

Este proyecto implementa un sistema para la planificación de un torneo deportivo, utilizando técnicas de satisfacción de restricciones (SAT) y el solver Glucose. El sistema toma como entrada un archivo JSON con la configuración del torneo y genera un archivo iCalendar (.ics) con la programación de los juegos.

## **Problema a resolver**

El problema consiste en encontrar una asignación de fechas y horas para los juegos de un torneo, satisfaciendo las siguientes restricciones:

* Cada participante debe jugar dos veces con cada uno de los demás, una vez como local y otra como visitante.
* No pueden ocurrir dos juegos al mismo tiempo.
* Un participante puede jugar como máximo un juego por día.
* Un participante no puede jugar como visitante en dos días consecutivos, ni como local dos días seguidos.
* Todos los juegos deben empezar en horas en punto.
* Los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas.
* Los juegos deben ocurrir dentro de un rango de horas específico.
* Todos los juegos tienen una duración de dos horas.

## **Solución**

El sistema se compone de tres módulos:

1. **Traductor a CNF:** Este módulo convierte la configuración del torneo en formato JSON a una fórmula booleana en formato DIMACS CNF.
2. **Solver SAT:** El solver Glucose se utiliza para encontrar una solución satisfactoria a la fórmula booleana.
3. **Traductor a iCalendar:** Este módulo convierte la solución del solver SAT a un archivo iCalendar con la programación de los juegos.

## **Comenzando** :rocket:
Estas instrucciones le permitirán obtener una copia del proyecto en funcionamiento en su máquina local para fines de desarrollo y prueba.

Para este proyecto, necesitará tener instalado Python y C++. Puede descargar Python desde [aquí](https://www.python.org/downloads/) y el compilador de C++ desde los siguientes enlaces, dependiendo de su sistema operativo:

- Para sistemas basados en Windows, puede descargar el redistribuible de Microsoft Visual C++ desde [aquí](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170).
- Para sistemas Linux, deberá instalar el compilador GCC. Esto se puede hacer a través de la línea de comandos en la terminal.

Además, necesitará tener pip, el administrador de paquetes para Python, instalado. Puede aprender más sobre pip [aquí](https://pip.pypa.io/en/stable/).

## Instalación :coffee:

Para poner en marcha el proyecto, siga estos pasos:

1. Comience clonando el repositorio en su máquina local y navegando a él:

```bash
git clone git@github.com:thebug-code/-proyecto-3-ci5437.git
cd proyecto-3-ci5437.git
```

2. Cree y active un entorno virtual para manejar las dependencias del proyecto:

```powershell
python -m venv venv
source venv/bin/activate # o simplemente .\venv\Scripts\Activate.bat en Windows
```

3. Instale las dependencias necesarias:

```bash
pip install -r requirements.txt
```

4. Compile el SAT solver Glucose:

```bash
./CompileGlucosaSATSolver.sh
```

5. Inicie el proceso de asignación de fechas y horas de los juegos:

```bash
python main.py <nombre_archivo>
```

Donde `<nombre_archivo>` es el nombre del archivo JSON de entrada con la configuración del torneo. El cual debe tener el siguiente formato:

```json
{
  "tournament_name": "Nombre del torneo",
  "start_date": "Fecha de inicio del torneo en formato ISO 8601",
  "end_date": "Fecha de fin del torneo en formato ISO 8601",
  "start_time": "Hora a partir de la cual pueden ocurrir los juegos en cada día, en formato ISO 8601",
  "end_time": "Hora hasta la cual pueden ocurrir los juegos en cada día, en formato ISO 8601",
  "participants": ["Lista con los nombres de los participantes en el torneo"]
}
```

Donde:

* Las fechas y horas en formato ISO 8601 se deben especificar sin zona horaria. Se asume que la zona horaria es UTC.
* Las horas de inicio y la finalización no deben incluir milisegundo.
* La lista de participantes puede contener cualquier cantidad de equipos.
