# Contendrá la lógica para las fases de prueba

import numpy as np

def reset_neurona_para_prueba(neurona):
    """Resetea el estado de una neurona para una nueva prueba."""
    if neurona:
        neurona.potencial_membrana = neurona.potencial_reposo
        neurona.ultima_vez_disparo = -np.inf  # Resetear último disparo
        neurona.tiempo_en_periodo_refractario = 0
    else:
        print("Advertencia: Se intentó resetear una neurona None.")

def ejecutar_prueba_selectividad_secuencia(
    red,
    nombre_prueba,
    neurona_detector_id,
    neuronas_estimulo_secuencia, 
    ids_neuronas_a_resetear,    
    pasos_simulacion_prueba,
    dt_estimulo_prueba,
    impulso_estimulo,
    params_prueba, 
    tiempo_simulacion_global_actual,
    umbral_detector_especifico=None, 
    introducir_ruido=False 
):
    """
    Ejecuta una prueba de selectividad para una neurona detectora ante una secuencia específica.

    Args:
        red (RedBiologica): La instancia de la red.
        nombre_prueba (str): Nombre descriptivo de la prueba.
        neurona_detector_id (str): ID de la neurona detectora.
        neuronas_estimulo_secuencia (list): IDs de neuronas presinápticas a estimular, en orden.
        ids_neuronas_a_resetear (list): IDs de todas las neuronas a resetear antes de la prueba.
        pasos_simulacion_prueba (int): Duración de la prueba en pasos de simulación.
        dt_estimulo_prueba (int): Intervalo entre estímulos en la secuencia.
        impulso_estimulo (float): Magnitud del impulso para las neuronas de estímulo.
        params_prueba (dict): Diccionario con parámetros de prueba.
        tiempo_simulacion_global_actual (int): Tiempo de simulación global actual.
        umbral_detector_especifico (float, optional): Umbral específico para el detector.
        introducir_ruido (bool): Si es True, se introduce ruido.

    Returns:
        tuple: (bool, int) - Si la neurona detectora disparó, y tiempo global actualizado.
    """
    print(f"\n  {nombre_prueba}")

    neurona_detector = red.neuronas.get(neurona_detector_id)
    if not neurona_detector:
        print(f"Error en prueba: Neurona detectora '{neurona_detector_id}' no encontrada.")
        return False, tiempo_simulacion_global_actual

    for nid in ids_neuronas_a_resetear:
        n_reset = red.neuronas.get(nid)
        if n_reset:
            reset_neurona_para_prueba(n_reset)
        else:
            print(f"Advertencia: Neurona con ID '{nid}' no encontrada para resetear.")

    if umbral_detector_especifico is not None:
        neurona_detector.umbral_disparo = umbral_detector_especifico
    else:
        delta_umbral_base = params_prueba.get('DELTA_UMBRAL_PRUEBA_BASE', 2.20)
        neurona_detector.umbral_disparo = neurona_detector.potencial_reposo + delta_umbral_base

    if red.verbose:
        print(f"      Umbral de {neurona_detector_id} para prueba: {neurona_detector.umbral_disparo:.2f} mV")

    detector_disparo = False
    probabilidad_ruido_pre = params_prueba.get('PROBABILIDAD_RUIDO_PRE', 0.0) if introducir_ruido else 0.0

    for t_p in range(1, pasos_simulacion_prueba + 1):
        tiempo_simulacion_global_actual += 1
        impulsos_externos_paso = {}

        for i, pre_id_estimulo in enumerate(neuronas_estimulo_secuencia):
            tiempo_disparo_programado = 1 + i * dt_estimulo_prueba
            if t_p == tiempo_disparo_programado:
                impulsos_externos_paso[pre_id_estimulo] = impulso_estimulo
        
        if introducir_ruido and probabilidad_ruido_pre > 0:
            # Aplicar ruido a las neuronas que podrían ser estimuladas (las de la secuencia actual como proxy)
            for pre_id_ruido in neuronas_estimulo_secuencia: 
                if np.random.rand() < probabilidad_ruido_pre:
                    impulsos_externos_paso[pre_id_ruido] = impulsos_externos_paso.get(pre_id_ruido, 0) + impulso_estimulo
                    if red.verbose:
                         print(f"RUIDO: Impulso de ruido en '{pre_id_ruido}' en t_glob={tiempo_simulacion_global_actual}")

        if impulsos_externos_paso and red.verbose:
            # Este print es solo para confirmar que la lógica de pruebas preparó los impulsos
            for id_n, peso_imp in impulsos_externos_paso.items():
                print(f"PRUEBA (Preparado): Impulso externo de {peso_imp:.2f} para neurona '{id_n}' en t_glob={tiempo_simulacion_global_actual}, t_p={t_p}")
        
        disparos = red.actualizar_estado_red(
            tiempo_actual=tiempo_simulacion_global_actual,
            dt=1,
            aplicar_stdp_global=False, 
            neurona_objetivo_stdp=None,
            impulsos_externos=impulsos_externos_paso # <--- PASAR LOS IMPULSOS AQUÍ
        )

        if neurona_detector_id in disparos:
            detector_disparo = True
        
        if red.verbose:
            print(f"    t_glob={tiempo_simulacion_global_actual}, t_p={t_p}: {neurona_detector_id} Pot: {neurona_detector.potencial_membrana:.2f}, Disparos: {disparos}")
            if detector_disparo and neurona_detector_id in disparos: # Loguear solo la primera vez que dispara en la prueba
                 print(f"    ¡¡¡ {neurona_detector_id} DISPARÓ en t_p={t_p} !!!")

    print(f"  Resultado {nombre_prueba}: {neurona_detector_id} disparó -> {detector_disparo}")
    return detector_disparo, tiempo_simulacion_global_actual
