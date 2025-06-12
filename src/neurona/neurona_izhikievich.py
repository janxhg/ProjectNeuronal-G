import numpy as np

class NeuronaIzhikevich:
    """
    Implementa el modelo de neurona de Izhikevich, capaz de reproducir diversas dinámicas de disparo.

    Ecuaciones del modelo:
    dv/dt = 0.04*v^2 + 5*v + 140 - u + I
    du/dt = a*(b*v - u)

    Condición de reseteo (si v >= umbral_disparo, típicamente 30 mV):
    v = c
    u = u + d
    """
    def __init__(self, id_neurona, a, b, c, d, v_inicial=-65.0, umbral_disparo=30.0):
        """
        Inicializa la neurona de Izhikevich.

        Args:
            id_neurona (str): Identificador único para la neurona.
            a (float): Parámetro 'a' del modelo (escala de tiempo de u).
            b (float): Parámetro 'b' del modelo (sensibilidad de u a v).
            c (float): Parámetro 'c' del modelo (valor de reseteo de v post-disparo).
            d (float): Parámetro 'd' del modelo (incremento de u post-disparo).
            v_inicial (float, optional): Potencial de membrana inicial. Defaults to -65.0 mV.
            umbral_disparo (float, optional): Umbral para detectar un disparo. Defaults to 30.0 mV.
        """
        self.id = id_neurona
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.v = v_inicial  # Potencial de membrana (mV)
        self.u = self.b * self.v  # Variable de recuperación, inicializada para estar cerca del equilibrio con v
        self.umbral_disparo = umbral_disparo

        self.historial_v = []
        self.historial_u = []
        self.tiempos_disparo_abs = [] # Almacena el tiempo absoluto del disparo
        self.picos_v_disparo = [] # Almacena el valor de V en el pico

    def actualizar_estado(self, I_externa, dt, tiempo_actual_simulacion=None):
        """
        Actualiza el estado de la neurona (v y u) para un paso de tiempo dt, dada una corriente de entrada I_externa.

        Args:
            I_externa (float): Corriente de entrada a la neurona en este paso de tiempo.
            dt (float): Paso de tiempo de la simulación (ej. 1 ms, 0.5 ms).
            tiempo_actual_simulacion (float, optional): El tiempo actual en la simulación, para registrar el tiempo de disparo.

        Returns:
            bool: True si la neurona disparó en este paso de tiempo, False en caso contrario.
        """
        disparo_ocurrido = False

        # Actualizar v y u usando el método de Euler
        # dv/dt = 0.04*v^2 + 5*v + 140 - u + I
        # du/dt = a*(b*v - u)
        
        # Izhikevich sugiere que para dt=1ms, se puede hacer v dos veces para estabilidad,
        # o usar dt más pequeño (e.g., 0.5ms) con una sola actualización.
        # Aquí implementamos la actualización simple de Euler.
        # Si se usa dt=1ms, puede ser necesario ajustar o usar el método de dos pasos para v.
        
        delta_v = (0.04 * self.v**2 + 5 * self.v + 140 - self.u + I_externa) * dt
        # Para la actualización de u, usamos el valor de self.v *antes* de su propia actualización en este paso,
        # lo cual es una práctica común en la discretización de Euler para sistemas acoplados.
        delta_u = (self.a * (self.b * self.v - self.u)) * dt 

        self.v += delta_v
        self.u += delta_u
        
        # Comprobar si hubo disparo
        if self.v >= self.umbral_disparo:
            if tiempo_actual_simulacion is not None:
                self.tiempos_disparo_abs.append(tiempo_actual_simulacion)
            self.picos_v_disparo.append(self.v) # Guardar el pico real antes del reseteo
            
            self.v = self.c  # Resetear v
            self.u = self.u + self.d  # Incrementar u
            disparo_ocurrido = True
        
        # Guardar historial (opcional, para visualización)
        # Nota: self.v aquí ya está reseteado si hubo disparo.
        self.historial_v.append(self.v)
        self.historial_u.append(self.u)

        return disparo_ocurrido

    def __str__(self):
        return f"NeuronaIzhikevich(id='{self.id}', v={self.v:.2f}, u={self.u:.2f}, a={self.a}, b={self.b}, c={self.c}, d={self.d})"

# --- Ejemplos de conjuntos de parámetros para diferentes tipos de neuronas (de Izhikevich, 2003) ---
# Regular Spiking (RS): a=0.02, b=0.2, c=-65, d=8
# Intrinsically Bursting (IB): a=0.02, b=0.2, c=-55, d=4
# Chattering (CH): a=0.02, b=0.2, c=-50, d=2
# Fast Spiking (FS): a=0.1, b=0.2, c=-65, d=2
# Low-Threshold Spiking (LTS): a=0.02, b=0.25, c=-65, d=2
# Thalamo-Cortical (TC): a=0.02, b=0.25, c=-65, d=0.05 (requiere v_inicial=-87 para hiperpolarización)
# Resonator (RZ): a=0.1, b=0.26, c=-65, d=2
