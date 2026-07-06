import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY manquante. Copie .env.example vers .env "
        "et renseigne ta clé API Groq."
    )

# Seul endroit du projet où les noms de modèles apparaissent
STT_MODEL = "whisper-large-v3"
LLM_MODEL = "llama-3.3-70b-versatile"