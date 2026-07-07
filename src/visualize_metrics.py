
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

class VisualizeMetrics:
    @staticmethod
    def plot_density_heatmap(density_map: np.ndarray, floor_field: np.ndarray, title: str = "", output_path: str | None = None):
        """
        Gera um mapa de calor evidenciando as zonas de congestionamento.
        Obstáculos (células com valor 500) são coloridos com um tom neutro.
        """
        rows, cols = density_map.shape
        
        # Isola os obstáculos para que não interfiram na escala de cores da densidade
        mask_walls = (floor_field == 500.0)
        density_data = density_map.copy().astype(float)
        
        # Zera a densidade dentro dos obstáculos por segurança matemática
        density_data[mask_walls] = np.nan 
        
        # Configuração da figura mantendo proporção uniforme
        fig, ax = plt.subplots(figsize=(cols * 0.4, rows * 0.4))
        
        # Definição de uma paleta de cores objetiva e acadêmica
        cmap = plt.cm.YlOrRd
        cmap.set_bad(color='#d3d3d3')  # Cinza claro para obstáculos/paredes
        
        # Renderização da matriz
        im = ax.imshow(density_data, cmap=cmap, interpolation='nearest')
        
        # Remoção de eixos desnecessários para um aspecto minimalista
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Contorno padronizado
        for spine in ax.spines.values():
            spine.set_color('black')
            spine.set_linewidth(1.0)
            
        if title:
            ax.set_title(title, pad=15, fontsize=12, fontweight='bold')
            
        # Configuração unificada da legenda (colorbar)
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Passos de Tempo (Congestionamento)', rotation=270, labelpad=15, fontsize=10)
        cbar.set_label('Passos de Tempo (Congestionamento)', rotation=270, labelpad=15, fontsize=10)
        cbar.ax.spines['outline'].set_linewidth(1.0)
        
        plt.tight_layout()
        
        if output_path:
            # Salva em alta resolução (300 dpi) para publicações
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"Heatmap exportado: {output_path}")
        else:
            plt.show()
            
        plt.close()

    @staticmethod
    def plot_scenarios(matrix, cenario):
    
        rows, cols = matrix.shape
        
        mask_500 = (matrix == 500)
        matrix_normalized = matrix.copy()
        matrix_normalized[mask_500] = np.nan

        vmin = np.nanmin(matrix_normalized)
        vmax = np.nanmax(matrix_normalized)
        
        # Mapa monocromático ideal para artigos (tons de azul)
        cmap = plt.cm.Blues
        
        fig, ax = plt.subplots(figsize=(cols * 0.7, rows * 0.7))
        ax.set_xlim(0, cols)
        ax.set_ylim(rows, 0)
        ax.set_aspect('equal')
        
        for r in range(rows):
            for c in range(cols):
                value = matrix[r, c]
                
                if value == 500:
                    # Paredes em cinza escuro, sem texto
                    facecolor = "#333333" 
                    text = "" 
                else:
                    if vmax > vmin:
                        normalized = (value - vmin) / (vmax - vmin)
                    else:
                        normalized = 0.5
                    
                    # Suavizamos a escala para não gerar azuis escuros demais (que esconderiam o texto)
                    facecolor = cmap(normalized * 0.6 + 0.1)
                    
                    text = str(int(value)) if float(value).is_integer() else f"{value:.1f}"
                
                # Células com bordas brancas e finas para visual limpo
                rect = Rectangle(
                    (c, r),
                    1,
                    1,
                    facecolor=facecolor,
                    edgecolor="white",
                    linewidth=0.5
                )
                
                ax.add_patch(rect)
                
                if text:
                    ax.text(
                        c + 0.5,
                        r + 0.5,
                        text,
                        ha="center",
                        va="center",
                        fontsize=11, # Fonte mais delicada
                        family="sans-serif",
                        color="#1a1a1a" # Texto padronizado escuro
                    )
        
        ax.set_xticks([])
        ax.set_yticks([])
        
        plt.savefig(
            f"outputs/scenarios/floor_field_{cenario}.png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.05
        )
        
        # plt.show()


    @staticmethod
    def plot_simulation_trajectory(matrix, agent_paths, cenario):
        """
        Plota o cenário com a trajetória dos agentes, utilizando estética minimalista.
        """
        rows, cols = matrix.shape
        
        mask_500 = (matrix == 500)
        matrix_normalized = matrix.copy()
        matrix_normalized[mask_500] = np.nan

        vmin = np.nanmin(matrix_normalized)
        vmax = np.nanmax(matrix_normalized)
        cmap_bg = plt.cm.Blues
        
        fig, ax = plt.subplots(figsize=(cols * 0.7, rows * 0.7))
        ax.set_xlim(0, cols)
        ax.set_ylim(rows, 0)
        ax.set_aspect('equal')

        for r in range(rows):
            for c in range(cols):
                value = matrix[r, c]
                
                if value == 500:
                    facecolor = "#333333"
                else:
                    normalized = (value - vmin) / (vmax - vmin) if vmax > vmin else 0.5
                    facecolor = cmap_bg(normalized * 0.6 + 0.1)
                
                rect = Rectangle((c, r), 1, 1, facecolor=facecolor, edgecolor="white", linewidth=0.5, zorder=1)
                ax.add_patch(rect)
                
        colors = plt.cm.Set2.colors  # type: ignore
        
        for idx, (agent_id, path) in enumerate(agent_paths.items()):            
            x_coords = [c + 0.5 for r, c in path]
            y_coords = [r + 0.5 for r, c in path]
            
            ax.plot(x_coords, y_coords, color="#590808", linestyle="-", linewidth=2.5, alpha=1.0, zorder=2)
            

            ax.scatter(x_coords[0], y_coords[0], color="#590808", s=50, edgecolors="black", zorder=3)

            ax.scatter(x_coords[-1], y_coords[-1], color="#590808", s=70, edgecolors="black", marker='X', zorder=4)

        ax.set_xticks([])
        ax.set_yticks([])

        plt.savefig(
            f"outputs/scenarios/path_agents_{cenario}.png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.05
        )
        
        print(f"Trajetórias exportadas: outputs/path_agents_{cenario}.png")