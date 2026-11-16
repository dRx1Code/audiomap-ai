
from src.vision.detection import organizar_deteccoes
from src.intelligence.scene_analysis import descrever_cena


def main():
    largura_imagem = 1280

    # Simulação dos objetos identificados
    deteccoes = [
        {"nome": "cadeira", "x_centro": 200},
        {"nome": "mesa", "x_centro": 1050},
        {"nome": "pessoa", "x_centro": 640}
    ]

    # Organiza os objetos e identifica suas posições
    objetos = organizar_deteccoes(
        deteccoes,
        largura_imagem
    )

    # Transforma os dados em uma descrição
    descricao = descrever_cena(objetos)

    print("=" * 40)
    print("AUDIOMAP AI")
    print("=" * 40)
    print("\nDescrição do ambiente:")
    print(descricao)


if __name__ == "__main__":
    main()
