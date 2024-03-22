from traductor_cnf import TraductorCNF
import read_json as rj
import utils as util

# prueba
file = "ejemplo1.json"
data = rj.read_json_file(file)
traductor = TraductorCNF(data)
matches = traductor.match_generator()
clauses = traductor.cnf_clause()
tournament_name = rj.get_tournament_name(data)
traductor.dismacs(len(matches), clauses, tournament_name)
cnf_file_path = file.split(".")[0] + ".dimacs"
util.run_glucose(cnf_file_path, traductor)
