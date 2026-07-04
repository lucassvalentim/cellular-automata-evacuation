import random
from typing import List, Tuple, Dict, Set
import numpy as np
from src.agent import PedestrianAgent

class SimulationEngine:
    """
    Gerencia a execução síncrona do autómato celular, resolvendo conflitos
    por sorteio e limpando os agentes que cruzam as saídas.
    """
    def __init__(self, floor_field: np.ndarray, exits: List[Tuple[int, int]], walls: List[Tuple[int, int]], p_wait: float = 0.5):
        self.floor_field = floor_field
        self.exits = set(exits)
        self.walls = set(walls)
        self.p_wait = p_wait
        self.agents: List[PedestrianAgent] = []
        self.agent_paths: Dict[int, List[Tuple[int, int]]] = {}
        
    def populate_randomly(self, num_agents: int):
        self.agents = []
        self.agent_paths = {}
        rows, cols = self.floor_field.shape
        valid_positions = []
        
        # Mapeia células disponíveis para receber pedestres inicialmente
        for r in range(rows):
            for c in range(cols):
                if (r, c) not in self.walls and (r, c) not in self.exits:
                    valid_positions.append((r, c))
                    
        chosen_positions = random.sample(valid_positions, min(num_agents, len(valid_positions)))
        for idx, pos in enumerate(chosen_positions):
            self.agents.append(PedestrianAgent(idx, pos, self.p_wait))
            self.agent_paths[idx] = [pos]
            
    def step(self) -> int:
        """Executa um passo de tempo discreto (t -> t+1) de forma síncrona."""
        if not self.agents:
            return 0
            
        occupied_cells = {agent.pos for agent in self.agents}
        intentions: Dict[Tuple[int, int], List[PedestrianAgent]] = {}
        
        # Fase de cálculo das rotas individuais
        for agent in self.agents:
            other_occupied = occupied_cells - {agent.pos}
            target = agent.choose_intent(self.floor_field, other_occupied, self.walls)
            
            if target not in intentions:
                intentions[target] = []
            intentions[target].append(agent)
            
        # Fase de Resolução de Conflitos e Atualização do Reticulado
        evacuated = set()
        
        for target, candidates in intentions.items():
            if len(candidates) == 1:
                candidates[0].pos = target
            else:
                winner = random.choice(candidates)
                winner.pos = target
            
            for candidate in candidates:
                self.agent_paths[candidate.agent_id].append(candidate.pos)

            # Remoção imediata ao alcançar a saída
            if target in self.exits:
                for candidate in candidates:
                    if candidate.pos == target:
                        evacuated.add(candidate)
                        
        # Mantem apenas os agentes ativos no reticulado
        self.agents = [a for a in self.agents if a not in evacuated]
        return len(self.agents)

    def simulate(self, max_steps: int = 2000) -> int:
        steps = 0
        while len(self.agents) > 0 and steps < max_steps:
            self.step()
            steps += 1
        return steps