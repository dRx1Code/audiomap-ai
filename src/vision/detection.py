
from ultralytics import YOLO

from src.vision.positioning import identificar_posicao


def detectar_objetos(
    caminho_imagem: str,
    modelo: YOLO
) -> tuple[list[dict], int]:
    """
    Detecta objetos usando YOLO.

    Retorna as detecções com:
        - Nome do objeto.
        - Centro horizontal.
        - Coordenadas da caixa delimitadora.
        - Confiança da detecção.
        - Proporção da área ocupada.
    """

    resultados = modelo(
        caminho_imagem,
        device="cpu",
        verbose=False
    )

    deteccoes = []
    largura = 0

    for resultado in resultados:
        altura, largura = resultado.orig_shape

        if resultado.boxes is None:
            continue

        for caixa in resultado.boxes:
            x1, y1, x2, y2 = caixa.xyxy[0].tolist()

            # Calcula o centro horizontal do objeto
            x_centro = int((x1 + x2) / 2)

            # Calcula as dimensões da caixa delimitadora
            largura_caixa = x2 - x1
            altura_caixa = y2 - y1

            # Calcula a proporção da área ocupada
            area_caixa = largura_caixa * altura_caixa
            area_imagem = largura * altura

            proporcao_area = (
                area_caixa / area_imagem
                if area_imagem > 0
                else 0.0
            )

            # Identifica a classe e a confiança
            classe_id = int(caixa.cls[0])
            nome = resultado.names[classe_id]
            confianca = float(caixa.conf[0])

            # Armazena os dados da detecção
            deteccoes.append({
                "nome": nome,
                "x_centro": x_centro,
                "x1": float(x1),
                "y1": float(y1),
                "x2": float(x2),
                "y2": float(y2),
                "confianca": round(confianca, 2),
                "proporcao_area": round(proporcao_area, 4)
            })

    return deteccoes, largura


def organizar_deteccoes(
    deteccoes: list[dict],
    largura_imagem: int,
    confianca_minima: float = 0.50
) -> list[dict]:
    """
    Organiza as detecções, filtra por confiança
    e identifica a posição dos objetos.

    Preserva a proporção da área ocupada e,
    quando disponíveis, as coordenadas da caixa.
    """

    objetos_organizados = []

    for deteccao in deteccoes:
        confianca = deteccao.get("confianca", 0.0)

        # Descarta objetos abaixo da confiança mínima
        if confianca < confianca_minima:
            continue

        nome = deteccao["nome"]
        x_centro = deteccao["x_centro"]

        # Identifica a posição horizontal
        posicao = identificar_posicao(
            x_centro,
            largura_imagem
        )

        # Organiza as informações básicas
        objeto = {
            "objeto": nome,
            "posicao": posicao,
            "confianca": confianca,
            "proporcao_area": deteccao.get(
                "proporcao_area",
                0.0
            )
        }

        # Preserva a caixa somente quando todas
        # as coordenadas estiverem disponíveis
        coordenadas = ("x1", "y1", "x2", "y2")

        if all(
            coordenada in deteccao
            for coordenada in coordenadas
        ):
            objeto["caixa"] = {
                "x1": deteccao["x1"],
                "y1": deteccao["y1"],
                "x2": deteccao["x2"],
                "y2": deteccao["y2"]
            }

        objetos_organizados.append(objeto)

    return objetos_organizados
