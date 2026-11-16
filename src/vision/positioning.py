
def identificar_posicao(x_centro: int, largura_imagem: int) -> str:
    """
    Identifica a posição horizontal de um objeto na imagem.

    x_centro: coordenada horizontal do centro do objeto.
    largura_imagem: largura total da imagem em pixels.
    """

    if largura_imagem <= 0:
        raise ValueError("A largura da imagem deve ser maior que zero.")

    proporcao = x_centro / largura_imagem

    if proporcao < 0.35:
        return "à esquerda"

    elif proporcao > 0.65:
        return "à direita"

    else:
        return "no centro"
