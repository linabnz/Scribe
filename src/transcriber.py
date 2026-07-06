from pathlib import Path

import groq

from config import GROQ_API_KEY, STT_MODEL


def transcribe_audio(audio_path, model=STT_MODEL, language=None):
    """
    Transcrit un fichier audio en texte via l'API Groq (Whisper).
    """
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

    client = groq.Groq(api_key=GROQ_API_KEY)

    try:
        with open(path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(path.name, file.read()),
                model=model,
                language=language,
            )
    except (groq.APIConnectionError, groq.APIStatusError) as exc:
        raise RuntimeError(f"Échec de la transcription via l'API Groq : {exc}") from exc

    return transcription.text