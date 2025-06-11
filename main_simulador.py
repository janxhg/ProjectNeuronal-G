# -*- coding: utf-8 -*-
# --- Importaciones Críticas ---
# Matplotlib debe importarse y su backend debe establecerse ANTES que cualquier otra importación
# de biblioteca científica o del proyecto para evitar conflictos de backend.
import matplotlib
matplotlib.use('TkAgg') # Usar un backend interactivo para visualización
import matplotlib.pyplot as plt

# --- Otras Importaciones Estándar ---
import time
import numpy as np
import argparse
import sys
import logging
import os
import datetime
import traceback
import random

# --- Importaciones del Proyecto ---
logging.debug("Iniciando importaciones del proyecto...")

# Importaciones de configuración y parámetros
from configuracion import parametros_simulacion as ps

# Importaciones de la nueva arquitectura orientada a objetos
from src.core.red_dinamica import RedDinamica
from src.core.neurona_g1 import NeuronaG1
from src.core.neurona_g2 import NeuronaG2
from src.core.neurona_g3 import NeuronaG3
from src.core.elementos_neuronales import NeuronaBase
from src.visualizacion.visualizador_dinamico import VisualizadorDinamico

# Importaciones de utilidades (si se mantienen)
from src.main_parts.visualization_functions import plot_weight_evolution_summary
logging.debug("Todas las importaciones se han completado con éxito.")




# =============================================================================
#                             Función Principal
# =============================================================================
def demostrar_autoorganizacion(red, visualizar=False):
    """
    Demuestra la capacidad de la red para autoorganizarse, creando una neurona
    conceptual (G2) dinámicamente cuando detecta una co-ocurrencia frecuente
    de disparos en un par de neuronas G1.
    """
    logging.info("\n" + "="*80)
    logging.info("INICIO DE LA DEMOSTRACIÓN DE AUTOORGANIZACIÓN Y GENERALIZACIÓN")
    logging.info("="*80)

    visualizador = None
    if visualizar:
        visualizador = VisualizadorDinamico(red)

    # 1. Crear neuronas sensoriales G1
    red.agregar_neurona(NeuronaG1(id_neurona="G1_Sonido_Pajaro", secuencia_objetivo=["input_sonido"]))
    red.agregar_neurona(NeuronaG1(id_neurona="G1_Forma_Pajaro", secuencia_objetivo=["input_forma"]))
    red.agregar_neurona(NeuronaG1(id_neurona="G1_Color_Cielo", secuencia_objetivo=["input_cielo"]))

    logging.info("Estado inicial de la red. Solo existen neuronas G1.")
    red.log_estado_conexiones("al inicio")
    if visualizador: visualizador.actualizar_grafico()

    # 2. Simular la experiencia: ver y oír un pájaro repetidamente
    # El umbral de co-ocurrencia está en ps.UMBRAL_COOCURRENCIA.
    num_estimulos = ps.DEMO_AUTO_NUM_ESTIMULOS
    logging.info(f"\nSimulando la experiencia de 'ver y oír un pájaro' {num_estimulos} veces...")

    for i in range(num_estimulos):
        paso_actual = red.tiempo_actual
        logging.info(f"--- Estímulo conjunto #{i+1} en el paso {paso_actual} ---")
        # Aplicar impulsos muy juntos en el tiempo
        red.aplicar_impulso_externo("G1_Sonido_Pajaro", ps.INTENSIDAD_ESTIMULO, id_origen="input_sonido")
        red.simular_paso() # Avanzar un paso para que el segundo impulso esté en la ventana
        red.aplicar_impulso_externo("G1_Forma_Pajaro", ps.INTENSIDAD_ESTIMULO, id_origen="input_forma")
        
        # Dejar pasar algo de tiempo para que la red se estabilice y no se solapen las ventanas
        for _ in range(ps.PASOS_ESTABILIZACION):
            red.simular_paso()
            if visualizador: visualizador.actualizar_grafico()

    # 3. Simular un periodo de "reflexión" donde el gestor pueda actuar
    logging.info(f"\nSimulando {ps.PASOS_REFLEXION} pasos adicionales para que el Gestor de Plasticidad actúe...")
    for _ in range(ps.PASOS_REFLEXION):
        red.simular_paso()
        if visualizador: visualizador.actualizar_grafico()

    # 4. Verificar el resultado
    logging.info("\n" + "-"*80)
    logging.info("VERIFICACIÓN FINAL DEL ESTADO DE LA RED")
    logging.info("-"*80)
    logging.info(f"Número de neuronas al final: {len(red.neuronas)}")
    red.log_estado_conexiones("al final de la simulación")

    if len(red.neuronas) > 3:
        logging.info("¡ÉXITO! Se ha creado una nueva neurona dinámicamente.")
        for id_neurona in red.neuronas.keys():
            if "G2_Concepto" in id_neurona:
                logging.info(f"Neurona conceptual encontrada: {id_neurona}")
    else:
        logging.warning("FALLO: No se crearon nuevas neuronas.")

    if visualizador:
        logging.info(f"Cerrando visualizador en {ps.TIEMPO_CIERRE_VISUALIZADOR} segundos...")


    logging.info("="*80)
    logging.info("FIN DE LA DEMOSTRACIÓN DE AUTOORGANIZACIÓN")
    logging.info("="*80 + "\n")

    if visualizador:
        logging.info(f"La ventana de visualización se mantendrá abierta durante {ps.TIEMPO_CIERRE_VISUALIZADOR} segundos.")
        plt.pause(ps.TIEMPO_CIERRE_VISUALIZADOR)


