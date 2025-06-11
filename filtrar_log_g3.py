import os
import glob

def encontrar_log_mas_reciente(directorio_logs="logs"):
    archivos_log = glob.glob(os.path.join(directorio_logs, "simulacion_log_*.txt"))
    if not archivos_log:
        return None
    return max(archivos_log, key=os.path.getctime)

def filtrar_log_entrenamiento_g3(archivo_log_entrada, archivo_log_salida):
    patrones_interes = [
        "DEBUG PRE_FIRE_CHECK:",
        "DEBUG G1_TRAIN_STIM: Potencial de N_Detector_Secuencia123",
        "DEBUG G1_TRAIN_OBS: Potencial de N_Detector_Secuencia123",
        "DEBUG G1_TRAIN_STIM: Potencial de N_Detector_Secuencia321",
        "DEBUG G1_TRAIN_OBS: Potencial de N_Detector_Secuencia321",
        "G1 Detector N_Detector_Secuencia123 disparó",
        "G1 Detector N_Detector_Secuencia321 disparó",
        # Añadido para asegurar que capturamos el disparo de G2_AB
        "G2 Detector N_G2_DetectorAB disparó", 
        "N_G2_DetectorAB disparó", # Otra posible forma en que podría estar logueado
        "Fin Época", # Para capturar los pesos de G3
        "Época", # Para ver el inicio de cada época
        "Activando G1_A (N_Detector_Secuencia123)",
        "Activando G2_AB (N_G2_DetectorAB)",
        "N_G3_Detector_Evento_A_AB disparó" # Si existe tal mensaje
    ]

    en_fase_entrenamiento_g3 = False
    lineas_filtradas = []

    try:
        with open(archivo_log_entrada, 'r', encoding='utf-8') as f_in:
            for linea in f_in:
                if "--- Iniciando Fase de Entrenamiento G3 para N_G3_Detector_Evento_A_AB ---" in linea:
                    en_fase_entrenamiento_g3 = True
                    lineas_filtradas.append("\n" + "="*20 + " INICIO FASE ENTRENAMIENTO G3 " + "="*20 + "\n")
                    lineas_filtradas.append(linea)
                    continue
                
                if "--- Fin Fase de Entrenamiento G3 ---" in linea and en_fase_entrenamiento_g3:
                    lineas_filtradas.append(linea)
                    lineas_filtradas.append("="*20 + " FIN FASE ENTRENAMIENTO G3 " + "="*20 + "\n")
                    en_fase_entrenamiento_g3 = False
                    # Podríamos parar aquí si solo nos interesa la primera fase de entrenamiento G3
                    # break 

                if en_fase_entrenamiento_g3:
                    if any(patron in linea for patron in patrones_interes):
                        # Asegurarnos que 'Fin Época' también contenga 'Pesos G3 ->'
                        if "Fin Época" in linea and "Pesos G3 ->" not in linea:
                            continue
                        lineas_filtradas.append(linea)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de log {archivo_log_entrada}")
        return
    except Exception as e:
        print(f"Ocurrió un error leyendo el log: {e}")
        return

    try:
        with open(archivo_log_salida, 'w', encoding='utf-8') as f_out:
            for linea_filtrada in lineas_filtradas:
                f_out.write(linea_filtrada)
        print(f"Log filtrado guardado en: {archivo_log_salida}")
    except Exception as e:
        print(f"Ocurrió un error escribiendo el log filtrado: {e}")

if __name__ == "__main__":
    log_reciente = encontrar_log_mas_reciente()
    if log_reciente:
        print(f"Procesando log más reciente: {log_reciente}")
        nombre_base_log_reciente = os.path.basename(log_reciente)
        archivo_salida = os.path.join("logs", f"filtered_g3_training_{nombre_base_log_reciente}")
        filtrar_log_entrenamiento_g3(log_reciente, archivo_salida)
    else:
        print("No se encontraron archivos de log para procesar.")
