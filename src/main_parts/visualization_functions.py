from configuracion import parametros_simulacion as ps
from src.visualizacion.utilidades_graficas import plot_multiple_synaptic_weights_evolution

def plot_weight_evolution_summary(historial_pesos_detectores):
    """
    Genera y muestra la gráfica de evolución de pesos sinápticos para los detectores,
    agrupándolos por G1, G2 y G3, y utilizando el número de épocas correcto para cada grupo.
    """
    if not historial_pesos_detectores or not any(hist_detector for hist_detector in historial_pesos_detectores.values()):
        print("No hay datos de historial de pesos consolidados (historial_pesos_detectores) para graficar.")
        return

    historial_g1 = {}
    historial_g2 = {}
    historial_g3 = {}

    # Nombres literales de los detectores G2 y G3 (no están en ps)
    G2_DETECTOR_ID = 'N_G2_DetectorAB'
    G3_DETECTOR_ID = 'N_G3_Detector_Evento_A_AB'

    for detector_id, pesos_data in historial_pesos_detectores.items():
        if detector_id.startswith("N_Detector_Secuencia"):
            historial_g1[detector_id] = pesos_data
        elif detector_id == G2_DETECTOR_ID:
            historial_g2[detector_id] = pesos_data
        elif detector_id == G3_DETECTOR_ID:
            historial_g3[detector_id] = pesos_data
        # else: # Podría haber otros detectores no categorizados
            # print(f"ADVERTENCIA: Detector {detector_id} no categorizado para graficación de pesos.")

    if historial_g1:
        print("\nINFO: Generando gráfica de evolución de pesos para los detectores del Grupo 1...")
        plot_multiple_synaptic_weights_evolution(
            historial_pesos_detectores=historial_g1,
            num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE,
            titulo_grafico="Evolución de Pesos Sinápticos Durante Entrenamiento (Detectores Grupo 1)"
        )
    
    if historial_g2:
        print("\nINFO: Generando gráfica de evolución de pesos para el detector del Grupo 2...")
        plot_multiple_synaptic_weights_evolution(
            historial_pesos_detectores=historial_g2,
            num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_BASE, # Corregido: G2 usa las épocas BASE (25)
            titulo_grafico="Evolución de Pesos Sinápticos Durante Entrenamiento (Detector Grupo 2)"
        )

    if historial_g3:
        print("\nINFO: Generando gráfica de evolución de pesos para el detector del Grupo 3...")
        plot_multiple_synaptic_weights_evolution(
            historial_pesos_detectores=historial_g3,
            num_epocas=ps.NUM_EPOCAS_ENTRENAMIENTO_G3,
            titulo_grafico="Evolución de Pesos Sinápticos Durante Entrenamiento (Detector Grupo 3)"
        )
