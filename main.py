from traductor_cnf import TraductorCNF
import sys
import time
import read_json as rj
import utils as util


def main(json_file_path):
    # Verifica si el archivo de entrada es un .json
    if not util.is_json_file(json_file_path):
        print("El archivo de entrada no es un .json")
        exit()

    # Lee el .json
    data = rj.read_json_file(json_file_path)

    # Obtiene una instancia del traductorCNF
    traductor = TraductorCNF(data)

    # Registra la tiempo de inicio
    start_time = time.time()

    # Obtiene todos los posibles juegos
    matches = traductor.match_generator()

    # Obtienes las clausulas
    clauses = traductor.cnf_clause()

    # Obtiene el nombre del torneo
    tournament_name = rj.get_tournament_name(data)

    # 'Traduce' la expresion al formato DIMACS CNF
    traductor.dismacs(len(matches), clauses, tournament_name.lower())

    # Ejecuta el sat solver glucose
    cnf_file_path = tournament_name.lower() + ".dimacs"
    util.run_glucose(cnf_file_path, traductor)

    # Registrar el tiempo de finalización
    end_time = time.time()

    # Calcula el tiempo que toma la ejecucion
    time_taken = end_time - start_time
    print(f"Tiempo necesario para ejecutar el bloque de código: {time_taken} segundos")


if __name__ == "__main__":
    main(sys.argv[1])