def demostrar_red_compleja(red, visualizar=False):
    """
    Crea una red más grande y simula experiencias aleatorias para observar
    la formación de múltiples conceptos G2 de forma emergente.
    """
    logging.info("\n" + "="*80)
    logging.info("INICIO DE LA DEMOSTRACIÓN DE RED COMPLEJA Y APRENDIZAJE EMERGENTE")
    logging.info("="*80)

    visualizador = None
    if visualizar:
        visualizador = VisualizadorDinamico(red)

    # 1. Crear un conjunto más grande de neuronas sensoriales G1
    conceptos = ['Gato', 'Perro', 'Pajaro', 'Arbol', 'Coche']
    modalidades = ['Sonido', 'Forma', 'Color', 'Textura']
    
    neuronas_g1_por_concepto = {}

    for concepto in conceptos:
        neuronas_g1_por_concepto[concepto] = []
        for modalidad in modalidades:
            id_neurona = f"G1_{modalidad}_{concepto}"
            neurona = NeuronaG1(id_neurona=id_neurona, secuencia_objetivo=None)
            red.agregar_neurona(neurona)
            neuronas_g1_por_concepto[concepto].append(id_neurona)

    logging.info(f"Creadas {len(red.neuronas)} neuronas G1 iniciales.")
    if visualizador: visualizador.actualizar_grafico()

    # 2. Simular una serie de "experiencias" aleatorias
    num_pasos_simulacion = ps.DEMO_COMPLEJA_NUM_PASOS_SIMULACION
    logging.info(f"Simulando {num_pasos_simulacion} pasos con experiencias aleatorias...")

    for paso in range(num_pasos_simulacion):
        # En cada paso, hay una probabilidad de que se presente un concepto
        if random.random() < ps.DEMO_COMPLEJA_PROBABILIDAD_EXPERIENCIA: # Probabilidad de experiencia en cada paso
            concepto_a_estimular = random.choice(list(neuronas_g1_por_concepto.keys()))
            
            if len(neuronas_g1_por_concepto[concepto_a_estimular]) >= 2:
                # Seleccionar dos neuronas al azar de ese concepto para simular co-ocurrencia
                n1_id, n2_id = random.sample(neuronas_g1_por_concepto[concepto_a_estimular], 2)
                logging.debug(f"Paso {paso}: Estimulando co-ocurrencia para concepto '{concepto_a_estimular}' con {n1_id} y {n2_id}")
                red.aplicar_impulso_externo(n1_id, ps.INTENSIDAD_ESTIMULO)
                red.aplicar_impulso_externo(n2_id, ps.INTENSIDAD_ESTIMULO)

        red.simular_paso()
        if visualizador and paso % ps.VISUALIZADOR_FRECUENCIA_ACTUALIZACION == 0: # Actualizar el gráfico cada 5 pasos para no ralentizar
            visualizador.actualizar_grafico()

    if visualizador: visualizador.actualizar_grafico()

    # 3. Verificar el resultado
    logging.info("\n" + "-"*80)
    logging.info("VERIFICACIÓN FINAL DEL ESTADO DE LA RED COMPLEJA")
    logging.info("-"*80)
    logging.info(f"Número de neuronas al final: {len(red.neuronas)}")
    red.log_estado_conexiones()

    neuronas_g2_creadas = [n.id for n in red.neuronas.values() if isinstance(n, NeuronaG2)]
    if neuronas_g2_creadas:
        logging.info(f"¡ÉXITO! Se crearon {len(neuronas_g2_creadas)} neuronas conceptuales G2:")
        for id_g2 in neuronas_g2_creadas:
            logging.info(f"  - {id_g2}")
    else:
        logging.warning("No se crearon nuevas neuronas conceptuales G2.")

    if visualizador:
        logging.info(f"Cerrando visualizador en {ps.TIEMPO_CIERRE_VISUALIZADOR} segundos...")


    logging.info("="*80)
    logging.info("FIN DE LA DEMOSTRACIÓN DE RED COMPLEJA")
    logging.info("="*80 + "\n")

    if visualizador:
        logging.info(f"La ventana de visualización se mantendrá abierta durante {ps.TIEMPO_CIERRE_VISUALIZADOR} segundos.")
        plt.pause(ps.TIEMPO_CIERRE_VISUALIZADOR)


