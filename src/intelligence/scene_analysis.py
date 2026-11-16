
def descrever_cena(objetos: list[dict]) -> str:
    """
    Agrupa objetos por posição e quantidade,
    gerando uma descrição textual da cena.
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

    ordem = ["à esquerda", "no centro", "à direita"]

    grupos = {}

    for objeto in objetos:
        posicao = objeto["posicao"]
        nome = objeto["objeto"]

        if posicao not in grupos:
            grupos[posicao] = {}

        grupos[posicao][nome] = grupos[posicao].get(nome, 0) + 1

    descricoes = []

    for posicao in ordem:
        if posicao not in grupos:
            continue

        itens = []

        for nome, quantidade in grupos[posicao].items():
            singular, plural = nomes.get(
                nome,
                (nome, nome + "s")
            )

            if quantidade == 1:
                descricao = singular
            else:
                descricao = f"{quantidade} {plural}"

            itens.append(descricao)

        descricoes.append(
            f"{posicao.capitalize()}: {', '.join(itens)}"
        )

    return ". ".join(descricoes) + "."
