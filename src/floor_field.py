import numpy as np
import heapq
from typing import List, Tuple, Dict

class FloorFieldGenerator:
    @staticmethod
    def generate(shape: Tuple[int, int], exits_dict: Dict[str, List[Tuple[int, int]]], walls: List[Tuple[int, int]]) -> np.ndarray:
        rows, cols = shape
        floor_field = np.full((rows, cols), 500.0)
        queue = []
        
        # Extrai todas as células independentemente de qual porta pertencem
        all_exit_cells = [cell for cells in exits_dict.values() for cell in cells]
        
        for r, c in all_exit_cells:
            floor_field[r, c] = 1.0  
            heapq.heappush(queue, (1.0, r, c))
            
        walls_set = set(walls)
        
        while queue:
            current_dist, r, c = heapq.heappop(queue)
            
            if current_dist > floor_field[r, c]:
                continue
                
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                        
                    nr, nc = r + dr, c + dc
                    
                    if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in walls_set:
                        weight_increment = 1.0 if (dr == 0 or dc == 0) else 1.5
                        new_dist = current_dist + weight_increment
                        
                        if new_dist < floor_field[nr, nc]:
                            floor_field[nr, nc] = new_dist
                            heapq.heappush(queue, (new_dist, nr, nc))
                            
        for r, c in walls:
            floor_field[r, c] = 500.0
            
        return floor_field