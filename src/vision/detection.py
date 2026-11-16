
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

    
from ultralytics import YOLO
from src.vision.positioning import identificar_posicao


def detectar_objetos(
    caminho_imagem: str,
    modelo: YOLO
) -> tuple[list[dict], int]:
    """
    Detecta objetos em uma imagem usando YOLO.

    Retorna as detecções e a largura da imagem.
    """

    resultados = modelo(
        caminho_imagem,
        device="cpu",
        verbose=False
    )

    deteccoes = []

    for resultado in resultados:
        altura, largura = resultado.orig_shape

        if resultado.boxes is None:
            continue

        for caixa in resultado.boxes:
            x1, y1, x2, y2 = caixa.xyxy[0].tolist()

            x_centro = int((x1 + x2) / 2)

            classe_id = int(caixa.cls[0])
            nome = resultado.names[classe_id]
            confianca = float(caixa.conf[0])

            deteccoes.append({
                "nome": nome,
                "x_centro": x_centro,
                "confianca": round(confianca, 2)
            })

    return deteccoes, largura


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
    "posicao": posicao,
    "confianca": deteccao.get("confianca", 0.0)
}

        objetos_organizados.append(objeto)

    return objetos_organizados
