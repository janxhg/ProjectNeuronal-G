import matplotlib.pyplot as plt
import networkx as nx
import logging

class VisualizadorDinamico:
    """
    Gestiona la visualización en tiempo real de la red neuronal.

    Utiliza matplotlib y networkx para dibujar el grafo de la red, actualizándolo
    en cada paso de la simulación para reflejar cambios estructurales (nuevas
    neuronas/conexiones) y de estado (potencial, pesos).
    """
    def __init__(self, red):
        """
        Inicializa el visualizador.
        Args:
            red (RedDinamica): La instancia de la red a visualizar.
        """
        self.red = red
        self.pos = None  # Almacenará las posiciones para un layout estable
        plt.ion()  # Activar modo interactivo de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(15, 10))
        logging.info("Visualizador dinámico inicializado.")

    def actualizar_grafico(self):
        """
        Borra el gráfico anterior y dibuja el estado actual de la red.
        """
        self.ax.clear()
        
        G = nx.DiGraph()
        
        # 1. Añadir nodos (neuronas) al grafo
        for neurona in self.red.neuronas.values():
            G.add_node(neurona.id)

        # 2. Añadir aristas (conexiones) al grafo
        edge_labels = {}
        edge_widths = []
        for neurona in self.red.neuronas.values():
            for conexion in neurona.conexiones_salientes:
                G.add_edge(conexion.neurona_origen.id, conexion.neurona_destino.id)
                edge_labels[(conexion.neurona_origen.id, conexion.neurona_destino.id)] = f"{conexion.peso:.2f}"
                edge_widths.append(1 + (conexion.peso * 1.5))

        # 3. Calcular layout (si es la primera vez o si hay nodos nuevos)
        if self.pos is None or set(G.nodes()) != set(self.pos.keys()):
            # Si el layout necesita recalcularse (p. ej. por nodos nuevos), usa las
            # posiciones antiguas como punto de partida para una transición más suave.
            self.pos = nx.spring_layout(G, pos=self.pos, k=0.8, iterations=50)

        # 4. Definir propiedades visuales de los nodos
        node_colors = []
        node_sizes = []
        for node_id in G.nodes():
            neurona = self.red.neuronas[node_id]
            if 'G1' in neurona.__class__.__name__:
                node_colors.append('skyblue')
            elif 'G2' in neurona.__class__.__name__:
                node_colors.append('lightgreen')
            elif 'G3' in neurona.__class__.__name__:
                node_colors.append('salmon')
            else:
                node_colors.append('grey')
            
            # El tamaño refleja el potencial de membrana
            size = 300 + neurona.potencial_membrana * 1000
            node_sizes.append(max(300, size))

        # 5. Dibujar la red
        nx.draw_networkx_nodes(G, self.pos, ax=self.ax, node_color=node_colors, node_size=node_sizes, edgecolors='black')
        nx.draw_networkx_edges(G, self.pos, ax=self.ax, edgelist=G.edges(), width=edge_widths, alpha=0.7, arrowsize=20)
        nx.draw_networkx_labels(G, self.pos, ax=self.ax, font_size=8, font_weight='bold')
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels=edge_labels, ax=self.ax, font_size=7, font_color='red')

        # 6. Configurar y mostrar el gráfico
        self.ax.set_title(f"Estado de la Red en el Paso {self.red.tiempo_actual}", fontsize=16)
        self.ax.margins(0.1)
        plt.draw()
        plt.pause(0.05) # Pausa para permitir que la GUI se actualice

    def cerrar(self):
        """Cierra la ventana de visualización."""
        plt.ioff()
        plt.close(self.fig)
        logging.info("Ventana de visualización cerrada.")
