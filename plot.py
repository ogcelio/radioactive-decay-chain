import matplotlib.pyplot as plt
import numpy as np

from read import lbda

# CONSTANTES
L1 = 6.795e-3
L2 = 3.648e-2
L3 = 2.930e-5
L4 = 2.106e-5
N1_0 = 1e24

CORES = {1: "red", 2: "orange", 3: "green", 4: "blue", 5: "purple"}

# CÁLCULO DIRETO DAS DIFERENÇAS (Mantém a precisão máxima de 64-bits)
d21 = L2 - L1
d31 = L3 - L1
d32 = L3 - L2
d41 = L4 - L1
d42 = L4 - L2
d43 = L4 - L3

# CÁLCULO DOS COEFICIENTES (Fatorados sem aplicar N1_0 ainda)
C2_1 = L1 / d21

C3_1 = (L1 * L2) / (d21 * d31)
C3_2 = -(L1 * L2) / (d21 * d32)
# Nota: C3_3 é matematicamente igual a -(C3_1 + C3_2)

C4_1 = (L1 * L2 * L3) / (d21 * d31 * d41)
C4_2 = -(L1 * L2 * L3) / (d21 * d32 * d42)
C4_3 = (L1 * L2 * L3) / (d31 * d32 * d43)
# Nota: C4_4 é matematicamente igual a -(C4_1 + C4_2 + C4_3)


def calcular_analitica(t):
    """Calcula as funções analíticas para o array de tempo t."""
    # Precalculando os decaimentos
    E1 = np.exp(-L1 * t)
    E2 = np.exp(-L2 * t)
    E3 = np.exp(-L3 * t)
    E4 = np.exp(-L4 * t)

    N1 = N1_0 * E1

    # O agrupamento (Ei - Ej) garante que em t=0 o valor seja estruturalmente 0.0
    N2 = N1_0 * C2_1 * (E1 - E2)

    N3 = N1_0 * (C3_1 * (E1 - E3) + C3_2 * (E2 - E3))

    N4 = N1_0 * (C4_1 * (E1 - E4) + C4_2 * (E2 - E4) + C4_3 * (E3 - E4))

    N5 = N1_0 - (N1 + N2 + N3 + N4)

    return {1: N1, 2: N2, 3: N3, 4: N4, 5: N5}


def gerar_grafico(metodo, h):
    """Lê os dados, gera e salva o gráfico para um método e passo específicos."""
    prefixo = f"{metodo}_{h}"
    data = lbda(f"resultados/numerico/{prefixo}.txt")

    t = np.linspace(0, 600, data["NUM_PTS"])
    N_analitica = calcular_analitica(t)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Criação do Inset (Zoom).
    axins = ax.inset_axes((0.45, 0.3, 0.45, 0.40))

    for i in range(1, 6):
        # Plotando no gráfico principal
        ax.plot(t, N_analitica[i], label=f"N{i} Analítica", color=CORES[i])
        ax.plot(t, data[f"N{i}"], label=f"N{i} Numérica", color=CORES[i], linestyle=":")

        # Plotando as mesmas linhas dentro do inset
        axins.plot(t, N_analitica[i], color=CORES[i])
        axins.plot(t, data[f"N{i}"], color=CORES[i], linestyle=":")

    # Configurações do gráfico principal
    ax.set_ylabel("Número de Núcleos")
    ax.set_xlabel("Tempo (s)")
    ax.grid(True)

    # Configurações do Inset
    axins.set_xlim(500, 600)
    axins.set_ylim(-0.5e22, 3.5e22)
    axins.grid(True, linestyle="--", alpha=0.6)
    axins.spines["bottom"].set_color("gray")  # Deixa o eixo X do inset cinza
    axins.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

    # Linhas conectoras
    _, conectores = ax.indicate_inset_zoom(axins, edgecolor="gray", alpha=0.5)

    # Oculta as escolhas automáticas do Matplotlib
    for conector in conectores:
        conector.set_visible(False)

    # Força a exibição apenas das linhas que saem da base (0 e 3)
    conectores[0].set_visible(True)  # Canto inferior esquerdo
    conectores[3].set_visible(True)  # Canto inferior direito

    # Move a legenda para fora do gráfico
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 0.75))

    plt.savefig(f"resultados/grafico/{prefixo}.pdf", dpi=300, bbox_inches="tight")
    plt.close()  # Libera a figura da memória


# CONFIGURAÇÃO DE EXECUÇÃO
execucoes = {"euler": (1, 5, 10), "rk4": (2, 5, 10)}

for metodo, passos in execucoes.items():
    for h in passos:
        gerar_grafico(metodo, h)
