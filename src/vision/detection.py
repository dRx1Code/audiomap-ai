
from src.vision.positioning import identificar_posicao


def organizar_deteccoes(
    deteccoes: list[dict],
    largura_imagem: int
) -> list[dict]:
    """
    Organiza os objetos detectados e identifica suas posições.
    """

    objetos_organizados = []

    for deteccao in deteccoes:
        nome = deteccao["nome"]
        x_centro = deteccao["x_centro"]

        posicao = identificar_posicao(
            x_centro,
            largura_imagem
        )

        objeto = {
            "objeto": nome,
            "posicao": posicao
        }

        objetos_organizados.append(objeto)

    return objetos_organizados
    