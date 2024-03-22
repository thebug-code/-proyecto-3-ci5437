import subprocess
import sys


def get_keys_by_value(dictionary, value_to_find):
    return [key for key, value in dictionary.items() if value == value_to_find]


def run_glucose(cnf_file_path, traductor):
    # Comando para ejecutar glucose con el archivo CNF en formato Dimacs
    command = [
        "glucose/simp/glucose",
        cnf_file_path,
        "glucose-sol.txt",
        "-model",
        "-verb=0",
    ]

    # Ejecutar Glucose
    subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with open("glucose-sol.txt", "r") as file:
        solution = file.readline().strip()
        file.close()

    # Verifica si la solucion existe
    if solution == "UNSAT":
        print("Fórmula lógica insatisfacible")
        exit()
    else:
        traductor.ical(solution)
        print(f"{cnf_file_path}.isc fue creado exitosamente")

        # Obtiene el numero de clausulas y variables creadas
        with open(cnf_file_path, "r") as file:
            first_line = file.readline().strip()
            file.close()

        heads = first_line.split()
        variables = int(heads[2])
        clauses = int(heads[3])

        print()
        print("Numero de variables y clausulas en DIMACS CNF:")
        print(f"- {variables} variables")
        print(f"- {clauses} clausulas")
