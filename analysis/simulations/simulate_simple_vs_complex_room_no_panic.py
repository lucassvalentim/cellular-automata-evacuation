import random
import numpy as np

from src.metrics import ScenarioManager, MetricsCollector
from src.floor_field import FloorFieldGenerator

random.seed(42)
np.random.seed(42)

config_simple_room = {
    "Porta_Principal": [(7, 0), (8, 0)]
}

config_complex_room = {
    "Porta_principal": [(10, 0), (9, 0)]
}

# REALIZA A SIMULAÇÃO PARA O QUARTO MAIS SIMPLES
print("Executando bateria de testes estatísticos para validação do simple room...")
shape_simple_room, exits_simple_room, walls_simple_room = ScenarioManager.simple_room_custom_exits(config_simple_room)
ff_simple_room = FloorFieldGenerator.generate(shape_simple_room, exits_simple_room, walls_simple_room)

collector_simple_room = MetricsCollector(shape_simple_room, exits_simple_room, walls_simple_room)
collector_simple_room.run_batch(num_agents=65, num_simulations=100)

collector_simple_room.save_history('outputs/simulations/history_simple_room_no_panic.csv')
collector_simple_room.save_density(ff_simple_room, 'outputs/heatmaps/density_simple_room_no_panic.png')

# REALIZA A SIMULAÇÃO PARA O QUARTO MAIS COMPLEXO
print("Executando bateria de testes estatísticos para validação do complex room...")
shape_complex_room, exits_complex_room, walls_complex_room = ScenarioManager.complex_scenario_custom_exits(config_complex_room)
ff_complex_room = FloorFieldGenerator.generate(shape_complex_room, exits_complex_room, walls_complex_room)

collector_complex_room = MetricsCollector(shape_complex_room, exits_complex_room, walls_complex_room)
collector_complex_room.run_batch(num_agents=130, num_simulations=100)

collector_complex_room.save_history('outputs/simulations/history_complex_room_no_panic.csv')
collector_complex_room.save_density(ff_complex_room, 'outputs/heatmaps/density_complex_room_no_panic.png')