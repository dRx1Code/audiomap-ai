
import pytest

from src.vision.depth_comparison import comparar_profundidades


def test_ordenar_objetos_por_profundidade():
    objetos = [
        {"objeto": "bus", "profundidade_relativa": 3.0},
        {"objeto": "person", "profundidade_relativa": 2.0},
        {"objeto": "car", "profundidade_relativa": 5.0}
    ]

    resultado = comparar_profundidades(objetos)

    assert [
        objeto["objeto"] for objeto in resultado
    ] == ["person", "bus", "car"]


def test_ignorar_objetos_sem_profundidade():
    objetos = [
        {"objeto": "bus", "profundidade_relativa": 3.0},
        {"objeto": "person", "profundidade_relativa": None}
    ]

    resultado = comparar_profundidades(objetos)

    assert len(resultado) == 1
    assert resultado[0]["objeto"] == "bus"


def test_calcular_diferenca_entre_objetos():
    objetos = [
        {"objeto": "bus", "profundidade_relativa": 3.0},
        {"objeto": "person", "profundidade_relativa": 2.0},
        {"objeto": "car", "profundidade_relativa": 5.0}
    ]

    resultado = comparar_profundidades(objetos)

    assert resultado[0]["diferenca_anterior"] is None
    assert resultado[1]["diferenca_anterior"] == 1.0
    assert resultado[2]["diferenca_anterior"] == 2.0


def test_rejeitar_profundidade_invalida():
    objetos = [
        {"objeto": "bus", "profundidade_relativa": float("nan")}
    ]

    with pytest.raises(ValueError):
        comparar_profundidades(objetos)


def test_nao_modificar_objetos_originais():
    objetos = [
        {"objeto": "bus", "profundidade_relativa": 3.0},
        {"objeto": "person", "profundidade_relativa": 2.0}
    ]

    comparar_profundidades(objetos)

    assert "diferenca_anterior" not in objetos[0]
    assert "diferenca_anterior" not in objetos[1]


def test_lista_vazia():
    resultado = comparar_profundidades([])

    assert resultado == []
