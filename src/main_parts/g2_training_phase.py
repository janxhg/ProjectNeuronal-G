# main_parts/g2_training_phase.py
from configuracion import parametros_simulacion as ps
from src.escenarios.entrenamiento.logica_entrenamiento import entrenar_detector_secuencia

def run_g2_training_phase(red_neuronal,
                           N_G2_DETECTOR_AB_ID,
                           N_G2_PRE_A_ID, N_G2_PRE_B_ID,
                           historial_pesos_detectores,
                           tiempo_simulacion_global):
    """
    Ejecuta la fase de entrenamiento para el detector de secuencia del Grupo 2.
    La secuencia objetivo será PreB -> PreA -> DetectorAB.
    """
    print("\n Iniciando Fase de Entrenamiento para Grupo 2...")

    # Conexiones específicas para el detector del Grupo 2
    conexiones_a_registrar_pesos_g2 = [
        (N_G2_PRE_A_ID, N_G2_DETECTOR_AB_ID),
        (N_G2_PRE_B_ID, N_G2_DETECTOR_AB_ID)
    ]

    # Parámetros de entrenamiento (pueden ser los mismos o específicos para G2)
    params_entrenamiento_dict = {
        'TRAINING_THRESHOLD_OFFSET_BASE': ps.TRAINING_THRESHOLD_OFFSET_BASE,
        'DELTA_UMBRAL_BASE': ps.DELTA_UMBRAL_BASE
    }

    # Secuencia objetivo para el Grupo 2
    secuencia_objetivo_g2_ab = [N_G2_PRE_B_ID, N_G2_PRE_A_ID] # MODIFICADO para B->A
    print(f"\n--- Iniciando entrenamiento para {N_G2_DETECTOR_AB_ID} con secuencia [{', '.join(secuencia_objetivo_g2_ab)}] ---")
    
    # Asegurar que el diccionario para este detector exista en historial_pesos_detectores
    # y que las listas para cada conexión estén inicializadas.
    # La función entrenar_detector_secuencia espera que historial_pesos_ref 
    # sea un diccionario de la forma {(pre_id, post_id): lista_de_pesos}
    # para las conexiones específicas del detector actual.
    if N_G2_DETECTOR_AB_ID not in historial_pesos_detectores:
        historial_pesos_detectores[N_G2_DETECTOR_AB_ID] = {}
    
    # Este es el sub-diccionario que se pasará a entrenar_detector_secuencia
    historial_pesos_para_detector_g2_actual = historial_pesos_detectores[N_G2_DETECTOR_AB_ID]
    
    for conn_tuple in conexiones_a_registrar_pesos_g2:
        if conn_tuple not in historial_pesos_para_detector_g2_actual:
            historial_pesos_para_detector_g2_actual[conn_tuple] = []

    # Llamada a la lógica de entrenamiento genérica
    tiempo_simulacion_global = entrenar_detector_secuencia(
        red=red_neuronal,
        neurona_detector_id=N_G2_DETECTOR_AB_ID,
        neuronas_presinapticas_secuencia=secuencia_objetivo_g2_ab,
        num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_G2,
        pasos_por_epoca=ps.PASOS_ENTRENAMIENTO_G2, 
        dt_estimulo=ps.DT_ENTRENAMIENTO_ESTIMULO_G2,
        impulso_fuerte=ps.IMPULSO_FUERTE_G2,
        params_entrenamiento=params_entrenamiento_dict,
        conexiones_a_registrar=conexiones_a_registrar_pesos_g2, # Define qué conexiones monitorear
        historial_pesos_ref=historial_pesos_para_detector_g2_actual, # Pasa la referencia para almacenar historiales
        tiempo_simulacion_global_actual=tiempo_simulacion_global
    )
    
    # La modificación de historial_pesos_detectores[N_G2_DETECTOR_AB_ID] ocurre in-place
    # a través de historial_pesos_para_detector_g2_actual.
        
    print(f"Entrenamiento para {N_G2_DETECTOR_AB_ID} completado. Tiempo de simulación global: {tiempo_simulacion_global}")
    print(f"\nFase de Entrenamiento para Grupo 2 completada. Tiempo de simulación global: {tiempo_simulacion_global}")

    return tiempo_simulacion_global, historial_pesos_detectores
