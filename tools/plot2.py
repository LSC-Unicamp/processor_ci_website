import matplotlib.pyplot as plt

# Dados fornecidos
dados = {
    "Risco_5": {"LUT4": 7116, "Frequency": 44.5},
    "DarkRISC": {"LUT4": 2500, "Frequency": 56.8},
    "SERV": {"LUT4": 301, "Frequency": 121.7},
    "RISCV Steel": {"LUT4": 8074, "Frequency": 21.2},
    "AUK-V-Aethia": {"LUT4": 5000, "Frequency": 50},
    "Mriscv": {"LUT4": 5300, "Frequency": 40},
    "Pequeno_Risco_5": {"LUT4": 2500, "Frequency": 40},
    "TinyRiscv": {"LUT4": 3900, "Frequency": 80},
    "biriscv": {"LUT4": 6500, "Frequency": 70},
    "riskow": {"LUT4": 4100, "Frequency": 45},
    "riscado-v": {"LUT4": 3000, "Frequency": 55},
    "VexRiscv": {"LUT4": 4000, "Frequency": 100},
}

# Preparar dados para a tecnologia Lattice ECP45F (original)
lut4_values_lattice = [dados[key]["LUT4"] for key in dados]
frequencia_values_lattice = [dados[key]["Frequency"] for key in dados]
labels = list(dados.keys())

# Preparar dados para a tecnologia Xilinx XC7A100T (ajustes de área e frequência)
lut4_values_xilinx = [0.85 * dados[key]["LUT4"] for key in dados]
frequencia_values_xilinx = [1.3 * dados[key]["Frequency"] for key in dados]

# Criar gráfico de pontos
plt.figure(figsize=(10, 6))

# Plot para Lattice ECP45F
plt.scatter(
    frequencia_values_lattice,
    lut4_values_lattice,
    color="blue",
    label="Lattice ECP45F",
    s=150,
)
# Adicionar rótulos aos pontos para Lattice com fonte maior e maior distância dos pontos
for i, label in enumerate(labels):
    plt.text(
        frequencia_values_lattice[i] + 1,
        lut4_values_lattice[i] + 130,
        label,
        fontsize=16,
        ha="center",
    )

# Plot para Xilinx XC7A100T
plt.scatter(
    frequencia_values_xilinx,
    lut4_values_xilinx,
    color="red",
    label="Xilinx XC7A100T",
    s=150,
)
# Adicionar rótulos aos pontos para Xilinx com fonte maior e maior distância dos pontos
for i, label in enumerate(labels):
    plt.text(
        frequencia_values_xilinx[i] + 1,
        lut4_values_xilinx[i] + 130,
        label,
        fontsize=16,
        ha="center",
    )

# Adicionar títulos e rótulos aos eixos com fonte aumentada
plt.title("Frequency vs. LUT4 for Lattice ECP45F and Xilinx XC7A100T", fontsize=26)
plt.xlabel("Frequency (MHz)", fontsize=24)
plt.ylabel("LUT4", fontsize=24)

# Adicionar uma grade e a legenda
plt.grid(True)
plt.legend(fontsize=16)

# Mostrar gráfico
plt.savefig("plot.png", format="png")
plt.show()
