import logging
from .elementos_neuronales import NeuronaBase

class NeuronaG2(NeuronaBase):
    """
    Representa una neurona G2, que detecta la ocurrencia de dos eventos
    (disparos de neuronas G1) en un orden y con un intervalo de tiempo específicos.
    """
    def __init__(self, id_neurona, id_input_A, id_input_B, ventana_temporal, umbral_disparo=1.0):
        """
        Inicializa la neurona G2.

        Args:
            id_neurona (str): Identificador único.
            id_input_A (str): ID de la primera neurona en la secuencia (evento A).
            id_input_B (str): ID de la segunda neurona en la secuencia (evento B).
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
        super().recibir_impulso(magnitud_impulso, id_origen)
        """
        Procesa un impulso de entrada, verificando la secuencia temporal A->B.
        """
        if id_origen == self.id_input_A and not self.esperando_B:
            # Si recibimos A, iniciamos la ventana de espera para B
            self.esperando_B = True
            self.contador_ventana = self.ventana_temporal
            # print(f"{self.id}: Evento A detectado. Esperando B durante {self.ventana_temporal} pasos.")
        
        elif id_origen == self.id_input_B and self.esperando_B:
            # Si recibimos B mientras esperábamos, la secuencia es correcta
            # print(f"{self.id}: Evento B detectado en ventana. ¡Secuencia G2 completada!")
            self.potencial_membrana = self.umbral_disparo
            self.resetear_estado()

    def actualizar_estado(self):
        """
        Actualiza el estado de la neurona, incluyendo el contador de la ventana temporal.
        """
        # Primero, gestiona el disparo y decaimiento del potencial base
        super().actualizar_estado()

        # Luego, gestiona la lógica de la ventana temporal
        if self.esperando_B:
            self.contador_ventana -= 1
            if self.contador_ventana <= 0:
                # Si la ventana se cierra, reseteamos el estado
                # print(f"{self.id}: Ventana temporal cerrada. Secuencia fallida.")
                self.resetear_estado()

    def resetear_estado(self):
        """Resetea el estado de detección de la neurona G2."""
        self.esperando_B = False
        self.contador_ventana = 0
    
    def disparar(self):
        """Dispara y luego resetea el estado para futuras detecciones."""
        super().disparar()
        self.resetear_estado()
