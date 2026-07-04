import random
import numpy as np
from typing import Tuple, Set

class PedestrianAgent:
    """
    Representa o indivíduo e encapsula a tomada de decisão probabilística 
    de movimento com base na matriz do Campo de Piso.
    """
    def __init__(self, agent_id: int, start_pos: Tuple[int, int], p_wait: float = 0.5):
        self.agent_id = agent_id
        self.pos = start_pos
        self.p_wait = p_wait

    def choose_intent(self, floor_field: np.ndarray, other_occupied: Set[Tuple[int, int]], walls: Set[Tuple[int, int]]) -> Tuple[int, int]:
        r, c = self.pos
        rows, cols = floor_field.shape
        
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in walls:
                    neighbors.append(((nr, nc), floor_field[nr, nc]))
                    
        if not neighbors:
            return (r, c)
            
        neighbors.sort(key=lambda x: x[1])
        best_cell, best_val = neighbors[0]
        
        if best_cell not in other_occupied or best_cell == self.pos:
            return best_cell
            
        # Fusão lógica [Varas vs Carneiro]: Se estiver ocupada, escolhe via probabilidade
        if random.random() < self.p_wait:
            return (r, c)
        else:
            for cell, val in neighbors[1:]:
                if cell not in other_occupied:
                    return cell
            return (r, c)