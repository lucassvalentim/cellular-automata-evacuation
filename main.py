import os
import random
import numpy as np
from src.metrics import ScenarioManager
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine
from src.visualize_metrics import VisualizeMetrics

random.seed(42)
np.random.seed(42)

# Garante o diretório de imagens
os.makedirs("outputs/heatmaps", exist_ok=True)

# 1. Carrega o cenário complexo
shape, exits, walls = ScenarioManager.complex_scenario_custom_exits({"saida1":[(10,0)]})
ff = FloorFieldGenerator.generate(shape, exits, walls)

# 2. Configura a simulação com um nível de pânico específico
engine = SimulationEngine(ff, exits, walls, p_wait=0.5, p_panic=0.3)
engine.populate_randomly(num_agents=100)

# 3. Executa e extrai as métricas
passos_totais, mapa_densidade, uso_saidas = engine.simulate(max_steps=3000)

print(f"Evacuação finalizada em {passos_totais} passos.")
print("Eficiência das saídas:", uso_saidas)

# 4. Gera e salva o mapa de calor com estética acadêmica
caminho_imagem = "outputs/heatmaps/cenario_complexo_panico_03.png"
VisualizeMetrics.plot_density_heatmap(
    density_map=mapa_densidade, 
    floor_field=ff, 
    title="Distribuição Espacial de Congestionamento (Pânico: 30%)",
    output_path=caminho_imagem
)