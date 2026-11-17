
from src.intelligence.scene_analysis import descrever_cena


def test_prioridade_dos_objetos():
    objetos = [
        {"objeto": "bottle", "posicao": "no centro"},
        {"objeto": "bus", "posicao": "no centro"},
        {"objeto": "person", "posicao": "no centro"},
    ]

    resultado = descrever_cena(objetos)

    esperado = "No centro, há um ônibus, uma pessoa, uma garrafa."

    assert resultado == esperado


def test_contagem_de_objetos():
    objetos = [
        {"objeto": "person", "posicao": "à esquerda"},
        {"objeto": "person", "posicao": "à esquerda"},
        {"objeto": "person", "posicao": "à esquerda"},
    ]

    resultado = descrever_cena(objetos)

    assert resultado == "À esquerda, há 3 pessoas."


def test_ordem_das_posicoes():
    objetos = [
        {"objeto": "person", "posicao": "à direita"},
        {"objeto": "bus", "posicao": "no centro"},
        {"objeto": "car", "posicao": "à esquerda"},
    ]

    resultado = descrever_cena(objetos)

    esperado = (
        "No centro, há um ônibus. "
        "À esquerda, há um carro. "
        "À direita, há uma pessoa."
    )

    assert resultado == esperado
