import math
import logging
import uuid
from configuracion.parametros_simulacion import FACTOR_APRENDIZAJE_HEBBIANO, PESO_MINIMO_SINAPTICO, PESO_MAXIMO_SINAPTICO

class Conexion:
    """Representa una conexión sináptica entre dos neuronas.

    Esta clase encapsula la lógica de una sinapsis, incluyendo su fuerza (peso)
    y la capacidad de ajustar dicha fuerza, sentando las bases para la
    plasticidad sináptica.
    """
    def __init__(self, neurona_origen, neurona_destino, peso_inicial=1.0, plastica=True):
        """Inicializa la conexión.

        Args:
            neurona_origen (NeuronaBase): La neurona presináptica.
            neurona_destino (NeuronaBase): La neurona postsináptica.
            peso_inicial (float): La fuerza inicial de la conexión.
            plastica (bool): Si la conexión puede modificar su peso (aprender).
        """
        self.id = str(uuid.uuid4())
        self.neurona_origen = neurona_origen
        self.neurona_destino = neurona_destino
        self.peso = peso_inicial
        self.plastica = plastica
        self.es_recurrente = (neurona_origen.id == neurona_destino.id)

    def ajustar_peso(self, factor_ajuste):
        """Modifica el peso de la sinapsis basado en el aprendizaje.

        Args:
            factor_ajuste (float): El valor a sumar (si es positivo) o restar
                                   (si es negativo) al peso actual.
        """
        if not self.plastica:
            return  # No modificar conexiones no plásticas (reflejos)

        self.peso += factor_ajuste
        # Asegurar que el peso no caiga por debajo del umbral mínimo.
        self.peso = max(PESO_MINIMO_SINAPTICO, min(self.peso, PESO_MAXIMO_SINAPTICO))

    def __repr__(self):
        estado_plasticidad = "P" if self.plastica else "F" # Plástica o Fija
        return f"Conexion({self.neurona_origen.id} -> {self.neurona_destino.id}, P: {self.peso:.2f}, [{estado_plasticidad}])"


