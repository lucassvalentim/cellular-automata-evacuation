import random
import numpy as np
from src.metrics import ScenarioManager, MetricsCollector
from src.visualize_metrics import VisualizeMetrics
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine, PedestrianAgent

# Configuração A: Uma saída Estreita (1 célula)
config_estreita = {
    "Porta_Principal": [(7, 0)]
}

# Configuração B: Uma saída Larga (3 células juntas, permitindo 3 pessoas simultaneamente)
config_larga = {
    "Porta_Principal": [(7, 0), (8, 0), (9, 0)]
}

# Configuração C: Múltiplas Saídas Estratégicas
config_multiplas = {
    "Saida_Superior": [(2, 0), (3, 0)],
    "Saida_Inferior": [(13, 0), (14, 0)]
}

# Executando um experimento com a Configuração C
shape, exits_dict, walls = ScenarioManager.simple_room_custom_exits(config_multiplas)
ff = FloorFieldGenerator.generate(shape, exits_dict, walls)

engine = SimulationEngine(ff, exits_dict, walls, p_wait=0.5, p_panic=0.3)
engine.populate_randomly(num_agents=100)

passos, densidade, eficiencia = engine.simulate()

print(f"Evacuação concluída em {passos} passos.")
print(f"Eficiência Analítica por Porta Lógica: {eficiencia}")

# Gera e salva o mapa de calor com estética acadêmica
caminho_imagem = "outputs/heatmaps/cenario_simples_panico_03.png"
VisualizeMetrics.plot_density_heatmap(
    density_map=densidade, 
    floor_field=ff, 
    title="Distribuição Espacial de Congestionamento (Pânico: 30%)",
    output_path=caminho_imagem
)
# Retornará algo como: {'Saida_Superior': 42, 'Saida_Inferior': 58}