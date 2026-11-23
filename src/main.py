
from ultralytics import YOLO

from src.vision.detection import (
    detectar_objetos,
    organizar_deteccoes
)

from src.vision.depth_estimation import EstimadorProfundidade
from src.vision.spatial_analysis import associar_profundidade

from src.intelligence.scene_analysis import descrever_cena
from src.audio.speech import AudioManager


def main():
    print("=" * 40)
    print("AUDIOMAP AI")
    print("=" * 40)

    caminho_imagem = "bus.jpg"

    # Inicializa o modelo de detecção
    modelo = YOLO("yolo11n.pt")

    # Inicializa o sistema de áudio
    audio = AudioManager()

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

    # Inicializa o estimador de profundidade
    estimador = EstimadorProfundidade()

    # Gera o mapa de profundidade relativa
    print("\nEstimando profundidade da imagem...")

    mapa_profundidade = estimador.estimar_arquivo(
        caminho_imagem
    )

    # Associa a profundidade relativa aos objetos
    objetos = associar_profundidade(
        objetos,
        mapa_profundidade
    )

    # Exibe os dados espaciais dos objetos
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

    # Gera a descrição textual do ambiente
    descricao = descrever_cena(objetos)

    print("\nDescrição do ambiente:")
    print(descricao)

    # Reproduz a descrição por áudio
    print("\nReproduzindo descrição...")
    audio.falar(descricao)


if __name__ == "__main__":
    main()
