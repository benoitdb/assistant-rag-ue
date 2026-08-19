"""Génération des embeddings via l'API Mistral Embed.

Appel HTTP direct plutôt qu'un SDK/framework supplémentaire (cf. ADR 0001
— pas de framework RAG, contrôle fin nécessaire sur ce qui est indexé) :
seul le SDK officiel du vector store (`qdrant-client`) est utilisé côté
indexation.
"""

import os

from mistral_http import post_with_retry

MISTRAL_EMBED_URL = "https://api.mistral.ai/v1/embeddings"
MISTRAL_EMBED_MODEL = "mistral-embed"
BATCH_SIZE = 32


def embed_texts(texts: list[str], api_key: str | None = None) -> list[list[float]]:
    """Retourne un vecteur d'embedding par texte, dans le même ordre.

    Envoyé par lots de `BATCH_SIZE` plutôt qu'en une seule requête : les
    chunks longs (jusqu'à plusieurs milliers de caractères après
    découpage, cf. ADR 0002) additionnés sur tout le corpus dépasseraient
    la taille de requête raisonnable pour l'API si envoyés d'un coup.
    """
    api_key = api_key or os.environ["MISTRAL_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    vectors: list[list[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = post_with_retry(
            MISTRAL_EMBED_URL,
            headers=headers,
            json={"model": MISTRAL_EMBED_MODEL, "input": batch},
            timeout=60,
        )
        data = response.json()["data"]
        vectors.extend(item["embedding"] for item in data)
    return vectors
