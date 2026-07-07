import random
import numpy as np

from src.metrics import ScenarioManager, MetricsCollector

random.seed(42)
np.random.seed(42)

# Cria o cenário onde ficarão todos os agents
print("Executando bateria de testes estatísticos para validação...")
shape, exits, walls = ScenarioManager.complex_scenario()

# Posiciona todos os agents para simualção
collector = MetricsCollector(shape, exits, walls, p_wait=0.5) 
collector.run_batch(num_agents=130, num_simulations=100)
collector.report(cenario='complex')