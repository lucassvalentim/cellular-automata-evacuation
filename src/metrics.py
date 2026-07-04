import pandas as pd
from typing import Tuple, List
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine

class ScenarioManager:
    """
    Facilita a montagem geométrica automatizada de layouts de teste para validação.
    """
    @staticmethod
    def simple_room_one_obstacle() -> Tuple[Tuple[int, int], List[Tuple[int, int]], List[Tuple[int, int]]]:
        shape = (16, 20)
        exits = [(7, 0), (8, 0)]
        
        walls = []
        # Paredes externas
        for r in range(shape[0]):
            for c in range(shape[1]):
                if r == 0 or r == shape[0] - 1 or c == 0 or c == shape[1] - 1:
                    if (r, c) not in exits:
                        walls.append((r, c))
                        
        # Obstáculo ortogonal centralizado interno
        for r in range(5, 12):
            walls.append((r, 4))
            
        return shape, exits, walls

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

    def run_batch(self, num_agents: int, num_simulations: int):
        self.history = []
        # Gera o campo de piso estático uma única vez para o cenário
        ff = FloorFieldGenerator.generate(self.shape, self.exits, self.walls)
        
        for _ in range(num_simulations):
            engine = SimulationEngine(ff, self.exits, self.walls, self.p_wait)
            engine.populate_randomly(num_agents)
            steps = engine.simulate()
            self.history.append(steps)
            
    def report(self):
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
        series.to_csv('outputs/history.csv', index=False)