from pathlib import Path

import groq

from config import GROQ_API_KEY, TTS_MODEL, TTS_VOICE


def speak_report(text: str, output_path: str = "compte_rendu_audio.wav") -> str:
    """
    Convertit le texte du compte rendu en fichier audio via l'API TTS de Groq.

    Args:
        text: le texte à lire à voix haute (le compte rendu généré par le LLM).
        output_path: chemin du fichier audio de sortie.

    Returns:
        str: le chemin du fichier audio généré.

    Raises:
        RuntimeError: si l'appel à l'API Groq échoue.
    """
    client = groq.Groq(api_key=GROQ_API_KEY)

    try:
        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=TTS_VOICE,
            input=text,
            response_format="wav",
        )
    except (groq.APIConnectionError, groq.APIStatusError) as exc:
        raise RuntimeError(f"Échec de la synthèse vocale via l'API Groq : {exc}") from exc

    path = Path(output_path)
    response.write_to_file(path)

    return str(path)