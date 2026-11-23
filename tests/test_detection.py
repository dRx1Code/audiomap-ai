
from src.vision.detection import (
    detectar_objetos,
    organizar_deteccoes
)


def test_filtrar_deteccoes_com_baixa_confianca():
    deteccoes = [
        {
            "nome": "person",
            "x_centro": 200,
            "confianca": 0.95
        },
        {
            "nome": "bottle",
            "x_centro": 600,
            "confianca": 0.30
        },
        {
            "nome": "bus",
            "x_centro": 1000,
            "confianca": 0.80
        }
    ]

    resultado = organizar_deteccoes(
        deteccoes,
        largura_imagem=1280
    )

    assert len(resultado) == 2

    nomes = [objeto["objeto"] for objeto in resultado]

    assert "person" in nomes
    assert "bus" in nomes
    assert "bottle" not in nomes


def test_manter_deteccao_no_limite_de_confianca():
    deteccoes = [
        {
            "nome": "person",
            "x_centro": 640,
            "confianca": 0.50
        }
    ]

    resultado = organizar_deteccoes(
        deteccoes,
        largura_imagem=1280
    )

    assert len(resultado) == 1
    assert resultado[0]["objeto"] == "person"
    assert resultado[0]["confianca"] == 0.50


def test_preservar_proporcao_area():
    deteccoes = [
        {
            "nome": "person",
            "x_centro": 640,
            "confianca": 0.95,
            "proporcao_area": 0.1832
        }
    ]

    resultado = organizar_deteccoes(
        deteccoes,
        largura_imagem=1280
    )

    assert len(resultado) == 1
    assert resultado[0]["proporcao_area"] == 0.1832


def test_proporcao_area_padrao_quando_ausente():
    deteccoes = [
        {
            "nome": "person",
            "x_centro": 640,
            "confianca": 0.95
        }
    ]

    resultado = organizar_deteccoes(
        deteccoes,
        largura_imagem=1280
    )

    assert resultado[0]["proporcao_area"] == 0.0

def test_calcular_proporcao_area_da_deteccao():
    class Coordenadas:
        def tolist(self):
            return [10.0, 20.0, 50.0, 60.0]

    class Caixa:
        xyxy = [Coordenadas()]
        cls = [0]
        conf = [0.95]

    class Resultado:
        orig_shape = (100, 200)
        boxes = [Caixa()]
        names = {0: "person"}

    class Modelo:
        def __call__(self, *args, **kwargs):
            return [Resultado()]

    deteccoes, largura = detectar_objetos(
        "imagem_teste.jpg",
        Modelo()
    )

    assert largura == 200
    assert len(deteccoes) == 1
    assert deteccoes[0]["nome"] == "person"
    assert deteccoes[0]["proporcao_area"] == 0.08