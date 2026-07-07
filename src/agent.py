import random
import numpy as np
from typing import Tuple, Set

class PedestrianAgent:
    def __init__(self, agent_id: int, start_pos: Tuple[int, int], p_wait: float = 0.5, p_panic: float = 0.0):
        self.agent_id = agent_id
        self.pos = start_pos
        self.p_wait = p_wait
        self.p_panic = p_panic

    def choose_intent(self, floor_field: np.ndarray, other_occupied: Set[Tuple[int, int]], walls: Set[Tuple[int, int]]) -> Tuple[int, int]:
        r, c = self.pos
        
        # Avaliação estocástica do estado de pânico
        if random.random() < self.p_panic:
            return (r, c) # Indivíduo paralisado no passo atual
            
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
            
        if random.random() < self.p_wait:
            return (r, c)
        else:
            for cell, val in neighbors[1:]:
                if cell not in other_occupied:
                    return cell
            return (r, c)