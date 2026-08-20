"""Génération de réponse à partir des chunks retrouvés, avec citation contrainte.

Les deux exigences non négociables du cadrage (§4) sont portées par le
prompt système, pas par du post-traitement : citer la source exacte
(document + article/section) pour chaque affirmation, et répondre
explicitement "je ne sais pas" quand les extraits fournis ne couvrent
pas la question plutôt que d'inventer. C'est le point de vigilance
identifié dans l'ADR 0001 (fiabilité d'un LLM free tier sur ces deux
consignes) — à vérifier par `tests/test_generation.py`.
"""

import os

from mistral_http import post_with_retry
from retrieval.retriever import RetrievedChunk

MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_CHAT_MODEL = "mistral-small-latest"

DOCUMENT_LABELS = {
    "reglement_ue_2021_1060": "Règlement (UE) 2021/1060",
    "decret_2022_608": "Décret n° 2022-608",
    "guide_regional_centre_val_de_loire": "Guide du porteur de projet — Centre-Val de Loire",
}

REFUS_HORS_CORPUS = "Je ne sais pas : cette question n'est pas couverte par les documents fournis."

SYSTEM_PROMPT = f"""Tu es un assistant documentaire sur la réglementation des fonds \
européens de cohésion (FEDER, FSE+), utilisé en aide à l'instruction et à l'audit. \
Tu n'es pas une source faisant foi : tu aides à retrouver et citer la réglementation, \
tu ne remplaces pas une vérification par un professionnel.

Réponds uniquement à partir des extraits fournis ci-dessous, jamais à partir de \
connaissances générales sur la réglementation européenne.

Règles strictes, à respecter systématiquement :
1. Chaque affirmation doit être suivie de sa source exacte, en reprenant \
mot pour mot le libellé de document entre crochets dans les extraits fournis \
(ne jamais reformuler, traduire ou corriger ce libellé), au format \
[Document — Article N] ou [Document — Fiche N].
2. Si les extraits fournis ne permettent pas de répondre à la question — même \
partiellement, même si le sujet semble proche — réponds EXACTEMENT et UNIQUEMENT : \
"{REFUS_HORS_CORPUS}" Ne complète jamais cette réponse par une supposition, un \
résumé de ce que tu sais par ailleurs, ou une reformulation de la question.
"""


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Formate les chunks retrouvés en contexte pour le prompt.

    Utilise un libellé de document lisible (`DOCUMENT_LABELS`) plutôt que
    l'identifiant technique snake_case stocké dans les métadonnées Qdrant
    (`chunk.document`) — constaté à l'usage : sans ça, le modèle
    reformate spontanément l'identifiant technique dans sa citation
    (accents ajoutés, casse changée), ce qui rend la citation à la fois
    peu présentable pour l'utilisateur final et peu fiable à vérifier
    automatiquement (cf. tests/test_generation.py).
    """
    parts = []
    for chunk in chunks:
        document_label = DOCUMENT_LABELS.get(chunk.document, chunk.document)
        label = "Article" if "article" in chunk.type_unite else "Fiche"
        titre = f" — {chunk.titre}" if chunk.titre else ""
        parts.append(f"[{document_label} — {label} {chunk.numero}{titre}]\n{chunk.texte}")
    return "\n\n".join(parts)


def generate_answer(question: str, chunks: list[RetrievedChunk], api_key: str | None = None) -> str:
    api_key = api_key or os.environ["MISTRAL_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    context = format_context(chunks)
    user_message = f"Extraits disponibles :\n\n{context}\n\nQuestion : {question}"

    response = post_with_retry(
        MISTRAL_CHAT_URL,
        headers=headers,
        json={
            "model": MISTRAL_CHAT_MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.0,
        },
        timeout=60,
    )
    return response.json()["choices"][0]["message"]["content"]
