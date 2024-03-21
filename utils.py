import subprocess
import sys

def run_glucose(cnf_file_path):
    # Comando para ejecutar glucose con el archivo CNF en formato Dimacs
    command = ['glucose/simp/glucose', cnf_file_path, "-model", "-verb=0"]
    
    # Abrir un archivo de texto para escribir la salida
    with open('glucose-sol.txt', 'w') as out_file:
        # Ejecutar Glucose y redirigir la salida al archivo
        subprocess.run(command, stdout=out_file, stderr=subprocess.PIPE, text=True)
    
if __name__ == '__main__':
    run_glucose(sys.argv[1])



