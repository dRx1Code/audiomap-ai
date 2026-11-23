
import pytest

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

    esperado = (
        "No centro, há um ônibus. "
        "À esquerda, há um carro. "
        "À direita, há uma pessoa."
    )

    assert descrever_cena(objetos) == esperado


def test_limitar_categorias_por_posicao():
    objetos = [
        {"objeto": "bottle", "posicao": "no centro"},
        {"objeto": "chair", "posicao": "no centro"},
        {"objeto": "bus", "posicao": "no centro"},
        {"objeto": "person", "posicao": "no centro"},
        {"objeto": "car", "posicao": "no centro"},
    ]

    resultado = descrever_cena(
        objetos,
        limite_por_posicao=3
    )

    esperado = (
        "No centro, há um ônibus, uma pessoa, um carro "
        "e mais 2 tipos de objetos."
    )

    assert resultado == esperado


def test_limite_independente_por_posicao():
    objetos = [
        {"objeto": "bus", "posicao": "no centro"},
        {"objeto": "person", "posicao": "no centro"},
        {"objeto": "car", "posicao": "no centro"},
        {"objeto": "chair", "posicao": "no centro"},
        {"objeto": "dog", "posicao": "à esquerda"},
        {"objeto": "bicycle", "posicao": "à esquerda"},
        {"objeto": "cat", "posicao": "à esquerda"},
        {"objeto": "bottle", "posicao": "à esquerda"},
    ]

    resultado = descrever_cena(
        objetos,
        limite_por_posicao=2
    )

    esperado = (
        "No centro, há um ônibus, uma pessoa e mais 2 tipos de objetos. "
        "À esquerda, há um cachorro, uma bicicleta e mais 2 tipos de objetos."
    )

    assert resultado == esperado


def test_rejeitar_limite_invalido():
    objetos = [
        {"objeto": "person", "posicao": "no centro"}
    ]

    with pytest.raises(ValueError):
        descrever_cena(objetos, limite_por_posicao=0)
