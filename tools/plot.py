import matplotlib.pyplot as plt

# Dados fornecidos
dados = {
    "Risco_5": {"LUT4": 7116, "Frequency": 44.5},
    "DarkRISC": {"LUT4": 2291, "Frequency": 56.8},
    "SERV": {"LUT4": 301, "Frequency": 121.7},
    "RISCV Steel": {"LUT4": 8074, "Frequency": 21.2},
    "AUK-V-Aethia": {"LUT4": 5000, "Frequency": 50},
    "Mriscv": {"LUT4": 5500, "Frequency": 40},
    "Pequeno_Risco_5": {"LUT4": 2500, "Frequency": 40},
    "TinyRiscv": {"LUT4": 3900, "Frequency": 80},
    "biriscv": {"LUT4": 6500, "Frequency": 70},
    "riskow": {"LUT4": 4000, "Frequency": 45},
    "riscado-v": {"LUT4": 3500, "Frequency": 55},
    "VexRiscv": {"LUT4": 4000, "Frequency": 100},
}

# Preparar dados para o gráfico
lut4_values = [0.85 * dados[key]["LUT4"] for key in dados]
frequencia_values = [1.3 * dados[key]["Frequency"] for key in dados]
labels = list(dados.keys())

# Criar gráfico de pontos
plt.figure(figsize=(10, 6))
plt.scatter(frequencia_values, lut4_values, color="red")

# Adicionar rótulos aos pontos
for i, label in enumerate(labels):
    plt.text(frequencia_values[i], lut4_values[i], label, fontsize=9, ha="left")

# Adicionar títulos e rótulos aos eixos
plt.title("Frequency vs. LUT4")
plt.xlabel("Frequency (MHz)")
plt.ylabel("LUT4")

# Mostrar gráfico
plt.grid(True)
plt.savefig("plot.png", format="png")
plt.show()
