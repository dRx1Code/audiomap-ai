
from pathlib import Path

import cv2
from ultralytics import YOLO

from src.vision.detection import (
    detectar_objetos,
    organizar_deteccoes
)

from src.vision.depth_estimation import EstimadorProfundidade
from src.vision.spatial_analysis import associar_profundidade
from src.vision.depth_comparison import comparar_profundidades

from src.intelligence.scene_analysis import descrever_cena
from src.audio.speech import AudioManager


def salvar_visualizacao_profundidade(
    mapa_profundidade,
    objetos,
    diretorio="outputs/depth"
):
    """
    Salva o mapa de profundidade em escala de cinza
    e uma versão colorida com as caixas dos objetos.
    """

    caminho_saida = Path(diretorio)
    caminho_saida.mkdir(parents=True, exist_ok=True)

    # Normaliza os valores apenas para visualização
    mapa_normalizado = cv2.normalize(
        mapa_profundidade,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    mapa_normalizado = mapa_normalizado.astype("uint8")

    # Gera as imagens de visualização
    mapa_cinza = mapa_normalizado
    mapa_colorido = cv2.applyColorMap(
        mapa_normalizado,
        cv2.COLORMAP_JET
    )

    # Desenha as caixas dos objetos
    for objeto in objetos:
        caixa = objeto.get("caixa")

        if caixa is None:
            continue

        x1 = int(caixa["x1"])
        y1 = int(caixa["y1"])
        x2 = int(caixa["x2"])
        y2 = int(caixa["y2"])

        nome = objeto["objeto"]
        profundidade = objeto["profundidade_relativa"]

        cv2.rectangle(
            mapa_colorido,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            2
        )

        texto = (
            f"{nome}: {profundidade}"
            if profundidade is not None
            else f"{nome}: N/A"
        )

        cv2.putText(
            mapa_colorido,
            texto,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA
        )

    # Salva os arquivos
    cv2.imwrite(
        str(caminho_saida / "mapa_cinza.png"),
        mapa_cinza
    )

    cv2.imwrite(
        str(caminho_saida / "mapa_colorido.png"),
        mapa_colorido
    )

    print("\nVisualizações salvas:")
    print(caminho_saida / "mapa_cinza.png")
    print(caminho_saida / "mapa_colorido.png")


def main():
    print("=" * 40)
    print("AUDIOMAP AI")
    print("=" * 40)

    caminho_imagem = "bus.jpg"

    # Inicializa os modelos e o sistema de áudio
    modelo = YOLO("yolo11n.pt")
    audio = AudioManager()
    estimador = EstimadorProfundidade()

    # Detecta objetos na imagem
    deteccoes, largura_imagem = detectar_objetos(
        caminho_imagem,
        modelo
    )

    # Organiza as detecções
    objetos = organizar_deteccoes(
        deteccoes,
        largura_imagem
    )

    # Estima a profundidade relativa
    print("\nEstimando profundidade da imagem...")

    mapa_profundidade = estimador.estimar_arquivo(
        caminho_imagem
    )

    # Associa a profundidade aos objetos
    objetos = associar_profundidade(
        objetos,
        mapa_profundidade
    )

    # Gera as visualizações
    salvar_visualizacao_profundidade(
        mapa_profundidade,
        objetos
    )

    # Exibe os dados espaciais
    print("\nDados espaciais dos objetos:")

    for objeto in objetos:
        profundidade = objeto["profundidade_relativa"]

        if profundidade is None:
            profundidade_texto = "indisponível"
        else:
            profundidade_texto = str(profundidade)

        print(
            f"{objeto['objeto']}: "
            f"posição = {objeto['posicao']}, "
            f"área ocupada = "
            f"{objeto['proporcao_area'] * 100:.2f}%, "
            f"profundidade relativa = {profundidade_texto}"
        )

    # Compara as profundidades relativas
    comparacao = comparar_profundidades(objetos)

    print("\nComparação de profundidade relativa:")

    if not comparacao:
        print("Nenhum objeto possui profundidade válida.")

    for indice, objeto in enumerate(comparacao, start=1):
        print(
            f"{indice}. "
            f"{objeto['objeto']} "
            f"({objeto['posicao']}): "
            f"{objeto['profundidade_relativa']}"
        )

        diferenca = objeto["diferenca_anterior"]

        if diferenca is not None:
            print(
                f"   Diferença em relação ao anterior: "
                f"{diferenca:.4f}"
            )

    # Gera a descrição textual
    descricao = descrever_cena(objetos)

    print("\nDescrição do ambiente:")
    print(descricao)

    # Reproduz a descrição por áudio
    print("\nReproduzindo descrição...")
    audio.falar(descricao)


if __name__ == "__main__":
    main()
