import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from typing import Tuple, List, Dict

from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine

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
    def __init__(self, shape, exits, walls, p_wait=0.5):
        self.shape = shape
        self.exits = exits
        self.walls = walls
        self.p_wait = p_wait
        self.history = []

    def run_batch(self, num_agents: int, num_simulations: int, type_populate='populate_randomly'):
        self.history = []
        # Gera o campo de piso estático uma única vez para o cenário
        ff = FloorFieldGenerator.generate(self.shape, self.exits, self.walls)
        
        for _ in range(num_simulations):
            engine = SimulationEngine(ff, self.exits, self.walls, self.p_wait)
            
            if type_populate == 'populate_randomly':
                engine.populate_randomly(num_agents)
            elif type_populate == 'populate_exits':
                engine.populate_exits()

            steps = engine.simulate()
            self.history.append(steps)

    def get_history(self):
        if not self.history:
            return None

        return self.history
            
    def report(self, cenario):
        if not self.history:
            print("Nenhum dado coletado.")
            return

        series = pd.Series(self.history)
        print("\n" + "="*45)
        print("        RELATÓRIO ESTATÍSTICO DE EVACUAÇÃO       ")
        print("="*45)
        print(f"Média Geral (Passos):    {series.mean():.2f}")
        print(f"Desvio Padrão (s):       {series.std():.2f}")
        print(f"Mediana (Xm):            {series.median():.2f}")
        print(f"Moda (Mo):               {series.mode().iloc[0]:.2f}")
        print(f"Tempo Mínimo Registrado: {series.min()} passos")
        print(f"Tempo Máximo Registrado: {series.max()} passos")
        print("="*45)
        series.to_csv(f'outputs/history_{cenario}.csv', index=False)