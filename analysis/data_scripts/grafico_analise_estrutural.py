import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurar estilo do matplotlib
plt.style.use('default')
plt.rcParams['font.size'] = 11
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
plt.rcParams['grid.linestyle'] = '--'

# Ler o arquivo CSV
df = pd.read_csv('outputs/simulations/resultados_analise_estrutural.csv')

# Calcular médias para cada saída
media_evacuacao = df.groupby('Saida')['evacuação media'].mean()
desvio_evacuacao = df.groupby('Saida')['evacuação media'].std()
tempo_media = df.groupby('Saida')['tempo'].mean()
tempo_desvio = df.groupby('Saida')['tempo'].std()

# Criar figura com 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# ============ GRÁFICO 1: Média de Evacuação ============
# Plotar pontos com barras de erro
ax1.errorbar(media_evacuacao.index, media_evacuacao.values, 
             yerr=desvio_evacuacao, 
             fmt='o', color='#2196F3', 
             capsize=5, capthick=2, elinewidth=1.5,
             markersize=9, markeredgecolor='black', markeredgewidth=0.5,
             label='Média de evacuação (± desvio padrão)')

# Linha contínua conectando os pontos
ax1.plot(media_evacuacao.index, media_evacuacao.values, 
         '-', color='#1976D2', linewidth=2, alpha=0.7)

# Configurar eixos
ax1.set_xlim(0, 35)
ax1.set_ylim(0, 110)
ax1.set_xticks(np.arange(0, 36, 5))
ax1.set_yticks(np.arange(0, 121, 20))
ax1.set_xlabel('Saída', fontsize=12, fontweight='bold')
ax1.set_ylabel('Média das interações', fontsize=12, fontweight='bold')
ax1.set_title('Média de Evacuação por Saída', fontsize=14, fontweight='bold', pad=15)

# Adicionar grade
ax1.grid(True, alpha=0.3, linestyle='--')

# Adicionar valores nos pontos
for i, (saida, valor) in enumerate(zip(media_evacuacao.index, media_evacuacao.values)):
    ax1.annotate(f'{valor:.1f}', 
                 xy=(saida, valor), 
                 xytext=(0, 8), 
                 textcoords='offset points',
                 ha='center',
                 fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# ============ GRÁFICO 2: Tempo ============
# Plotar pontos com barras de erro
ax2.errorbar(tempo_media.index, tempo_media.values, 
             yerr=tempo_desvio, 
             fmt='s', color='#FF5722', 
             capsize=5, capthick=2, elinewidth=1.5,
             markersize=9, markeredgecolor='black', markeredgewidth=0.5,
             label='Tempo médio (± desvio padrão)')

# Linha contínua conectando os pontos
ax2.plot(tempo_media.index, tempo_media.values, 
         '-', color='#D84315', linewidth=2, alpha=0.7)

# Configurar eixos
ax2.set_xlim(0, 35)
ax2.set_ylim(0, 50)
ax2.set_xticks(np.arange(0, 36, 5))
ax2.set_yticks(np.arange(0, 51, 10))
ax2.set_xlabel('Saída', fontsize=12, fontweight='bold')
ax2.set_ylabel('Tempo', fontsize=12, fontweight='bold')
ax2.set_title('Tempo Médio por Saída', fontsize=14, fontweight='bold', pad=15)

# Adicionar grade
ax2.grid(True, alpha=0.3, linestyle='--')

# Adicionar valores nos pontos
for i, (saida, valor) in enumerate(zip(tempo_media.index, tempo_media.values)):
    ax2.annotate(f'{valor:.1f}', 
                 xy=(saida, valor), 
                 xytext=(0, 8), 
                 textcoords='offset points',
                 ha='center',
                 fontsize=9,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# Ajustar layout
plt.tight_layout()
plt.savefig('outputs/graphics/meus_resultados.png', dpi=300, bbox_inches='tight')
plt.show()

# ============ GRÁFICO 3: Gráfico combinado com ambos os parâmetros ============
fig, ax1 = plt.subplots(figsize=(12, 7))

# Eixo y esquerdo - Média de evacuação
ax1.errorbar(media_evacuacao.index, media_evacuacao.values,  # type: ignore
             yerr=desvio_evacuacao, 
             fmt='o-', color="#02233E", 
             capsize=5, capthick=2, elinewidth=1.5,
             markersize=9, markeredgecolor='black', markeredgewidth=0.5,
             label='Média de evacuação', linewidth=2)
ax1.set_xlabel('Saída', fontsize=16, fontweight='bold')
ax1.set_ylabel('Média das interações', fontsize=16, fontweight='bold', color='#02233E')

# Aumentar os números dos eixos
ax1.tick_params(axis='both', labelsize=16)  # <-- AQUI: aumenta fonte dos números
ax1.tick_params(axis='y', labelcolor="#02233E")

ax1.tick_params(axis='y', labelcolor="#02233E")
ax1.set_xlim(0, 35)
ax1.set_ylim(0, 110)
ax1.set_xticks(np.arange(0, 36, 5))
ax1.set_yticks(np.arange(0, 121, 20))
ax1.grid(True, alpha=0.3, linestyle='--')

# Eixo y direito - Tempo
ax2 = ax1.twinx()
ax2.errorbar(tempo_media.index, tempo_media.values,  # type: ignore
             yerr=tempo_desvio, 
             fmt='s-', color='#FF5722', 
             capsize=5, capthick=2, elinewidth=1.5,
             markersize=9, markeredgecolor='black', markeredgewidth=0.5,
             label='Tempo', linewidth=2)
ax2.set_ylabel('Tempo', fontsize=12, fontweight='bold', color='#FF5722')
ax2.tick_params(axis='y', labelcolor='#FF5722')
ax2.set_ylim(0, 50)
ax2.set_yticks(np.arange(0, 51, 10))

# Legendas
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=10)

ax1.set_title('Resultados da Análise Estrutural', fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('outputs/graphics/meus_resultados_combinados.png', dpi=300, bbox_inches='tight')
plt.show()

# ============ ESTATÍSTICAS RESUMO ============
print("\n" + "="*60)
print("RESULTADOS DA ANÁLISE ESTRUTURAL".center(60))
print("="*60)

print("\n📊 MÉDIA DE EVACUAÇÃO:")
print(f"  • Média geral: {media_evacuacao.mean():.2f}")
print(f"  • Desvio padrão: {media_evacuacao.std():.2f}")
print(f"  • Valor mínimo: {media_evacuacao.min():.2f} (Saída {media_evacuacao.idxmin()})")
print(f"  • Valor máximo: {media_evacuacao.max():.2f} (Saída {media_evacuacao.idxmax()})")

print("\n⏱️  TEMPO:")
print(f"  • Média geral: {tempo_media.mean():.2f}")
print(f"  • Desvio padrão: {tempo_media.std():.2f}")
print(f"  • Valor mínimo: {tempo_media.min():.2f} (Saída {tempo_media.idxmin()})")
print(f"  • Valor máximo: {tempo_media.max():.2f} (Saída {tempo_media.idxmax()})")

print("\n📈 MELHORES RESULTADOS:")
melhor_evacuacao = media_evacuacao.idxmin()
melhor_tempo = tempo_media.idxmin()
print(f"  • Melhor saída para evacuação: {melhor_evacuacao} (média: {media_evacuacao[melhor_evacuacao]:.2f})")
print(f"  • Melhor saída para tempo: {melhor_tempo} (média: {tempo_media[melhor_tempo]:.2f})")

print("\n" + "="*60)