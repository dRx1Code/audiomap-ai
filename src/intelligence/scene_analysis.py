
def descrever_cena(
    objetos: list[dict],
    limite_por_posicao: int = 3
) -> str:
    """
    Organiza os objetos detectados por posição e prioridade,
    gerando uma descrição textual natural e objetiva.

    limite_por_posicao: quantidade máxima de categorias
    de objetos mencionadas em cada posição.
    """

    if limite_por_posicao < 1:
        raise ValueError("O limite deve ser pelo menos 1.")

    if not objetos:
        return "Não foram identificados objetos no ambiente."

    nomes = {
        "person": ("uma pessoa", "pessoas"),
        "bus": ("um ônibus", "ônibus"),
        "car": ("um carro", "carros"),
        "chair": ("uma cadeira", "cadeiras"),
        "table": ("uma mesa", "mesas"),
        "bicycle": ("uma bicicleta", "bicicletas"),
        "motorcycle": ("uma moto", "motos"),
        "dog": ("um cachorro", "cachorros"),
        "cat": ("um gato", "gatos"),
        "bottle": ("uma garrafa", "garrafas"),
    }

    prioridades = {
        "person": 1,
        "car": 1,
        "bus": 1,
        "motorcycle": 2,
        "bicycle": 2,
        "dog": 2,
        "chair": 3,
        "table": 3,
        "cat": 3,
        "bottle": 4,
    }

    ordem_posicoes = [
        "no centro",
        "à esquerda",
        "à direita"
    ]

    grupos = {}

    for objeto in objetos:
        posicao = objeto["posicao"]
        nome = objeto["objeto"]

        if posicao not in grupos:
            grupos[posicao] = {}

        grupos[posicao][nome] = (
            grupos[posicao].get(nome, 0) + 1
        )

    descricoes = []

    for posicao in ordem_posicoes:
        if posicao not in grupos:
            continue

        itens = sorted(
            grupos[posicao].items(),
            key=lambda item: prioridades.get(item[0], 5)
        )

        itens_prioritarios = itens[:limite_por_posicao]

        categorias_omitidas = len(itens) - len(itens_prioritarios)

        descricoes_itens = []

        for nome, quantidade in itens_prioritarios:
            singular, plural = nomes.get(
                nome,
                (nome, nome + "s")
            )

            if quantidade == 1:
                descricao = singular
            else:
                descricao = f"{quantidade} {plural}"

            descricoes_itens.append(descricao)

        conteudo = ", ".join(descricoes_itens)

        if categorias_omitidas == 1:
            conteudo += " e mais 1 tipo de objeto"
        elif categorias_omitidas > 1:
            conteudo += (
                f" e mais {categorias_omitidas} tipos de objetos"
            )

        descricoes.append(
            f"{posicao.capitalize()}, há {conteudo}"
        )

    return ". ".join(descricoes) + "."
