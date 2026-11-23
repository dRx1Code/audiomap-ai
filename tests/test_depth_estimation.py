
import numpy as np
import pytest

from src.vision.depth_estimation import EstimadorProfundidade


def test_estimar_retorna_mapa_de_profundidade():
    class ModeloFalso:
        def infer_image(self, imagem, tamanho):
            return np.ones((100, 200), dtype=np.float32)

    estimador = EstimadorProfundidade()
    estimador.modelo = ModeloFalso()

    imagem = np.zeros((100, 200, 3), dtype=np.uint8)

    resultado = estimador.estimar(imagem)

    assert resultado.shape == (100, 200)
    assert resultado.dtype == np.float32


def test_rejeitar_imagem_vazia():
    estimador = EstimadorProfundidade()

    with pytest.raises(ValueError):
        estimador.estimar(None)


def test_rejeitar_imagem_sem_tres_canais():
    estimador = EstimadorProfundidade()

    imagem = np.zeros((100, 200), dtype=np.uint8)

    with pytest.raises(ValueError):
        estimador.estimar(imagem)


def test_reutilizar_modelo_ja_carregado():
    class ModeloFalso:
        def infer_image(self, imagem, tamanho):
            return np.ones((100, 200), dtype=np.float32)

    estimador = EstimadorProfundidade()
    carregamentos = 0

    def carregar_modelo_falso():
        nonlocal carregamentos
        carregamentos += 1
        estimador.modelo = ModeloFalso()

    estimador.carregar_modelo = carregar_modelo_falso

    imagem = np.zeros((100, 200, 3), dtype=np.uint8)

    estimador.estimar(imagem)
    estimador.estimar(imagem)

    assert carregamentos == 1
