"""Mesure du retrieval sur le jeu de questions de référence (cadrage §6).

Test d'intégration réel : hits l'API Mistral (embedding de la question)
et Qdrant Cloud (recherche vectorielle) plutôt que des mocks — le
retrieval est précisément la brique qui ne peut pas être validée
autrement (ce n'est pas la logique de recherche qui compte mais son
comportement sur le vrai corpus indexé). Nécessite `.env` rempli et le
corpus déjà indexé (`scripts/index_corpus.py`).

Seuil de rappel choisi à 80% : mesuré à 9/9 (100%) au moment de
l'écriture de ce test sur le jeu de référence actuel — 80% laisse une
marge avant de considérer une régression comme un échec de test,
plutôt que d'exiger un score parfait à chaque exécution (variabilité
possible du modèle d'embedding).
"""

from dotenv import load_dotenv

load_dotenv()

from indexation.qdrant_index import get_client  # noqa: E402
from retrieval.retriever import search  # noqa: E402

from data.reference_questions import REFERENCE_QUESTIONS  # noqa: E402

TOP_K = 5
MINIMUM_RECALL = 0.8


def _is_expected_chunk(result, expected: dict) -> bool:
    return (
        result.document == expected["document"]
        and result.type_unite == expected["type_unite"]
        and result.numero == expected["numero"]
    )


def test_rappel_sur_le_jeu_de_questions_de_reference():
    client = get_client()
    hits = 0
    echecs = []

    for expected in REFERENCE_QUESTIONS:
        results = search(client, expected["question"], top_k=TOP_K)
        if any(_is_expected_chunk(r, expected) for r in results):
            hits += 1
        else:
            echecs.append(expected["question"])

    recall = hits / len(REFERENCE_QUESTIONS)
    assert recall >= MINIMUM_RECALL, (
        f"rappel {recall:.0%} sous le seuil de {MINIMUM_RECALL:.0%} — "
        f"questions manquées : {echecs}"
    )
