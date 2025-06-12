import logging
from collections import defaultdict

from src.core.elementos_neuronales import NeuronaBase, Conexion
from src.core.gestor_plasticidad import GestorPlasticidad
from configuracion.parametros_simulacion import (
    ACTIVAR_PODA_SINAPTICA, FACTOR_PODA_SINAPTICA, PESO_MINIMO_SINAPTICO,
    ACTIVAR_GESTION_PLASTICIDAD
)

class RedDinamica:
    """
    Gestiona una red de neuronas-objeto, permitiendo la creación dinámica
    de neuronas, conexiones y la ejecución de la simulación paso a paso.
    """
    def __init__(self):
        """Inicializa el gestor de la red dinámica."""
        self.conexiones = {}
        self.historial_disparos = defaultdict(list)
        self.neuronas = {}  # Diccionario para almacenar neuronas por ID

        # El Gestor de Plasticidad supervisa la red para crear nuevas estructuras.
        self.gestor_plasticidad = None
        if ACTIVAR_GESTION_PLASTICIDAD:
            self.gestor_plasticidad = GestorPlasticidad(self)
        self.tiempo_actual = 0

    def agregar_neurona(self, neurona):
        """
        Registra una nueva neurona en la red.

        Args:
            neurona (NeuronaBase): La instancia de la neurona a agregar.
        """
        if neurona.id in self.neuronas:
            raise ValueError(f"Ya existe una neurona con el ID '{neurona.id}' en la red.")
        self.neuronas[neurona.id] = neurona
        print(f"Neurona {neurona.id} ({type(neurona).__name__}) agregada a la red.")

    def conectar_neuronas(self, id_origen, id_destino, peso_inicial=1.0, plastica=True):
        """
        Crea una conexión entre dos neuronas existentes en la red.

        Args:
            id_origen (str): El ID de la neurona presináptica.
            id_destino (str): El ID de la neurona postsináptica.
            peso_inicial (float): El peso inicial de la conexión.
            plastica (bool): Si la conexión debe ser plástica (modificable).
        """
        if id_origen not in self.neuronas or id_destino not in self.neuronas:
            raise ValueError("Ambas neuronas (origen y destino) deben existir en la red.")
        
        neurona_origen = self.neuronas[id_origen]
        neurona_destino = self.neuronas[id_destino]
        
        # Clave de la conexión: una tupla que garantiza unicidad y búsqueda eficiente.
        clave_conexion = (id_origen, id_destino)
        if clave_conexion in self.conexiones:
            # Si la conexión ya existe, simplemente actualizamos su peso.
            # Esto puede ocurrir si la plasticidad intenta recrear una conexión existente.
            self.conexiones[clave_conexion].peso = peso_inicial
            print(f"Conexión existente actualizada: {id_origen} -> {id_destino} con nuevo peso {peso_inicial:.2f}")
            return self.conexiones[clave_conexion]

        conexion = neurona_origen.agregar_conexion_saliente(neurona_destino, peso_inicial, plastica=plastica)
        self.conexiones[clave_conexion] = conexion
        print(f"Conexión creada: {id_origen} -> {id_destino} con peso {peso_inicial:.2f}")
        return conexion

    def aplicar_impulso_externo(self, id_neurona_destino, magnitud, id_origen='mundo_exterior'):
        """
        Aplica un impulso a una neurona específica, simulando una entrada.

        Args:
            id_neurona_destino (str): El ID de la neurona que recibirá el impulso.
            magnitud (float): La fuerza del impulso.
            id_origen (str, optional): El ID de la neurona/fuente que origina el impulso.
                                       Defaults to 'mundo_exterior'.
        """
        if id_neurona_destino in self.neuronas:
            self.neuronas[id_neurona_destino].recibir_impulso(magnitud, id_origen=id_origen)
        else:
            print(f"Advertencia: Se intentó aplicar un impulso a una neurona inexistente: {id_neurona_destino}")

    def simular_paso(self):
        """
        Avanza la simulación un único paso de tiempo y devuelve las neuronas que dispararon.
        
        El proceso es síncrono y se divide en fases para asegurar un comportamiento
        determinista y biológicamente más plausible.

        Returns:
            list: Una lista con los IDs de las neuronas que se dispararon en este paso.
        """
        paso_actual = self.tiempo_actual
        neuronas_disparadas_en_paso = []

        # --- Fase 1: Mantenimiento y Plasticidad de la Red ---
        # La red se ajusta a sí misma basándose en la actividad pasada.
        if ACTIVAR_PODA_SINAPTICA:
            for conexion in self.conexiones.values():
                if conexion.plastica:
                    conexion.peso = max(PESO_MINIMO_SINAPTICO, conexion.peso + FACTOR_PODA_SINAPTICA)

        if self.gestor_plasticidad:
            self.gestor_plasticidad.analizar_y_actuar(paso_actual)

        # --- Fase 2: Actualización de Potencial ---
        # Todas las neuronas calculan su nuevo potencial de membrana y deciden si deben disparar.
        # Esto ocurre para todas antes de que ninguna dispare.
        for neurona in self.neuronas.values():
            neurona.actualizar_estado()

        # --- Fase 3: Disparo y Propagación ---
        # Las neuronas marcadas para disparar lo hacen ahora, todas a la vez.
        # Sus impulsos se pondrán en cola para ser procesados en el *siguiente* paso.
        for neurona in self.neuronas.values():
            if neurona.disparo_pendiente:
                neuronas_disparadas_en_paso.append(neurona.id)
                neurona.disparar()
                self.historial_disparos[neurona.id].append(paso_actual)
                # Informar al gestor de plasticidad sobre el disparo para futuro análisis
                if self.gestor_plasticidad:
                    self.gestor_plasticidad.registrar_disparo(neurona, paso_actual)
        
        self.tiempo_actual += 1
        return neuronas_disparadas_en_paso

    def log_estado_conexiones(self, mensaje_contexto=""):
        """Registra el estado actual de todas las conexiones en la red."""
        logging.info(f"--- Estado de Conexiones {mensaje_contexto} ---")
        conexiones_encontradas = False
        # Ordenar por neurona de origen y luego destino para una salida consistente y legible.
        conexiones_ordenadas = sorted(self.conexiones.values(), key=lambda c: (c.neurona_origen.id, c.neurona_destino.id))
        for conexion in conexiones_ordenadas:
            conexiones_encontradas = True
            logging.info(f"  - {conexion}")
        if not conexiones_encontradas:
            logging.info("  - No hay conexiones en la red.")

    def __repr__(self):
        return f"RedDinamica (Neuronas: {len(self.neuronas)}, Tiempo: {self.tiempo_actual})"
