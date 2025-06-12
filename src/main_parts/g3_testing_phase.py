# -*- coding: utf-8 -*-
"""
Módulo para la fase de pruebas del detector G3.
"""

from configuracion import parametros_simulacion as ps

# Si se necesita type hinting para RedBiologica, se podría añadir:
# from ..red.red_clase import RedBiologica

def _estimular_secuencia_g1_para_g3_test(red_neuronal, pre_neuronas_estimulo_ids, target_g1_detector_id, 
                                         impulso, dt_estimulo_componente, pasos_observacion, verbose=False):
    """ 
    Aplica un impulso secuencial para pruebas G1 y simula para observar el disparo.
    Retorna el número de pasos de simulación consumidos.
    """
    pasos_consumidos_estimulo = 0
    if verbose:
        logging.info(f"        Estimulando secuencia (test) con pre-neuronas: {pre_neuronas_estimulo_ids} para target G1: {target_g1_detector_id} at t_sim={red_neuronal.tiempo_actual_simulacion}")

    if target_g1_detector_id in red_neuronal.neuronas:
        red_neuronal.neuronas[target_g1_detector_id].limpiar_historia_disparos()

    for i, pre_neurona_id in enumerate(pre_neuronas_estimulo_ids):
        red_neuronal.aplicar_impulso(pre_neurona_id, impulso, red_neuronal.tiempo_actual_simulacion)
        if verbose:
            logging.info(f"          Impulso (test) a {pre_neurona_id} en t_sim={red_neuronal.tiempo_actual_simulacion}")
        red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=dt_estimulo_componente, aplicar_stdp_global=False)
        pasos_consumidos_estimulo += dt_estimulo_componente
        if verbose:
            logging.info(f"          DEBUG: Tras estimular {pre_neurona_id} y actualizar red, red_neuronal.tiempo_actual_simulacion = {red_neuronal.tiempo_actual_simulacion}")
    
    red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=pasos_observacion, aplicar_stdp_global=False)
    pasos_consumidos_estimulo += pasos_observacion

    disparos = red_neuronal.contar_disparos_neurona(target_g1_detector_id)
    if verbose:
        if disparos > 0:
            logging.info(f"        G1 Detector {target_g1_detector_id} disparó {disparos} veces (test). t_sim={red_neuronal.tiempo_actual_simulacion}")
        else:
            logging.info(f"        G1 Detector {target_g1_detector_id} NO disparó (test). t_sim={red_neuronal.tiempo_actual_simulacion}")
    return pasos_consumidos_estimulo

import logging
from configuracion import parametros_simulacion as ps

