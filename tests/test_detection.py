
from src.vision.detection import organizar_deteccoes


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
