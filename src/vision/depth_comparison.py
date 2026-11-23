
import math


def comparar_profundidades(
    objetos: list[dict]
) -> list[dict]:
    """
    Ordena objetos pela profundidade relativa,
    do menor para o maior valor.

    Objetos sem profundidade válida são ignorados.

    Também calcula a diferença entre cada objeto
    e o objeto anterior na ordenação.
    """

    objetos_validos = []

    for objeto in objetos:
        profundidade = objeto.get("profundidade_relativa")

        if profundidade is None:
            continue

        if (
            isinstance(profundidade, bool)
            or not isinstance(profundidade, (int, float))
            or not math.isfinite(profundidade)
        ):
            raise ValueError(
                "A profundidade relativa deve ser um número finito."
            )

        objetos_validos.append(objeto.copy())

    # Ordena pelo valor de profundidade relativa
    objetos_ordenados = sorted(
        objetos_validos,
        key=lambda objeto: objeto["profundidade_relativa"]
    )

    # Calcula a diferença entre valores consecutivos
    for indice, objeto in enumerate(objetos_ordenados):
        if indice == 0:
            objeto["diferenca_anterior"] = None
            continue

        profundidade_atual = objeto["profundidade_relativa"]

        profundidade_anterior = objetos_ordenados[
            indice - 1
        ]["profundidade_relativa"]

        objeto["diferenca_anterior"] = round(
            profundidade_atual - profundidade_anterior,
            4
        )

    return objetos_ordenados
