"""Requête HTTP vers l'API Mistral avec retry sur erreur transitoire.

Le free tier Mistral renvoie occasionnellement un 503 (service
temporairement indisponible) ou un 429 (rate limit) sous charge —
observé en exécutant la suite de tests complète d'affilée (embeddings +
génération), cf. issue #13. Un retry avec backoff court suffit : pas
question d'absorber une vraie panne prolongée, juste la variabilité
normale d'un service gratuit partagé, partagé entre `indexation.embeddings`
et `generation.generator` (même risque, même remède, d'où ce module commun).
"""

import time

import requests

TRANSIENT_STATUS_CODES = {429, 503}
MAX_ATTEMPTS = 3
BACKOFF_SECONDS = 2


def post_with_retry(url: str, **kwargs) -> requests.Response:
    response = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = requests.post(url, **kwargs)
        if response.status_code not in TRANSIENT_STATUS_CODES:
            break
        if attempt < MAX_ATTEMPTS:
            time.sleep(BACKOFF_SECONDS * attempt)
    response.raise_for_status()
    return response
