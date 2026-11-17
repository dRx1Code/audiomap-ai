
import pyttsx3


class AudioManager:
    def __init__(self):
        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 165)
        self.engine.setProperty("volume", 1.0)

        self.configurar_voz()

    def configurar_voz(self):
        vozes = self.engine.getProperty("voices")

        for voz in vozes:
            nome = voz.name.lower()
            identificador = voz.id.lower()

            if "brazil" in nome or "portuguese" in nome or "brazil" in identificador:
                self.engine.setProperty("voice", voz.id)
                break

    def falar(self, texto: str):
        if not texto.strip():
            return

        self.engine.say(texto)
        self.engine.runAndWait()
