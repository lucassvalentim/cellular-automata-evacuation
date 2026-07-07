from src.visualize_metrics import VisualizeMetrics
from src.metrics import ScenarioManager
from src.floor_field import FloorFieldGenerator

config_estreita = {
    "Porta_Principal": [(7, 0), (8, 0)]
}

shape, exits, walls = ScenarioManager.simple_room_custom_exits(config_estreita)
ff = FloorFieldGenerator.generate(shape, exits, walls)

VisualizeMetrics.plot_scenarios(ff, 'simple_room')