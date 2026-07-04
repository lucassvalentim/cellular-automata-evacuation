import numpy as np
import heapq
from typing import List, Tuple

class FloorFieldGenerator:
    """
    Responsável por estruturar o reticulado e calcular a matriz de pesos (Floor Field)
    a partir das saídas usando a Vizinhança de Moore e custos ortogonais/diagonais.
    """
    @staticmethod
    def generate(shape: Tuple[int, int], exits: List[Tuple[int, int]], walls: List[Tuple[int, int]]) -> np.ndarray:
        rows, cols = shape
        # Inicializa todo o campo com o valor de parede
        floor_field = np.full((rows, cols), 500.0)
        
        # Fila de prioridade para a propagação de Dijkstra-like
        queue = []
        
        for r, c in exits:
            floor_field[r, c] = 1.0
            heapq.heappush(queue, (1.0, r, c))
            
        walls_set = set(walls)
        
        # Algoritmo de propagação de pesos pelas 8 direções (Moore)
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
                        # Acréscimo de +1.0 para movimentos ortogonais e +1.5 para diagonais
                        weight_increment = 1.0 if (dr == 0 or dc == 0) else 1.5
                        new_dist = current_dist + weight_increment
                        
                        if new_dist < floor_field[nr, nc]:
                            floor_field[nr, nc] = new_dist
                            heapq.heappush(queue, (new_dist, nr, nc))
                            
        # Garante que todas as paredes mantenham rigidamente o valor limite de 500
        for r, c in walls:
            floor_field[r, c] = 500.0
            
        return floor_field