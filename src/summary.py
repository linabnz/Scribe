from pathlib import Path
from groq import Groq
from groq import APIError
from config import GROQ_API_KEY, LLM_MODEL

client = Groq(api_key=GROQ_API_KEY)

PROMPT_PATH = Path(__file__).parent / "prompts" / "system_prompt.txt"


def generate_summary(transcript_text: str) -> str:
    """
    Reçoit une transcription brute et retourne un compte rendu structuré
    (titre, résumé, points clés, décisions/actions) via le LLM Groq.
    """
    system_prompt = PROMPT_PATH.read_text(encoding="utf-8")

    try:
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript_text},
            ],
        )
    except APIError as e:
        raise RuntimeError(f"Erreur API Groq lors de la génération du compte rendu : {e}")

    return completion.choices[0].message.content