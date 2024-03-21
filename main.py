from traductor_cnf import TraductorCNF
import read_json as rj

# prueba
file = 'ejemplo1.json'
data = rj.read_json_file(file)
traductor = TraductorCNF(data)
matches = traductor.match_generator()
print(matches)
cnf = traductor.one_team_one_opponent(matches, [])
nombre = rj.get_tournament_name(data)
print(nombre)
traductor.dismacs(len(matches), cnf, nombre)
