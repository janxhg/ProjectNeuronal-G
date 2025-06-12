# Contendrá funciones para la visualización de datos

import matplotlib.pyplot as plt
import numpy as np
import os # Añadido para manejar rutas y crear carpetas
from datetime import datetime # Añadido para timestamps en nombres de archivo
import re # Añadido para sanitizar nombres de archivo

def plot_evolucion_pesos(epocas_historial, historial_pesos_epocas, conexiones_a_plotear, titulo_grafico="Evolución de Pesos Sinápticos"):
    """
    Grafica la evolución de los pesos sinápticos especificados a lo largo de las épocas.
    Guarda la gráfica en logs/graficas/ y luego la muestra (si el backend lo permite).
    """
    if not historial_pesos_epocas or not epocas_historial:
        print("No hay historial de pesos o épocas para graficar.")
        return

    fig = plt.figure(figsize=(12, 7)) # Obtener referencia a la figura

    marcadores = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h']
    lineas = ['-', '--', '-.', ':']

    for i, (id_pre, id_post) in enumerate(conexiones_a_plotear):
        pesos_conexion = []
        for epoca_data in historial_pesos_epocas:
            peso = epoca_data.get((id_pre, id_post), np.nan)
            pesos_conexion.append(peso)
        
        label_conexion = f'{id_pre} -> {id_post}'
        marcador_actual = marcadores[i % len(marcadores)]
        linea_actual = lineas[(i // len(marcadores)) % len(lineas)]

        plt.plot(epocas_historial, pesos_conexion, marker=marcador_actual, linestyle=linea_actual, label=label_conexion)

    plt.title(titulo_grafico)
    plt.xlabel('Época')
    plt.ylabel('Peso Sináptico')
    plt.legend(loc='best')
    plt.grid(True)
    
    if epocas_historial:
        min_epoca = min(epocas_historial)
        max_epoca = max(epocas_historial)
        if len(epocas_historial) <= 20:
             plt.xticks(epocas_historial)
        else:
            # Para muchas épocas, usar np.linspace para generar ticks. Asegurar que sean enteros.
            num_ticks_deseados = 10
            # Asegurar que num_ticks no exceda la cantidad de épocas únicas disponibles
            num_ticks = min(len(np.unique(epocas_historial)), num_ticks_deseados) 
            if num_ticks > 0: # Evitar error con linspace si num_ticks es 0
                ticks = np.linspace(min_epoca, max_epoca, num=num_ticks, dtype=int)
                plt.xticks(ticks)
            # Si num_ticks es 0 (ej. epocas_eje_x vacío), matplotlib manejará los ticks

    plt.tight_layout()

    # Guardar la gráfica
    graficas_dir = os.path.join("logs", "graficas")
    os.makedirs(graficas_dir, exist_ok=True)
    
    # Sanitizar el título para usarlo en el nombre del archivo
    nombre_base_sanitizado = re.sub(r'[\\/*?:"<>|]', "", titulo_grafico).replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{nombre_base_sanitizado}_{timestamp}.png"
    ruta_completa_archivo = os.path.join(graficas_dir, nombre_archivo)
    
    try:
        plt.savefig(ruta_completa_archivo)
        print(f"INFO: Gráfica guardada en: {ruta_completa_archivo}")
    except Exception as e:
        print(f"ERROR: No se pudo guardar la gráfica en {ruta_completa_archivo}: {e}")

    plt.close(fig) # Cerrar la figura para liberar memoria


def plot_sfa_dynamics(tiempos, historiales_vm, historiales_i_sfa, historiales_umbral_eff, umbral_base, titulo="Dinámica SFA de Neurona de Prueba"):
    """
    Grafica la dinámica de la Spike-Frequency Adaptation (SFA) para una neurona.
    Guarda la gráfica en logs/graficas/ y luego la muestra (si el backend lo permite).
    """
    if not tiempos or not historiales_vm or not historiales_i_sfa or not historiales_umbral_eff:
        print("INFO: No hay suficientes datos para graficar la dinámica SFA.")
        return

    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True) # fig ya es la referencia
    fig.suptitle(titulo, fontsize=16)

    # Potencial de Membrana
    axs[0].plot(tiempos, historiales_vm, label='Potencial de Membrana (Vm)', color='blue')
    axs[0].axhline(umbral_base, color='gray', linestyle=':', linewidth=1, label=f'Umbral Base ({umbral_base:.2f} mV)')
    axs[0].set_ylabel('Potencial de Membrana (mV)')
    axs[0].legend(loc='upper right')
    axs[0].grid(True, linestyle='--', alpha=0.7)

    # Corriente de Adaptación SFA
    axs[1].plot(tiempos, historiales_i_sfa, label='Corriente de Adaptación (I_sfa)', color='green')
    axs[1].set_ylabel('Corriente SFA (mV)') # La corriente SFA se suma al umbral, por eso unidades de mV
    axs[1].legend(loc='upper right')
    axs[1].grid(True, linestyle='--', alpha=0.7)

    # Umbral de Disparo Efectivo
    axs[2].plot(tiempos, historiales_umbral_eff, label='Umbral Efectivo', color='red')
    axs[2].axhline(umbral_base, color='gray', linestyle=':', linewidth=1, label=f'Umbral Base ({umbral_base:.2f} mV)')
    axs[2].set_ylabel('Umbral de Disparo (mV)')
    axs[2].set_xlabel('Tiempo (ms)')
    axs[2].legend(loc='upper right')
    axs[2].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout(rect=[0, 0, 1, 0.96]) # Ajustar para el suptitle

    # Guardar la gráfica
    graficas_dir = os.path.join("logs", "graficas")
    os.makedirs(graficas_dir, exist_ok=True)
    
    nombre_base_sanitizado = re.sub(r'[\\/*?:"<>|]', "", titulo).replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{nombre_base_sanitizado}_{timestamp}.png"
    ruta_completa_archivo = os.path.join(graficas_dir, nombre_archivo)
    
    try:
        plt.savefig(ruta_completa_archivo)
        print(f"INFO: Gráfica guardada en: {ruta_completa_archivo}")
    except Exception as e:
        print(f"ERROR: No se pudo guardar la gráfica en {ruta_completa_archivo}: {e}")

    plt.close(fig) # Cerrar la figura para liberar memoria

# Ejemplo de uso (comentado para no interferir):
# if __name__ == '__main__':
#     epocas_ej = [1, 2, 3, 4, 5, 10, 15, 20]
#     historial_ej = [
#         {('N1','ND'): 0.1, ('N2','ND'): 0.5}, {('N1','ND'): 0.15, ('N2','ND'): 0.5},
#         {('N1','ND'): 0.2, ('N2','ND'): 0.45}, {('N1','ND'): 0.25, ('N2','ND'): 0.45},
#         {('N1','ND'): 0.3, ('N2','ND'): 0.4}, {('N1','ND'): 0.35, ('N2','ND'): 0.4},
#         {('N1','ND'): 0.4, ('N2','ND'): 0.35}, {('N1','ND'): 0.45, ('N2','ND'): 0.35},
#         {('N1','ND'): 0.5, ('N2','ND'): 0.3}
#     ]
#     # Asegurarse que historial_ej tenga la misma longitud que epocas_ej
#     historial_ej = historial_ej[:len(epocas_ej)] 

#     conexiones_ej = [('N1','ND'), ('N2','ND')]
#     plot_evolucion_pesos(epocas_ej, historial_ej, conexiones_ej, "Ejemplo de Gráfico de Pesos")


def plot_multiple_synaptic_weights_evolution(historial_pesos_detectores, num_epocas, titulo_grafico="Evolución de Pesos Sinápticos por Detector"):
    """
    Grafica la evolución de los pesos sinápticos para múltiples detectores y sus conexiones.
    Guarda la gráfica en logs/graficas/ y luego la muestra (si el backend lo permite).
    """
    if not historial_pesos_detectores:
        print("INFO: No hay historial de pesos de detectores para graficar.")
        return

    fig = plt.figure(figsize=(14, 8)) # Obtener referencia a la figura
    
    epocas_eje_x = list(range(1, num_epocas + 1))

    marcadores = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', '+', 'x']
    lineas = ['-', '--', '-.', ':']
    
    plot_idx = 0 # Para ciclar marcadores y estilos de línea globalmente

    for detector_idx, (detector_id, conexiones_historial) in enumerate(historial_pesos_detectores.items()):
        if not conexiones_historial:
            print(f"INFO: No hay historial de conexiones para el detector {detector_id}.")
            continue
            
        for (id_pre, id_post), lista_pesos in conexiones_historial.items():
            if len(lista_pesos) != num_epocas:
                print(f"ADVERTENCIA: La longitud de la lista de pesos ({len(lista_pesos)}) para la conexión {id_pre}->{id_post} del detector {detector_id} no coincide con num_epocas ({num_epocas}). Se omitirá esta conexión.")
                continue

            label_conexion = f'{detector_id}: {id_pre} -> {id_post}'
            marcador_actual = marcadores[plot_idx % len(marcadores)]
            linea_actual = lineas[(plot_idx // len(marcadores)) % len(lineas)]
            
            plt.plot(epocas_eje_x, lista_pesos, marker=marcador_actual, linestyle=linea_actual, label=label_conexion)
            plot_idx += 1

    if plot_idx == 0: # No se ploteó nada
        print("INFO: No se graficó ninguna conexión. Verifique los datos de entrada y las advertencias.")
        plt.close(fig) # Cierra la figura vacía si no se ploteó nada
        return

    plt.title(titulo_grafico)
    plt.xlabel('Época de Entrenamiento')
    plt.ylabel('Peso Sináptico')
    plt.legend(loc='best', fontsize='small')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    if epocas_eje_x:
        min_epoca = min(epocas_eje_x)
        max_epoca = max(epocas_eje_x)
        if len(epocas_eje_x) <= 20:
             plt.xticks(epocas_eje_x)
        else:
            # Para muchas épocas, usar np.linspace para generar ticks. Asegurar que sean enteros.
            num_ticks_deseados = 10
            # Asegurar que num_ticks no exceda la cantidad de épocas únicas disponibles
            num_ticks = min(len(np.unique(epocas_eje_x)), num_ticks_deseados) 
            if num_ticks > 0: # Evitar error con linspace si num_ticks es 0
                ticks = np.linspace(min_epoca, max_epoca, num=num_ticks, dtype=int)
                plt.xticks(ticks)
            # Si num_ticks es 0 (ej. epocas_eje_x vacío), matplotlib manejará los ticks

    plt.tight_layout()

    # Guardar la gráfica
    graficas_dir = os.path.join("logs", "graficas")
    os.makedirs(graficas_dir, exist_ok=True)
    
    nombre_base_sanitizado = re.sub(r'[\\/*?:"<>|]', "", titulo_grafico).replace(" ", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"{nombre_base_sanitizado}_{timestamp}.png"
    ruta_completa_archivo = os.path.join(graficas_dir, nombre_archivo)
    
    try:
        plt.savefig(ruta_completa_archivo)
        print(f"INFO: Gráfica guardada en: {ruta_completa_archivo}")
    except Exception as e:
        print(f"ERROR: No se pudo guardar la gráfica en {ruta_completa_archivo}: {e}")
    
    plt.close(fig) # Cerrar la figura para liberar memoria