
from pathlib import Path

import groq


def transcribe_audio(audio_path, model="whisper-large-v3-turbo", language=None):
    """
    Transcrit un fichier audio en texte via l'API Groq (Whisper).

    Args:
        audio_path: chemin vers le fichier audio à transcrire.
        model: modèle STT Groq à utiliser.
        language: code langue ISO-639-1 optionnel (ex: "fr").

    Returns:
        str: le texte transcrit.

    Raises:
        FileNotFoundError: si le fichier audio n'existe pas.
        RuntimeError: si l'appel à l'API Groq échoue (erreur réseau ou
            réponse en erreur de l'API).
    """
    path = Path(audio_path)
    if not path.is_file():
        raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

    client = groq.Groq()  # lit GROQ_API_KEY dans l'environnement

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