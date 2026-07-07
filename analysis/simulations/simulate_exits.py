import random
import numpy as np
import os
import csv

from src.visualize_metrics import VisualizeMetrics
from src.metrics import ScenarioManager, MetricsCollector
from src.floor_field import FloorFieldGenerator

random.seed(42)
np.random.seed(42)

# Define cada uma das saidas
exits = { "5" : (5, 0),  "8" : (8, 0), "10" : (10, 0), "11" : (11, 0), 
        "12" : (12, 0), "13" : (13, 0), "14" : (14, 0), "15" : (15, 1), 
        "16" : (15, 2), "17" : (15, 3), "18" : (15, 6), "20" : (15, 12), 
        "22" : (15, 18), "23" : (14, 19), "24" : (13, 19), "25" : (12, 19), 
        "26" : (11, 19), "27" : (10, 19), "28" : (9, 19), "29" : (8, 19), 
        "30" : (7, 19) }

# Configuração da Simulação
numero_de_simulacoes = 10
solucoes = []

for exit_label, pos in exits.items():
    # Cria o cenário onde ficarão todos os agents
    shape, _, walls = ScenarioManager.scenario_simulate_exits(exits=[pos])
    ff = FloorFieldGenerator.generate(shape, [pos], walls)

    collector = MetricsCollector(shape, [pos], walls, p_wait=0.5)
    collector.run_batch(
        num_agents=10, 
        num_simulations=numero_de_simulacoes, 
        type_populate='populate_exits'
    )
    
    # Extrai os resultados e realiza os cálculos solicitados
    results = np.array(collector.get_history())
    evacuacao_media = results.mean()
    tempo = evacuacao_media * 0.4
    
    # Armazena os dados da iteração atual em formato de linha para o CSV
    linha_resultado = {
        'Saida': exit_label,
        'numero de simulaçoes': numero_de_simulacoes,
        'evacuação media': evacuacao_media,
        'tempo': tempo
    }
    solucoes.append(linha_resultado)
    
    # Print no terminal para acompanhamento do progresso
    print(f"Saída {exit_label}: Evacuação Média = {evacuacao_media:.2f} | Tempo = {tempo:.2f}s")


# EXPORTAÇÃO DOS RESULTADOS PARA CSV
diretorio_saida = "outputs"
os.makedirs(diretorio_saida, exist_ok=True)

# Define o caminho completo do arquivo
caminho_csv = os.path.join(diretorio_saida, "resultados_analise_estrutural.csv")

# Escreve os dados no arquivo
with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    colunas = ['Saida', 'numero de simulaçoes', 'evacuação media', 'tempo']
    writer = csv.DictWriter(arquivo_csv, fieldnames=colunas)
    
    writer.writeheader()
    for solucao in solucoes:
        writer.writerow(solucao)

print(f"\n✅ Resultados salvos com sucesso no caminho: {caminho_csv}")