# main_parts/g2_testing_phase.py
import logging
from configuracion import parametros_simulacion as ps

def run_g2_testing_phase(
    red_neuronal,
    N_G2_PRE_A_ID, N_G2_PRE_B_ID,
    N_G2_DETECTOR_AB_ID,
    ids_neuronas_g2_detectoras, # Lista que contiene N_G2_DETECTOR_AB_ID
    ids_neuronas_todas, # Para resetear todas las neuronas de la red
    tiempo_simulacion_global,
    ejecutar_prueba_selectividad_secuencia # Función de lógica de prueba
):
    """
    Ejecuta la fase de pruebas para el detector del Grupo 2 (N_G2_DetectorAB_ID).
    Prueba la respuesta a su secuencia objetivo (B->A) y a secuencias no objetivo.
    """
    logging.info("\n--- INICIO FASE DE PRUEBAS GRUPO 2 ---")

    params_prueba_dict = {
        'DELTA_UMBRAL_PRUEBA_BASE': ps.DELTA_UMBRAL_PRUEBA_BASE,
        'AJUSTE_SELECTIVIDAD_PRUEBA': ps.AJUSTE_SELECTIVIDAD_PRUEBA,
        'PROBABILIDAD_RUIDO_PRE': ps.PROBABILIDAD_RUIDO_PRE
    }

    # Definición de pruebas para el Grupo 2
    # Secuencia objetivo: A -> B
    # Secuencia no objetivo: B -> A
    pruebas_g2 = [
        {"nombre": "Prueba G2 Target (B->A)", "secuencia_ids": [N_G2_PRE_B_ID, N_G2_PRE_A_ID], "es_target": True},
        {"nombre": "Prueba G2 Non-Target (A->B)", "secuencia_ids": [N_G2_PRE_A_ID, N_G2_PRE_B_ID], "es_target": False},
        # Podríamos añadir más secuencias no objetivo si tuviéramos más neuronas presinápticas en G2
    ]

    resultados_pruebas_g2_sin_ruido = {}
    resultados_pruebas_g2_con_ruido = {}

    # Umbrales para el detector del Grupo 2
    # Asumimos que ids_neuronas_g2_detectoras[0] es N_G2_DETECTOR_AB_ID
    potencial_reposo_g2_detector = red_neuronal.neuronas[N_G2_DETECTOR_AB_ID].potencial_reposo
    umbral_base_objetivo_g2 = potencial_reposo_g2_detector + \
                               params_prueba_dict['DELTA_UMBRAL_PRUEBA_BASE'] - \
                               params_prueba_dict['AJUSTE_SELECTIVIDAD_PRUEBA']
    umbral_base_no_objetivo_g2 = potencial_reposo_g2_detector + \
                                 params_prueba_dict['DELTA_UMBRAL_PRUEBA_BASE'] + \
                                 params_prueba_dict['AJUSTE_SELECTIVIDAD_PRUEBA']

    # --- PRUEBAS SIN RUIDO GRUPO 2 ---
    logging.info("\n--- Pruebas SIN RUIDO para Grupo 2 ---")
    for prueba_info in pruebas_g2:
        umbral_prueba_detector_g2 = umbral_base_objetivo_g2 if prueba_info["es_target"] else umbral_base_no_objetivo_g2

        disparo_detector_g2, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_G2_DETECTOR_AB_ID})",
            neurona_detector_id=N_G2_DETECTOR_AB_ID,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas, # Reseteamos todas para aislamiento
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA, # Usamos prueba corta para G2 por ahora
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_g2,
            introducir_ruido=False
        )
        resultados_pruebas_g2_sin_ruido[(N_G2_DETECTOR_AB_ID, prueba_info["nombre"])] = disparo_detector_g2
        tiempo_simulacion_global = tiempo_simulacion_global_temp

    logging.info("\n--- Resumen de Resultados de Pruebas SIN RUIDO (Grupo 2) ---")
    for nombre, resultado in resultados_pruebas_g2_sin_ruido.items():
        logging.info(f"{nombre}: Detector disparó -> {resultado}")
    logging.info(f"Fase de Pruebas SIN RUIDO (Grupo 2) completada. Tiempo de simulación global: {tiempo_simulacion_global}")

    # --- PRUEBAS CON RUIDO GRUPO 2 ---
    logging.info("\n--- Pruebas CON RUIDO para Grupo 2 ---")
    for prueba_info in pruebas_g2:
        umbral_prueba_detector_g2_ruido = umbral_base_objetivo_g2 if prueba_info["es_target"] else umbral_base_no_objetivo_g2

        disparo_detector_g2_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_G2_DETECTOR_AB_ID}, CON RUIDO)",
            neurona_detector_id=N_G2_DETECTOR_AB_ID,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA, 
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_g2_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_g2_con_ruido[(N_G2_DETECTOR_AB_ID, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_g2_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

    logging.info("\n--- Resumen de Resultados de Pruebas CON RUIDO (Grupo 2) ---")
    for nombre, resultado in resultados_pruebas_g2_con_ruido.items():
        logging.info(f"{nombre}: Detector disparó -> {resultado}")
    logging.info(f"Fase de Pruebas CON RUIDO (Grupo 2) completada. Tiempo de simulación global: {tiempo_simulacion_global}")

    logging.info(f"\nFase de Pruebas GRUPO 2 completada. Tiempo de simulación global: {tiempo_simulacion_global}")
    return tiempo_simulacion_global, resultados_pruebas_g2_sin_ruido, resultados_pruebas_g2_con_ruido
