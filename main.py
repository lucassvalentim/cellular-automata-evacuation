import random
import numpy as np
from src.metrics import ScenarioManager, MetricsCollector
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine

if __name__ == "__main__":
    # Configurando semente aleatória para consistência de replicação
    random.seed(42)
    np.random.seed(42)
    
    print("1. Executando bateria de testes estatísticos para validação...")
    shape, exits, walls = ScenarioManager.simple_room_one_obstacle()
    
    collector = MetricsCollector(shape, exits, walls, p_wait=0.5)
    collector.run_batch(num_agents=50, num_simulations=100)
    collector.report()
    
    print("\n2. Executando uma simulação única para extrair trajetórias dos agentes...")
    
    # Gera o campo de piso e inicializa o motor individualizado
    ff = FloorFieldGenerator.generate(shape, exits, walls)
    engine = SimulationEngine(ff, exits, walls, p_wait=0.5)
    
    # Vamos colocar apenas 3 agentes para inspecionar o output do caminho de forma limpa
    num_agentes_teste = 3
    engine.populate_randomly(num_agents=num_agentes_teste)
    
    # Executa a simulação completa
    passos_totais = engine.simulate()
    print(f"Simulação finalizada em {passos_totais} passos.")
    
    # Recupera o dicionário de caminhos gerado pelo motor
    caminhos_dos_agentes = engine.agent_paths
    
    print("\nTrajetórias capturadas (prontas para plotagem no mapa):")
    print("="*55)
    for agent_id, rota in caminhos_dos_agentes.items():
        print(f"Pedestre ID {agent_id}:")
        print(f" -> Posição Inicial: {rota[0]}")
        print(f" -> Caminho percorrido: {rota}")
        print(f" -> Posição Final (Saída): {rota[-1]}")
        print(f" -> Total de posições registradas: {len(rota)}")
        print("-"*55)