def run_testing_phase_g3(red_neuronal, historial_disparos_detectores_prueba, 
                       ids_neuronas_presinapticas, 
                       N_PRE1_ID, N_PRE2_ID, N_PRE3_ID, 
                       N_DETECTOR_ID_G1_A, N_DETECTOR_ID_G1_B, 
                       N_G2_DETECTOR_AB_ID, N_G3_DETECTOR_EVENTO_A_AB_ID, 
                       pasos_por_prueba, dt_estimulo_componente, impulso_prueba, 
                       tiempo_entre_eventos_g1_g2, aplicar_ruido, prob_ruido, verbose=False):
    logging.info(f"--- Iniciando Fase de Pruebas G3 para {N_G3_DETECTOR_EVENTO_A_AB_ID} ---")
    logging.info(f"Parámetros: Pasos/Prueba={pasos_por_prueba}, dt_comp_test={dt_estimulo_componente}, T_inter_G1_G2_test={tiempo_entre_eventos_g1_g2}")
    logging.info(f"             PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST={ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST}, TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST={ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST}")

    secuencia_P1P2P3_pre_ids = [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID]
    secuencia_P3P2P1_pre_ids = [N_PRE3_ID, N_PRE2_ID, N_PRE1_ID]

    if N_G3_DETECTOR_EVENTO_A_AB_ID not in historial_disparos_detectores_prueba:
        historial_disparos_detectores_prueba[N_G3_DETECTOR_EVENTO_A_AB_ID] = {}

    tipos_de_prueba = [
        "G1A_then_G2AB_CorrectTiming", 
        "Only_G1A", 
        "Only_G2AB", 
        "G1A_then_G2AB_LongDelay", 
        "G2AB_then_G1A_WrongOrder"
    ]

    for nombre_prueba in tipos_de_prueba:
        red_neuronal.resetear_estado_red()
        
        neuronas_a_modificar_umbral = [N_DETECTOR_ID_G1_A, N_DETECTOR_ID_G1_B, N_G2_DETECTOR_AB_ID]
        umbrales_originales = {}
        if verbose:
            logging.info(f"  Modificando temporalmente umbrales para {neuronas_a_modificar_umbral} para la prueba '{nombre_prueba}'...")

        for neurona_id_mod in neuronas_a_modificar_umbral:
            umbral_actual = red_neuronal.get_umbral_neurona(neurona_id_mod)
            pot_reposo_actual = red_neuronal.get_potencial_reposo_neurona(neurona_id_mod)
            
            if umbral_actual is not None and pot_reposo_actual is not None:
                umbrales_originales[neurona_id_mod] = umbral_actual
                nuevo_umbral_temporal = pot_reposo_actual + ps.TRAINING_THRESHOLD_OFFSET_BASE
                red_neuronal.set_umbral_neurona(neurona_id_mod, nuevo_umbral_temporal)
                if verbose:
                    logging.info(f"    Neurona {neurona_id_mod}: Umbral original={umbral_actual:.2f}, Pot. Reposo={pot_reposo_actual:.2f}. Nuevo umbral temporal={nuevo_umbral_temporal:.2f}")
            elif verbose:
                logging.info(f"    Advertencia: No se pudo obtener umbral/pot.reposo para {neurona_id_mod}. No se modificó su umbral.")
        
        pasos_consumidos_prueba = 0

        if aplicar_ruido:
            if verbose: logging.info(f"  Aplicando ruido pre-sináptico con probabilidad: {prob_ruido} para prueba {nombre_prueba}")
        
        if verbose: 
            logging.info(f"  Prueba G3: '{nombre_prueba}' (tiempo_actual_simulacion = {red_neuronal.tiempo_actual_simulacion})")

        if nombre_prueba == "G1A_then_G2AB_CorrectTiming":
            if verbose: print("    1. Activando G1_A...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            if verbose: logging.info(f"    2. Pausa de {tiempo_entre_eventos_g1_g2} pasos...")
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=tiempo_entre_eventos_g1_g2, aplicar_stdp_global=False)
            pasos_consumidos_prueba += tiempo_entre_eventos_g1_g2
            if verbose: print("    3. Activando G2_AB...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P3P2P1_pre_ids, N_DETECTOR_ID_G1_B, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST

        elif nombre_prueba == "Only_G1A":
            if verbose: print("    Activando Solo G1_A...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim

        elif nombre_prueba == "Only_G2AB":
            if verbose: print("    Activando Solo G2_AB...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P3P2P1_pre_ids, N_DETECTOR_ID_G1_B, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST

        elif nombre_prueba == "G1A_then_G2AB_LongDelay":
            if verbose: print("    1. Activando G1_A (Long Delay Test)...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            pausa_larga = tiempo_entre_eventos_g1_g2 * 3
            if verbose: logging.info(f"    2. Pausa Larga de {pausa_larga} pasos...")
            # Iterative update for long pause to correctly advance simulation time
            for _ in range(pausa_larga):
                red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=1, aplicar_stdp_global=False)
            pasos_consumidos_prueba += pausa_larga
            if verbose: print("    3. Activando G2_AB (Long Delay Test)...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P3P2P1_pre_ids, N_DETECTOR_ID_G1_B, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST

        elif nombre_prueba == "G2AB_then_G1A_WrongOrder":
            if verbose: print("    1. Activando G2_AB (Wrong Order Test)...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TEST
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P3P2P1_pre_ids, N_DETECTOR_ID_G1_B, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, aplicar_stdp_global=False)
            pasos_consumidos_prueba += ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST
            if verbose: logging.info(f"    2. Pausa de {tiempo_entre_eventos_g1_g2} pasos...")
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=tiempo_entre_eventos_g1_g2, aplicar_stdp_global=False)
            pasos_consumidos_prueba += tiempo_entre_eventos_g1_g2
            if verbose: print("    3. Activando G1_A (Wrong Order Test)...")
            pasos_estim = _estimular_secuencia_g1_para_g3_test(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A, impulso_prueba, dt_estimulo_componente, ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TEST, verbose)
            pasos_consumidos_prueba += pasos_estim

        pasos_restantes_prueba = pasos_por_prueba - pasos_consumidos_prueba
        if pasos_restantes_prueba > 0:
            if verbose: logging.info(f"    Simulando {pasos_restantes_prueba} pasos restantes de la prueba '{nombre_prueba}' (tiempo_actual_simulacion = {red_neuronal.tiempo_actual_simulacion})")
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=pasos_restantes_prueba, aplicar_stdp_global=False)
        elif verbose:
            logging.info(f"    ADVERTENCIA (Prueba G3 '{nombre_prueba}'): No hay pasos restantes. Pasos consumidos: {pasos_consumidos_prueba}, Pasos por prueba: {pasos_por_prueba}. Considere aumentar ps.PASOS_PRUEBA_G3.")

        disparos_g3 = red_neuronal.contar_disparos_neurona(N_G3_DETECTOR_EVENTO_A_AB_ID)
        disparos_g1a = red_neuronal.contar_disparos_neurona(N_DETECTOR_ID_G1_A)
        disparos_g2ab = red_neuronal.contar_disparos_neurona(N_G2_DETECTOR_AB_ID)
        
        historial_disparos_detectores_prueba[N_G3_DETECTOR_EVENTO_A_AB_ID][nombre_prueba] = {
            'disparos_g3': disparos_g3,
            'disparos_g1a': disparos_g1a,
            'disparos_g2ab': disparos_g2ab,
            'pasos_estimulo_consumidos': pasos_consumidos_prueba
        }
        if verbose:
            logging.info(f"  Resultado Prueba '{nombre_prueba}': G3 disparó {disparos_g3} veces. G1_A: {disparos_g1a}, G2_AB: {disparos_g2ab}. (t_sim_final={red_neuronal.tiempo_actual_simulacion})")
        
        # --- Restauración de umbrales originales --- (Reconstruido)
        if verbose:
            logging.info(f"  Restaurando umbrales originales para prueba '{nombre_prueba}'...")
        for neurona_id_mod, umbral_original_val in umbrales_originales.items():
            red_neuronal.set_umbral_neurona(neurona_id_mod, umbral_original_val)
            if verbose:
                logging.info(f"    Neurona {neurona_id_mod}: Umbral restaurado a {umbral_original_val:.2f} mV")
    
    logging.info(f"--- Fin Fase de Pruebas G3 ---") # (Reconstruido)
