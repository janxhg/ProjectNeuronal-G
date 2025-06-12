import numpy as np
from configuracion import parametros_simulacion as ps

def run_inhibition_test_scenario(
    red_neuronal,
    N_PRE1_ID, N_PRE2_ID, N_PRE3_ID,
    N_DETECTOR_ID,
    N_INHIB1_ID,
    tiempo_simulacion_global # Pasado para consistencia, pero la prueba usa una copia local para su tiempo.
):
    """
    Ejecuta el escenario de prueba de inhibición.
    Prueba el efecto de N_INHIB1_ID sobre N_DETECTOR_ID.
    """
    print("\n\n--- Iniciando Escenario de Prueba de Inhibición para N_Inhib1 sobre N_Detector_Secuencia123 ---")
    
    # Parámetros para la prueba de inhibición
    secuencia_objetivo_detector123 = [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID]
    impulso_prueba_inhibicion = ps.IMPULSO_MEDIO_PRUEBA_BASE # Usar un impulso estándar
    dt_estimulo_prueba_inhibicion = ps.DT_PRUEBA
    pasos_prueba_inhibicion = ps.PASOS_PRUEBA_LARGA 

    # IDs a resetear para esta prueba específica
    ids_neuronas_prueba_inhibicion = [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID, N_DETECTOR_ID, N_INHIB1_ID]

    # 1. Prueba de Control: Excitación sin inhibición activa
    print("\n  Prueba de Control: Estimulando N_Detector_Secuencia123 con 1->2->3 (sin N_Inhib1 activa)")
    # Resetear neuronas
    for neurona_id_reset in ids_neuronas_prueba_inhibicion:
        if neurona_id_reset in red_neuronal.neuronas:
            red_neuronal.neuronas[neurona_id_reset].potencial_membrana = red_neuronal.neuronas[neurona_id_reset].potencial_reposo
            red_neuronal.neuronas[neurona_id_reset].ultima_vez_disparo = -np.inf
            red_neuronal.neuronas[neurona_id_reset].historia_disparos = [] # Limpiar historial de disparos también

    disparos_control = []
    max_potencial_control = red_neuronal.neuronas[N_DETECTOR_ID].potencial_reposo
    tiempo_simulacion_global_inhib_test = tiempo_simulacion_global # Copiar para no afectar el global principal aún

    for i, id_pre_estimulo in enumerate(secuencia_objetivo_detector123):
        tiempo_simulacion_global_inhib_test += dt_estimulo_prueba_inhibicion
        impulsos_externos_paso = {id_pre_estimulo: impulso_prueba_inhibicion}
        disparos_paso = red_neuronal.actualizar_estado_red(
            tiempo_actual=tiempo_simulacion_global_inhib_test,
            dt=1, # Asumimos dt=1 para estos pasos discretos
            impulsos_externos=impulsos_externos_paso,
            aplicar_stdp_global=False # No queremos STDP durante esta prueba específica
        )
        if N_DETECTOR_ID in disparos_paso:
            disparos_control.append(True)
        if red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana > max_potencial_control:
            max_potencial_control = red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana
    
    # Simular unos pasos más para decaimiento o disparo tardío
    for _ in range(pasos_prueba_inhibicion - len(secuencia_objetivo_detector123)):
        tiempo_simulacion_global_inhib_test += 1
        disparos_paso = red_neuronal.actualizar_estado_red(tiempo_simulacion_global_inhib_test, dt=1, aplicar_stdp_global=False)
        if N_DETECTOR_ID in disparos_paso and not any(disparos_control): # Solo registrar el primer disparo
             disparos_control.append(True)
        if red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana > max_potencial_control:
            max_potencial_control = red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana

    disparo_detector_control = any(disparos_control)
    print(f"    Resultado Control: N_Detector_Secuencia123 disparó -> {disparo_detector_control}. Potencial Máx: {max_potencial_control:.3f} mV")

    # 2. Prueba de Inhibición: N_Inhib1 dispara justo antes de la secuencia excitatoria
    print("\n  Prueba de Inhibición: Estimulando N_Inhib1 y luego 1->2->3 para N_Detector_Secuencia123")
    # Resetear neuronas
    for neurona_id_reset in ids_neuronas_prueba_inhibicion:
        if neurona_id_reset in red_neuronal.neuronas:
            red_neuronal.neuronas[neurona_id_reset].potencial_membrana = red_neuronal.neuronas[neurona_id_reset].potencial_reposo
            red_neuronal.neuronas[neurona_id_reset].ultima_vez_disparo = -np.inf
            red_neuronal.neuronas[neurona_id_reset].historia_disparos = []

    disparos_inhibicion = []
    max_potencial_inhibicion = red_neuronal.neuronas[N_DETECTOR_ID].potencial_reposo
    tiempo_simulacion_global_inhib_test = tiempo_simulacion_global # Resetear tiempo de esta sub-prueba

    # Estimular N_Inhib1 primero
    tiempo_simulacion_global_inhib_test += 1
    impulso_para_inhib1 = ps.UMBRAL_DISPARO_BASE + 1.0
    impulsos_externos_paso_inhib = {N_INHIB1_ID: impulso_para_inhib1} 
    disparos_paso_inhib = red_neuronal.actualizar_estado_red(
        tiempo_actual=tiempo_simulacion_global_inhib_test,
        dt=1,
        impulsos_externos=impulsos_externos_paso_inhib,
        aplicar_stdp_global=False
    )
    if N_INHIB1_ID in disparos_paso_inhib:
        print(f"    INFO: N_Inhib1 disparó en t={tiempo_simulacion_global_inhib_test}")
    else:
        print(f"    ADVERTENCIA: N_Inhib1 NO disparó como se esperaba. Potencial N_Inhib1: {red_neuronal.neuronas[N_INHIB1_ID].potencial_membrana:.3f} / Umbral: {red_neuronal.neuronas[N_INHIB1_ID].umbral_disparo:.2f}")
    
    tiempo_simulacion_global_inhib_test += 1
    red_neuronal.actualizar_estado_red(tiempo_actual=tiempo_simulacion_global_inhib_test, dt=1, aplicar_stdp_global=False)
    print(f"    Potencial de N_Detector_Secuencia123 después de inhibición (t={tiempo_simulacion_global_inhib_test}): {red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana:.3f} mV")

    # Luego, estimular la secuencia excitatoria
    for i, id_pre_estimulo in enumerate(secuencia_objetivo_detector123):
        tiempo_simulacion_global_inhib_test += dt_estimulo_prueba_inhibicion
        impulsos_externos_paso = {id_pre_estimulo: impulso_prueba_inhibicion}
        disparos_paso = red_neuronal.actualizar_estado_red(
            tiempo_actual=tiempo_simulacion_global_inhib_test,
            dt=1,
            impulsos_externos=impulsos_externos_paso,
            aplicar_stdp_global=False
        )
        if N_DETECTOR_ID in disparos_paso:
            disparos_inhibicion.append(True)
        if red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana > max_potencial_inhibicion:
            max_potencial_inhibicion = red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana
            
    # Simular unos pasos más
    for _ in range(pasos_prueba_inhibicion - len(secuencia_objetivo_detector123)):
        tiempo_simulacion_global_inhib_test += 1
        disparos_paso = red_neuronal.actualizar_estado_red(tiempo_simulacion_global_inhib_test, dt=1, aplicar_stdp_global=False)
        if N_DETECTOR_ID in disparos_paso and not any(disparos_inhibicion):
             disparos_inhibicion.append(True)
        if red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana > max_potencial_inhibicion:
            max_potencial_inhibicion = red_neuronal.neuronas[N_DETECTOR_ID].potencial_membrana

    disparo_detector_inhibicion = any(disparos_inhibicion)
    print(f"    Resultado Inhibición: N_Detector_Secuencia123 disparó -> {disparo_detector_inhibicion}. Potencial Máx: {max_potencial_inhibicion:.3f} mV")
    print("--- Fin Escenario de Prueba de Inhibición ---")
    # El tiempo_simulacion_global principal no se modifica por esta prueba aislada.
