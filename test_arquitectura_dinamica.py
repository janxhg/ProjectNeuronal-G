import sys
import os

# Añadir el directorio 'src' al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from core.red_dinamica import RedDinamica
from core.elementos_neuronales import NeuronaBase
from core.neurona_g1 import NeuronaG1
from core.neurona_g2 import NeuronaG2
from core.neurona_g3 import NeuronaG3

def run_test():
    """Configura y ejecuta una prueba de la arquitectura dinámica."""
    print("--- INICIANDO PRUEBA DE ARQUITECTURA DINÁMICA ---")

    # 1. Crear la red
    red = RedDinamica()

    # 2. Crear neuronas
    # Neuronas de entrada (presinápticas)
    red.agregar_neurona(NeuronaBase(id_neurona='N_Pre1'))
    red.agregar_neurona(NeuronaBase(id_neurona='N_Pre2'))
    red.agregar_neurona(NeuronaBase(id_neurona='N_Pre3'))
    red.agregar_neurona(NeuronaBase(id_neurona='N_Pre4')) # Para la segunda G1

    # Neuronas G1 (Detectores de secuencia simple)
    g1_a = NeuronaG1(id_neurona='G1_A_Detector_123', secuencia_objetivo=['N_Pre1', 'N_Pre2', 'N_Pre3'])
    g1_b = NeuronaG1(id_neurona='G1_B_Detector_4', secuencia_objetivo=['N_Pre4'])
    red.agregar_neurona(g1_a)
    red.agregar_neurona(g1_b)

    # Neurona G2 (Detector de secuencia G1_A -> G1_B)
    g2 = NeuronaG2(id_neurona='G2_Detector_A_then_B', id_input_A='G1_A_Detector_123', id_input_B='G1_B_Detector_4', ventana_temporal=10)
    red.agregar_neurona(g2)

    # Neurona G3 (Detector de evento complejo G1_A -> G2)
    g3 = NeuronaG3(id_neurona='G3_Detector_Evento_Complejo', id_input_g1='G1_A_Detector_123', id_input_g2='G2_Detector_A_then_B', ventana_temporal=20)
    red.agregar_neurona(g3)

    # 3. Conectar las neuronas para formar la jerarquía
    print("\n--- CONECTANDO NEURONAS ---")
    # G2 escucha a G1_A y G1_B
    red.conectar_neuronas('G1_A_Detector_123', 'G2_Detector_A_then_B')
    red.conectar_neuronas('G1_B_Detector_4', 'G2_Detector_A_then_B')

    # G3 escucha a G1_A y a G2
    red.conectar_neuronas('G1_A_Detector_123', 'G3_Detector_Evento_Complejo')
    red.conectar_neuronas('G2_Detector_A_then_B', 'G3_Detector_Evento_Complejo')


    print("\n--- ESTRUCTURA DE RED CREADA ---")

    # 3. Simulación
    print("\n--- INICIANDO SIMULACIÓN PASO A PASO ---")
    
    # Escenario: G1_A se activa, luego G1_B, lo que debería activar G2.
    # Finalmente, la activación de G2 (después de G1_A) debería activar G3.

    # Activar secuencia para G1_A
    print("\n* Estimulando secuencia para G1_A (1->2->3)")
    red.aplicar_impulso_externo('G1_A_Detector_123', 1.0, id_origen='N_Pre1')
    red.simular_paso()
    red.aplicar_impulso_externo('G1_A_Detector_123', 1.0, id_origen='N_Pre2')
    red.simular_paso()
    red.aplicar_impulso_externo('G1_A_Detector_123', 1.0, id_origen='N_Pre3')
    red.simular_paso() # G1_A debería disparar aquí

    # Simular unos pasos para crear un lapso de tiempo
    for _ in range(5):
        red.simular_paso()

    # Activar G1_B
    print("\n* Estimulando a G1_B")
    red.aplicar_impulso_externo('G1_B_Detector_4', 1.0, id_origen='N_Pre4')
    red.simular_paso() # G1_B debería disparar aquí. A su vez, G2 debería disparar.

    # Simular más pasos para que G3 tenga tiempo de detectar G2
    for _ in range(10):
        red.simular_paso() # G3 debería disparar en uno de estos pasos.

    print("\n--- FIN DE LA SIMULACIÓN ---")

if __name__ == "__main__":
    run_test()
