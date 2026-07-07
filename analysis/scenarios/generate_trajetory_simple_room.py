import numpy as np
from src.metrics import ScenarioManager
from src.visualize_metrics import VisualizeMetrics
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine, PedestrianAgent

config_estreita = {
    "Porta_Principal": [(7, 0), (8, 0)]
}

shape, exits, walls = ScenarioManager.simple_room_custom_exits(config_estreita)
ff = FloorFieldGenerator.generate(shape, exits, walls)

engine = SimulationEngine(ff, exits, walls, p_wait=0.5)

num_agentes_teste = 2

agent1 = PedestrianAgent(0, (7, 14))
agent2 = PedestrianAgent(1, (12, 6))

engine.agent_paths[0] = [(7,14)]
engine.agent_paths[1] = [(12, 6)]

engine.agents.append(agent1)
engine.agents.append(agent2)
    
passos_totais = engine.simulate()
print(f"Simulação finalizada em {passos_totais} passos.")

caminhos_dos_agentes = engine.agent_paths

VisualizeMetrics.plot_simulation_trajectory(ff, caminhos_dos_agentes, 'simple_room')