def demostrar_aprendizaje_jerarquico(red, visualizar=False):
    """
    Demuestra la capacidad de la red para aprender en jerarquías:
    1. Aprende conceptos G2 (ej. 'Gato', 'Perro') a partir de sensaciones G1.
    2. Aprende una abstracción G3 (ej. 'Animal') a partir de los conceptos G2.
    """
    logging.info("\n" + "="*80)
    logging.info("INICIO DE LA DEMOSTRACIÓN DE APRENDIZAJE JERÁRQUICO (G1->G2->G3)")
    logging.info("="*80)

    if visualizar:
        logging.warning("ADVERTENCIA: La visualización está activada para una simulación larga.")
        logging.warning("NO CIERRE LA VENTANA DEL GRÁFICO, incluso si parece no responder.")
        logging.warning("Cerrar la ventana interrumpirá la simulación.")

    visualizador = None
    if visualizar:
        visualizador = VisualizadorDinamico(red)

    def _identificar_neurona_concepto(red, ids_neuronas_fuente):
        """
        Encuentra la neurona G2 que mejor representa un conjunto de G1s,
        basándose en la fuerza total de sus conexiones entrantes.
        """
        logging.debug(f"--- INICIANDO IDENTIFICACIÓN DE CONCEPTO para fuentes: {ids_neuronas_fuente} ---")
        
        candidatos = {}
        neuronas_g2 = [n for n in red.neuronas.values() if isinstance(n, NeuronaG2)]
        
        if not neuronas_g2:
            logging.warning("IDENTIFICACION: No existen neuronas G2 en la red en este momento.")
            return None
        
        logging.debug(f"IDENTIFICACION: Encontradas {len(neuronas_g2)} neuronas G2 en total: {[n.id for n in neuronas_g2]}")

        MIN_CONEXIONES_REQUERIDAS = ps.MIN_CONEXIONES_REQUERIDAS_G2
        logging.debug(f"IDENTIFICACION: Requisito mínimo de conexiones: {MIN_CONEXIONES_REQUERIDAS}")

        for g2 in neuronas_g2:
            logging.debug(f"  -> Evaluando candidata G2: {g2.id}")
            
            conexiones_desde_fuente = {
                origen_id: red.conexiones[(origen_id, g2.id)]
                for origen_id in ids_neuronas_fuente
                if (origen_id, g2.id) in red.conexiones
            }
            
            num_conexiones = len(conexiones_desde_fuente)
            logging.debug(f"     - Conexiones encontradas desde fuentes: {num_conexiones}")
            
            if num_conexiones < MIN_CONEXIONES_REQUERIDAS:
                logging.debug(f"     - RECHAZADA: No cumple el mínimo de {MIN_CONEXIONES_REQUERIDAS} conexiones.")
                continue

            fuerza_total = sum(c.peso for c in conexiones_desde_fuente.values())
            candidatos[g2.id] = fuerza_total
            logging.debug(f"     - ACEPTADA como candidata con fuerza total {fuerza_total:.2f}.")

        if not candidatos:
            logging.warning(f"IDENTIFICACION: No se encontró ninguna neurona G2 que cumpla los requisitos para las fuentes: {ids_neuronas_fuente}")
            return None

        id_ganador = max(candidatos, key=candidatos.get)
        logging.info(f"IDENTIFICACION: Concepto identificado para '{ids_neuronas_fuente[0].split('_')[1]}': '{id_ganador}' (Fuerza: {candidatos[id_ganador]:.2f}).")
        return id_ganador

    # 1. Crear neuronas sensoriales G1
    neuronas_gato = ['G1_Forma_Gato', 'G1_Sonido_Gato', 'G1_Textura_Gato']
    neuronas_perro = ['G1_Forma_Perro', 'G1_Sonido_Perro', 'G1_Color_Perro']
    for id_n in neuronas_gato + neuronas_perro:
        red.agregar_neurona(NeuronaG1(id_neurona=id_n))
    logging.info(f"Creadas {len(red.neuronas)} neuronas G1.")

    logging.info("\n--- ESTADO INICIAL DE LA RED ---")
    red.log_estado_conexiones("Inicial")

    # Parámetros de entrenamiento
    num_ciclos_g2 = ps.DEMO_JERARQUICO_NUM_CICLOS_G2
    num_ciclos_g3 = ps.DEMO_JERARQUICO_NUM_CICLOS_G3
    pasos_sim_por_ciclo = ps.DEMO_JERARQUICO_PASOS_SIMULACION_POR_CICLO

    # --- FASE 1A: Aprender el concepto 'Gato' ---
    logging.info("\n--- FASE 1A: Entrenando concepto G2 ('Gato') ---")
    for i in range(num_ciclos_g2):
        logging.debug(f"Ciclo de entrenamiento Gato #{i+1}/{num_ciclos_g2}")
        for n_gato in neuronas_gato:
            red.aplicar_impulso_externo(n_gato, ps.INTENSIDAD_ESTIMULO)
        for _ in range(pasos_sim_por_ciclo):
            red.simular_paso()
            if visualizador: visualizador.actualizar_grafico()

    logging.info("\n--- ESTADO DE LA RED POST-ENTRENAMIENTO 'GATO' ---")
    red.log_estado_conexiones("Post-Gato")

    # --- FASE 1B: Aprender el concepto 'Perro' ---
    logging.info("\n--- FASE 1B: Entrenando concepto G2 ('Perro') ---")
    for i in range(num_ciclos_g2):
        logging.info(f"Ciclo de entrenamiento Perro #{i+1}/{num_ciclos_g2}")
        for n_perro in neuronas_perro:
            red.aplicar_impulso_externo(n_perro, ps.INTENSIDAD_ESTIMULO)
        for _ in range(pasos_sim_por_ciclo):
            red.simular_paso()
    logging.info("\n--- ESTADO DE LA RED POST-ENTRENAMIENTO 'PERRO' ---")
    red.log_estado_conexiones("Post-Perro")

    # --- Periodo de Consolidación para G2 ---
    logging.info("\n--- Simulando un periodo de consolidación para que se formen los conceptos G2 ---")
    for _ in range(ps.DEMO_JERARQUICO_PASOS_CONSOLIDACION_G2): # Dar tiempo suficiente para que el GestorPlasticidad actúe
        red.simular_paso()
        if visualizador:
            visualizador.actualizar_grafico()
            time.sleep(0.01)

    # --- Verificación intermedia: Identificar neuronas G2 ---
    logging.info("\n--- VERIFICACIÓN INTERMEDIA: Identificando neuronas G2 aprendidas ---")
    id_g2_gato = _identificar_neurona_concepto(red, neuronas_gato)
    id_g2_perro = _identificar_neurona_concepto(red, neuronas_perro)

    if not id_g2_gato or not id_g2_perro or id_g2_gato == id_g2_perro:
        logging.error(f"No se pudieron identificar conceptos G2 distintos. Gato: {id_g2_gato}, Perro: {id_g2_perro}. Abortando.")
    else:
        logging.info(f"Neurona G2 para 'Gato' identificada: {id_g2_gato}")
        logging.info(f"Neurona G2 para 'Perro' identificada: {id_g2_perro}")

        # --- FASE 2: Formación de Abstracción G3 ---
        logging.info("\n--- FASE 2: Entrenando abstracción G3 ('Animal') ---")
        for i in range(num_ciclos_g3):
            logging.info(f"Ciclo de entrenamiento G3 #{i+1}/{num_ciclos_g3}")
            for id_n in neuronas_gato + neuronas_perro:
                red.aplicar_impulso_externo(id_n, 1.0)
            for _ in range(pasos_sim_por_ciclo):
                red.simular_paso()
                if visualizador: visualizador.actualizar_grafico()

    # --- Verificación Final ---
    logging.info("\n" + "-"*80)
    logging.info("VERIFICACIÓN FINAL DEL APRENDIZAJE JERÁRQUICO")
    logging.info("-"*80)
    logging.info("\n--- ESTADO FINAL DE LA RED ---")
    red.log_estado_conexiones("Final (Post-Abstracción)")

    neuronas_g3_creadas = [n.id for n in red.neuronas.values() if isinstance(n, NeuronaG3)]
    if neuronas_g3_creadas:
        logging.info(f"¡ÉXITO! Se creó la neurona de abstracción G3: {neuronas_g3_creadas[0]}")
    else:
        logging.warning("No se logró crear una neurona de abstracción G3.")

    if visualizador:
        logging.info(f"Cerrando visualizador en {ps.TIEMPO_CIERRE_VISUALIZADOR} segundos...")


