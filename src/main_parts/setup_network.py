import logging

logging.debug("DEBUG: Iniciando src/main_parts/setup_network.py")
logging.debug("DEBUG SETUP_NETWORK.PY: Archivo siendo cargado AHORA MISMO - v20250609_0027")
import numpy as np
from configuracion import parametros_simulacion as ps
from src.red.red_clase import RedBiologica
logging.debug("DEBUG: RedBiologica importada correctamente en setup_network.py")
from src.neurona.neurona_clase import NeuronaBiologica
from src.neurona.tipos_neurona import EXCITATORIA, INHIBITORIA
from configuracion.parametros_simulacion import (
    USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE, 
    PESO_EXCITATORIO_A_INHIBIDORA_BASE, PESO_INHIBITORIO_BASE,
    N_G3_DETECTOR_EVENTO_A_AB_ID # Importar el ID del nuevo detector G3
)


def initialize_network(verbose_general=True):
    import sys
    logging.debug("DEBUG INITIALIZE_NETWORK: ABSOLUTE START - v04, verbose_general IS: %s", verbose_general)
    logging.debug("DEBUG INITIALIZE_NETWORK: WRITING TO STDERR - v04, verbose_general IS: %s", verbose_general)
    try:
        # IDs de las neuronas Grupo 1
        N_PRE1_ID = 'N_Pre1'
        N_PRE2_ID = 'N_Pre2'
        N_PRE3_ID = 'N_Pre3'
        N_DETECTOR_ID = 'N_Detector_Secuencia123'
        N_DETECTOR_ID_2 = 'N_Detector_Secuencia321'
        N_DETECTOR_ID_3 = 'N_Detector_Secuencia132' # Neurona detectora para secuencia 1->3->2
        N_DETECTOR_ID_4 = 'N_Detector_Secuencia213' # Neurona detectora para secuencia 2->1->3
        N_DETECTOR_ID_5 = 'N_Detector_Secuencia231' # Neurona detectora para secuencia 2->3->1
        N_DETECTOR_ID_6 = 'N_Detector_Secuencia312' # Neurona detectora para secuencia 3->1->2
        N_INHIB1_ID = 'N_Inhib1' # Neurona inhibitoria para Grupo 1
        N_SFA_TEST_ID = 'N_SFA_Test' # Neurona para probar SFA (general)
        logging.debug("DEBUG INITIALIZE_NETWORK: AFTER G1 ID ASSIGNMENTS - v04")

        logging.debug("DEBUG INITIALIZE_NETWORK: AFTER G1 ID ASSIGNMENTS - v04")
        if verbose_general: 
            logging.debug(f"DEBUG SETUP: IDs G1 definidos. Último: {N_SFA_TEST_ID}. ANTES de listas G1.")
    
            logging.debug(f"DEBUG SETUP: IDs G1 definidos. Último: {N_SFA_TEST_ID}. ANTES de listas G1.")

        ids_neuronas_presinapticas = [N_PRE1_ID, N_PRE2_ID, N_PRE3_ID]
        ids_neuronas_detectoras_g1 = [N_DETECTOR_ID, N_DETECTOR_ID_2, N_DETECTOR_ID_3, N_DETECTOR_ID_4, N_DETECTOR_ID_5, N_DETECTOR_ID_6] # Actualizada lista de detectoras G1
        ids_neuronas_inhibitorias = [N_INHIB1_ID]
        ids_neuronas_sfa_test = [N_SFA_TEST_ID]
        if verbose_general: logging.debug(f"DEBUG SETUP: Listas G1 creadas. Última: ids_neuronas_sfa_test. ANTES de IDs G2.")

        # IDs para Grupo 2
        N_G2_PRE_A_ID = 'N_G2_PreA'
        N_G2_PRE_B_ID = 'N_G2_PreB'
        N_G2_DETECTOR_AB_ID = 'N_G2_DetectorAB'

        ids_neuronas_g2_presinapticas = [N_G2_PRE_A_ID, N_G2_PRE_B_ID]
        ids_neuronas_g2_detectoras = [N_G2_DETECTOR_AB_ID]
        if verbose_general: logging.debug(f"DEBUG SETUP: Listas G2 creadas. Última: ids_neuronas_g2_detectoras. ANTES de IDs G3.")

        # IDs para Grupo 3
        # N_G3_DETECTOR_EVENTO_A_AB_ID ya está importado
        ids_neuronas_detectoras_g3 = [N_G3_DETECTOR_EVENTO_A_AB_ID]

        if verbose_general:
            logging.debug(f"DEBUG SETUP: ANTES de instanciar RedBiologica. verbose_general: {verbose_general}")
        # Crear la red
        red_neuronal = RedBiologica(verbose=verbose_general)
        if verbose_general:
            logging.debug(f"DEBUG SETUP: DESPUÉS de instanciar RedBiologica. Tipo de red_neuronal: {type(red_neuronal)}")
        historial_pesos_detectores = {}

        # Parámetros STDP por defecto (pueden ser sobreescritos por neuronas específicas si es necesario)
        if verbose_general:
            logging.debug(f"DEBUG SETUP: ANTES de definir params_stdp. verbose_general: {verbose_general}")
        params_stdp = {
            'A_plus': ps.A_PLUS_BASE,
            'A_minus': ps.A_MINUS_BASE,
            'tau_plus': ps.TAU_PLUS_BASE,
            'tau_minus': ps.TAU_MINUS_BASE,
            'peso_max_stdp': ps.PESO_MAX_STDP_BASE
        }

        # Crear neuronas
        neuronas_a_crear = [
            # Grupo 1
            (N_PRE1_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, False, {}, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_PRE2_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, False, {}, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_PRE3_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, False, {}, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_DETECTOR_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_DETECTOR_ID_2, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_DETECTOR_ID_3, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_DETECTOR_ID_4, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_DETECTOR_ID_5, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_DETECTOR_ID_6, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_INHIB1_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, INHIBITORIA, False, {}, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_SFA_TEST_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, False, {}, True, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            # Grupo 2
            (N_G2_PRE_A_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, False, {}, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_G2_PRE_B_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, False, {}, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE),
            (N_G2_DETECTOR_AB_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_G2_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE), # Detector G2
            
            # Grupo 3
            (N_G3_DETECTOR_EVENTO_A_AB_ID, ps.POTENCIAL_REPOSO_BASE, ps.UMBRAL_DISPARO_G3_BASE, ps.POTENCIAL_POST_DISPARO_BASE, EXCITATORIA, True, params_stdp, USA_SFA_BASE, TAU_SFA_BASE, INCREMENTO_SFA_POR_DISPARO_BASE), # Detector G3
        ]

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Definición de 'neuronas_a_crear' COMPLETADA. Longitud: {len(neuronas_a_crear)}")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: ANTES del bucle principal de creación de neuronas. verbose_general: {verbose_general}. Primer elemento de neuronas_a_crear: {neuronas_a_crear[0] if neuronas_a_crear else 'VACIO'}")

        for neurona_id, p_reposo, u_disparo, p_post_disparo, tipo, usa_stdp_flag, stdp_params_dict, usa_sfa_flag, tau_sfa_val, incr_sfa_val in neuronas_a_crear:
            if usa_stdp_flag:
                neurona = NeuronaBiologica(
                    id_neurona=neurona_id,
                    potencial_reposo=p_reposo,
                    umbral_disparo=u_disparo,
                    potencial_post_disparo=p_post_disparo,
                    tipo_neurona=tipo,
                    usa_stdp=usa_stdp_flag,
                    verbose=verbose_general,
                    A_plus=stdp_params_dict['A_plus'],
                    A_minus=stdp_params_dict['A_minus'],
                    tau_plus=stdp_params_dict['tau_plus'],
                    tau_minus=stdp_params_dict['tau_minus'],
                    peso_max_stdp=stdp_params_dict['peso_max_stdp'],
                    tau_membrana=ps.TAU_M_DETECTOR_SEC123 if neurona_id == N_DETECTOR_ID else ps.TAU_M_DETECTOR_BASE, # CONFIGURACIÓN CRÍTICA (Exp7-10): N_Detector_Secuencia123 usa tau_m específico.
                    usa_sfa=usa_sfa_flag,
                    tau_sfa=tau_sfa_val,
                    incremento_sfa_por_disparo=incr_sfa_val
                )
            else:
                neurona = NeuronaBiologica(
                    id_neurona=neurona_id,
                    potencial_reposo=p_reposo,
                    umbral_disparo=u_disparo,
                    potencial_post_disparo=p_post_disparo,
                    tipo_neurona=tipo,
                    usa_stdp=usa_stdp_flag,
                    verbose=verbose_general,
                    usa_sfa=usa_sfa_flag,
                    tau_sfa=tau_sfa_val,
                    incremento_sfa_por_disparo=incr_sfa_val
                )
            if neurona_id == N_DETECTOR_ID and verbose_general:
                logging.debug(f"    INFO: {neurona_id} creada con tau_m = {ps.TAU_M_DETECTOR_SEC123} ms (específico). Otras detectoras G1 con STDP usan tau_m = {ps.TAU_M_DETECTOR_BASE} ms.")
            red_neuronal.agregar_neurona(neurona)

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Justo ANTES del primer bucle de conexiones (para N_DETECTOR_ID='{N_DETECTOR_ID}'). ids_a_iterar: {ids_neuronas_presinapticas}, tipo: {type(ids_neuronas_presinapticas)}")

        try:
            if verbose_general:
                logging.debug(f"DEBUG SETUP: Todas las N_..._ID asignadas. Último ID (N_G3_DETECTOR_EVENTO_A_AB_ID): {N_G3_DETECTOR_EVENTO_A_AB_ID}. ANTES de definir listas de IDs.")
        except Exception as e_print_ids:
            logging.debug(f"DEBUG SETUP: ERROR AL INTENTAR IMPRIMIR N_..._IDs: {e_print_ids}")

        # Definiciones de grupos de IDs para facilitar las conexiones
        # Conexiones para Grupo 1
        if verbose_general: logging.debug(f"DEBUG SETUP: Iniciando bucle de conexiones para {N_DETECTOR_ID}")
        for pre_id in ids_neuronas_presinapticas:
            if verbose_general and N_DETECTOR_ID == 'N_Detector_Estimulo_A':
                logging.debug(f"DEBUG SETUP N_D_Estimulo_A Loop: Iterando con pre_id={pre_id} para {N_DETECTOR_ID}")
            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_DETECTOR_ID,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if verbose_general and N_DETECTOR_ID == 'N_Detector_Estimulo_A':
                logging.debug(f"DEBUG SETUP N_D_Estimulo_A Loop: Conexión {pre_id}->{N_DETECTOR_ID} realizada.")

            if N_DETECTOR_ID not in historial_pesos_detectores:
                historial_pesos_detectores[N_DETECTOR_ID] = {}

            if verbose_general and N_DETECTOR_ID == 'N_Detector_Estimulo_A':
                logging.debug(f"DEBUG SETUP N_D_Estimulo_A Loop: Antes de asignar lista vacía para {(pre_id, N_DETECTOR_ID)}.")

            historial_pesos_detectores[N_DETECTOR_ID][(pre_id, N_DETECTOR_ID)] = []

            if verbose_general and N_DETECTOR_ID == 'N_Detector_Estimulo_A':
                logging.debug(f"DEBUG SETUP N_D_Estimulo_A Loop: Fin de iteración para pre_id={pre_id}, N_DETECTOR_ID={N_DETECTOR_ID}.")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: ANTES DEL BUCLE N_D2 ('{N_DETECTOR_ID_2}'). ids_neuronas_presinapticas: {ids_neuronas_presinapticas}, tipo: {type(ids_neuronas_presinapticas)}")

        for pre_id in ids_neuronas_presinapticas:
            if verbose_general and N_DETECTOR_ID_2 == 'N_Detector_Secuencia123':
                logging.debug(f"DEBUG SETUP N_D2 Loop: Iterando con pre_id={pre_id} para {N_DETECTOR_ID_2}")
            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_DETECTOR_ID_2,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if verbose_general and N_DETECTOR_ID_2 == 'N_Detector_Secuencia123':
                logging.debug(f"DEBUG SETUP N_D2 Loop: Conexión {pre_id}->{N_DETECTOR_ID_2} realizada.")

            if N_DETECTOR_ID_2 not in historial_pesos_detectores:
                historial_pesos_detectores[N_DETECTOR_ID_2] = {}
            
            if verbose_general and N_DETECTOR_ID_2 == 'N_Detector_Secuencia123':
                logging.debug(f"DEBUG SETUP N_D2 Loop: Antes de asignar lista vacía para {(pre_id, N_DETECTOR_ID_2)}.")

            historial_pesos_detectores[N_DETECTOR_ID_2][(pre_id, N_DETECTOR_ID_2)] = []
            if verbose_general and N_DETECTOR_ID_2 == 'N_Detector_Secuencia123':
                logging.debug(f"DEBUG SETUP N_D2 Loop: Fin de iteración para pre_id={pre_id}, N_DETECTOR_ID_2={N_DETECTOR_ID_2}.")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: FIN BUCLE N_D2 ('{N_DETECTOR_ID_2}'). INICIO BUCLE N_D3 ('{N_DETECTOR_ID_3}').")

        for pre_id in ids_neuronas_presinapticas:
            if verbose_general and N_DETECTOR_ID_3 == 'N_Detector_Secuencia321':
                logging.debug(f"DEBUG SETUP N_D3 Loop: Iterando con pre_id={pre_id} para {N_DETECTOR_ID_3}")

            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_DETECTOR_ID_3,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if verbose_general and N_DETECTOR_ID_3 == 'N_Detector_Secuencia321':
                logging.debug(f"DEBUG SETUP N_D3 Loop: Conexión {pre_id}->{N_DETECTOR_ID_3} realizada.")

            if N_DETECTOR_ID_3 not in historial_pesos_detectores:
                historial_pesos_detectores[N_DETECTOR_ID_3] = {}
            
            if verbose_general and N_DETECTOR_ID_3 == 'N_Detector_Secuencia321':
                logging.debug(f"DEBUG SETUP N_D3 Loop: Antes de asignar lista vacía para {(pre_id, N_DETECTOR_ID_3)}.")

            historial_pesos_detectores[N_DETECTOR_ID_3][(pre_id, N_DETECTOR_ID_3)] = []
            if verbose_general and N_DETECTOR_ID_3 == 'N_Detector_Secuencia321':
                logging.debug(f"DEBUG SETUP N_D3 Loop: Fin de iteración para pre_id={pre_id}, N_DETECTOR_ID_3={N_DETECTOR_ID_3}.")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Finalizado bucle N_D3 ('{N_DETECTOR_ID_3}'). Preparando para N_D4 ('{N_DETECTOR_ID_4}').")

        for pre_id in ids_neuronas_presinapticas:
            if verbose_general and N_DETECTOR_ID_4 == 'N_Detector_Secuencia132':
                logging.debug(f"DEBUG SETUP N_D4 Loop: Iterando con pre_id={pre_id} para {N_DETECTOR_ID_4}")

            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_DETECTOR_ID_4,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if verbose_general and N_DETECTOR_ID_4 == 'N_Detector_Secuencia132':
                logging.debug(f"DEBUG SETUP N_D4 Loop: Conexión {pre_id}->{N_DETECTOR_ID_4} realizada.")

            if N_DETECTOR_ID_4 not in historial_pesos_detectores:
                historial_pesos_detectores[N_DETECTOR_ID_4] = {}
            
            if verbose_general and N_DETECTOR_ID_4 == 'N_Detector_Secuencia132':
                logging.debug(f"DEBUG SETUP N_D4 Loop: Antes de asignar lista vacía para {(pre_id, N_DETECTOR_ID_4)}.")

            historial_pesos_detectores[N_DETECTOR_ID_4][(pre_id, N_DETECTOR_ID_4)] = []
            if verbose_general and N_DETECTOR_ID_4 == 'N_Detector_Secuencia132':
                logging.debug(f"DEBUG SETUP N_D4 Loop: Fin de iteración para pre_id={pre_id}, N_DETECTOR_ID_4={N_DETECTOR_ID_4}.")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: ANTES del bucle N_D5. Valor de N_DETECTOR_ID_5 = '{N_DETECTOR_ID_5}'")

        for pre_id in ids_neuronas_presinapticas:
            if verbose_general:
                logging.debug(f"DEBUG SETUP: DENTRO del bucle N_D5. pre_id='{pre_id}'. N_DETECTOR_ID_5='{N_DETECTOR_ID_5}'. Comparacion (N_DETECTOR_ID_5 == 'N_Detector_Secuencia231') es {N_DETECTOR_ID_5 == 'N_Detector_Secuencia231'}")

            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_DETECTOR_ID_5,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if verbose_general and N_DETECTOR_ID_5 == 'N_Detector_Secuencia231':
                logging.debug(f"DEBUG SETUP N_D5 Loop: Conexión {pre_id}->{N_DETECTOR_ID_5} realizada.")

            if N_DETECTOR_ID_5 not in historial_pesos_detectores:
                historial_pesos_detectores[N_DETECTOR_ID_5] = {}
            if verbose_general and N_DETECTOR_ID_5 == 'N_Detector_Secuencia231':
                logging.debug(f"DEBUG SETUP N_D5 Loop: Antes de asignar lista vacía para {(pre_id, N_DETECTOR_ID_5)}.")
            historial_pesos_detectores[N_DETECTOR_ID_5][(pre_id, N_DETECTOR_ID_5)] = []
            if verbose_general and N_DETECTOR_ID_5 == 'N_Detector_Secuencia231':
                logging.debug(f"DEBUG SETUP N_D5 Loop: Después de asignar lista vacía para {(pre_id, N_DETECTOR_ID_5)}. Fin de iteración para {pre_id}.")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Finalizado bucle de conexiones para {N_DETECTOR_ID_5}")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Iniciando conexiones para {N_DETECTOR_ID_6}")
        for pre_id in ids_neuronas_presinapticas:
            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_DETECTOR_ID_6,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if verbose_general:
                logging.debug(f"DEBUG SETUP: Conexión {pre_id} -> {N_DETECTOR_ID_6} establecida.")
            if N_DETECTOR_ID_6 not in historial_pesos_detectores:
                historial_pesos_detectores[N_DETECTOR_ID_6] = {}
            historial_pesos_detectores[N_DETECTOR_ID_6][(pre_id, N_DETECTOR_ID_6)] = []
        if verbose_general:
            logging.debug(f"DEBUG SETUP: Finalizadas conexiones para {N_DETECTOR_ID_6}")

        # Conexiones de ENTRADA para N_INHIB1_ID (Feed-forward inhibition)
        # Hacer que N_INHIB1_ID reciba entradas excitatorias de TODAS las neuronas presinápticas del Grupo 1
        for pre_id in ids_neuronas_presinapticas:
            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_id,
                id_neurona_destino=N_INHIB1_ID,
                peso_inicial=ps.PESO_EXCITATORIO_A_INHIBIDORA_BASE,
                plastica=False
            )
        if verbose_general:
            logging.debug(f"Conexiones excitatorias establecidas de neuronas presinápticas G1 a '{N_INHIB1_ID}' con peso {ps.PESO_EXCITATORIO_A_INHIBIDORA_BASE}.")

        # Conexiones de SALIDA para N_INHIB1_ID
        # CONFIGURACIÓN CRÍTICA (Resultado Exp7-10): Asignación de tau_m específico para N_Detector_Secuencia123.
        for detector_id_g1 in ids_neuronas_detectoras_g1:
            if detector_id_g1 == N_DETECTOR_ID: # N_DETECTOR_ID es "N_Detector_Secuencia123"
                if verbose_general:
                    logging.debug(f"CONFIG CRÍTICA: Omitiendo conexión inhibitoria de '{N_INHIB1_ID}' a '{detector_id_g1}' (N_Detector_Secuencia123). Esta es la configuración óptima.")
                continue # Omitir la conexión para N_Detector_Secuencia123

            # Conectar N_INHIB1_ID a las otras neuronas detectoras del Grupo 1
            red_neuronal.conectar_neuronas(
                id_neurona_origen=N_INHIB1_ID,
                id_neurona_destino=detector_id_g1,
                peso_inicial=ps.PESO_INHIBITORIO_BASE, # Usar el peso base definido
                plastica=False
            )
        if verbose_general:
            logging.debug(f"Conexiones inhibitorias establecidas de '{N_INHIB1_ID}' a detectoras G1 (excepto '{N_DETECTOR_ID}') con peso {ps.PESO_INHIBITORIO_BASE}.")

        # Conexiones para Grupo 2
        for pre_g2_id in ids_neuronas_g2_presinapticas:
            red_neuronal.conectar_neuronas(
                id_neurona_origen=pre_g2_id,
                id_neurona_destino=N_G2_DETECTOR_AB_ID,
                peso_inicial=ps.PESO_INICIAL_SINAPSIS_BASE,
                plastica=True
            )
            if N_G2_DETECTOR_AB_ID not in historial_pesos_detectores:
                historial_pesos_detectores[N_G2_DETECTOR_AB_ID] = {}
            historial_pesos_detectores[N_G2_DETECTOR_AB_ID][(pre_g2_id, N_G2_DETECTOR_AB_ID)] = []

        # Conexiones para Grupo 3 (N_G3_Detector_Evento_A_AB)
        # Conectar N_DETECTOR_ID (G1_A) a N_G3_DETECTOR_EVENTO_A_AB_ID
        red_neuronal.conectar_neuronas(
            id_neurona_origen=N_DETECTOR_ID,
            id_neurona_destino=N_G3_DETECTOR_EVENTO_A_AB_ID,
            peso_inicial=ps.PESO_INICIAL_G1_A_G3_BASE,
            plastica=True
        )
        if N_G3_DETECTOR_EVENTO_A_AB_ID not in historial_pesos_detectores:
            historial_pesos_detectores[N_G3_DETECTOR_EVENTO_A_AB_ID] = {}
        historial_pesos_detectores[N_G3_DETECTOR_EVENTO_A_AB_ID][(N_DETECTOR_ID, N_G3_DETECTOR_EVENTO_A_AB_ID)] = []

        # Conectar N_G2_DETECTOR_AB_ID (G2_AB) a N_G3_DETECTOR_EVENTO_A_AB_ID
        red_neuronal.conectar_neuronas(
            id_neurona_origen=N_G2_DETECTOR_AB_ID,
            id_neurona_destino=N_G3_DETECTOR_EVENTO_A_AB_ID,
            peso_inicial=ps.PESO_INICIAL_G2_AB_G3_BASE,
            plastica=True
        )
        historial_pesos_detectores[N_G3_DETECTOR_EVENTO_A_AB_ID][(N_G2_DETECTOR_AB_ID, N_G3_DETECTOR_EVENTO_A_AB_ID)] = []

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Conexiones a G3 ({N_G3_DETECTOR_EVENTO_A_AB_ID}) creadas. De: {N_DETECTOR_ID} y {N_G2_DETECTOR_AB_ID}")

        if verbose_general:
            logging.debug(f"DEBUG SETUP: Inicialización de la red CASI completa. A punto de devolver la red. Estado de verbose_general: {verbose_general}")

        return (
            red_neuronal, historial_pesos_detectores, 
            ids_neuronas_presinapticas, ids_neuronas_detectoras_g1, ids_neuronas_inhibitorias, ids_neuronas_sfa_test,
            ids_neuronas_g2_presinapticas, ids_neuronas_g2_detectoras,
            N_PRE1_ID, N_PRE2_ID, N_PRE3_ID, 
            N_DETECTOR_ID, N_DETECTOR_ID_2, N_DETECTOR_ID_3, N_DETECTOR_ID_4, N_DETECTOR_ID_5, N_DETECTOR_ID_6, 
            N_INHIB1_ID, N_SFA_TEST_ID,
            N_G2_PRE_A_ID, N_G2_PRE_B_ID, N_G2_DETECTOR_AB_ID,
            ids_neuronas_detectoras_g3, N_G3_DETECTOR_EVENTO_A_AB_ID # Añadir G3 al retorno
        )

    except Exception as e_init_net:
        logging.critical(f"CRITICAL ERROR in initialize_network: {e_init_net}", exc_info=True)
        # Volver a lanzar la excepción es importante para que el programa principal sepa que algo falló.
        raise
