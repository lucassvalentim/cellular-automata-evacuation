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

p_wait_list = [0.1, 0.3, 0.5]

for p_wait in p_wait_list:
    # REALIZA A SIMULAÇÃO PARA O QUARTO MAIS SIMPLES
    print("Executando bateria de testes estatísticos para validação do simple room...")
    shape_simple_room, exits_simple_room, walls_simple_room = ScenarioManager.simple_room_custom_exits(config_simple_room)
    ff_simple_room = FloorFieldGenerator.generate(shape_simple_room, exits_simple_room, walls_simple_room)

    collector_simple_room = MetricsCollector(shape_simple_room, exits_simple_room, walls_simple_room, p_panic=p_wait)
    collector_simple_room.run_batch(num_agents=65, num_simulations=100)

    collector_simple_room.save_history(f'outputs/simulations/history_simple_room_{p_wait}.csv')
    collector_simple_room.save_density(ff_simple_room, f'outputs/heatmaps/density_simple_room_{p_wait}.png')

    # REALIZA A SIMULAÇÃO PARA O QUARTO MAIS COMPLEXO
    print("Executando bateria de testes estatísticos para validação do complex room...")
    shape_complex_room, exits_complex_room, walls_complex_room = ScenarioManager.complex_scenario_custom_exits(config_complex_room)
    ff_complex_room = FloorFieldGenerator.generate(shape_complex_room, exits_complex_room, walls_complex_room)

    collector_complex_room = MetricsCollector(shape_complex_room, exits_complex_room, walls_complex_room, p_panic=p_wait)
    collector_complex_room.run_batch(num_agents=130, num_simulations=100)

    collector_complex_room.save_history(f'outputs/simulations/history_complex_room_{p_wait}.csv')
    collector_complex_room.save_density(ff_complex_room, f'outputs/heatmaps/density_complex_room_{p_wait}.png')