print("DEBUG: Iniciando prueba de importación...")

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
print("DEBUG: Matplotlib importado con éxito.")

import numpy as np
print("DEBUG: NumPy importado con éxito.")

from src.red.red_clase import RedBiologica
print("DEBUG: RedBiologica importado con éxito.")

from configuracion import parametros_simulacion as ps
print("DEBUG: parametros_simulacion importado con éxito.")

from src.escenarios.pruebas.logica_pruebas import ejecutar_prueba_selectividad_secuencia
print("DEBUG: logica_pruebas importado con éxito.")

from src.main_parts.setup_network import initialize_network
print("DEBUG: setup_network importado con éxito.")

from src.main_parts.training_phase import run_training_phase
print("DEBUG: training_phase importado con éxito.")

from src.main_parts.testing_phase import run_testing_phase
print("DEBUG: testing_phase importado con éxito.")

from src.main_parts.g2_training_phase import run_g2_training_phase
print("DEBUG: g2_training_phase importado con éxito.")

from src.main_parts.g2_testing_phase import run_g2_testing_phase
print("DEBUG: g2_testing_phase importado con éxito.")

from src.main_parts.g3_training_phase import run_training_phase_g3
print("DEBUG: g3_training_phase importado con éxito.")

from src.main_parts.g3_testing_phase import run_testing_phase_g3
print("DEBUG: g3_testing_phase importado con éxito.")

from src.main_parts.inhibition_test_scenario import run_inhibition_test_scenario
print("DEBUG: inhibition_test_scenario importado con éxito.")

from src.main_parts.sfa_test_scenario import run_sfa_test_scenario
print("DEBUG: sfa_test_scenario importado con éxito.")

print("\n--- Todo hasta sfa_test_scenario funciona correctamente ---")
