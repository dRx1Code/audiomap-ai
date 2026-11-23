
import numpy as np
import pytest

from src.vision.spatial_analysis import associar_profundidade


def test_calcular_mediana_da_regiao_do_objeto():
    mapa = np.array([
        [1.0, 2.0, 3.0, 4.0],
        [5.0, 6.0, 7.0, 8.0],
        [9.0, 10.0, 11.0, 12.0],
        [13.0, 14.0, 15.0, 16.0]
    ], dtype=np.float32)

    deteccoes = [{
        "objeto": "person",
        "caixa": {
            "x1": 0,
            "y1": 0,
            "x2": 2,
            "y2": 2
        }
    }]

    resultado = associar_profundidade(
        deteccoes,
        mapa
    )

    assert resultado[0]["profundidade_relativa"] == 3.5


def test_limitar_caixa_ao_tamanho_do_mapa():
    mapa = np.array([
        [1.0, 2.0],
        [3.0, 4.0]
    ], dtype=np.float32)

    deteccoes = [{
        "objeto": "bus",
        "caixa": {
            "x1": -10,
            "y1": -10,
            "x2": 10,
            "y2": 10
        }
    }]

    resultado = associar_profundidade(
        deteccoes,
        mapa
    )

    assert resultado[0]["profundidade_relativa"] == 2.5


def test_ignorar_valores_invalidos():
    mapa = np.array([
        [1.0, np.nan],
        [np.inf, 5.0]
    ], dtype=np.float32)

    deteccoes = [{
        "objeto": "person",
        "caixa": {
            "x1": 0,
            "y1": 0,
            "x2": 2,
            "y2": 2
        }
    }]

    resultado = associar_profundidade(
        deteccoes,
        mapa
    )

    assert resultado[0]["profundidade_relativa"] == 3.0


def test_retorna_none_sem_caixa_delimitadora():
    mapa = np.ones((10, 10), dtype=np.float32)

    deteccoes = [{
        "objeto": "person"
    }]

    resultado = associar_profundidade(
        deteccoes,
        mapa
    )

    assert resultado[0]["profundidade_relativa"] is None


def test_rejeitar_mapa_com_dimensoes_invalidas():
    mapa = np.ones((10, 10, 3), dtype=np.float32)

    with pytest.raises(ValueError):
        associar_profundidade([], mapa)


def test_nao_modificar_deteccoes_originais():
    mapa = np.ones((10, 10), dtype=np.float32)

    deteccoes = [{
        "objeto": "person",
        "caixa": {
            "x1": 0,
            "y1": 0,
            "x2": 5,
            "y2": 5
        }
    }]

    associar_profundidade(deteccoes, mapa)

    assert "profundidade_relativa" not in deteccoes[0]
