
from ultralytics import YOLO

from src.vision.detection import (
    detectar_objetos,
    organizar_deteccoes
)

from src.intelligence.scene_analysis import descrever_cena
from src.audio.speech import AudioManager


def main():
    print("=" * 40)
    print("AUDIOMAP AI")
    print("=" * 40)

    # Inicializa o modelo de visão computacional
    modelo = YOLO("yolo11n.pt")

    # Inicializa o sistema de áudio
    audio = AudioManager()

    # Analisa a imagem
    deteccoes, largura_imagem = detectar_objetos(
        "bus.jpg",
        modelo
    )

    # Organiza os objetos detectados
    objetos = organizar_deteccoes(
        deteccoes,
        largura_imagem
    )

    # Gera a descrição textual
    descricao = descrever_cena(objetos)

    print("\nDescrição do ambiente:")
    print(descricao)

    # Reproduz a descrição por voz
    print("\nReproduzindo descrição...")
    audio.falar(descricao)


if __name__ == "__main__":
    main()
