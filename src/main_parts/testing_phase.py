import logging
from configuracion import parametros_simulacion as ps

def run_testing_phase(
    red_neuronal,
    N_PRE1_ID, N_PRE2_ID, N_PRE3_ID,
    N_DETECTOR_ID, N_DETECTOR_ID_2, N_DETECTOR_ID_3, 
    N_DETECTOR_ID_4, N_DETECTOR_ID_5, N_DETECTOR_ID_6, # Nuevos IDs añadidos
    ids_neuronas_detectoras,
    ids_neuronas_todas,
    tiempo_simulacion_global,
    ejecutar_prueba_selectividad_secuencia
):
    """
    Ejecuta la fase de pruebas, incluyendo pruebas sin y con ruido.

    Retorna el tiempo de simulación global actualizado y los resultados de las pruebas.
    """
    params_prueba_dict = {
        'DELTA_UMBRAL_PRUEBA_BASE': ps.DELTA_UMBRAL_PRUEBA_BASE,
        'AJUSTE_SELECTIVIDAD_PRUEBA': ps.AJUSTE_SELECTIVIDAD_PRUEBA,
        'PROBABILIDAD_RUIDO_PRE': ps.PROBABILIDAD_RUIDO_PRE
    }

    pruebas = [
        {"nombre": "Prueba A (Target Sec123): 1->2->3", "secuencia_ids": [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID], 
         "target_para_detector123": True,  "target_para_detector321": False, "target_para_detector132": False,
         "target_para_detector213": False, "target_para_detector231": False, "target_para_detector312": False},

        {"nombre": "Prueba B (Target Sec321): 3->2->1", "secuencia_ids": [N_PRE3_ID, N_PRE2_ID, N_PRE1_ID], 
         "target_para_detector123": False, "target_para_detector321": True,  "target_para_detector132": False,
         "target_para_detector213": False, "target_para_detector231": False, "target_para_detector312": False},

        {"nombre": "Prueba C (Target Sec132): 1->3->2", "secuencia_ids": [N_PRE1_ID, N_PRE3_ID, N_PRE2_ID], 
         "target_para_detector123": False, "target_para_detector321": False, "target_para_detector132": True,
         "target_para_detector213": False, "target_para_detector231": False, "target_para_detector312": False},

        {"nombre": "Prueba D (Target Sec213): 2->1->3", "secuencia_ids": [N_PRE2_ID, N_PRE1_ID, N_PRE3_ID], 
         "target_para_detector123": False, "target_para_detector321": False, "target_para_detector132": False,
         "target_para_detector213": True,  "target_para_detector231": False, "target_para_detector312": False},

        {"nombre": "Prueba E (Target Sec231): 2->3->1", "secuencia_ids": [N_PRE2_ID, N_PRE3_ID, N_PRE1_ID], 
         "target_para_detector123": False, "target_para_detector321": False, "target_para_detector132": False,
         "target_para_detector213": False, "target_para_detector231": True,  "target_para_detector312": False},

        {"nombre": "Prueba F (Target Sec312): 3->1->2", "secuencia_ids": [N_PRE3_ID, N_PRE1_ID, N_PRE2_ID], 
         "target_para_detector123": False, "target_para_detector321": False, "target_para_detector132": False,
         "target_para_detector213": False, "target_para_detector231": False, "target_para_detector312": True},
    ]

    # --- FASE DE PRUEBAS SIN RUIDO ---
    logging.info("\n--- INICIO FASE DE PRUEBAS SIN RUIDO ---")
    resultados_pruebas_sin_ruido = {}

    potencial_reposo_comun = red_neuronal.neuronas[ids_neuronas_detectoras[0]].potencial_reposo 
    umbral_base_objetivo = potencial_reposo_comun + \
                           params_prueba_dict['DELTA_UMBRAL_PRUEBA_BASE'] - \
                           params_prueba_dict['AJUSTE_SELECTIVIDAD_PRUEBA']
    umbral_base_no_objetivo = potencial_reposo_comun + \
                              params_prueba_dict['DELTA_UMBRAL_PRUEBA_BASE'] + \
                              params_prueba_dict['AJUSTE_SELECTIVIDAD_PRUEBA']

    for prueba_info in pruebas:
        es_target_para_123 = prueba_info["target_para_detector123"]
        umbral_prueba_detector_123 = umbral_base_objetivo if es_target_para_123 else umbral_base_no_objetivo

        es_target_para_321 = prueba_info["target_para_detector321"]
        umbral_prueba_detector_321 = umbral_base_objetivo if es_target_para_321 else umbral_base_no_objetivo

        es_target_para_132 = prueba_info["target_para_detector132"]
        umbral_prueba_detector_132 = umbral_base_objetivo if es_target_para_132 else umbral_base_no_objetivo

        disparo_detector_123, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID})",
            neurona_detector_id=N_DETECTOR_ID,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_123,
            introducir_ruido=False
        )
        resultados_pruebas_sin_ruido[(N_DETECTOR_ID, prueba_info["nombre"])] = disparo_detector_123
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        disparo_detector_321, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_2})",
            neurona_detector_id=N_DETECTOR_ID_2,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA, 
            dt_estimulo_prueba=ps.DT_PRUEBA, 
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_321,
            introducir_ruido=False
        )
        resultados_pruebas_sin_ruido[(N_DETECTOR_ID_2, prueba_info["nombre"])] = disparo_detector_321
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        disparo_detector_132, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_3})",
            neurona_detector_id=N_DETECTOR_ID_3,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_132,
            introducir_ruido=False
        )
        resultados_pruebas_sin_ruido[(N_DETECTOR_ID_3, prueba_info["nombre"])] = disparo_detector_132
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        # Pruebas para N_DETECTOR_ID_4 (Secuencia 213)
        es_target_para_213 = prueba_info["target_para_detector213"]
        umbral_prueba_detector_213 = umbral_base_objetivo if es_target_para_213 else umbral_base_no_objetivo
        disparo_detector_213, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_4})",
            neurona_detector_id=N_DETECTOR_ID_4,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_213,
            introducir_ruido=False
        )
        resultados_pruebas_sin_ruido[(N_DETECTOR_ID_4, prueba_info["nombre"])] = disparo_detector_213
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        # Pruebas para N_DETECTOR_ID_5 (Secuencia 231)
        es_target_para_231 = prueba_info["target_para_detector231"]
        umbral_prueba_detector_231 = umbral_base_objetivo if es_target_para_231 else umbral_base_no_objetivo
        disparo_detector_231, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_5})",
            neurona_detector_id=N_DETECTOR_ID_5,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_231,
            introducir_ruido=False
        )
        resultados_pruebas_sin_ruido[(N_DETECTOR_ID_5, prueba_info["nombre"])] = disparo_detector_231
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        # Pruebas para N_DETECTOR_ID_6 (Secuencia 312)
        es_target_para_312 = prueba_info["target_para_detector312"]
        umbral_prueba_detector_312 = umbral_base_objetivo if es_target_para_312 else umbral_base_no_objetivo
        disparo_detector_312, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_6})",
            neurona_detector_id=N_DETECTOR_ID_6,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_prueba_detector_312,
            introducir_ruido=False
        )
        resultados_pruebas_sin_ruido[(N_DETECTOR_ID_6, prueba_info["nombre"])] = disparo_detector_312
        tiempo_simulacion_global = tiempo_simulacion_global_temp

    logging.info("\n--- Resumen de Resultados de Pruebas SIN RUIDO ---")
    for nombre, resultado in resultados_pruebas_sin_ruido.items():
        logging.info(f"{nombre}: Detector disparó -> {resultado}")
    logging.info(f"Fase de Pruebas SIN RUIDO completada. Tiempo de simulación global: {tiempo_simulacion_global}")

    # --- Fase de Prueba CON RUIDO ---
    logging.info("\n Iniciando Fase de Prueba CON RUIDO...")
    resultados_pruebas_con_ruido = {}
    
    for prueba_info in pruebas:
        es_target_para_123_ruido = prueba_info["target_para_detector123"]
        umbral_detector_123_ruido = umbral_base_objetivo if es_target_para_123_ruido else umbral_base_no_objetivo

        es_target_para_321_ruido = prueba_info["target_para_detector321"]
        umbral_detector_321_ruido = umbral_base_objetivo if es_target_para_321_ruido else umbral_base_no_objetivo

        es_target_para_132_ruido = prueba_info["target_para_detector132"]
        umbral_detector_132_ruido = umbral_base_objetivo if es_target_para_132_ruido else umbral_base_no_objetivo

        disparo_detector_123_con_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID}, CON RUIDO)",
            neurona_detector_id=N_DETECTOR_ID,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict, 
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_detector_123_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_con_ruido[(N_DETECTOR_ID, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_123_con_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        disparo_detector_321_con_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_2}, CON RUIDO)",
            neurona_detector_id=N_DETECTOR_ID_2,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict, 
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_detector_321_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_con_ruido[(N_DETECTOR_ID_2, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_321_con_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        disparo_detector_132_con_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_3}, CON RUIDO)",
            neurona_detector_id=N_DETECTOR_ID_3,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict, 
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_detector_132_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_con_ruido[(N_DETECTOR_ID_3, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_132_con_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        # Pruebas CON RUIDO para N_DETECTOR_ID_4 (Secuencia 213)
        es_target_para_213_ruido = prueba_info["target_para_detector213"]
        umbral_detector_213_ruido = umbral_base_objetivo if es_target_para_213_ruido else umbral_base_no_objetivo
        disparo_detector_213_con_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_4}, CON RUIDO)",
            neurona_detector_id=N_DETECTOR_ID_4,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_detector_213_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_con_ruido[(N_DETECTOR_ID_4, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_213_con_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        # Pruebas CON RUIDO para N_DETECTOR_ID_5 (Secuencia 231)
        es_target_para_231_ruido = prueba_info["target_para_detector231"]
        umbral_detector_231_ruido = umbral_base_objetivo if es_target_para_231_ruido else umbral_base_no_objetivo
        disparo_detector_231_con_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_5}, CON RUIDO)",
            neurona_detector_id=N_DETECTOR_ID_5,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_detector_231_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_con_ruido[(N_DETECTOR_ID_5, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_231_con_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

        # Pruebas CON RUIDO para N_DETECTOR_ID_6 (Secuencia 312)
        es_target_para_312_ruido = prueba_info["target_para_detector312"]
        umbral_detector_312_ruido = umbral_base_objetivo if es_target_para_312_ruido else umbral_base_no_objetivo
        disparo_detector_312_con_ruido, tiempo_simulacion_global_temp = ejecutar_prueba_selectividad_secuencia(
            red=red_neuronal,
            nombre_prueba=f"{prueba_info['nombre']} (Detector: {N_DETECTOR_ID_6}, CON RUIDO)",
            neurona_detector_id=N_DETECTOR_ID_6,
            neuronas_estimulo_secuencia=prueba_info["secuencia_ids"],
            ids_neuronas_a_resetear=ids_neuronas_todas,
            pasos_simulacion_prueba=ps.PASOS_PRUEBA_LARGA,
            dt_estimulo_prueba=ps.DT_PRUEBA,
            impulso_estimulo=ps.IMPULSO_MEDIO_PRUEBA_BASE,
            params_prueba=params_prueba_dict,
            tiempo_simulacion_global_actual=tiempo_simulacion_global,
            umbral_detector_especifico=umbral_detector_312_ruido,
            introducir_ruido=True
        )
        resultados_pruebas_con_ruido[(N_DETECTOR_ID_6, f"{prueba_info['nombre']} (CON RUIDO)")] = disparo_detector_312_con_ruido
        tiempo_simulacion_global = tiempo_simulacion_global_temp

    logging.info("\n--- Resumen de Resultados de Pruebas CON RUIDO ---")
    for nombre, resultado in resultados_pruebas_con_ruido.items():
        logging.info(f"{nombre}: Detector disparó -> {resultado}")
    logging.info(f"Fase de Pruebas CON RUIDO completada. Tiempo de simulación global: {tiempo_simulacion_global}")

    logging.info("--- FIN FASE DE PRUEBAS GRUPO 1 ---")
    return tiempo_simulacion_global, resultados_pruebas_sin_ruido, resultados_pruebas_con_ruido
