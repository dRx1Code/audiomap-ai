
def descrever_cena(objetos: list[dict]) -> str:
    """
    Organiza os objetos detectados por posição e prioridade,
    gerando uma descrição textual mais natural da cena.
    """

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

        descricoes_itens = []

        for nome, quantidade in itens:
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

        descricoes.append(
            f"{posicao.capitalize()}, há {conteudo}"
        )

    return ". ".join(descricoes) + "."
