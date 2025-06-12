# -*- coding: utf-8 -*-
"""
Módulo para la fase de entrenamiento del detector G3.
"""

from configuracion import parametros_simulacion as ps
from configuracion.parametros_simulacion import TRAINING_THRESHOLD_OFFSET_BASE

# Si se necesita type hinting para RedBiologica, se podría añadir:
# from ..red.red_clase import RedBiologica 

def _estimular_secuencia_g1_para_g3_train(red_neuronal, pre_neuronas_estimulo_ids, target_g1_detector_id, 
                                          impulso, dt_estimulo_componente, pasos_observacion, verbose=False):
    """ 
    Aplica un impulso secuencial a un conjunto de neuronas PRE para activar una secuencia G1
    y simula para observar el disparo del target_g1_detector_id.
    Retorna el número de pasos de simulación consumidos.
    """
    pasos_consumidos_estimulo = 0
    if verbose:
        print(f"      Estimulando secuencia con pre-neuronas: {pre_neuronas_estimulo_ids} para target G1: {target_g1_detector_id}")

    if target_g1_detector_id in red_neuronal.neuronas:
        red_neuronal.neuronas[target_g1_detector_id].limpiar_historia_disparos()

    for i, pre_neurona_id in enumerate(pre_neuronas_estimulo_ids):
        red_neuronal.aplicar_impulso(pre_neurona_id, impulso, red_neuronal.tiempo_actual_simulacion)
        if verbose:
            print(f"        Impulso a {pre_neurona_id} en t_sim={red_neuronal.tiempo_actual_simulacion}")
        
        neurona_pre_obj = red_neuronal.neuronas.get(pre_neurona_id)
        if neurona_pre_obj and verbose:
            vm_after_impulse = neurona_pre_obj.potencial_membrana
            umbral_actual = neurona_pre_obj.umbral_disparo
            would_fire_now = vm_after_impulse >= umbral_actual
            print(f"        DEBUG PRE_FIRE_CHECK: {pre_neurona_id} Vm_post_impulso={vm_after_impulse:.2f}, Umbral={umbral_actual:.2f}, Supera_Umbral={would_fire_now}")

        red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=dt_estimulo_componente, aplicar_stdp_global=True)
        pasos_consumidos_estimulo += dt_estimulo_componente
        if verbose and target_g1_detector_id in red_neuronal.neuronas:
            print(f"        DEBUG G1_TRAIN_STIM: Potencial de {target_g1_detector_id} = {red_neuronal.neuronas[target_g1_detector_id].potencial_membrana:.4f} mV en t_sim={red_neuronal.tiempo_actual_simulacion} (después de estímulo a {pre_neurona_id})")
    
    disparos_previos_observacion = red_neuronal.contar_disparos_neurona(target_g1_detector_id)
    for paso_obs in range(pasos_observacion):
        red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=1, aplicar_stdp_global=True)
        pasos_consumidos_estimulo += 1
        if verbose and target_g1_detector_id in red_neuronal.neuronas:
            print(f"        DEBUG G1_TRAIN_OBS: Potencial de {target_g1_detector_id} = {red_neuronal.neuronas[target_g1_detector_id].potencial_membrana:.4f} mV en t_sim={red_neuronal.tiempo_actual_simulacion} (paso observación {paso_obs+1})")

    disparos = red_neuronal.contar_disparos_neurona(target_g1_detector_id)
    if verbose:
        if disparos > 0:
            print(f"      G1 Detector {target_g1_detector_id} disparó {disparos} veces.")
        else:
            print(f"      G1 Detector {target_g1_detector_id} NO disparó.")
    return pasos_consumidos_estimulo

