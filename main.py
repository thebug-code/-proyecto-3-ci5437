from traductor_cnf import TraductorCNF
import time
import read_json as rj
import utils as util

# prueba
file = "ejemplo1.json"
data = rj.read_json_file(file)
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
traductor.dismacs(len(matches), clauses, tournament_name)

# Ejecuta el sat solver glucose
cnf_file_path = file.split(".")[0] + ".dimacs"
util.run_glucose(cnf_file_path, traductor)

# Registrar el tiempo de finalización
end_time = time.time()

# Calcula el tiempo que toma la ejecucion
time_taken = end_time - start_time
print(f"Tiempo necesario para ejecutar el bloque de código: {time_taken} segundos")
