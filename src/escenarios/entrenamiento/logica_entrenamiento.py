# Contendrá la lógica para las fases de entrenamiento

import numpy as np
# No es necesario importar RedBiologica o NeuronaBiologica aquí si se pasan como argumentos.
# Los parámetros de simulación se pasarán a través del argumento 'params_entrenamiento'
# o se importarán si son muchos y fijos para esta lógica.

def entrenar_detector_secuencia(
    red,
    neurona_detector_id,
    neuronas_presinapticas_secuencia,
    num_epocas,
    pasos_por_epoca,
    dt_estimulo,
    impulso_fuerte,
    params_entrenamiento, # dict: {'TRAINING_THRESHOLD_OFFSET_BASE': val, 'DELTA_UMBRAL_BASE': val}
    conexiones_a_registrar,
    tiempo_simulacion_global_actual,
    historial_pesos_ref=None
):
    """
    Entrena una neurona detectora para una secuencia específica de disparos presinápticos.
    """
    if red.verbose:
        print(f"--- INICIO FASE DE ENTRENAMIENTO para {neurona_detector_id} ---")

    neurona_detector = red.neuronas.get(neurona_detector_id)
    if not neurona_detector:
        print(f"Error: Neurona detectora '{neurona_detector_id}' no encontrada en la red.")
        return tiempo_simulacion_global_actual

    potencial_reposo_detector = neurona_detector.potencial_reposo
    training_offset = params_entrenamiento.get('TRAINING_THRESHOLD_OFFSET_BASE', 1.5)
    delta_umbral = params_entrenamiento.get('DELTA_UMBRAL_BASE', 1.0)

    for epoca in range(num_epocas):
        if not neuronas_presinapticas_secuencia:
            largo_una_presentacion_secuencia = 1 # Evita división por cero, aunque no se usará
        elif dt_estimulo == 0:
            largo_una_presentacion_secuencia = 1
        else:
            largo_una_presentacion_secuencia = 1 + (len(neuronas_presinapticas_secuencia) - 1) * dt_estimulo
        if red.verbose:
            print(f"\n  Época de Entrenamiento: {epoca + 1}/{num_epocas} para {neurona_detector_id}")

        umbral_objetivo_entrenamiento = potencial_reposo_detector + training_offset - delta_umbral
        neurona_detector.umbral_disparo = umbral_objetivo_entrenamiento
        neurona_detector.potencial_membrana = neurona_detector.potencial_reposo

        if red.verbose:
            print(f"      Ajustando umbral de {neurona_detector_id} a: {umbral_objetivo_entrenamiento:.2f} mV")

        for t_epoca in range(1, pasos_por_epoca + 1):
            tiempo_simulacion_global_actual += 1
            impulsos_externos_paso = {}

            if neuronas_presinapticas_secuencia:
                paso_actual_en_presentacion = ((t_epoca - 1) % largo_una_presentacion_secuencia) + 1
                
                for i, pre_id in enumerate(neuronas_presinapticas_secuencia):
                    tiempo_disparo_objetivo = 1 + i * dt_estimulo
                    if dt_estimulo == 0:
                        tiempo_disparo_objetivo = 1

                    if paso_actual_en_presentacion == tiempo_disparo_objetivo:
                        impulsos_externos_paso[pre_id] = impulso_fuerte
            
            if red.verbose and impulsos_externos_paso:
                print(f"    t_glob={tiempo_simulacion_global_actual}, t_ep={t_epoca}: Aplicando impulsos a {list(impulsos_externos_paso.keys())}")

            red.actualizar_estado_red(tiempo_simulacion_global_actual, dt=1, impulsos_externos=impulsos_externos_paso)

        if historial_pesos_ref is not None:
            if red.verbose_entrenamiento:
                print(f"    Fin de Época {epoca + 1}. Registrando pesos para {neurona_detector_id}:")
            for pre_id_reg, post_id_reg in conexiones_a_registrar:
                if (pre_id_reg, post_id_reg) in historial_pesos_ref:
                    peso = red.obtener_peso_sinaptico(pre_id_reg, post_id_reg)
                    if peso is not None:
                        historial_pesos_ref[(pre_id_reg, post_id_reg)].append(peso)
                        if red.verbose_entrenamiento:
                            print(f"      REG PESO: {pre_id_reg}->{post_id_reg}: {peso:.3f}")

    if red.verbose:
        print(f"--- FIN FASE DE ENTRENAMIENTO para {neurona_detector_id} ---")
    return tiempo_simulacion_global_actual
