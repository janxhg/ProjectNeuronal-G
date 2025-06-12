"""
Define la clase NeuronaBiologica para simular una neurona con mayor fidelidad biologica,
capaz de aprendizaje continuo.
"""

print("DEBUG: Iniciando src/neurona/neurona_clase.py")
import numpy as np
from .tipos_neurona import EXCITATORIA, INHIBITORIA # Usar . para import relativo

class NeuronaBiologica:
    def __init__(self, id_neurona, potencial_reposo=0.0, umbral_disparo=15.0, potencial_post_disparo=0.0,
                 tipo_neurona=EXCITATORIA, usa_stdp=False, verbose=True,
                 posicion=None, tasa_aprendizaje=0.01, tau_membrana=20.0, 
                 A_plus=0.05, tau_plus=10.0, A_minus=0.05, tau_minus=12.0, 
                 peso_max_stdp=1.0, peso_min_stdp=0.0,
                 usa_sfa=False, tau_sfa=100.0, incremento_sfa_por_disparo=0.05):
        self.id = id_neurona
        self.potencial_reposo = potencial_reposo
        self.umbral_disparo = umbral_disparo
        self.potencial_post_disparo = potencial_post_disparo # Almacenar el potencial post disparo
        self.potencial_membrana = potencial_reposo # Iniciar en reposo
        
        self.tipo_neurona = tipo_neurona
        self.usa_stdp = usa_stdp # Almacenar si la neurona usa STDP
        self.verbose = verbose
        
        self.posicion = np.array(posicion) if posicion else np.zeros(3)
        self.tasa_aprendizaje = tasa_aprendizaje # Aunque no se use explícitamente en STDP, puede ser para otras reglas
        self.tau_membrana = tau_membrana
        
        self.conexiones_entrantes = {}
        self.conexiones_salientes = {}

        self.historia_potencial = [self.potencial_membrana]
        self.historia_disparos = []
        
        self.ultima_vez_disparo = -np.inf
        self.periodo_refractario_absoluto = 2

        self.tiempos_ultimos_impulsos_entrantes = {}

        # Parámetros STDP (se inicializan siempre, pero solo se usan si self.usa_stdp es True en la lógica de la red/neurona)
        self.A_plus = A_plus
        self.tau_plus = tau_plus
        self.A_minus = A_minus
        self.tau_minus = tau_minus
        self.peso_max_stdp = peso_max_stdp
        self.peso_min_stdp = peso_min_stdp

        # Parámetros SFA (Spike-Frequency Adaptation)
        self.usa_sfa = usa_sfa
        self.tau_sfa = tau_sfa  # ms, constante de tiempo para la corriente de adaptación
        self.incremento_sfa_por_disparo = incremento_sfa_por_disparo # Cantidad que aumenta la corriente SFA por disparo
        self.corriente_adaptacion_sfa = 0.0

        # Listas para historial de SFA (solo para N_SFA_Test)
        self.historial_potencial_membrana_sfa = []
        self.historial_corriente_adaptacion_sfa = []
        self.historial_umbral_efectivo_sfa = []
        self.historial_tiempo_sfa = [] # Para registrar el tiempo global # Corriente de adaptación actual

    def recibir_impulso(self, id_neurona_presinaptica, peso_sinaptico, tiempo_actual, aplicar_stdp=True):
        """Procesa un impulso sinaptico entrante."""
        self.potencial_membrana += peso_sinaptico
        # Registrar el tiempo del ultimo impulso para esta sinapsis (para STDP LTP)
        # Esto es necesario incluso si STDP no se aplica, para tener el delta_t correcto si STDP se reactiva.
        self.tiempos_ultimos_impulsos_entrantes[id_neurona_presinaptica] = tiempo_actual
        
        if aplicar_stdp:
            # Aplicar LTD si es pertinente (Post-antes-que-Pre)
            self._aplicar_ltd_al_recibir_impulso(id_neurona_presinaptica, tiempo_actual)

    def actualizar_estado(self, tiempo_actual, dt=1, aplicar_stdp=True):
        """
        Actualiza el estado de la neurona en un paso de tiempo dt.
        Incluye decaimiento del potencial y verificacion de disparo.
        """
        disparo_ocurrido = False
        sfa_debug_print = False # Inicializar para evitar UnboundLocalError si no es N_SFA_Test

        # Guardar el valor de la corriente SFA al inicio del método para depuración
        sfa_current_at_start_of_method = self.corriente_adaptacion_sfa

        # 1. Decaimiento de la corriente de adaptación SFA y cálculo del umbral efectivo
        if self.usa_sfa:
            self.corriente_adaptacion_sfa *= np.exp(-dt / self.tau_sfa)
            sfa_current_after_decay_for_threshold = self.corriente_adaptacion_sfa
            effective_threshold = self.umbral_disparo + sfa_current_after_decay_for_threshold
        else:
            sfa_current_after_decay_for_threshold = 0.0
            effective_threshold = self.umbral_disparo

        # Debug SFA y registro de historial para N_SFA_Test
        if self.id == "N_SFA_Test":
            # sfa_debug_print = True # Descomentar para depuración detallada de SFA
            # Registrar datos para visualización de SFA
            self.historial_tiempo_sfa.append(tiempo_actual)
            self.historial_potencial_membrana_sfa.append(self.potencial_membrana) # Vm antes de posible disparo
            self.historial_corriente_adaptacion_sfa.append(sfa_current_after_decay_for_threshold)
            self.historial_umbral_efectivo_sfa.append(effective_threshold)
            # pass # No es necesario si hay código después

        # El bloque de sfa_debug_print ahora puede usar las variables calculadas
        if sfa_debug_print:
            print(f"[SFA_DEBUG t={tiempo_actual:.2f}] ID: {self.id}")
            print(f"  Potencial Memb (antes de disparo check): {self.potencial_membrana:.4f}")
            print(f"  SFA Current (al inicio de actualizar_estado): {sfa_current_at_start_of_method:.4f}")
            print(f"  SFA Current (después decaimiento, para umbral): {sfa_current_after_decay_for_threshold:.4f}")
            print(f"  Umbral Base: {self.umbral_disparo:.4f}, Umbral Efectivo: {effective_threshold:.4f}")

        # 3. Comprobar si la neurona dispara
        disparo_eval_result = self.potencial_membrana >= effective_threshold
        if sfa_debug_print:
            print(f"  Condición Disparo: V_mem ({self.potencial_membrana:.4f}) >= Umbral_Eff ({effective_threshold:.4f}) -> {disparo_eval_result}")

        if disparo_eval_result:
            if (tiempo_actual - self.ultima_vez_disparo) > self.periodo_refractario_absoluto:
                if self.disparar(tiempo_actual): # disparar() se encarga de resetear potencial e incrementar SFA
                    disparo_ocurrido = True
                    if aplicar_stdp and self.usa_stdp:
                        self._aplicar_ltp_al_disparar(tiempo_actual)
        
        # 4. Aplicar decaimiento del potencial de membrana si no hubo disparo en este paso
        # Si disparó, self.potencial_membrana ya fue reseteado por self.disparar().
        if not disparo_ocurrido:
            # El decaimiento es hacia el potencial de reposo. SFA ya no afecta V_target_decay aquí.
            decay_factor = np.exp(-dt / self.tau_membrana)
            self.potencial_membrana = self.potencial_reposo + \
                                     (self.potencial_membrana - self.potencial_reposo) * decay_factor
        
        # La historia del potencial se guarda después de todas las actualizaciones.
        self.historia_potencial.append(self.potencial_membrana)
        return disparo_ocurrido

    def disparar(self, tiempo_actual):
        """Genera un potencial de accion (disparo)."""
        # print(f"Neurona {self.id} disparó en t={tiempo_actual}!")
        self.potencial_membrana = self.potencial_reposo # Reseteo del potencial (o a un valor de hiperpolarizacion)
        self.historia_disparos.append(tiempo_actual)
        self.ultima_vez_disparo = tiempo_actual

        if self.usa_sfa:
            self.corriente_adaptacion_sfa += self.incremento_sfa_por_disparo

        if self.verbose:
            sfa_info = f", SFA current: {self.corriente_adaptacion_sfa:.3f}" if self.usa_sfa else ""
            print(f"Neurona {self.id} disparó en t={tiempo_actual}. Potencial reseteado a {self.potencial_membrana:.2f}{sfa_info}")
        return True # Indica que hubo un disparo

    def agregar_conexion_entrante(self, id_neurona_presinaptica, peso_sinaptico, tipo_neurona_presinaptica, plastica=True):
        """Agrega una conexión entrante de otra neurona."""
        self.conexiones_entrantes[id_neurona_presinaptica] = {
            'peso': peso_sinaptico,
            'tipo': tipo_neurona_presinaptica,
            'ultimo_impulso_presinaptico': -np.inf, # Inicializar para STDP
            'plastica': plastica # Indica si la conexión es sujeta a plasticidad
        }
        # print(f"DEBUG NEURONA ({self.id}): Agregada conexión entrante de {id_neurona_presinaptica} con peso {peso_sinaptico}, plastica={plastica}. Conexiones ahora: {self.conexiones_entrantes}")

    # --- Metodos para aprendizaje continuo (Plasticidad) ---
    # Estos son esqueletos y necesitaran mucha mas definicion.

    def aplicar_hebbian_learning(self, id_neurona_presinaptica, actividad_presinaptica, actividad_postsinaptica, dt=1):
        """Ajusta el peso de una sinapsis entrante usando una regla Hebbiana simple."""
        # Esta regla puede coexistir o ser reemplazada/manejada por STDP
        # Por ahora, la llamada a esta función se removerá del __main__ para enfocarse en STDP
        if id_neurona_presinaptica in self.conexiones_entrantes:
            # Regla Hebbiana basica: dw = eta * pre * post
            cambio_peso = self.tasa_aprendizaje * actividad_presinaptica * actividad_postsinaptica * dt
            self.conexiones_entrantes[id_neurona_presinaptica]['peso'] += cambio_peso
            # Podria necesitar limites para los pesos (ej. no negativos, maximo valor)
            self.conexiones_entrantes[id_neurona_presinaptica]['peso'] = np.clip(self.conexiones_entrantes[id_neurona_presinaptica]['peso'], 0, 20) # Ejemplo, limite superior aumentado

    def _aplicar_ltp_al_disparar(self, tiempo_disparo_postsinaptico):
        """Aplica LTP a las sinapsis entrantes basado en el tiempo del disparo postsinaptico (Pre-antes-que-Post)."""
        # print(f"DEBUG _aplicar_ltp_al_disparar: id={self.id} t_post_spike={tiempo_disparo_postsinaptico} A_plus={self.A_plus}, tau_plus={self.tau_plus}")
        for id_pre, info_conexion in list(self.conexiones_entrantes.items()): 
            if not info_conexion.get('plastica', True): # Si no es plastica, saltar STDP. Default a True por retrocompatibilidad.
                continue

            tiempo_impulso_presinaptico = self.tiempos_ultimos_impulsos_entrantes.get(id_pre)

            if tiempo_impulso_presinaptico is not None:
                delta_t = tiempo_disparo_postsinaptico - tiempo_impulso_presinaptico
                cambio_peso = 0.0

                if delta_t >= 0: # LTP: Pre antes que Post (o simultáneo)
                    if 0 <= delta_t <= self.tau_plus:  # LTP si el disparo post es simultáneo o después del pre, dentro de la ventana causal
                        cambio_peso = self.A_plus * np.exp(-delta_t / self.tau_plus)
                
                if cambio_peso != 0.0:
                    nuevo_peso = info_conexion['peso'] + cambio_peso
                    self.conexiones_entrantes[id_pre]['peso'] = np.clip(nuevo_peso, self.peso_min_stdp, self.peso_max_stdp)
                    print(f"LTP: pre={id_pre}, post={self.id}, delta_t={delta_t:.2f}, cambio={cambio_peso:.4f}, nuevo_peso={self.conexiones_entrantes[id_pre]['peso']:.3f}")

    def _aplicar_ltd_al_recibir_impulso(self, id_neurona_presinaptica, tiempo_llegada_impulso):
        """Aplica LTD a una sinapsis entrante basado en el tiempo de llegada del impulso (Post-antes-que-Pre)."""
        info_conexion_actual = self.conexiones_entrantes.get(id_neurona_presinaptica)
        if not info_conexion_actual or not info_conexion_actual.get('plastica', True): # Si no existe la conexion o no es plastica, saltar STDP.
            return

        # print(f"DEBUG _aplicar_ltd_al_recibir_impulso: pre_id={id_neurona_presinaptica}, post_id={self.id}, t_pre_arrival={tiempo_llegada_impulso}, t_last_post_spike={self.ultima_vez_disparo}")
        if self.ultima_vez_disparo > 0 and self.ultima_vez_disparo != -np.inf: # Post ha disparado alguna vez
            delta_t = self.ultima_vez_disparo - tiempo_llegada_impulso # t_post - t_pre
            cambio_peso = 0.0

            if delta_t < 0: # LTD: Post antes que Pre (t_post < t_pre)
                if abs(delta_t) < 5 * self.tau_minus: # Heurística para la ventana acausal
                    cambio_peso = -self.A_minus * np.exp(delta_t / self.tau_minus) # delta_t es negativo
            
            if cambio_peso != 0.0:
                peso_actual = self.conexiones_entrantes[id_neurona_presinaptica]['peso']
                nuevo_peso = peso_actual + cambio_peso
                self.conexiones_entrantes[id_neurona_presinaptica]['peso'] = np.clip(nuevo_peso, self.peso_min_stdp, self.peso_max_stdp)
                print(f"LTD: pre={id_neurona_presinaptica}, post={self.id}, delta_t={delta_t:.2f}, cambio={cambio_peso:.4f}, nuevo_peso={self.conexiones_entrantes[id_neurona_presinaptica]['peso']:.3f}")

    def resetear_estado(self):
        """Resetea el estado de la neurona a sus condiciones iniciales."""
        self.potencial_membrana = self.potencial_reposo
        self.ultima_vez_disparo = -np.inf
        self.corriente_adaptacion_sfa = 0.0 # Resetear SFA current
        self.historia_potencial = [self.potencial_membrana]
        self.historia_disparos = []
        self.tiempos_ultimos_impulsos_entrantes = {}
        # Los historiales específicos de SFA_test no se resetean aquí, 
        # ya que son para un escenario de prueba particular y largo.
        # Si fuera necesario, se podrían añadir como parámetro opcional.
        if self.verbose and self.id == "N_SFA_Test": # Ejemplo de log si es necesario
            print(f"DEBUG Neurona {self.id}: Estado reseteado.")

    def limpiar_historia_disparos(self):
        """Limpia únicamente el historial de disparos de la neurona."""
        self.historia_disparos = []
        # Opcional: log para depuración si es necesario y la neurona es verbosa
        # if self.verbose:
        #     print(f"DEBUG Neurona {self.id}: Historia de disparos limpiada.")

    def __repr__(self):
        return f"NeuronaBiologica(id={self.id}, potencial={self.potencial_membrana:.2f}, umbral={self.umbral_disparo})"

