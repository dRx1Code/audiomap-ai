
import sys
from pathlib import Path

import cv2
import numpy as np
import torch


# Localização do repositório oficial do Depth Anything V2
RAIZ_PROJETO = Path(__file__).resolve().parents[2]

REPOSITORIO_DEPTH = (
    RAIZ_PROJETO
    / "external"
    / "Depth-Anything-V2"
)

CAMINHO_PESOS = (
    REPOSITORIO_DEPTH
    / "checkpoints"
    / "depth_anything_v2_vits.pth"
)

# Permite importar o código oficial do modelo
if str(REPOSITORIO_DEPTH) not in sys.path:
    sys.path.insert(0, str(REPOSITORIO_DEPTH))

from depth_anything_v2.dpt import DepthAnythingV2


class EstimadorProfundidade:

    def __init__(self, tamanho_entrada: int = 518):
        self.tamanho_entrada = tamanho_entrada
        self.modelo = None

    def carregar_modelo(self):
        """
        Carrega o Depth Anything V2 Small em CPU.
        """

        if not CAMINHO_PESOS.is_file():
            raise FileNotFoundError(
                f"Pesos do modelo não encontrados: {CAMINHO_PESOS}"
            )

        configuracao = {
            "encoder": "vits",
            "features": 64,
            "out_channels": [48, 96, 192, 384]
        }

        modelo = DepthAnythingV2(**configuracao)

        pesos = torch.load(
            CAMINHO_PESOS,
            map_location="cpu"
        )

        modelo.load_state_dict(pesos)

        self.modelo = modelo.to("cpu").eval()

    def estimar(self, imagem: np.ndarray) -> np.ndarray:
        """
        Recebe uma imagem BGR e retorna um mapa
        de profundidade relativa.
        """

        if imagem is None:
            raise ValueError("A imagem não pode ser vazia.")

        if imagem.ndim != 3 or imagem.shape[2] != 3:
            raise ValueError(
                "A imagem deve possuir três canais de cor."
            )

        if self.modelo is None:
            self.carregar_modelo()

        profundidade = self.modelo.infer_image(
            imagem,
            self.tamanho_entrada
        )

        return profundidade

    def estimar_arquivo(self, caminho_imagem: str) -> np.ndarray:
        """
        Carrega uma imagem do disco e estima sua profundidade.
        """

        imagem = cv2.imread(caminho_imagem)

        if imagem is None:
            raise FileNotFoundError(
                f"Não foi possível abrir a imagem: {caminho_imagem}"
            )

        return self.estimar(imagem)
