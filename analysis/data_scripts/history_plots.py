import pandas as pd

# Ler o arquivo CSV
df = pd.read_csv('outputs/simulations/history_complex_room_0.5.csv')

# Extrair a primeira coluna como Series
series = df.iloc[:, 0]

print("\n" + "="*45)
print("        RELATÓRIO ESTATÍSTICO DE EVACUAÇÃO       ")
print("="*45)
print(f"Média Geral (Passos):    {series.mean():.2f}")
print(f"Desvio Padrão (s):       {series.std():.2f}")
print(f"Mediana (Xm):            {series.median():.2f}")
print(f"Moda (Mo):               {series.mode().iloc[0]:.2f}")
print(f"Tempo Mínimo Registrado: {series.min()} passos")
print(f"Tempo Máximo Registrado: {series.max()} passos")
print("="*45)