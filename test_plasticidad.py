import logging
import os
from src.core.red_dinamica import RedDinamica
from src.core.neurona_g1 import NeuronaG1 # Usamos G1 como neuronas base para el test

# --- Configuración del Logging ---
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
log_filename = os.path.join(LOG_DIR, 'test_plasticidad.log')

# Configurar para que el log se escriba en un archivo, borrando el anterior
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename,
    filemode='w' # 'w' para sobrescribir el archivo en cada ejecución
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# --- Experimento de Plasticidad Sináptica ---

def ejecutar_test_plasticidad():
    """
    Realiza un experimento para validar el refuerzo Hebbiano y la poda sináptica.
    """
    logging.info("--- INICIO DEL TEST DE PLASTICIDAD SINÁPTICA ---")

    # 1. Crear la red
    red = RedDinamica()

    # 2. Crear neuronas
    neurona_A = NeuronaG1(id_neurona="A", umbral_disparo=0.5)
    neurona_B = NeuronaG1(id_neurona="B", umbral_disparo=0.5)
    neurona_C = NeuronaG1(id_neurona="C", umbral_disparo=0.8) # Umbral más alto para requerir inputs

    red.agregar_neurona(neurona_A)
    red.agregar_neurona(neurona_B)
    red.agregar_neurona(neurona_C)

    # 3. Conectar neuronas
    red.conectar_neuronas("A", "C", peso_inicial=0.5)
    red.conectar_neuronas("B", "C", peso_inicial=0.5)

    logging.info("\n--- ESTADO INICIAL DE LA RED ---")
    red.log_estado_conexiones("al inicio")

    # 4. Simulación
    ciclos_estimulacion = 15
    logging.info(f"\n--- INICIANDO SIMULACIÓN: {ciclos_estimulacion} ciclos de estimulación para A ---")

    for i in range(ciclos_estimulacion):
        logging.info(f"\n--- CICLO DE SIMULACIÓN {i+1}/{ciclos_estimulacion} ---")
        
        # Estimulamos selectivamente la neurona A
        logging.info(f"Aplicando impulso externo a la neurona A.")
        red.aplicar_impulso_externo("A", 1.0)
        
        # Avanzamos la simulación un paso
        red.simular_paso()

        # Loguear estado de conexiones en momentos clave
        if (i+1) in [1, 5, 10, ciclos_estimulacion]:
            red.log_estado_conexiones(f"después del ciclo {i+1}")

    logging.info("\n--- ESTADO FINAL DE LA RED ---")
    red.log_estado_conexiones("al final")

    logging.info("\n--- ANÁLISIS DE RESULTADOS ---")
    conexion_AC = next(c for c in red.conexiones.values() if c.neurona_origen.id == 'A' and c.neurona_destino.id == 'C')
    conexion_BC = next(c for c in red.conexiones.values() if c.neurona_origen.id == 'B' and c.neurona_destino.id == 'C')

    logging.info(f"Peso final A->C: {conexion_AC.peso:.4f}")
    logging.info(f"Peso final B->C: {conexion_BC.peso:.4f}")

    if conexion_AC.peso > 0.5 and conexion_BC.peso < 0.5:
        logging.info("\033[92mÉXITO: La conexión A->C se reforzó y la conexión B->C se debilitó como se esperaba.\033[0m")
    else:
        logging.error("\033[91mFALLO: Los pesos de las conexiones no se comportaron como se esperaba.\033[0m")

if __name__ == "__main__":
    ejecutar_test_plasticidad()
