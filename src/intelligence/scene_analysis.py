
def descrever_cena(objetos: list[dict]) -> str:
    """
    Transforma os objetos identificados em uma descrição textual.
    """

    if not objetos:
        return "Não foram identificados objetos no ambiente."

    descricoes = []

    for objeto in objetos:
        nome = objeto["objeto"]
        posicao = objeto["posicao"]

        frase = f"{posicao.capitalize()}: {nome}"
        descricoes.append(frase)

    return ". ".join(descricoes) + "."
