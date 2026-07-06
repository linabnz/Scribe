# Scribe

Scribe est un outil en ligne de commande qui transforme un enregistrement audio (une réunion, un cours, une note vocale) en compte rendu écrit et structuré. Il repose sur deux modèles hébergés par Groq : un modèle de transcription (Speech-to-Text) et un modèle de langage (LLM) qui reformule cette transcription en compte rendu.

## Fonctionnement

Le programme prend un fichier audio en entrée. Ce fichier est d'abord transcrit en texte brut par Whisper, servi via l'API de Groq. Ce texte brut est ensuite envoyé à un LLM, accompagné d'un prompt système qui lui demande de produire un compte rendu structuré : titre, résumé, points clés, décisions et actions à mener. Avant cette dernière étape, le texte transcrit passe par un contrôle de modération, qui vérifie que la transcription correspond bien à un usage normal de l'outil et pas à une tentative de le détourner. Si ce contrôle échoue, Scribe refuse poliment de générer un compte rendu et n'envoie jamais le texte suspect au LLM.

Le compte rendu final est affiché à l'écran et sauvegardé dans un fichier Markdown, avec un nom horodaté pour ne jamais écraser les précédents.

## Installation

```bash
git clone https://github.com/linabnz/Scribe.git
cd Scribe

python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\Activate.ps1       # Windows PowerShell

pip install -r requirements.txt
```

## Configuration

Scribe a besoin d'une clé API Groq, disponible gratuitement sur console.groq.com/keys. Copiez le fichier d'exemple et renseignez votre clé :

```bash
cp .env.example .env
```

Le fichier `.env` contient alors :

```
GROQ_API_KEY=votre_cle_ici
```

Cette clé n'est jamais écrite en dur dans le code. Elle est chargée à l'exécution via python-dotenv, et le fichier `.env` est exclu du dépôt Git par le `.gitignore`, pour éviter qu'elle ne se retrouve un jour dans l'historique du projet.

## Utilisation

```bash
python src/cli.py audio_samples/audiotest.mp4
```

Le programme affiche sa progression au fur et à mesure : transcription en cours, puis rédaction du compte rendu. Une fois terminé, le résultat s'affiche dans le terminal et un fichier est créé dans le dossier `comptes_rendus`, nommé par exemple `compte_rendu_2026-07-06_143000.md`.

## Structure du projet

Le code source se trouve dans `src`. On y trouve `config.py`, qui centralise la clé API et les noms des modèles utilisés, `transcriber.py` pour la transcription audio, `summary.py` pour la génération du compte rendu, `moderation.py` pour le contrôle de détournement, et `cli.py` qui assemble le tout dans une commande utilisable. Le dossier `audio_samples` contient des exemples audio légers pour les tests manuels. Le dossier `comptes_rendus` contient les fichiers générés à l'exécution et n'est pas suivi par Git.

## Modèles utilisés

Pour la transcription, Scribe utilise whisper-large-v3. Groq propose aussi une variante turbo, moins chère et plus rapide, mais légèrement moins précise. Comme Scribe traite des enregistrements de réunion, avec parfois du bruit de fond, des accents ou plusieurs personnes qui parlent en même temps, on préfère la version standard : la fiabilité de la transcription compte plus que les quelques secondes gagnées, d'autant que l'usage n'est pas temps réel.

Pour la génération du compte rendu, Scribe utilise llama-3.3-70b-versatile. Un modèle plus léger, comme llama-3.1-8b-instant, serait plus rapide et moins cher, mais la tâche demandée consiste à extraire fidèlement des décisions et des actions à partir d'une transcription, sans en inventer, ce qui demande un modèle capable de suivre des instructions strictes. Le surcoût d'un modèle plus grand reste marginal à l'échelle d'un usage personnel ou d'une petite équipe.

Un point important à noter : Groq a annoncé la dépréciation de llama-3.3-70b-versatile, avec un arrêt prévu le 16 août 2026. Le modèle recommandé pour prendre le relais est openai/gpt-oss-120b. À cette date, la constante LLM_MODEL dans config.py devra être mise à jour, sans quoi les appels à l'API échoueront.

