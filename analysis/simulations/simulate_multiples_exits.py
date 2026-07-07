import os
import random
import numpy as np
from src.metrics import ScenarioManager
from src.floor_field import FloorFieldGenerator
from src.engine import SimulationEngine
from src.visualize_metrics import VisualizeMetrics

def run_experiment(config_name: str, exits_dict: dict, num_agents: int = 120, p_panic: float = 0.3):
    print(f"\n--- Iniciando Simulação: {config_name} ---")
    
    # 1. Geração do Cenário Parametrizado
    shape, exits, walls = ScenarioManager.complex_scenario_custom_exits(exits_dict)
    ff = FloorFieldGenerator.generate(shape, exits_dict, walls)
    
    # 2. Inicialização do Motor de Simulação
    engine = SimulationEngine(ff, exits_dict, walls, p_wait=0.5, p_panic=p_panic)
    engine.populate_randomly(num_agents=num_agents)
    
    # 3. Execução Síncrona
    passos_totais, mapa_densidade, eficiencia = engine.simulate(max_steps=3000)
    
    # 4. Exibição dos Resultados Analíticos
    print(f"Tempo Total de Evacuação: {passos_totais} passos (Aprox. {passos_totais * 0.4:.1f} segundos)")
    print("Eficiência Estrutural (Indivíduos por Saída):")
    for porta, qtd in eficiencia.items():
        print(f"  -> {porta}: {qtd} pessoas")
        
    # 5. Geração do Heatmap Minimalista
    output_file = f"outputs/heatmaps/fase3_densidade_{config_name.lower().replace(' ', '_')}.png"
    VisualizeMetrics.plot_density_heatmap(
        density_map=mapa_densidade,
        floor_field=ff,
        title=f"Congestionamento: {config_name} (Pânico 30%)",
        output_path=output_file
    )
    
    return passos_totais, eficiencia

if __name__ == "__main__":
    # Fixando semente para reprodutibilidade no simpósio
    random.seed(101)
    np.random.seed(101)
    
    os.makedirs("outputs/heatmaps", exist_ok=True)
    
    # ==========================================
    # TOPOLOGIA A: Saída Única Larga (4 células conjuntas)
    # ==========================================
    config_saida_unica = {
        "Porta_Central_Larga": [(8, 0), (9, 0), (10, 0), (11, 0)]
    }
    
    # ==========================================
    # TOPOLOGIA B: Múltiplas Saídas Distribuídas (4 células separadas)
    # ==========================================
    config_multiplas_saidas = {
        "Saida_Topo": [(4, 31)],
        "Saida_Meio_Sup": [(9, 0)],
        "Saida_Meio_Inf": [(14, 31)],
        "Saida_Base": [(18, 0)]
    }
    
    # Execução sequencial para garantir o mesmo estado base do gerador aleatório
    # Utilizamos 120 agentes para gerar densidade suficiente no mapa (20x32)
    passos_a, ef_a = run_experiment("Saida Unica", config_saida_unica, num_agents=130)
    passos_b, ef_b = run_experiment("Multiplas Saidas", config_multiplas_saidas, num_agents=130)
    
    # ==========================================
    # CONCLUSÃO AUTOMATIZADA
    # ==========================================
    print("\n" + "="*50)
    print("RESUMO DA COMPARAÇÃO (Fase 3)")
    print("="*50)
    print(f"Tempo Saída Única:      {passos_a} passos")
    print(f"Tempo Múltiplas Saídas: {passos_b} passos")
    
    melhoria = ((passos_a - passos_b) / passos_a) * 100
    if melhoria > 0:
        print(f"\nConclusão: A topologia de múltiplas saídas mitigou o efeito do pânico,")
        print(f"reduzindo o tempo de evacuação em {melhoria:.1f}%.")
    else:
        print(f"\nConclusão: A fragmentação das saídas não apresentou ganho de tempo,")
        print(f"podendo ter gerado gargalos secundários na navegação.")