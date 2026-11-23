
import math

import numpy as np


def associar_profundidade(
    deteccoes: list[dict],
    mapa_profundidade: np.ndarray,
    proporcao_interna: float = 0.5
) -> list[dict]:
    """
    Associa cada detecção ao mapa de profundidade relativa.

    Utiliza somente a região central da caixa delimitadora
    para reduzir a influência de elementos nas bordas.

    proporcao_interna:
        0.5 = utiliza os 50% centrais da caixa.
        1.0 = utiliza a caixa inteira.
    """

    if mapa_profundidade is None:
        raise ValueError("O mapa de profundidade não pode ser vazio.")

    if not isinstance(mapa_profundidade, np.ndarray):
        raise TypeError("O mapa de profundidade deve ser um array NumPy.")

    if mapa_profundidade.ndim != 2:
        raise ValueError(
            "O mapa de profundidade deve possuir duas dimensões."
        )

    if (
        not isinstance(proporcao_interna, (int, float))
        or not math.isfinite(proporcao_interna)
        or not 0 < proporcao_interna <= 1
    ):
        raise ValueError(
            "A proporção interna deve estar entre 0 e 1."
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

        # Verifica se a caixa possui área válida
        if x2 <= x1 or y2 <= y1:
            objeto["profundidade_relativa"] = None
            objetos_analisados.append(objeto)
            continue

        # Calcula as dimensões da região central
        largura_caixa = x2 - x1
        altura_caixa = y2 - y1

        largura_interna = max(
            1,
            round(largura_caixa * proporcao_interna)
        )

        altura_interna = max(
            1,
            round(altura_caixa * proporcao_interna)
        )

        # Centraliza a região de análise
        inicio_x = x1 + (largura_caixa - largura_interna) // 2
        inicio_y = y1 + (altura_caixa - altura_interna) // 2

        fim_x = inicio_x + largura_interna
        fim_y = inicio_y + altura_interna

        # Recorta somente a região central
        regiao = mapa_profundidade[
            inicio_y:fim_y,
            inicio_x:fim_x
        ]

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