## Ce que renvoie l'API de transcription

Au-delà du texte, l'API de Groq, quand on lui demande un format de réponse détaillé (verbose_json), renvoie aussi la langue détectée, la durée de l'audio, et un découpage en segments horodatés. Chaque segment est accompagné d'indicateurs utiles : un score de confiance (avg_logprob), une probabilité de silence (no_speech_prob), et un ratio de compression qui peut révéler des répétitions ou du bégaiement.

Ces informations ne sont pas utilisées aujourd'hui dans Scribe, mais elles ouvrent des pistes d'évolution intéressantes. Les timestamps permettraient par exemple de relier chaque point du compte rendu à l'instant exact de l'audio correspondant. Les segments avec un score de confiance faible pourraient être signalés comme à vérifier, plutôt que d'être intégrés tels quels dans le compte rendu final.

## Modération

Scribe intègre un contrôle de modération qui analyse le texte transcrit avant de le transmettre au modèle chargé de rédiger le compte rendu. L'idée est de détecter les cas où le fichier audio ne contiendrait pas réellement une réunion, mais des instructions destinées à manipuler le modèle, une tentative de contournement ou tout autre usage manifestement hors du cadre de l'outil.

Ce contrôle intervient juste après la transcription et avant l'appel au modèle de résumé. Si une tentative de détournement est détectée, Scribe s'arrête et affiche un refus poli, sans jamais transmettre le texte suspect au LLM. Cette logique s'inspire du principe d'agent modérateur vu en cours dans la démonstration RAG, où une étape de contrôle est intercalée avant de faire confiance à une entrée utilisateur.

## Température

Le modèle de génération du compte rendu est appelé avec une température de 0.2. La température détermine à quel point les réponses du modèle sont prévisibles ou variées. Une valeur proche de 0 donne des réponses très stables et reproductibles, tandis qu'une valeur proche de 1 favorise des formulations plus variées, au prix d'une certaine imprévisibilité.

Pour un compte rendu de réunion, l'important est de rester fidèle à ce qui a été dit, sans invention ni reformulation trop libre des décisions et des actions. Une température basse convient donc mieux ici qu'une température élevée, qui serait plus adaptée à une tâche créative comme la génération d'un texte littéraire.

## Prompt système et tokens en cache

Le prompt système envoyé au modèle de résumé est identique à chaque appel, seul le texte de la transcription change d'une requête à l'autre. Ce préfixe fixe correspond exactement au cas d'usage du prompt caching vu en cours : plusieurs fournisseurs, dont Groq, mettent en cache les tokens d'entrée identiques d'une requête à l'autre et les facturent moins cher que des tokens nouveaux.

Concrètement, cela veut dire que le coût du prompt système tend à diminuer une fois qu'il a été envoyé une première fois, sans rien à faire de particulier côté code, puisque le mécanisme s'active automatiquement côté serveur. Un point de vigilance cependant : la documentation de Groq mentionne ce mécanisme surtout pour certains modèles, notamment ceux de la famille GPT-OSS. Il faudrait vérifier au cas par cas si llama-3.3-70b-versatile, ou le modèle qui le remplacera après sa dépréciation, en bénéficie réellement avant d'en tenir compte dans une estimation de coût.

## Tests

Les tests unitaires du projet s'exécutent avec pytest.

```bash
pip install -r requirements-dev.txt
pytest -v
```

Ils utilisent un client Groq simulé, donc aucun appel réseau réel n'est effectué et aucun quota n'est consommé.

## Organisation du travail

Le projet suit un modèle de branches simple, avec une branche dev qui sert d'intégration et une branche main réservée aux versions stables, taguées à chaque jalon. Chaque fonctionnalité est développée sur sa propre branche, créée depuis dev, avec des commits atomiques et des messages clairs. Une fois la fonctionnalité terminée, une pull request est ouverte vers dev, relue par le binôme, puis mergée.

---

Projet réalisé dans le cadre du TP Scribe : Git, GitHub et intégration d'IA serverless, Master 2 MD5, 2026.
