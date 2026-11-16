
from ultralytics import YOLO

from src.vision.detection import (
    detectar_objetos,
    organizar_deteccoes
)

from src.intelligence.scene_analysis import descrever_cena


def main():
    print("=" * 40)
    print("AUDIOMAP AI")
    print("=" * 40)

    modelo = YOLO("yolo11n.pt")

    deteccoes, largura_imagem = detectar_objetos(
        "bus.jpg",
        modelo
    )

    objetos = organizar_deteccoes(
        deteccoes,
        largura_imagem
    )

    descricao = descrever_cena(objetos)

    print("\nDescrição do ambiente:")
    print(descricao)


if __name__ == "__main__":
    main()