def demostrar_recurrencia():
    """Crea una demo para probar la memoria neuronal vía recurrencia."""
    logging.info("\n--- 3. DEMOSTRACIÓN DE RECURRENCIA (MEMORIA) ---")
    red_recurrente = RedDinamica()
    
    # 1. Crear una única neurona
    neurona_memoria = NeuronaBase(id_neurona="N_Memoria", umbral_disparo=0.8)
    red_recurrente.agregar_neurona(neurona_memoria)
    
    # 2. Conectarla a sí misma
    # Un peso < 1 asegura que la actividad se extinga sola con el tiempo.
    # Un peso >= 1 crearía un bucle infinito.
    conexion_recurrente = neurona_memoria.agregar_conexion_saliente(neurona_memoria, peso_inicial=0.95)
    logging.info(f"Creada conexión recurrente en {neurona_memoria.id}. ¿Es recurrente? {conexion_recurrente.es_recurrente}")

    # 3. Darle un único impulso para activarla
    logging.info("\nAplicando un único impulso inicial para activar la memoria...")
    neurona_memoria.recibir_impulso(1.0)
    
    # 4. Simular y observar
    logging.info("Observando cómo la neurona se mantiene activa por sí sola...")
    for i in range(10):
        logging.info(f"--- Paso de Simulación Recurrente {i+1} ---")
        red_recurrente.simular_paso()

