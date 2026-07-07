from src.visualize_metrics import VisualizeMetrics
from src.metrics import ScenarioManager
from src.engine import SimulationEngine
from src.floor_field import FloorFieldGenerator

config_exit = {
    "saida1": [(15,2)],
    "saida2": [(3,19)]
}
# Cria o cenário onde ficarão todos os agents
shape, exits, walls = ScenarioManager.scenario_simulate_exits(exits_dict=config_exit)
ff = FloorFieldGenerator.generate(shape, exits, walls)

# Posiciona todos os agents para simualção
engine = SimulationEngine(ff, exits, walls, p_wait=0.5)
engine.populate_exits()

# Plota o cenário e uma instância da posição aleatória dos agents
caminhos_dos_agentes = engine.agent_paths
VisualizeMetrics.plot_simulation_trajectory(ff, caminhos_dos_agentes, 'room_exits')
VisualizeMetrics.plot_scenarios(ff, 'room_exits')