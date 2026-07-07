import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from typing import Tuple, List, Dict

from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine
from src.visualize_metrics import VisualizeMetrics

class ScenarioManager:
    """
    Facilita a montagem geométrica automatizada de layouts de teste para validação.
    """
    @staticmethod
    def simple_room_custom_exits(exits_dict: Dict[str, List[Tuple[int, int]]]) -> Tuple[Tuple[int, int], Dict[str, List[Tuple[int, int]]], List[Tuple[int, int]]]:
        """
        Cenário simples que aceita qualquer configuração de saídas injetada externamente.
        """
        shape = (16, 20)
        walls = []
        
        # Achata todas as células de saída em um Set para verificação rápida (O(1))
        all_exit_cells = {cell for cells in exits_dict.values() for cell in cells}
        
        # Paredes externas
        for r in range(shape[0]):
            for c in range(shape[1]):
                if r == 0 or r == shape[0] - 1 or c == 0 or c == shape[1] - 1:
                    if (r, c) not in all_exit_cells:
                        walls.append((r, c))
                        
        # Obstáculo ortogonal centralizado interno
        for r in range(5, 12):
            walls.append((r, 4))
            
        return shape, exits_dict, walls

    # Saída na parede superior esquerda, como indicado pelos pontinhos na imagem
    @staticmethod
    def complex_scenario_custom_exits(exits_dict: Dict[str, List[Tuple[int, int]]]) -> Tuple[Tuple[int, int], Dict[str, List[Tuple[int, int]]], List[Tuple[int, int]]]:
        """
        Cenário complexo adaptado para saídas parametrizáveis.
        """
        shape = (20, 32)
        walls = []
        all_exit_cells = {cell for cells in exits_dict.values() for cell in cells}
        
        # Paredes Externas
        for r in range(shape[0]):
            for c in range(shape[1]):
                if r == 0 or r == shape[0] - 1 or c == 0 or c == shape[1] - 1:
                    if (r, c) not in all_exit_cells:
                        walls.append((r, c))

        # Paredes Internas (mantidas conforme seu design)
        for c in range(1, 10): walls.append((7, c))
        for c in range(28, 31): walls.append((7, c))
        for c in range(25, 31): walls.append((12, c))
        for c in range(17, 19): walls.append((12, c))
        for c in range(1, 10): walls.append((12, c))
        for r in range(1, 8): walls.append((r, 13))
        for r in range(12, 20): walls.append((r, 13))
        for r in range(12, 20): walls.append((r, 19))
        for r in range(1, 8): walls.append((r, 24))
        for c in range(17, 25): walls.append((7, c))

        return shape, exits_dict, walls

    @staticmethod
    def scenario_simulate_exits(exits_dict: Dict[str, List[Tuple[int, int]]]) -> Tuple[Tuple[int, int], Dict[str, List[Tuple[int, int]]], List[Tuple[int, int]]]:
        shape = (16, 20)
                
        walls = []
        all_exit_cells = {cell for cells in exits_dict.values() for cell in cells}

        # Paredes Externas (Borda da matriz, exceto a saída)
        for r in range(shape[0]):
            for c in range(shape[1]):
                if r == 0 or r == shape[0] - 1 or c == 0 or c == shape[1] - 1:
                    if (r, c) not in all_exit_cells:
                        walls.append((r, c))

        # Paredes Internas
        for r in range(1, 4): walls.append((r, 4))
        for r in range(6, 10): walls.append((r, 4))
        for r in range(12, 15): walls.append((r, 4))
        for r in range(1, 4): walls.append((r, 7))
        for r in range(6, 10): walls.append((r, 7))
        for r in range(12, 15): walls.append((r, 7))
        for r in range(1, 4): walls.append((r, 10))
        for r in range(6, 10): walls.append((r, 10))
        for r in range(12, 15): walls.append((r, 10))
        for r in range(1, 4): walls.append((r, 13))
        for r in range(6, 10): walls.append((r, 13))
        for r in range(12, 15): walls.append((r, 13))
        for r in range(1, 4): walls.append((r, 16))
        for r in range(6, 10): walls.append((r, 16))
        for r in range(12, 15): walls.append((r, 16))

        return shape, exits_dict, walls

class MetricsCollector:
    """
    Executa baterias repetidas de testes em lote para extrair consistência estatística.
    """
    def __init__(self, 
        shape : Tuple[int, int], 
        exits_dict: Dict[str, List[Tuple[int, int]]], 
        walls: List[Tuple[int, int]],
        p_wait: float = 0.5,
        p_panic: float = 0.0
    ):
        self.exits = exits_dict
        self.shape = shape
        self.walls = walls
        self.p_wait = p_wait
        self.p_panic = p_panic
        self.history = []
        self.density_map = np.zeros(shape, dtype=int)
        
        # A eficiência agora é rastreada pelo NOME da porta, não pela célula
        self.exit_efficiency = {exit_name: 0 for exit_name in exits_dict.keys()}

    def run_batch(self, num_agents: int, num_simulations: int, type_populate='populate_randomly'):
        self.history = []
        # Gera o campo de piso estático uma única vez para o cenário
        ff = FloorFieldGenerator.generate(self.shape, self.exits, self.walls)
        
        for _ in range(num_simulations):
            engine = SimulationEngine(ff, self.exits, self.walls, self.p_wait, self.p_panic)
            
            if type_populate == 'populate_randomly':
                engine.populate_randomly(num_agents)
            elif type_populate == 'populate_exits':
                engine.populate_exits()

            steps, self.density, self.exit_efficiency  = engine.simulate()
            
            self.history.append(steps)

    def get_history(self):
        if not self.history:
            return None

        return self.history

    def get_density(self):
        if not self.density:
            return None

        return self.density
    
    def get_exit_efficiency(self):
        if not self.exit_efficiency:
            return None

        return self.exit_efficiency
            
    def save_history(self, path):
        if not self.history:
            print("Nenhum dado coletado.")
            return
        
        series = pd.Series(self.history)
        series.to_csv(f'{path}', index=False)
    
    def save_density(self, ff, path):
        VisualizeMetrics.plot_density_heatmap(
            density_map=self.density, 
            floor_field=ff, 
            title=f"Distribuição Espacial de Congestionamento (Pânico: {self.p_wait}%)",
            output_path=path
        )