import numpy as np
# Ajustar las importaciones para la nueva estructura de directorios
from src.neurona.neurona_clase import NeuronaBiologica
from src.neurona.tipos_neurona import EXCITATORIA, INHIBITORIA

class RedBiologica:
    def __init__(self, nombre_red="mi_red", verbose=True, verbose_config=False, verbose_entrenamiento=True):
        """Inicializa la red neuronal."""
        print("DEBUG: Iniciando constructor RedBiologica.__init__")
        self.nombre = nombre_red
        self.neuronas = {} # Diccionario para almacenar neuronas por ID
        self.conexiones_salientes = {} # Diccionario para almacenar conexiones salientes: {id_origen: {id_destino: info_conexion}}
        self.tiempo_actual_simulacion = 0
        self.historial_pesos_epocas = [] # Lista de dicts: { (pre_id, post_id): peso }
        self.epocas_historial = []      # Lista de números de época
        self.verbose = verbose  # General verbosity for simulation steps, propagation etc.
        self.verbose_config = verbose_config  # Verbosity for network setup, neuron/connection adding, reset
        self.verbose_entrenamiento = verbose_entrenamiento  # Verbosity for training specific logs like weight registration, direct impulses during training

    def agregar_neurona(self, neurona):
        """Agrega una neurona a la red."""
        if not isinstance(neurona, NeuronaBiologica):
            raise TypeError("Solo se pueden agregar instancias de NeuronaBiologica a la red.")
        if neurona.id in self.neuronas:
            print(f"Advertencia: Ya existe una neurona con ID '{neurona.id}'. No se agregó la nueva neurona.")
            return
        self.neuronas[neurona.id] = neurona
        if self.verbose:
            print(f"Neurona '{neurona.id}' agregada a la red '{self.nombre}'.")

    def conectar_neuronas(self, id_neurona_origen, id_neurona_destino, peso_inicial, plastica=True):
        """Conecta dos neuronas en la red.

        Args:
            id_neurona_origen (str): ID de la neurona presináptica.
            id_neurona_destino (str): ID de la neurona postsináptica.
            peso_inicial (float): Peso inicial de la sinapsis.
            tipo_conexion (str, optional): Tipo de conexión (ej. EXCITATORIA, INHIBITORIA).
                                         Si no se especifica, se infiere del tipo de neurona origen.
            plastica (bool, optional): Indica si la conexión es sujeta a plasticidad. Por defecto True.
        """
        neurona_origen = self.neuronas.get(id_neurona_origen)
        neurona_destino = self.neuronas.get(id_neurona_destino)

        if not neurona_origen:
            print(f"Error al conectar: No se encontró la neurona de origen con ID '{id_neurona_origen}'.")
            return
        if not neurona_destino:
            print(f"Error al conectar: No se encontró la neurona de destino con ID '{id_neurona_destino}'.")
            return
        
        # El tipo de conexión se infiere directamente del tipo de la neurona de origen.
        tipo_conexion_inferido = neurona_origen.tipo_neurona

        if tipo_conexion_inferido == INHIBITORIA:
            peso_real = -abs(peso_inicial) # Asegura que el peso sea negativo para sinapsis inhibitorias
        elif tipo_conexion_inferido == EXCITATORIA:
            peso_real = abs(peso_inicial)  # Asegura que el peso sea positivo para sinapsis excitatorias
        else:
            # Esto no debería ocurrir si tipo_neurona siempre es EXCITATORIA o INHIBITORIA.
            # Si ocurre, es un estado inesperado.
            print(f"ADVERTENCIA: Tipo de neurona origen '{neurona_origen.tipo_neurona}' no es EXCITATORIA ni INHIBITORIA. Usando peso_inicial ({peso_inicial}) tal cual.")
            peso_real = peso_inicial

        neurona_destino.agregar_conexion_entrante(
            id_neurona_presinaptica=id_neurona_origen, 
            peso_sinaptico=peso_real, 
            tipo_neurona_presinaptica=neurona_origen.tipo_neurona,
            plastica=plastica
        )

        if id_neurona_origen not in self.conexiones_salientes:
            self.conexiones_salientes[id_neurona_origen] = {}
        self.conexiones_salientes[id_neurona_origen][id_neurona_destino] = {
            'peso': peso_real, 
            'tipo': tipo_conexion_inferido # Usar el tipo inferido
        }
        
        if self.verbose:
            print(f"Conexión establecida de '{id_neurona_origen}' a '{id_neurona_destino}' con peso inicial {peso_real:.3f}.")

    def simular_paso(self, tiempo_actual_global, dt=1, impulsos_externos=None, aplicar_stdp=True):
        """Simula un paso de tiempo en la red.

        Args:
            tiempo_actual_global (int): El tiempo actual global de la simulación.
            dt (int): Incremento de tiempo para este paso.
            impulsos_externos (dict, optional): Diccionario {id_neurona: peso_impulso} para estímulos externos.
            aplicar_stdp (bool): Si es True, se aplican las reglas de plasticidad STDP. Por defecto es True.
        """
        self.tiempo_actual_simulacion = tiempo_actual_global
        # neuronas_disparadas_en_este_paso = [] # No parece usarse localmente

        if impulsos_externos:
            for id_neurona, peso_impulso in impulsos_externos.items():
                neurona_objetivo = self.neuronas.get(id_neurona)
                if neurona_objetivo:
                    neurona_objetivo.potencial_membrana += peso_impulso
                    if self.verbose:
                        print(f"RED: Impulso externo de {peso_impulso:.2f} a neurona '{id_neurona}' en t={self.tiempo_actual_simulacion}")

        disparos_en_paso = self.actualizar_estado_red(tiempo_actual=self.tiempo_actual_simulacion, dt=dt, aplicar_stdp_global=aplicar_stdp, neurona_objetivo_stdp=None)
        
        # La propagación de impulsos de neuronas que dispararon ya está integrada en actualizar_estado_red
        # por lo que no es necesario un bucle adicional aquí si actualizar_estado_red lo maneja.
        # Revisando actualizar_estado_red, sí parece manejar la propagación.
        return disparos_en_paso

    def obtener_peso_sinaptico(self, id_neurona_origen, id_neurona_destino):
        """Obtiene el peso sináptico actual de una conexión específica."""
        neurona_destino_obj = self.neuronas.get(id_neurona_destino)
        if neurona_destino_obj and id_neurona_origen in neurona_destino_obj.conexiones_entrantes:
            return neurona_destino_obj.conexiones_entrantes[id_neurona_origen]['peso']
        # if self.verbose: # Podríamos añadir un print si la conexión no se encuentra
        #     print(f"Advertencia: Conexión de {id_neurona_origen} a {id_neurona_destino} no encontrada o peso no disponible.")
        return None # O np.nan, o levantar un error

    def actualizar_estado_red(self, tiempo_actual, dt=1, aplicar_stdp_global=True, neurona_objetivo_stdp=None, impulsos_externos=None):
        self.tiempo_actual_simulacion = tiempo_actual # Asegurar que el tiempo de la red se actualice al inicio del paso
        disparos_en_paso = []

        # Aplicar impulsos externos ANTES de la actualización de estado normal de las neuronas
        if impulsos_externos:
            # NUEVO PRINT PARA DEPURAR FASE DE PRUEBAS
            if tiempo_actual >= 400: # Las pruebas comienzan en t_glob=400 o 401
                print(f"DEBUG RED (TESTING PHASE at t={tiempo_actual}): Received impulsos_externos: {impulsos_externos}")
            
            for id_neurona, peso_impulso in impulsos_externos.items():
                neurona_objetivo = self.neuronas.get(id_neurona)
                if neurona_objetivo:
                    # Aplicar el impulso directamente al potencial de membrana
                    neurona_objetivo.potencial_membrana += peso_impulso
                    # Mantenemos este print para ver la aplicación, pero es menos verboso que los anteriores.
                    if neurona_objetivo.id.startswith("N_Pre") or neurona_objetivo.id == "N_Detector_Secuencia123":
                        print(f"RED: Impulso externo directo de {peso_impulso:.2f} a neurona '{id_neurona}' en t={tiempo_actual} aplicado en actualizar_estado_red.")

        for neurona_id, neurona in self.neuronas.items():
            aplicar_stdp_local = aplicar_stdp_global
            if neurona_objetivo_stdp is not None:
                if neurona_id == neurona_objetivo_stdp:
                    aplicar_stdp_local = True 
                else: 
                    aplicar_stdp_local = False
            
            pot_antes_actualizar_estado = neurona.potencial_membrana
            disparo = neurona.actualizar_estado(tiempo_actual, dt, aplicar_stdp=aplicar_stdp_local)

            if tiempo_actual >= 400 and neurona_id in ['N_Pre1', 'N_Pre2', 'N_Pre3'] and self.verbose:
                print(f"DEBUG PRE-SYN (t_glob={tiempo_actual}): {neurona_id:<25} | Vm_pre_update: {pot_antes_actualizar_estado:>6.2f} | Vm_post_update: {neurona.potencial_membrana:>7.2f} | Umbral: {neurona.umbral_disparo:>5.2f} | Disparó: {str(disparo):<5} | t_ult_disp: {neurona.ultima_vez_disparo}")

            if disparo:
                disparos_en_paso.append(neurona.id)
        
        if disparos_en_paso:
            for neurona_id_que_disparo in disparos_en_paso:
                neurona_que_disparo = self.neuronas[neurona_id_que_disparo]
                # Solo propagar si la neurona que disparó tiene conexiones salientes registradas
                if neurona_id_que_disparo in self.conexiones_salientes:
                    for id_neurona_destino, _ in self.conexiones_salientes[neurona_id_que_disparo].items():
                        if id_neurona_destino in self.neuronas:
                            neurona_destino = self.neuronas[id_neurona_destino]
                            
                            aplicar_stdp_recepcion_local = aplicar_stdp_global
                            if neurona_objetivo_stdp is not None:
                                if neurona_destino.id == neurona_objetivo_stdp:
                                    aplicar_stdp_recepcion_local = True
                                else:
                                    aplicar_stdp_recepcion_local = False
                            
                            # Leer el peso actualizado desde la conexión entrante de la neurona destino
                            if neurona_id_que_disparo in neurona_destino.conexiones_entrantes:
                                peso_actualizado = neurona_destino.conexiones_entrantes[neurona_id_que_disparo]['peso']
                                neurona_destino.recibir_impulso(neurona_que_disparo.id, peso_actualizado, tiempo_actual, aplicar_stdp=aplicar_stdp_recepcion_local)
                                if self.verbose:
                                    print(f"RED: Propagando impulso de '{neurona_id_que_disparo}' a '{id_neurona_destino}' con peso {peso_actualizado:.3f} (tipo: {neurona_que_disparo.tipo_neurona}) en t={tiempo_actual}")
                            else: 
                                if neurona_id_que_disparo.startswith("N_Pre") and neurona_destino.id == "N_Detector_Secuencia123" and self.verbose:
                                    print(f"DEBUG RED ERROR: Neurona '{neurona_id_que_disparo}' disparó y tiene conexión saliente a '{id_neurona_destino}', PERO '{id_neurona_destino}' NO tiene la conexión entrante registrada desde '{neurona_id_que_disparo}'. Conexiones entrantes de '{id_neurona_destino}': {list(neurona_destino.conexiones_entrantes.keys())}")
                        else:
                            if neurona_id_que_disparo.startswith("N_Pre") and self.verbose:
                                print(f"DEBUG RED WARNING: Target '{id_neurona_destino}' for '{neurona_id_que_disparo}' not found in self.neuronas.")
                else:
                    if neurona_id_que_disparo.startswith("N_Pre") and self.verbose:
                        print(f"DEBUG RED ERROR: Firing PreNeuron '{neurona_id_que_disparo}' NOT in self.conexiones_salientes. Keys: {list(self.conexiones_salientes.keys())}")
        self.tiempo_actual_simulacion = tiempo_actual + dt # Actualizar el tiempo de simulación de la red
        return disparos_en_paso

    def imprimir_estado_red(self, detallado=False):
        """Imprime el estado actual de la red."""
        if not self.verbose_config and not detallado:
            return

        print(f"\n--- Estado de la Red: '{self.nombre}' en t={self.tiempo_actual_simulacion} ---")
        if not self.neuronas:
            print("La red está vacía.")
            return
        
        for neurona_id, neurona in self.neuronas.items():
            print(f"  Neurona ID: {neurona_id} ({neurona.tipo_neurona})")
            print(f"    Potencial: {neurona.potencial_membrana:.3f}")
            print(f"    Umbral: {neurona.umbral_disparo:.3f}")
            print(f"    Último disparo: {neurona.ultima_vez_disparo if neurona.ultima_vez_disparo != -np.inf else 'Nunca'}")
            if detallado:
                print(f"    Conexiones Entrantes:")
                if neurona.conexiones_entrantes:
                    for pre_id, info_con in neurona.conexiones_entrantes.items():
                        tipo_presinaptico = info_con.get('tipo_neurona_presinaptica', 'N/A')
                        ultimo_impulso = info_con.get('ultima_vez_impulso_recibido', 'N/A')
                        print(f"      De '{pre_id}': Peso={info_con['peso']:.3f}, TipoPresinaptico='{tipo_presinaptico}', UltimoImpulsoRecibido={ultimo_impulso}")
                else:
                    print("      Ninguna.")
                
                print(f"    Conexiones Salientes Registradas en RedBiologica:")
                if neurona_id in self.conexiones_salientes and self.conexiones_salientes[neurona_id]:
                    for post_id, info_conexion_saliente in self.conexiones_salientes[neurona_id].items():
                        neurona_destino_obj = self.neuronas.get(post_id)
                        if neurona_destino_obj and neurona_id in neurona_destino_obj.conexiones_entrantes:
                            peso_real_actual = neurona_destino_obj.conexiones_entrantes[neurona_id]['peso']
                            print(f"      A: {post_id}, Tipo Conexión: {info_conexion_saliente.get('tipo', 'N/A')}, Peso (actual): {peso_real_actual:.3f}")
                        else:
                            print(f"      A: {post_id}, Tipo Conexión: {info_conexion_saliente.get('tipo', 'N/A')} (Peso actual no disponible o conexión inconsistente)")
                else:
                    print("      Ninguna")
        print("-------------------------------------")

    def get_umbral_neurona(self, neurona_id):
        """Obtiene el umbral de disparo de una neurona específica."""
        neurona = self.neuronas.get(neurona_id)
        if neurona:
            return neurona.umbral_disparo
        if self.verbose_config:
            print(f"RED WARN: Neurona '{neurona_id}' no encontrada al intentar obtener umbral.")
        return None

    def set_umbral_neurona(self, neurona_id, nuevo_umbral):
        """Establece el umbral de disparo de una neurona específica."""
        neurona = self.neuronas.get(neurona_id)
        if neurona:
            neurona.umbral_disparo = nuevo_umbral
            if self.verbose_config: # Usar verbose_config para este tipo de log
                print(f"RED CONFIG: Umbral de '{neurona_id}' establecido a {nuevo_umbral:.2f}")
            return True
        if self.verbose_config:
            print(f"RED WARN: Neurona '{neurona_id}' no encontrada al intentar establecer umbral.")
        return False

    def get_potencial_reposo_neurona(self, neurona_id):
        """Obtiene el potencial de reposo de una neurona específica."""
        neurona = self.neuronas.get(neurona_id)
        if neurona:
            return neurona.potencial_reposo
        if self.verbose_config:
            print(f"RED WARN: Neurona '{neurona_id}' no encontrada al intentar obtener potencial de reposo.")
        return None

    def registrar_pesos_epoca(self, epoca, conexiones_a_registrar):
        """Registra los pesos de las conexiones especificadas al final de una época.

        Args:
            epoca (int): Número de la época actual.
            conexiones_a_registrar (list of tuples): Lista de tuplas (id_pre, id_post)
                                                      cuyos pesos se deben registrar.
        """
        pesos_epoca_actual = {}
        for id_pre, id_post in conexiones_a_registrar:
            neurona_post = self.neuronas.get(id_post)
            if neurona_post and id_pre in neurona_post.conexiones_entrantes:
                pesos_epoca_actual[(id_pre, id_post)] = neurona_post.conexiones_entrantes[id_pre]['peso']
            else:
                # Podría ser que la conexión no exista o el ID sea incorrecto
                pesos_epoca_actual[(id_pre, id_post)] = np.nan # Marcar como no disponible
                if self.verbose:
                    print(f"Advertencia al registrar pesos: Conexión {id_pre}->{id_post} no encontrada.")
        
        self.historial_pesos_epocas.append(pesos_epoca_actual)
        self.epocas_historial.append(epoca)
        if self.verbose:
            print(f"Pesos registrados para la época {epoca}: {pesos_epoca_actual}")

    def aplicar_impulso(self, id_neurona_destino, magnitud_impulso, tiempo_actual):
        """Aplica un impulso externo directo a una neurona específica."""
        neurona_destino = self.neuronas.get(id_neurona_destino)
        if neurona_destino:
            # Para impulsos externos, no aplicamos STDP directamente aquí, 
            # y el 'id_neurona_presinaptica' puede ser conceptual (ej. "EXTERNO").
            # La magnitud del impulso actúa como el 'peso_sinaptico' para este evento.
            neurona_destino.recibir_impulso(
                id_neurona_presinaptica="EXTERNO", 
                peso_sinaptico=magnitud_impulso, 
                tiempo_actual=tiempo_actual, 
                aplicar_stdp=False # Generalmente False para impulsos directos/externos
            )
            if self.verbose_entrenamiento: # Usar una verbosidad más específica si se desea
                print(f"DEBUG RED: Impulso externo de {magnitud_impulso:.2f} aplicado a {id_neurona_destino} en t={tiempo_actual}")
        else:
            if self.verbose:
                print(f"Advertencia: Neurona {id_neurona_destino} no encontrada para aplicar impulso externo.")

    def resetear_estado_red(self):
        """Resetea el estado de todas las neuronas en la red y el tiempo de simulación de la red."""
        for neurona_id, neurona in self.neuronas.items():
            neurona.resetear_estado()
        self.tiempo_actual_simulacion = 0
        if self.verbose:
            print(f"Red '{self.nombre}': Estado de todas las neuronas y tiempo de simulación reseteados.")

    def contar_disparos_neurona(self, neurona_id):
        """Cuenta los disparos registrados en la historia de una neurona específica."""
        neurona = self.neuronas.get(neurona_id)
        if neurona:
            return len(neurona.historia_disparos)
        else:
            if self.verbose:
                print(f"Advertencia: Neurona {neurona_id} no encontrada para contar disparos. Retornando 0.")
            return 0

