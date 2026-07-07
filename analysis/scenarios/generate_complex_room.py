from src.visualize_metrics import VisualizeMetrics
from src.metrics import ScenarioManager
from src.engine import SimulationEngine, PedestrianAgent
from src.floor_field import FloorFieldGenerator

config_exits = {
    "Porta_principal": [(10, 0), (9, 0)]
}

# Cria o cenário onde ficarão todos os agents
shape, exits, walls = ScenarioManager.complex_scenario_custom_exits(config_exits)
ff = FloorFieldGenerator.generate(shape, exits, walls)

VisualizeMetrics.plot_scenarios(ff, 'complex_room')