import random
from typing import List, Tuple, Dict, Set
import numpy as np
from src.agent import PedestrianAgent

class SimulationEngine:
    def __init__(self, floor_field: np.ndarray, exits_dict: Dict[str, List[Tuple[int, int]]], walls: List[Tuple[int, int]], p_wait: float = 0.5, p_panic: float = 0.0):
        self.floor_field = floor_field
        self.exits_dict = exits_dict
        self.walls = set(walls)
        self.p_wait = p_wait
        self.p_panic = p_panic
        self.agents: List[PedestrianAgent] = []
        
        # MAPEAMENTO REVERSO: Qual célula pertence a qual saída?
        self.cell_to_exit_name = {}
        for exit_name, cells in exits_dict.items():
            for cell in cells:
                self.cell_to_exit_name[cell] = exit_name
                
        # Set plano para verificação rápida de colisão O(1) no laço de tempo
        self.exit_cells_set = set(self.cell_to_exit_name.keys())
        
        self.agent_paths: Dict[int, List[Tuple[int, int]]] = {}
        self.density_map = np.zeros(floor_field.shape, dtype=int)
        
        # A eficiência agora é rastreada pelo NOME da porta, não pela célula
        self.exit_efficiency = {exit_name: 0 for exit_name in exits_dict.keys()}
        
    def populate_randomly(self, num_agents: int):
        self.agents = []
        self.agent_paths = {}
        self.density_map.fill(0)
        for exit_name in self.exit_efficiency:
            self.exit_efficiency[exit_name] = 0
            
        rows, cols = self.floor_field.shape
        valid_positions = [(r, c) for r in range(rows) for c in range(cols) if (r, c) not in self.walls and (r, c) not in self.exit_cells_set]
                    
        chosen_positions = random.sample(valid_positions, min(num_agents, len(valid_positions)))
        for idx, pos in enumerate(chosen_positions):
            self.agents.append(PedestrianAgent(idx, pos, self.p_wait, self.p_panic))
            self.agent_paths[idx] = [pos]
            self.density_map[pos] += 1
    
    def populate_exits(self):
        self.agents = []
        self.agent_paths = {}
        rows, cols = self.floor_field.shape

        positions = []
        for c in range(5, cols, 3):
            for r in [1, 6, 12]:
                qtd = 0
                if r == 1 or r == 12:
                    qtd = 3
                else:
                    qtd = 4
                for i in range(0, qtd):
                    positions.append((r + i, c))
        
        for idx, pos in enumerate(positions):
            self.agents.append(PedestrianAgent(idx, pos, self.p_wait))
            self.agent_paths[idx] = [pos]
            
    def step(self) -> int:
        if not self.agents:
            return 0
            
        occupied_cells = {agent.pos for agent in self.agents}
        intentions: Dict[Tuple[int, int], List[PedestrianAgent]] = {}
        
        for agent in self.agents:
            other_occupied = occupied_cells - {agent.pos}
            target = agent.choose_intent(self.floor_field, other_occupied, self.walls)
            
            if target not in intentions:
                intentions[target] = []
            intentions[target].append(agent)
            
        evacuated = set()
        
        for target, candidates in intentions.items():
            if len(candidates) == 1:
                candidates[0].pos = target
            else:
                winner = random.choice(candidates)
                winner.pos = target
                
            for candidate in candidates:
                self.agent_paths[candidate.agent_id].append(candidate.pos)
                self.density_map[candidate.pos] += 1 
                
            # Identifica se o alvo é uma célula de saída
            if target in self.exit_cells_set:
                for candidate in candidates:
                    if candidate.pos == target:
                        evacuated.add(candidate)
                        
                        # Recupera a qual porta esta célula pertence e soma a métrica
                        nome_da_porta = self.cell_to_exit_name[target]
                        self.exit_efficiency[nome_da_porta] += 1 
                        
        self.agents = [a for a in self.agents if a not in evacuated]
        return len(self.agents)

    def simulate(self, max_steps: int = 2000) -> Tuple[int, np.ndarray, Dict[str, int]]:
        steps = 0
        while len(self.agents) > 0 and steps < max_steps:
            self.step()
            steps += 1
        return steps, self.density_map, self.exit_efficiency