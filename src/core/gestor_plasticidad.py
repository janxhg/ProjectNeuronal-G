# -*- coding: utf-8 -*-
import logging
from collections import defaultdict
from itertools import combinations

# Importaciones del proyecto
from configuracion.parametros_simulacion import UMBRAL_COOCURRENCIA, VENTANA_TEMPORAL_ASOCIACION
from src.core.neurona_g2 import NeuronaG2
from src.core.neurona_g3 import NeuronaG3

class GestorPlasticidad:
    """
    Clase supervisora que monitoriza la actividad de la red y aplica reglas
    de desarrollo y autoorganización, como la creación de nuevas neuronas
    para generalizar conceptos.
    """
    def __init__(self, red_dinamica):
        """
        Inicializa el gestor de plasticidad.

        Args:
            red_dinamica (RedDinamica): Una referencia a la red neuronal que gestionará.
        """
        self.red = red_dinamica
        # Historial de disparos para G1 -> G2
        self.historial_disparos_g1 = defaultdict(list)
        self.pares_g1_ya_asociados = set()

        # Historial de disparos para G2 -> G3
        self.historial_disparos_g2 = defaultdict(list)
        self.pares_g2_ya_asociados = set()
        logging.info("Gestor de Plasticidad inicializado.")

    def registrar_disparo(self, neurona, paso_actual):
        """
        Registra el disparo de una neurona para su posterior análisis.
        Solo se interesa por las neuronas de tipo G1.

        Args:
            neurona (NeuronaBase): La neurona que ha disparado.
            paso_actual (int): El paso de simulación actual.
        """
        # Registrar disparos de G1 para formar conceptos G2
        if 'G1' in neurona.id:
            self.historial_disparos_g1[neurona.id].append(paso_actual)
            if len(self.historial_disparos_g1[neurona.id]) > 50:
                self.historial_disparos_g1[neurona.id].pop(0)
        # Registrar disparos de G2 para formar abstracciones G3
        elif 'G2' in neurona.id:
            self.historial_disparos_g2[neurona.id].append(paso_actual)
            if len(self.historial_disparos_g2[neurona.id]) > 50:
                self.historial_disparos_g2[neurona.id].pop(0)

    def analizar_y_actuar(self, paso_actual):
        """
        Analiza el historial de disparos en busca de patrones (co-ocurrencias)
        y, si se cumplen las condiciones, crea nuevas estructuras neuronales.
        
        Args:
            paso_actual (int): El paso de simulación actual.
        """
        # Para no analizar en cada paso, se puede hacer cada N pasos (ej. cada 10)
        # Analizar cada N pasos para no sobrecargar
        if paso_actual % 10 != 0:
            return

        # --- Nivel 1: Formación de Conceptos (G1 -> G2) ---
        if len(self.historial_disparos_g1) >= 2:
            self._analizar_coocurrencias_g1(paso_actual)

        # --- Nivel 2: Formación de Abstracciones (G2 -> G3) ---
        if len(self.historial_disparos_g2) >= 2:
            self._analizar_coocurrencias_g2(paso_actual)

    def _buscar_g2_candidata(self, id_g1):
        """
        Busca la neurona G2 (concepto) que ya podría estar representando a una
        neurona G1, basándose en la fuerza de la conexión.

        Returns:
            str or None: El ID de la mejor neurona G2 candidata, o None si no hay.
        """
        mejor_candidato = None
        max_peso = 0.0  # Umbral mínimo para considerar una conexión existente.
        for neurona in self.red.neuronas.values():
            if isinstance(neurona, NeuronaG2):
                for conexion in neurona.conexiones_entrantes:
                    # Buscamos la conexión más fuerte que supere el umbral
                    if conexion.neurona_origen.id == id_g1 and conexion.peso > max_peso:
                        max_peso = conexion.peso
                        mejor_candidato = neurona.id
        return mejor_candidato

    def _buscar_g3_candidata(self, id_g2):
        """
        Busca la neurona G3 (abstracción) que ya podría estar representando a una
        neurona G2, basándose en la fuerza de la conexión.

        Returns:
            str or None: El ID de la mejor neurona G3 candidata, o None si no hay.
        """
        mejor_candidato = None
        max_peso = 0.0  # Umbral mínimo para considerar una conexión existente.
        for neurona in self.red.neuronas.values():
            if isinstance(neurona, NeuronaG3):
                for conexion in neurona.conexiones_entrantes:
                    # Buscamos la conexión más fuerte que supere el umbral
                    if conexion.neurona_origen.id == id_g2 and conexion.peso > max_peso:
                        max_peso = conexion.peso
                        mejor_candidato = neurona.id
        return mejor_candidato

    def _analizar_coocurrencias_g1(self, paso_actual):
        logging.debug(f"[GestorPlasticidad] Analizando co-ocurrencias G1->G2 en paso {paso_actual}...")
        for id_g1_a, id_g1_b in combinations(self.historial_disparos_g1.keys(), 2):
            par_ordenado = tuple(sorted((id_g1_a, id_g1_b)))
            if par_ordenado in self.pares_g1_ya_asociados:
                continue

            co_ocurrencias = 0
            for t_a in self.historial_disparos_g1[id_g1_a]:
                for t_b in self.historial_disparos_g1[id_g1_b]:
                    if abs(t_a - t_b) <= VENTANA_TEMPORAL_ASOCIACION:
                        co_ocurrencias += 1
                        break

            if co_ocurrencias >= UMBRAL_COOCURRENCIA:
                logging.info(f"[GestorPlasticidad] Co-ocurrencia G1->G2 detectada para {par_ordenado} ({co_ocurrencias} veces).")
                candidato_a = self._buscar_g2_candidata(id_g1_a)
                candidato_b = self._buscar_g2_candidata(id_g1_b)

                if candidato_a and candidato_a == candidato_b:
                    logging.info(f"  -> El concepto '{candidato_a}' ya asocia a '{id_g1_a}' y '{id_g1_b}'. No se requiere acción.")
                elif candidato_a:
                    logging.info(f"  -> Reforzando concepto existente '{candidato_a}' con la neurona '{id_g1_b}'.")
                    self.red.conectar_neuronas(id_g1_b, candidato_a)
                elif candidato_b:
                    logging.info(f"  -> Reforzando concepto existente '{candidato_b}' con la neurona '{id_g1_a}'.")
                    self.red.conectar_neuronas(id_g1_a, candidato_b)
                else:
                    logging.info(f"  -> No se encontró un concepto existente. Creando uno nuevo para ({id_g1_a}, {id_g1_b}).")
                    self._crear_neurona_conceptual(id_g1_a, id_g1_b)
                
                self.pares_g1_ya_asociados.add(par_ordenado)

    def _analizar_coocurrencias_g2(self, paso_actual):
        logging.debug(f"[GestorPlasticidad] Analizando co-ocurrencias G2->G3 en paso {paso_actual}...")
        for id_g2_a, id_g2_b in combinations(self.historial_disparos_g2.keys(), 2):
            par_ordenado = tuple(sorted((id_g2_a, id_g2_b)))
            if par_ordenado in self.pares_g2_ya_asociados:
                continue

            co_ocurrencias = 0
            for t_a in self.historial_disparos_g2[id_g2_a]:
                for t_b in self.historial_disparos_g2[id_g2_b]:
                    if abs(t_a - t_b) <= VENTANA_TEMPORAL_ASOCIACION:
                        co_ocurrencias += 1
                        break

            if co_ocurrencias >= UMBRAL_COOCURRENCIA:
                logging.info(f"[GestorPlasticidad] Co-ocurrencia G2->G3 detectada para {par_ordenado} ({co_ocurrencias} veces).")
                candidato_a = self._buscar_g3_candidata(id_g2_a)
                candidato_b = self._buscar_g3_candidata(id_g2_b)

                if candidato_a and candidato_a == candidato_b:
                    logging.info(f"  -> La abstracción '{candidato_a}' ya asocia a '{id_g2_a}' y '{id_g2_b}'. No se requiere acción.")
                elif candidato_a:
                    logging.info(f"  -> Reforzando abstracción existente '{candidato_a}' con el concepto '{id_g2_b}'.")
                    self.red.conectar_neuronas(id_g2_b, candidato_a)
                elif candidato_b:
                    logging.info(f"  -> Reforzando abstracción existente '{candidato_b}' con el concepto '{id_g2_a}'.")
                    self.red.conectar_neuronas(id_g2_a, candidato_b)
                else:
                    logging.info(f"  -> No se encontró una abstracción existente. Creando una nueva para ({id_g2_a}, {id_g2_b}).")
                    self._crear_neurona_abstracta(id_g2_a, id_g2_b)

                self.pares_g2_ya_asociados.add(par_ordenado)

    def _crear_neurona_conceptual(self, id_g1_a, id_g1_b):
        """
        Crea una nueva neurona G2 para representar el concepto abstracto
        que une a dos neuronas G1.

        Args:
            id_g1_a (str): ID de la primera neurona G1.
            id_g1_b (str): ID de la segunda neurona G1.
        """
        try:
            # Crear un ID único para la nueva neurona G2
            num_conceptos = len([n for n in self.red.neuronas.keys() if 'G2_Concepto' in n])
            nuevo_id_g2 = f"G2_Concepto_{num_conceptos + 1}"

            logging.info(f"[GestorPlasticidad] Creando nueva neurona conceptual '{nuevo_id_g2}' para generalizar ({id_g1_a}, {id_g1_b}).")

            # Crear la neurona G2. Su ventana temporal puede ser la misma que la de asociación.
            nueva_g2 = NeuronaG2(id_neurona=nuevo_id_g2, id_input_A=id_g1_a, id_input_B=id_g1_b, ventana_temporal=VENTANA_TEMPORAL_ASOCIACION)
            
            # Añadir la neurona a la red
            self.red.agregar_neurona(nueva_g2)

            # Conectar las G1 originales a la nueva G2
            self.red.conectar_neuronas(id_g1_a, nuevo_id_g2)
            self.red.conectar_neuronas(id_g1_b, nuevo_id_g2)
            
            logging.info(f"[GestorPlasticidad] '{nuevo_id_g2}' creada y conectada en la red.")

        except Exception as e:
            logging.error(f"[GestorPlasticidad] Error creando neurona conceptual: {e}", exc_info=True)

    def _crear_neurona_abstracta(self, id_g2_a, id_g2_b):
        """
        Crea una nueva neurona G3 para representar la abstracción que une a dos neuronas G2.
        """
        try:
            num_abstracciones = len([n for n in self.red.neuronas.keys() if 'G3_Abstraccion' in n])
            nuevo_id_g3 = f"G3_Abstraccion_{num_abstracciones + 1}"

            logging.info(f"[GestorPlasticidad] Creando nueva neurona abstracta '{nuevo_id_g3}' para generalizar ({id_g2_a}, {id_g2_b}).")

            nueva_g3 = NeuronaG3(id_neurona=nuevo_id_g3, id_input_A=id_g2_a, id_input_B=id_g2_b, ventana_temporal=VENTANA_TEMPORAL_ASOCIACION)
            self.red.agregar_neurona(nueva_g3)

            self.red.conectar_neuronas(id_g2_a, nuevo_id_g3)
            self.red.conectar_neuronas(id_g2_b, nuevo_id_g3)
            
            logging.info(f"[GestorPlasticidad] '{nuevo_id_g3}' creada y conectada en la red.")

        except Exception as e:
            logging.error(f"[GestorPlasticidad] Error creando neurona abstracta: {e}", exc_info=True)
