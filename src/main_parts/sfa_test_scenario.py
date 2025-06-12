import numpy as np
from configuracion import parametros_simulacion as ps
from src.red.red_clase import RedBiologica # Necesario para crear red_sfa_test
from src.visualizacion.utilidades_graficas import plot_sfa_dynamics # Necesario para la gráfica

def run_sfa_test_scenario(
    red_neuronal, 
    N_SFA_TEST_ID, 
    # ps ya está importado en este módulo
    # np ya está importado en este módulo
    # RedBiologica ya está importada
    # plot_sfa_dynamics ya está importada
):
    """
    Ejecuta el escenario de prueba de Spike-Frequency Adaptation (SFA).
    """
    print("\n--- Inicio Escenario de Prueba de SFA ---")
    red_sfa_test = RedBiologica(verbose=False) # Nueva red para la prueba SFA
    neurona_sfa = red_neuronal.neuronas.get(N_SFA_TEST_ID)

    if neurona_sfa:
        red_sfa_test.agregar_neurona(neurona_sfa) 

        duracion_estimulo_sfa = 500  # ms
        dt_sfa = 1  # ms
        magnitud_estimulo_sfa = neurona_sfa.umbral_disparo - neurona_sfa.potencial_reposo + 1.0 
        
        tiempos_disparo_sfa = []
        historia_potencial_sfa = [] # No usado directamente, pero la neurona podría registrarlo internamente
        historia_corriente_sfa = [] # No usado directamente, pero la neurona podría registrarlo internamente

        print(f"Aplicando estímulo constante de {magnitud_estimulo_sfa:.2f} mV a {N_SFA_TEST_ID} durante {duracion_estimulo_sfa} ms...")
        # Reseteamos la neurona para la prueba
        neurona_sfa.potencial_membrana = neurona_sfa.potencial_reposo
        neurona_sfa.corriente_adaptacion_sfa = 0.0
        neurona_sfa.historia_disparos = []
        neurona_sfa.ultima_vez_disparo = -neurona_sfa.periodo_refractario_absoluto -1 # Para permitir disparo inmediato
        # Limpiar historiales específicos de SFA si existen en la neurona
        if hasattr(neurona_sfa, 'historial_tiempo_sfa'): neurona_sfa.historial_tiempo_sfa = []
        if hasattr(neurona_sfa, 'historial_potencial_membrana_sfa'): neurona_sfa.historial_potencial_membrana_sfa = []
        if hasattr(neurona_sfa, 'historial_corriente_adaptacion_sfa'): neurona_sfa.historial_corriente_adaptacion_sfa = []
        if hasattr(neurona_sfa, 'historial_umbral_efectivo_sfa'): neurona_sfa.historial_umbral_efectivo_sfa = []

        for t_sfa_local in range(0, duracion_estimulo_sfa, dt_sfa):
            tiempo_sim_actual_sfa = t_sfa_local # Tiempo local para esta prueba
            impulsos_externos_sfa = {N_SFA_TEST_ID: magnitud_estimulo_sfa}
            
            disparos_paso_sfa = red_sfa_test.actualizar_estado_red(
                tiempo_actual=tiempo_sim_actual_sfa,
                dt=dt_sfa,
                impulsos_externos=impulsos_externos_sfa,
                aplicar_stdp_global=False
            )
            
            # La neurona Izhikevich ahora actualiza sus propios historiales SFA internamente
            # historia_potencial_sfa.append(neurona_sfa.potencial_membrana)
            # if neurona_sfa.usa_sfa:
            #     historia_corriente_sfa.append(neurona_sfa.corriente_adaptacion_sfa)

            if N_SFA_TEST_ID in disparos_paso_sfa:
                tiempos_disparo_sfa.append(tiempo_sim_actual_sfa)
        
        print(f"Número total de disparos de {N_SFA_TEST_ID}: {len(tiempos_disparo_sfa)}")
        if len(tiempos_disparo_sfa) > 1:
            isis_sfa = np.diff(tiempos_disparo_sfa)
            print(f"Intervalos Inter-Spike (ISIs) para {N_SFA_TEST_ID} (ms): {isis_sfa}")
            if len(isis_sfa) > 5:
                mid_point = len(isis_sfa) // 2
                first_half_isis = isis_sfa[:mid_point]
                second_half_isis = isis_sfa[mid_point:]
                if len(first_half_isis) > 0 and len(second_half_isis) > 0:
                    mean_isi_first_half = np.mean(first_half_isis)
                    mean_isi_second_half = np.mean(second_half_isis)
                    print(f"    Mean ISI primera mitad: {mean_isi_first_half:.2f} ms, Mean ISI segunda mitad: {mean_isi_second_half:.2f} ms")
                    if mean_isi_second_half > mean_isi_first_half + 0.1: 
                        print("    SFA DEMOSTRADA: El ISI promedio aumentó significativamente.")
                    else:
                        print("    SFA NO CLARA: El ISI promedio no aumentó significativamente. Revisar parámetros o lógica.")
                else:
                    print("    No suficientes ISIs en ambas mitades para comparar promedios.")
            elif len(isis_sfa) > 1:
                 print("    No suficientes disparos para un análisis robusto de la tendencia de ISIs (se necesitan >5 ISIs).")
            else:
                print("    No suficientes disparos para analizar la tendencia de ISIs.")
        else:
            print(f"No suficientes disparos ({len(tiempos_disparo_sfa)}) para calcular ISIs.")

        if hasattr(neurona_sfa, 'historial_tiempo_sfa') and neurona_sfa.historial_tiempo_sfa:
            print(f"INFO: Generando gráfico de dinámica SFA para {N_SFA_TEST_ID}...")
            plot_sfa_dynamics(
                tiempos=neurona_sfa.historial_tiempo_sfa,
                historiales_vm=neurona_sfa.historial_potencial_membrana_sfa,
                historiales_i_sfa=neurona_sfa.historial_corriente_adaptacion_sfa,
                historiales_umbral_eff=neurona_sfa.historial_umbral_efectivo_sfa,
                umbral_base=ps.UMBRAL_DISPARO_BASE,
                titulo=f"Dinámica SFA de la Neurona {N_SFA_TEST_ID}"
            )
        else:
            print(f"INFO: No se generó gráfico SFA para {N_SFA_TEST_ID} porque no se registraron datos históricos en la neurona.")

    else:
        print(f"ADVERTENCIA: Neurona {N_SFA_TEST_ID} no encontrada en la red principal para la prueba SFA.")
    print("--- Fin Escenario de Prueba de SFA ---")
