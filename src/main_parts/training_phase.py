# main_parts/training_phase.py
import logging
from configuracion import parametros_simulacion as ps
from src.escenarios.entrenamiento.logica_entrenamiento import entrenar_detector_secuencia

def run_training_phase(red_neuronal, 
                       N_DETECTOR_ID, N_DETECTOR_ID_2, N_DETECTOR_ID_3, 
                       N_DETECTOR_ID_4, N_DETECTOR_ID_5, N_DETECTOR_ID_6, # Nuevos IDs añadidos
                       N_PRE1_ID, N_PRE2_ID, N_PRE3_ID,
                       historial_pesos_detectores, 
                       tiempo_simulacion_global):
    """
    Ejecuta la fase de entrenamiento para los detectores de secuencia.
    """
    logging.info("\n Iniciando Fase de Entrenamiento...")
    
    conexiones_a_registrar_pesos = [
        (N_PRE1_ID, N_DETECTOR_ID), 
        (N_PRE2_ID, N_DETECTOR_ID), 
        (N_PRE3_ID, N_DETECTOR_ID),
        (N_PRE1_ID, N_DETECTOR_ID_2), 
        (N_PRE2_ID, N_DETECTOR_ID_2), 
        (N_PRE3_ID, N_DETECTOR_ID_2),
        (N_PRE1_ID, N_DETECTOR_ID_3),
        (N_PRE2_ID, N_DETECTOR_ID_3),
        (N_PRE3_ID, N_DETECTOR_ID_3),
        (N_PRE1_ID, N_DETECTOR_ID_4),
        (N_PRE2_ID, N_DETECTOR_ID_4),
        (N_PRE3_ID, N_DETECTOR_ID_4),
        (N_PRE1_ID, N_DETECTOR_ID_5),
        (N_PRE2_ID, N_DETECTOR_ID_5),
        (N_PRE3_ID, N_DETECTOR_ID_5),
        (N_PRE1_ID, N_DETECTOR_ID_6),
        (N_PRE2_ID, N_DETECTOR_ID_6),
        (N_PRE3_ID, N_DETECTOR_ID_6)
    ]

    params_entrenamiento_dict = {
        'TRAINING_THRESHOLD_OFFSET_BASE': ps.TRAINING_THRESHOLD_OFFSET_BASE,
        'DELTA_UMBRAL_BASE': ps.DELTA_UMBRAL_BASE
    }

    # Fase de Entrenamiento para N_Detector_Secuencia123
    secuencia_objetivo_123 = [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID]
    logging.info(f"\n--- Iniciando entrenamiento para {N_DETECTOR_ID} ---")
    conexiones_detector123 = [conn for conn in conexiones_a_registrar_pesos if conn[1] == N_DETECTOR_ID]
    historial_detector123_temp = {conn: [] for conn in conexiones_detector123}
    
    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal, 
        neurona_detector_id=N_DETECTOR_ID,
        neuronas_presinapticas_secuencia=secuencia_objetivo_123,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_BASE, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO,
        impulso_fuerte=ps.IMPULSO_FUERTE_BASE,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_detector123,
        historial_pesos_ref=historial_detector123_temp,
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    historial_pesos_detectores[N_DETECTOR_ID] = historial_detector123_temp
    logging.info(f"Entrenamiento para {N_DETECTOR_ID} completado. Tiempo de simulación global: {tiempo_simulacion_global}")

    # Fase de Entrenamiento para N_Detector_Secuencia321
    secuencia_objetivo_321 = [N_PRE3_ID, N_PRE2_ID, N_PRE1_ID]
    logging.info(f"\n--- Iniciando entrenamiento para {N_DETECTOR_ID_2} ---")
    conexiones_detector321 = [conn for conn in conexiones_a_registrar_pesos if conn[1] == N_DETECTOR_ID_2]
    historial_detector321_temp = {conn: [] for conn in conexiones_detector321}

    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal, 
        neurona_detector_id=N_DETECTOR_ID_2,
        neuronas_presinapticas_secuencia=secuencia_objetivo_321,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_BASE, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO,
        impulso_fuerte=ps.IMPULSO_FUERTE_BASE,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_detector321,
        historial_pesos_ref=historial_detector321_temp,
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    historial_pesos_detectores[N_DETECTOR_ID_2] = historial_detector321_temp
    logging.info(f"Entrenamiento para {N_DETECTOR_ID_2} completado. Tiempo de simulación global: {tiempo_simulacion_global}")

    # Fase de Entrenamiento para N_Detector_Secuencia132 (N_DETECTOR_ID_3)
    secuencia_objetivo_132 = [N_PRE1_ID, N_PRE3_ID, N_PRE2_ID] # Secuencia 1->3->2
    logging.info(f"\n--- Iniciando entrenamiento para {N_DETECTOR_ID_3} ---")
    conexiones_detector132 = [conn for conn in conexiones_a_registrar_pesos if conn[1] == N_DETECTOR_ID_3]
    historial_detector132_temp = {conn: [] for conn in conexiones_detector132}

    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal, 
        neurona_detector_id=N_DETECTOR_ID_3,
        neuronas_presinapticas_secuencia=secuencia_objetivo_132,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_BASE, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO,
        impulso_fuerte=ps.IMPULSO_FUERTE_BASE,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_detector132,
        historial_pesos_ref=historial_detector132_temp,
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    historial_pesos_detectores[N_DETECTOR_ID_3] = historial_detector132_temp
    logging.info(f"Entrenamiento para {N_DETECTOR_ID_3} completado. Tiempo de simulación global: {tiempo_simulacion_global}")

    # Fase de Entrenamiento para N_Detector_Secuencia213 (N_DETECTOR_ID_4)
    secuencia_objetivo_213 = [N_PRE2_ID, N_PRE1_ID, N_PRE3_ID] # Secuencia 2->1->3
    logging.info(f"\n--- Iniciando entrenamiento para {N_DETECTOR_ID_4} ---")
    conexiones_detector213 = [conn for conn in conexiones_a_registrar_pesos if conn[1] == N_DETECTOR_ID_4]
    historial_detector213_temp = {conn: [] for conn in conexiones_detector213}
    
    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal, 
        neurona_detector_id=N_DETECTOR_ID_4,
        neuronas_presinapticas_secuencia=secuencia_objetivo_213,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_BASE, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO,
        impulso_fuerte=ps.IMPULSO_FUERTE_BASE,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_detector213,
        historial_pesos_ref=historial_detector213_temp,
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    historial_pesos_detectores[N_DETECTOR_ID_4] = historial_detector213_temp
    logging.info(f"Entrenamiento para {N_DETECTOR_ID_4} completado. Tiempo de simulación global: {tiempo_simulacion_global}")

    # Fase de Entrenamiento para N_Detector_Secuencia231 (N_DETECTOR_ID_5)
    secuencia_objetivo_231 = [N_PRE2_ID, N_PRE3_ID, N_PRE1_ID] # Secuencia 2->3->1
    logging.info(f"\n--- Iniciando entrenamiento para {N_DETECTOR_ID_5} ---")
    conexiones_detector231 = [conn for conn in conexiones_a_registrar_pesos if conn[1] == N_DETECTOR_ID_5]
    historial_detector231_temp = {conn: [] for conn in conexiones_detector231}
    
    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal, 
        neurona_detector_id=N_DETECTOR_ID_5,
        neuronas_presinapticas_secuencia=secuencia_objetivo_231,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_BASE, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO,
        impulso_fuerte=ps.IMPULSO_FUERTE_BASE,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_detector231,
        historial_pesos_ref=historial_detector231_temp,
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    historial_pesos_detectores[N_DETECTOR_ID_5] = historial_detector231_temp
    logging.info(f"Entrenamiento para {N_DETECTOR_ID_5} completado. Tiempo de simulación global: {tiempo_simulacion_global}")

    # Fase de Entrenamiento para N_Detector_Secuencia312 (N_DETECTOR_ID_6)
    secuencia_objetivo_312 = [N_PRE3_ID, N_PRE1_ID, N_PRE2_ID] # Secuencia 3->1->2
    logging.info(f"\n--- Iniciando entrenamiento para {N_DETECTOR_ID_6} ---")
    conexiones_detector312 = [conn for conn in conexiones_a_registrar_pesos if conn[1] == N_DETECTOR_ID_6]
    historial_detector312_temp = {conn: [] for conn in conexiones_detector312}
    
    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal, 
        neurona_detector_id=N_DETECTOR_ID_6,
        neuronas_presinapticas_secuencia=secuencia_objetivo_312,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_BASE, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO,
        impulso_fuerte=ps.IMPULSO_FUERTE_BASE,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_detector312,
        historial_pesos_ref=historial_detector312_temp,
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    historial_pesos_detectores[N_DETECTOR_ID_6] = historial_detector312_temp
    logging.info(f"Entrenamiento para {N_DETECTOR_ID_6} completado. Tiempo de simulación global: {tiempo_simulacion_global}")

    logging.info(f"\nFase de Entrenamiento GENERAL completada. Tiempo de simulación global: {tiempo_simulacion_global}")
    logging.debug("--- A punto de retornar desde run_training_phase. ---")
    return tiempo_simulacion_global, historial_pesos_detectores
