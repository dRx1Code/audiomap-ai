
import cv2


def iniciar_camera():

    # Conecta à primeira câmera USB disponível
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("ERRO: Não foi possível acessar a câmera.")
        return

    print("AudioMap AI iniciado!")
    print("Câmera conectada com sucesso.")
    print("Pressione ESC para encerrar.")

    while True:

        # Captura um frame da câmera
        sucesso, frame = camera.read()

        if not sucesso:
            print("Erro ao capturar imagem.")
            break

        # Exibe a imagem capturada
        cv2.imshow("AudioMap AI - Visao Computacional", frame)

        # ESC encerra o programa
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Libera os recursos
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    iniciar_camera()
