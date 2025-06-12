import logging
from .elementos_neuronales import NeuronaBase

class NeuronaG3(NeuronaBase):
    """
    Representa una neurona G3, que se forma para abstraer una co-activación
    frecuente entre dos neuronas de un nivel inferior (típicamente G2).

    Funciona detectando una secuencia A->B dentro de una ventana temporal, donde
    A y B son los disparos de las neuronas de entrada.
    """
    def __init__(self, id_neurona, id_input_A, id_input_B, ventana_temporal, umbral_disparo=1.0):
        """
        Inicializa la neurona de abstracción G3.

        Args:
            id_neurona (str): Identificador único.
            id_input_A (str): ID de la primera neurona de entrada (evento A).
            id_input_B (str): ID de la segunda neurona de entrada (evento B).
            ventana_temporal (int): Número de pasos de simulación durante los cuales
                                    el evento B debe ocurrir después del evento A.
            umbral_disparo (float): Umbral para el disparo.
        """
        super().__init__(id_neurona, umbral_disparo)
        self.id_input_A = id_input_A
        self.id_input_B = id_input_B
        self.ventana_temporal = ventana_temporal
        
        self.esperando_B = False
        self.contador_ventana = 0

    def recibir_impulso(self, magnitud_impulso, id_origen):
        """
        Procesa un impulso de entrada, verificando la secuencia temporal A->B.
        """
        super().recibir_impulso(magnitud_impulso, id_origen)

        if id_origen == self.id_input_A and not self.esperando_B:
            # Si recibimos el disparo de A, iniciamos la ventana de espera para B
            self.esperando_B = True
            self.contador_ventana = self.ventana_temporal
            logging.info(f"G3 {self.id}: Evento A ('{id_origen}') detectado. Abriendo ventana de {self.ventana_temporal} pasos para B ('{self.id_input_B}').")
        
        elif id_origen == self.id_input_B and self.esperando_B:
            # Si recibimos B mientras esperábamos, la secuencia es correcta
            logging.info(f"G3 {self.id}: Evento B ('{id_origen}') detectado en ventana. ¡ABSTRACCIÓN FORMADA!")
            self.potencial_membrana += self.umbral_disparo # Acumulamos para asegurar el disparo
            self.resetear_estado()

    def actualizar_estado(self):
        """
        Actualiza el estado de la neurona, incluyendo el contador de la ventana temporal.
        """
        super().actualizar_estado()

        if self.esperando_B:
            self.contador_ventana -= 1
            if self.contador_ventana <= 0:
                # Si la ventana se cierra, reseteamos el estado
                logging.info(f"G3 {self.id}: Ventana temporal cerrada. Secuencia A->B fallida.")
                self.resetear_estado()

    def resetear_estado(self):
        """
        Resetea el estado de detección de la neurona.
        """
        self.esperando_B = False
        self.contador_ventana = 0
    
    def disparar(self):
        """
        Dispara y luego resetea el estado para futuras detecciones.
        """
        super().disparar()
        self.resetear_estado()
