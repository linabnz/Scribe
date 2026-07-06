
Q2 — quels modèles STT et LLM propose Groq, lesquels choisis-tu ?
À vérifier précisément sur la doc (rubrique Models), mais en général Groq propose :


STT : plusieurs variantes Whisper (dont une "large" plus précise mais un peu plus lente, et une "turbo" plus rapide mais un peu moins précise). Pour un compte rendu de réunion où la précision compte, tu justifies un choix orienté qualité (large) sauf contrainte de vitesse.
LLM : plusieurs modèles Llama (tailles différentes) et parfois d'autres familles. Pour une tâche de reformulation/structuration, un modèle de taille moyenne à grande donne un bon compromis qualité/vitesse ; Groq est de toute façon connu pour sa vitesse d'inférence très élevée (LPU), donc même un gros modèle reste rapide chez eux.