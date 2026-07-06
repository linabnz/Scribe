"""
Interface en ligne de commande de Scribe.


"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from config import STT_MODEL
from summary import generate_summary
from transcriber import transcribe_audio

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "comptes_rendus"


def main():
    parser = argparse.ArgumentParser(
        prog="scribe",
        description="Transforme un enregistrement audio en compte rendu structuré.",
    )
    parser.add_argument("audio_path", help="Chemin vers le fichier audio à traiter")
    args = parser.parse_args()

    print(f"Transcription en cours ({args.audio_path})...")
    try:
        transcript = transcribe_audio(args.audio_path, model=STT_MODEL)
    except FileNotFoundError as exc:
        print(f"Erreur : {exc}")
        sys.exit(1)
    except RuntimeError as exc:
        print(f"Erreur lors de la transcription : {exc}")
        sys.exit(1)
    print("Transcription terminée.")

    print("Rédaction du compte rendu en cours...")
    try:
        compte_rendu = generate_summary(transcript)
    except RuntimeError as exc:
        print(f"Erreur lors de la génération du compte rendu : {exc}")
        sys.exit(1)
    print("Compte rendu généré.\n")

    print(compte_rendu)

    OUTPUT_DIR.mkdir(exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_path = OUTPUT_DIR / f"compte_rendu_{horodatage}.md"
    output_path.write_text(compte_rendu, encoding="utf-8")

    print(f"\n Compte rendu sauvegardé dans : {output_path}")


if __name__ == "__main__":
    main()