def run_simulation(verbose_general=False):
    """
    Función principal que configura y ejecuta la simulación utilizando la nueva
    arquitectura orientada a objetos.
    """
    try:
        logging.info("--- Iniciando simulación con Arquitectura Dinámica ---")

        # 1. Crear la red dinámica
        red = RedDinamica()

        # 2. Definir IDs de neuronas basados en parámetros
        # (Esto hace más fácil la transición desde el código antiguo)
        N_PRE1_ID = 'N_Pre1'
        N_PRE2_ID = 'N_Pre2'
        N_PRE3_ID = 'N_Pre3'
        G1_A_ID = 'G1_A_Seq_123'
        G1_B_ID = 'G1_B_Seq_321' # Ejemplo de otra neurona G1
        G2_AB_ID = 'G2_AB_Seq_A_then_B'
        G3_EVENT_ID = 'G3_Event_A_then_AB'

        # 3. Crear y agregar las neuronas a la red
        logging.info("Creando neuronas...")
        # Neuronas de entrada (simuladas, no necesitan lógica especial)
        red.agregar_neurona(NeuronaBase(id_neurona=N_PRE1_ID))
        red.agregar_neurona(NeuronaBase(id_neurona=N_PRE2_ID))
        red.agregar_neurona(NeuronaBase(id_neurona=N_PRE3_ID))

        # Neuronas G1
        g1_a = NeuronaG1(id_neurona=G1_A_ID, secuencia_objetivo=[N_PRE1_ID, N_PRE2_ID, N_PRE3_ID])
        red.agregar_neurona(g1_a)

        # Neurona G2
        g2_ab = NeuronaG2(id_neurona=G2_AB_ID, id_input_A=G1_A_ID, id_input_B=G1_B_ID, ventana_temporal=ps.TIEMPO_ENTRE_EVENTOS_G2)
        red.agregar_neurona(g2_ab)

        # Neurona G3
        g3_event = NeuronaG3(id_neurona=G3_EVENT_ID, id_input_g1=G1_A_ID, id_input_g2=G2_AB_ID, ventana_temporal=ps.TIEMPO_ENTRE_EVENTOS_G3)
        red.agregar_neurona(g3_event)

        # 4. Conectar las neuronas
        logging.info("Conectando neuronas...")
        # Conexiones para activar G1_A
        red.conectar_neuronas(N_PRE1_ID, G1_A_ID)
        red.conectar_neuronas(N_PRE2_ID, G1_A_ID)
        red.conectar_neuronas(N_PRE3_ID, G1_A_ID)

        # Conexión de G1_A a G2 y G3
        red.conectar_neuronas(G1_A_ID, G2_AB_ID)
        # Para que G2 funcione, necesita una segunda entrada. Crearemos una G1_B fantasma por ahora.
        red.agregar_neurona(NeuronaG1(id_neurona=G1_B_ID, secuencia_objetivo=['N_Pre_Fake']))
        red.conectar_neuronas(G1_B_ID, G2_AB_ID)
        
        red.conectar_neuronas(G1_A_ID, G3_EVENT_ID)
        red.conectar_neuronas(G2_AB_ID, G3_EVENT_ID)

        # 5. Demostración de Aprendizaje y Poda
        red.log_estado_conexiones("Inicial")

        logging.info("\n--- 1. FASE DE APRENDIZAJE: Ejecutando cascada G1->G2->G3 ---")
        # Aplicar estímulos para la secuencia de G1_A
        red.aplicar_impulso_externo(N_PRE1_ID, 1.0, id_origen='input_1')
        red.simular_paso()
        red.aplicar_impulso_externo(N_PRE2_ID, 1.0, id_origen='input_2')
        red.simular_paso()
        red.aplicar_impulso_externo(N_PRE3_ID, 1.0, id_origen='input_3')
        red.simular_paso() # G1_A dispara

        # Retraso y activación de G1_B para G2
        for _ in range(ps.TIEMPO_ENTRE_EVENTOS_G2 - 3):
            red.simular_paso()
        red.aplicar_impulso_externo(G1_B_ID, 1.0, id_origen='N_Pre_Fake')
        red.simular_paso() # G1_B dispara

        # Pasos de propagación para que G2 y G3 disparen
        for _ in range(2):
            red.simular_paso()

        red.log_estado_conexiones("Post-Aprendizaje")

        logging.info("\n--- 2. FASE DE PODA: Simulando 100 pasos de inactividad ---")
        pasos_de_poda = ps.SIMULACION_GENERAL_PASOS_PODA
        for i in range(pasos_de_poda):
            red.simular_paso()
        logging.info(f"Se han simulado {pasos_de_poda} pasos de decaimiento pasivo.")

        red.log_estado_conexiones("Final (Post-Poda)")

        logging.info("--- Simulación run_simulation finalizada exitosamente ---")

    except Exception as e:
        logging.critical(f"CRITICAL ERROR in run_simulation: {e}", exc_info=True)