class NeuronaBase:
    """
    Clase base para todas las neuronas del simulador.
    Define las propiedades y comportamientos fundamentales de una neurona,
    como su potencial de membrana, umbral de disparo y manejo de conexiones.
    Esta versión está adaptada para una simulación síncrona de dos fases.
    """
    def __init__(self, id_neurona, umbral_disparo=1.0, potencial_reposo=0.0):
        """
        Inicializa una neurona base.
        Args:
            id_neurona (str): Identificador único para la neurona.
            umbral_disparo (float): Potencial de membrana necesario para disparar.
            potencial_reposo (float): Potencial al que la neurona tiende a regresar.
        """
        self.id = id_neurona
        self.potencial_membrana = potencial_reposo
        self.umbral_disparo = umbral_disparo
        self.potencial_reposo = potencial_reposo
        self.conexiones_salientes = []
        self.conexiones_entrantes = []
        self.inputs_activos_recientes = []  # Para aprendizaje Hebbiano
        self.impulso_recurrente_pendiente = 0.0  # Para memoria a corto plazo

        # --- Banderas de estado para simulación síncrona ---
        self.disparo_pendiente = False  # True si debe disparar en la fase 2.
        self.disparada = False  # True si ha disparado en el paso actual (para logging/plasticidad).

    def agregar_conexion_saliente(self, neurona_destino, peso_inicial=1.0, plastica=True):
        """
        Crea una nueva conexión desde esta neurona hacia otra.
        Args:
            neurona_destino (NeuronaBase): La neurona a la que se conectará.
            peso_inicial (float): El peso inicial para la nueva conexión.
            plastica (bool): Si la conexión debe ser plástica (modificable).
        Returns:
            Conexion: El objeto de conexión recién creado.
        """
        conexion = Conexion(self, neurona_destino, peso_inicial, plastica=plastica)
        self.conexiones_salientes.append(conexion)
        neurona_destino.conexiones_entrantes.append(conexion)
        return conexion

    def recibir_impulso(self, magnitud_impulso, id_origen=None):
        """
        Incrementa el potencial de membrana al recibir un impulso.
        Args:
            magnitud_impulso (float): La fuerza del impulso.
            id_origen (str, optional): El ID de la neurona que origina el impulso.
        """
        self.potencial_membrana += magnitud_impulso
        if id_origen:
            self.inputs_activos_recientes.append(id_origen)

    def actualizar_estado(self):
        """
        Fase 1 de la simulación: Actualiza el potencial y determina si debe disparar.
        Aplica impulsos recurrentes, luego verifica si se alcanza el umbral. Si no,
        aplica un decaimiento de potencial. No dispara directamente.
        """
        self.disparada = False  # Resetea la bandera pública de disparo para este paso.

        # Aplicar impulso recurrente del ciclo anterior (memoria)
        if self.impulso_recurrente_pendiente > 0:
            self.recibir_impulso(self.impulso_recurrente_pendiente, id_origen=self.id)
            self.impulso_recurrente_pendiente = 0.0

        # Si ya está pendiente, no hacer nada más en esta fase.
        if self.disparo_pendiente:
            return

        # Verificar si se alcanza el umbral para marcarla como pendiente de disparo.
        if self.potencial_membrana >= self.umbral_disparo:
            self.disparo_pendiente = True
        else:
            # Si no va a disparar, simula el decaimiento del potencial hacia el reposo.
            if self.potencial_membrana > self.potencial_reposo:
                decaimento = (self.potencial_membrana - self.potencial_reposo) * 0.1
                self.potencial_membrana -= decaimento

    def disparar(self):
        """
        Fase 2 de la simulación: Propaga el impulso, aplica aprendizaje y resetea.
        Este método es llamado por RedDinamica solo si `disparo_pendiente` es True.
        """
        # Salvaguarda: no hacer nada si no estaba pendiente.
        if not self.disparo_pendiente:
            return

        logging.info(f"¡Disparo! Neurona {self.id} (Potencial: {self.potencial_membrana:.2f}, Umbral: {self.umbral_disparo:.2f})")
        self.disparada = True  # Marcar como disparada en este paso.

        # Propagar impulso a las neuronas conectadas.
        for conexion in self.conexiones_salientes:
            impulso_propagado = 1.0 * conexion.peso
            if conexion.es_recurrente:
                self.impulso_recurrente_pendiente += impulso_propagado
            else:
                conexion.neurona_destino.recibir_impulso(impulso_propagado, id_origen=self.id)

        # --- Lógica de Aprendizaje Hebbiano ---
        # --- Lógica de Aprendizaje Hebbiano ---
        # Reforzar conexiones basadas en las neuronas únicas que contribuyeron al disparo.
        if self.inputs_activos_recientes:
            inputs_unicos = set(self.inputs_activos_recientes)
            logging.info(f"APRENDIZAJE en {self.id}: Reforzando {len(inputs_unicos)} conexiones entrantes únicas.")
            for id_input in inputs_unicos:
                for conexion_entrante in self.conexiones_entrantes:
                    if conexion_entrante.neurona_origen.id == id_input:
                        peso_anterior = conexion_entrante.peso
                        conexion_entrante.ajustar_peso(FACTOR_APRENDIZAJE_HEBBIANO)
                        logging.info(f"  -> Conexión {id_input}->{self.id} reforzada. Peso: {peso_anterior:.2f} -> {conexion_entrante.peso:.2f}")
                        break  # Pasar al siguiente input único

        # --- Reseteo de estado post-disparo ---
        self.resetear_potencial()
        self.disparo_pendiente = False  # Ya ha disparado, no está pendiente.

    def resetear_potencial(self):
        """Resetea el potencial de membrana y la lista de inputs recientes."""
        self.potencial_membrana = self.potencial_reposo
        self.inputs_activos_recientes.clear()

    def __repr__(self):
        return f"Neurona({self.id}, Potencial: {self.potencial_membrana:.2f})"
