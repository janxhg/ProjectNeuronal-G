from .elementos_neuronales import NeuronaBase

class NeuronaG1(NeuronaBase):
    """Representa una neurona G1, especializada en detectar secuencias temporales.

    Hereda de NeuronaBase y añade la lógica para reconocer un patrón específico
    de eventos de entrada en un orden determinado.
    """
    def __init__(self, id_neurona, secuencia_objetivo=None, umbral_disparo=1.0):
        """Inicializa la neurona detectora de secuencias G1.

        Args:
            id_neurona (str): Identificador único.
            secuencia_objetivo (list): Lista de IDs de neuronas presinápticas
                                       en el orden que deben activarse.
            umbral_disparo (float): Umbral para el disparo.
        """
        super().__init__(id_neurona, umbral_disparo)
        self.secuencia_objetivo = secuencia_objetivo
        self.progreso_secuencia = 0

    def recibir_impulso(self, magnitud_impulso, id_origen=None):
        """
        Procesa un impulso entrante. Si la neurona tiene una secuencia_objetivo,
        intenta hacer coincidir el impulso con la secuencia. Si no, actúa como
        una neurona base.
        """
        # Primero, aplicar el comportamiento base para que el potencial aumente
        super().recibir_impulso(magnitud_impulso, id_origen)

        # Si no hay una secuencia que detectar, no hacemos nada más.
        if not self.secuencia_objetivo:
            return

        # Lógica de detección de secuencia
        if self.progreso_secuencia < len(self.secuencia_objetivo):
            if id_origen == self.secuencia_objetivo[self.progreso_secuencia]:
                self.progreso_secuencia += 1
                logging.info(f"Neurona {self.id}: Secuencia progresó a {self.progreso_secuencia}/{len(self.secuencia_objetivo)} por input '{id_origen}'.")
            else:
                # Si el input no es el esperado, resetea el progreso
                self.progreso_secuencia = 0
        
        # Si la secuencia se completa, se da un gran impulso al potencial
        if self.progreso_secuencia == len(self.secuencia_objetivo):
            self.potencial_membrana += 1.0 # Impulso extra por completar la secuencia
            logging.info(f"¡Secuencia completada para {self.id}! Potencial aumentado.")
            self.progreso_secuencia = 0 # Resetear para poder detectarla de nuevo

    def actualizar_estado(self):
        """Actualiza el estado de la neurona."""
        # La lógica de reseteo se ha movido a resetear_progreso() y se llama
        # cuando una secuencia es incorrecta o después de un disparo exitoso.
        super().actualizar_estado()

    def resetear_progreso(self):
        """Resetea el contador de progreso de la secuencia."""
        if self.progreso_secuencia > 0:
            # print(f"{self.id}: Secuencia rota. Reseteando progreso.")
            self.progreso_secuencia = 0

    def disparar(self):
        """Dispara y luego resetea el progreso para poder detectar de nuevo."""
        super().disparar()
        self.resetear_progreso()
