import numpy as np

from read import lbda

# CONSTANTES
L1 = 6.795e-3
L2 = 3.648e-2
L3 = 2.930e-5
L4 = 2.106e-5
N1_0 = 1e24

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


tempos = (0, 150, 300, 450, 600)  # Tempos em segundos para comparação


def rd(metodo, h):
    prefixo = f"{metodo}_{h}"
    data = lbda(f"resultados/numerico/{prefixo}.txt")

    t = np.linspace(0, 600, data["NUM_PTS"])
    N_analitica = calcular_analitica(t)

    indices = [i // h for i in tempos]

    print(f"\nMétodo: {metodo}, Passo: {h}")
    for i in indices:
        print(f"\nTempo: {t[i]:.2f} s")
        for j in range(1, 6):
            relative_deviation = (
                abs((N_analitica[j][i] - data[f"N{j}"][i]) / N_analitica[j][i]) * 100
                if N_analitica[j][i] != 0
                else 0
            )
            print(
                f"N{j} -> Analítica: {N_analitica[j][i]:.10e}, Numérica: {data[f'N{j}'][i]:.10e}, Desvio Relativo: {relative_deviation:.10e}%"
            )


# CONFIGURAÇÃO DE EXECUÇÃO
execucoes = {"euler": (1, 5, 10), "rk4": (2, 5, 10)}

for metodo, passos in execucoes.items():
    for h in passos:
        rd(metodo, h)
