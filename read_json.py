import json
from datetime import datetime, timedelta

# Función para leer un archivo JSON


def read_json_file(file):
    try:
        with open(file, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"El archivo {file} no existe")
        return None


# Función para obtener el rango de las fechas de un archivo JSON


def get_dates(data):
    start_date = datetime.fromisoformat(data["start_date"])
    end_date = datetime.fromisoformat(data["end_date"])

    # Se genera el rango de fechas
    range_dates = []
    actual_date = start_date
    while actual_date <= end_date:
        range_dates.append(actual_date.strftime("%Y-%m-%d"))
        actual_date += timedelta(days=1)

    return range_dates


# Función para obtener el rango de las horas de un archivo JSON


def get_hours(data):
    start_hour = datetime.strptime(data["start_time"], "%H:%M:%S")
    end_hour = datetime.strptime(data["end_time"], "%H:%M:%S").time()

    # Se redondea la hora de inicio a la siguiente hora en punto
    if start_hour.minute != 0 or start_hour.second != 0:
        start_hour = start_hour.replace(minute=0, second=0) + timedelta(hours=1)

    total_hours = end_hour.hour - start_hour.hour
    count = 2

    # Se genera el rango de horas
    range_hours = []
    actual_hour = start_hour
    while count <= total_hours:
        range_hours.append(actual_hour.strftime("%H:%M:%S"))
        actual_hour += timedelta(hours=2)

        count += 2
    return range_hours


# Función para obtener los equipos de un archivo JSON


def get_teams(data):
    return data["participants"]


# Función para obtener el nombre del torneo de un archivo JSON


def get_inicial_date(data):
    return datetime.fromisoformat(data["start_date"]).date()


# Función para obtener el nombre del torneo de un archivo JSON


def get_final_date(data):
    return datetime.fromisoformat(data["end_date"]).date()


# Función para obtener el nombre del torneo de un archivo JSON


def get_inicial_time(data):
    return datetime.strptime(data["start_time"], "%H:%M:%S").time()


# Función para obtener el nombre del torneo de un archivo JSON


def get_final_time(data):
    return datetime.strptime(data["end_time"], "%H:%M:%S").time()


# Función para obtener el nombre del torneo de un archivo JSON


def get_tournament_name(data):
    return data["tournament_name"]