# =============================================================================
#                             Punto de Entrada del Script
# =============================================================================
def configurar_argumentos():
    """Configura y parsea los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(description="Simulador de Red Neuronal Biológicamente Plausible")
    parser.add_argument("--log-file", action="store_true", help="Guardar la salida del log en un archivo.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Imprimir logs detallados en la consola.")
    parser.add_argument("--visualizar", action="store_true", help="Activar la visualización gráfica en tiempo real.")
    return parser.parse_args()

if __name__ == "__main__":
    # --- 1. Configuración de Argumentos ---
    args = configurar_argumentos()

    # --- 2. Configuración del Logging ---
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Limpiar handlers existentes para evitar duplicados
    if logger.hasHandlers():
        logger.handlers.clear()

    # Handler para la consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para el archivo (si está activado)
    full_log_path = None
    if args.log_file:
        logs_dir = "logs"
        os.makedirs(logs_dir, exist_ok=True)
        log_filename = f"simulacion_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        full_log_path = os.path.join(logs_dir, log_filename)
        try:
            file_handler = logging.FileHandler(full_log_path, 'w', 'utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except IOError as e:
            logging.error(f"No se pudo abrir el archivo de log {full_log_path}: {e}")

    # --- 3. Ejecución de la Simulación ---
    try:
        logging.info("Simulación iniciada con argumentos: %s", args)
        
        # --- SELECCIONE LA DEMOSTRACIÓN A EJECUTAR ---
        # Descomente la función que desea probar.

        # Demuestra aprendizaje Hebbiano y poda sináptica (simulación original).
        # run_simulation(verbose_general=args.verbose)

        # Demuestra memoria a corto plazo con una neurona recurrente.
        # demostrar_recurrencia()

        # Demuestra la creación dinámica de neuronas conceptuales (autoorganización).
        # red = RedDinamica()
        # # El gestor de plasticidad se crea automáticamente dentro de RedDinamica si está activado.
        # demostrar_autoorganizacion(red, visualizar=args.visualizar)

        # Demuestra la formación de múltiples conceptos en una red más compleja.
        # red = RedDinamica()
        # demostrar_red_compleja(red, visualizar=args.visualizar)

        # Demuestra el aprendizaje jerárquico G1->G2->G3
        red = RedDinamica()
        demostrar_aprendizaje_jerarquico(red, visualizar=args.visualizar)

    except Exception as e:
        logging.critical("Se ha producido una excepción no controlada en el nivel superior.", exc_info=True)
    finally:
        logging.info("--- Fin de la simulación ---")
        if full_log_path:
            print(f"INFO: Se ha completado el registro en {full_log_path}")
        logging.shutdown()
