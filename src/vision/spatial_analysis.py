
import math

import numpy as np


def associar_profundidade(
    deteccoes: list[dict],
    mapa_profundidade: np.ndarray
) -> list[dict]:
    """
    Associa cada detecção ao mapa de profundidade relativa.

    Para cada objeto:
        1. Obtém sua caixa delimitadora.
        2. Recorta a região correspondente no mapa.
        3. Remove valores inválidos.
        4. Calcula a mediana da profundidade relativa.

    Retorna uma nova lista de detecções com o campo
    'profundidade_relativa'.

    Objetos sem caixa delimitadora recebem None.
    """

    if mapa_profundidade is None:
        raise ValueError("O mapa de profundidade não pode ser vazio.")

    if not isinstance(mapa_profundidade, np.ndarray):
        raise TypeError("O mapa de profundidade deve ser um array NumPy.")

    if mapa_profundidade.ndim != 2:
        raise ValueError(
            "O mapa de profundidade deve possuir duas dimensões."
        )

    altura, largura = mapa_profundidade.shape

    if altura == 0 or largura == 0:
        raise ValueError("O mapa de profundidade está vazio.")

    objetos_analisados = []

    for deteccao in deteccoes:
        objeto = deteccao.copy()

        caixa = deteccao.get("caixa")

        if caixa is None:
            objeto["profundidade_relativa"] = None
            objetos_analisados.append(objeto)
            continue

        try:
            x1 = math.floor(float(caixa["x1"]))
            y1 = math.floor(float(caixa["y1"]))
            x2 = math.ceil(float(caixa["x2"]))
            y2 = math.ceil(float(caixa["y2"]))
        except (KeyError, TypeError, ValueError, OverflowError) as erro:
            raise ValueError(
                "A caixa delimitadora possui coordenadas inválidas."
            ) from erro

        # Limita as coordenadas ao tamanho do mapa
        x1 = max(0, min(x1, largura))
        x2 = max(0, min(x2, largura))
        y1 = max(0, min(y1, altura))
        y2 = max(0, min(y2, altura))

        # Verifica se a região possui área válida
        if x2 <= x1 or y2 <= y1:
            objeto["profundidade_relativa"] = None
            objetos_analisados.append(objeto)
            continue

        # Recorta a região correspondente ao objeto
        regiao = mapa_profundidade[y1:y2, x1:x2]

        # Remove valores NaN e infinitos
        valores_validos = regiao[np.isfinite(regiao)]

        if valores_validos.size == 0:
            objeto["profundidade_relativa"] = None
        else:
            mediana = float(np.median(valores_validos))

            objeto["profundidade_relativa"] = round(
                mediana,
                4
            )

        objetos_analisados.append(objeto)

    return objetos_analisados
