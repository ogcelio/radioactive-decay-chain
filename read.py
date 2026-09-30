import os.path as osp

import numpy as np


def lbda(file_path: str):
    """
    Lê os dados do arquivo de parâmetros (output) e retorna um dicionário com os valores
    """

    if not osp.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado em: {file_path}")

    data = {}

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 1)
            key = parts[0]
            values_str = parts[1] if len(parts) > 1 else ""

            if key == "NUM_PTS":
                data[key] = int(values_str)
            elif key == "DELTA_T":
                data[key] = float(values_str)
            elif key in {"N1", "N2", "N3", "N4", "N5"}:
                data[key] = np.fromstring(values_str, dtype=np.float64, sep=" ")

    return data
