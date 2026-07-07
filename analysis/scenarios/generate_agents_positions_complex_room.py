from src.metrics import ScenarioManager
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine
from src.visualize_metrics import VisualizeMetrics

config_exits = {
    "Porta_principal": [(10, 0), (9, 0)]
}

# Cria o cenário onde ficarão todos os agents
shape, exits, walls = ScenarioManager.complex_scenario_custom_exits(config_exits)
ff = FloorFieldGenerator.generate(shape, exits, walls)

# Posiciona todos os agents para simualção
engine = SimulationEngine(ff, exits, walls, p_wait=0.5)
num_agentes_teste = 130
engine.populate_randomly(num_agentes_teste)

# Plota o cenário e uma instância da posição aleatória dos agents
caminhos_dos_agentes = engine.agent_paths
VisualizeMetrics.plot_simulation_trajectory(ff, caminhos_dos_agentes, 'complex_room')