def run_training_phase_g3(red_neuronal, historial_pesos_detectores, 
                        ids_neuronas_presinapticas, 
                        N_PRE1_ID, N_PRE2_ID, N_PRE3_ID, 
                        N_DETECTOR_ID_G1_A, N_DETECTOR_ID_G1_B, 
                        N_G2_DETECTOR_AB_ID, N_G3_DETECTOR_EVENTO_A_AB_ID, 
                        num_epocas, pasos_por_epoca, dt_estimulo_componente, impulso_fuerte, 
                        tiempo_entre_eventos_g1_g2, verbose=False):
    print(f"--- Iniciando Fase de Entrenamiento G3 para {N_G3_DETECTOR_EVENTO_A_AB_ID} ---")
    print(f"Recibirá input de G1: {N_DETECTOR_ID_G1_A} y G2: {N_G2_DETECTOR_AB_ID}")
    print(f"Parámetros: Épocas={num_epocas}, Pasos/Época={pasos_por_epoca}, dt_comp={dt_estimulo_componente}, T_inter_G1_G2={tiempo_entre_eventos_g1_g2}")
    print(f"             PASOS_OBSERVACION_NEURONA_FIRE_G3_TRAIN={ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TRAIN}, TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TRAIN={ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TRAIN}")

    neurona_g3_target = red_neuronal.neuronas[N_G3_DETECTOR_EVENTO_A_AB_ID]
    secuencia_P1P2P3_pre_ids = [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID]
    # secuencia_P3P2P1_pre_ids = [N_PRE3_ID, N_PRE2_ID, N_PRE1_ID] # No se usa en esta lógica de entrenamiento G3

    neuronas_a_modificar_umbral_entrenamiento_g3 = [
        N_DETECTOR_ID_G1_A, 
        N_DETECTOR_ID_G1_B, # Aunque G1_B no se estimula aquí, se incluye para modificar umbral
        N_G2_DETECTOR_AB_ID,
        N_G3_DETECTOR_EVENTO_A_AB_ID
    ]
    umbrales_originales_entrenamiento_g3 = {}

    for epoca in range(num_epocas):
        if verbose:
            print(f"  Época {epoca + 1}/{num_epocas} - Modificando umbrales para G1A, G1B, G2AB, G3")
        
        for neurona_id_mod in neuronas_a_modificar_umbral_entrenamiento_g3:
            umbral_actual = red_neuronal.get_umbral_neurona(neurona_id_mod)
            umbrales_originales_entrenamiento_g3[neurona_id_mod] = umbral_actual
            potencial_reposo_neurona = red_neuronal.get_potencial_reposo_neurona(neurona_id_mod)
            nuevo_umbral_temporal = potencial_reposo_neurona + TRAINING_THRESHOLD_OFFSET_BASE
            red_neuronal.set_umbral_neurona(neurona_id_mod, nuevo_umbral_temporal)
            if verbose:
                print(f"    Neurona {neurona_id_mod}: Umbral original {umbral_actual:.2f} mV, nuevo umbral temporal {nuevo_umbral_temporal:.2f} mV (Reposo: {potencial_reposo_neurona:.2f} mV)")
        
        pasos_consumidos_epoca = 0
        red_neuronal.resetear_estado_red()

        if verbose:
            print(f"  Época {epoca + 1}/{num_epocas} - G3 Training (tiempo_actual_simulacion = {red_neuronal.tiempo_actual_simulacion})")

        # 1. Activar G1_A (N_Detector_Secuencia123)
        if verbose: print("    1. Activando G1_A (N_Detector_Secuencia123)...")
        pasos_activ_g1a = _estimular_secuencia_g1_para_g3_train(red_neuronal, secuencia_P1P2P3_pre_ids, N_DETECTOR_ID_G1_A,
                                                              impulso_fuerte, dt_estimulo_componente, 
                                                              ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TRAIN, verbose)
        pasos_consumidos_epoca += pasos_activ_g1a

        # 2. Pausa Temporal (para STDP en G3)
        if verbose: print(f"    2. Pausa de {tiempo_entre_eventos_g1_g2} pasos antes de G2_AB (tiempo_actual_simulacion = {red_neuronal.tiempo_actual_simulacion})")
        red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=tiempo_entre_eventos_g1_g2, aplicar_stdp_global=True)
        pasos_consumidos_epoca += tiempo_entre_eventos_g1_g2

        # 3. Activar G2_AB (N_G2_DetectorAB) - Estimulando directamente sus inputs N_G2_PreA y N_G2_PreB
        if ps.VERBOSE_TRAINING_G3: print(f"    3. Estimulando directamente N_G2_PreA y N_G2_PreB para activar {N_G2_DETECTOR_AB_ID}... (t_sim = {red_neuronal.tiempo_actual_simulacion})")

        # Estimular N_G2_PreA
        if ps.VERBOSE_TRAINING_G3: print(f"      Estimulando {ps.N_G2_PRE_A_ID} en t_sim={red_neuronal.tiempo_actual_simulacion} con impulso {ps.IMPULSO_FUERTE_G3}")
        red_neuronal.aplicar_impulso(ps.N_G2_PRE_A_ID, ps.IMPULSO_FUERTE_G3, red_neuronal.tiempo_actual_simulacion)
        red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=dt_estimulo_componente, aplicar_stdp_global=True)
        pasos_consumidos_epoca += dt_estimulo_componente

        # Pausa entre estímulos de G2 para que el detector de coincidencias funcione
        if ps.VERBOSE_TRAINING_G3: print(f"      Pausa de {ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TRAIN} pasos entre estímulos de G2")
        for _ in range(ps.TIEMPO_ENTRE_G1A_G1B_PARA_G2_EN_G3_TRAIN):
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=dt_estimulo_componente, aplicar_stdp_global=True)
            pasos_consumidos_epoca += dt_estimulo_componente

        # Estimular N_G2_PreB
        if ps.VERBOSE_TRAINING_G3: print(f"      Estimulando {ps.N_G2_PRE_B_ID} en t_sim={red_neuronal.tiempo_actual_simulacion} con impulso {ps.IMPULSO_FUERTE_G3}")
        red_neuronal.aplicar_impulso(ps.N_G2_PRE_B_ID, ps.IMPULSO_FUERTE_G3, red_neuronal.tiempo_actual_simulacion)
        red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=dt_estimulo_componente, aplicar_stdp_global=True)
        pasos_consumidos_epoca += dt_estimulo_componente
        
        # Observación de N_G2_DetectorAB
        if ps.VERBOSE_TRAINING_G3: print(f"      Observando {N_G2_DETECTOR_AB_ID} durante {ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TRAIN} pasos (inicio t_sim = {red_neuronal.tiempo_actual_simulacion})")
        for i_obs_g2 in range(ps.PASOS_OBSERVACION_NEURONA_FIRE_G3_TRAIN):
            if N_G2_DETECTOR_AB_ID in red_neuronal.neuronas:
                vm_g2_ab = red_neuronal.neuronas[N_G2_DETECTOR_AB_ID].potencial_membrana
                if ps.VERBOSE_TRAINING_G3: print(f"        DEBUG G2_TRAIN_OBS: Potencial de {N_G2_DETECTOR_AB_ID} = {vm_g2_ab:.4f} mV en t_sim={red_neuronal.tiempo_actual_simulacion} (paso observación {i_obs_g2 + 1})")
            # Simular un paso para observar el resultado
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=dt_estimulo_componente, aplicar_stdp_global=True)
            pasos_consumidos_epoca += dt_estimulo_componente
        
        if ps.VERBOSE_TRAINING_G3: print(f"      Fin observación de {N_G2_DETECTOR_AB_ID} (fin t_sim = {red_neuronal.tiempo_actual_simulacion})")
        disparos_g2_ab = red_neuronal.contar_disparos_neurona(N_G2_DETECTOR_AB_ID)
        if verbose:
            if disparos_g2_ab > 0: print(f"      G2 Detector {N_G2_DETECTOR_AB_ID} disparó {disparos_g2_ab} veces.")
            else: print(f"      G2 Detector {N_G2_DETECTOR_AB_ID} NO disparó.")

        # 4. Simular el resto de la época para STDP en G3
        pasos_restantes_epoca = pasos_por_epoca - pasos_consumidos_epoca
        if pasos_restantes_epoca > 0:
            if verbose: print(f"    4. Simulando {pasos_restantes_epoca} pasos restantes de la época para STDP en G3 (tiempo_actual_simulacion = {red_neuronal.tiempo_actual_simulacion})")
            red_neuronal.actualizar_estado_red(tiempo_actual=red_neuronal.tiempo_actual_simulacion, dt=pasos_restantes_epoca, aplicar_stdp_global=True)
        elif verbose:
            print(f"    ADVERTENCIA: No hay pasos restantes en la época. Pasos consumidos: {pasos_consumidos_epoca}, Pasos por época: {pasos_por_epoca}. Considere aumentar ps.PASOS_ENTRENAMIENTO_G3.")
        
        if verbose:
            print(f"  Época {epoca + 1}/{num_epocas} - Restaurando umbrales originales")
        for neurona_id_mod, umbral_original_val in umbrales_originales_entrenamiento_g3.items():
            red_neuronal.set_umbral_neurona(neurona_id_mod, umbral_original_val)
            if verbose:
                print(f"    Neurona {neurona_id_mod}: Umbral restaurado a {umbral_original_val:.2f} mV")

        for id_neurona_pre, info_conexion in neurona_g3_target.conexiones_entrantes.items():
            par_neuronas = (id_neurona_pre, neurona_g3_target.id) 
            if neurona_g3_target.id not in historial_pesos_detectores:
                 historial_pesos_detectores[neurona_g3_target.id] = {}
            if par_neuronas not in historial_pesos_detectores[neurona_g3_target.id]:
                historial_pesos_detectores[neurona_g3_target.id][par_neuronas] = []
            
            peso_actual = info_conexion['peso'] 
            historial_pesos_detectores[neurona_g3_target.id][par_neuronas].append(peso_actual)
        if verbose:
            pesos_actuales_str = []
            for origen_id, sinapsis in neurona_g3_target.conexiones_entrantes.items():
                pesos_actuales_str.append(f"{origen_id}->{neurona_g3_target.id}: {sinapsis['peso']:.4f}")
            print(f"  Fin Época {epoca + 1}: Pesos G3 -> {', '.join(pesos_actuales_str)}")

    print("--- Fin Fase de Entrenamiento G3 ---")
