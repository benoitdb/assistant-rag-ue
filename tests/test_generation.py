"""Test des deux exigences non négociables du cadrage (§4) sur la
génération réelle : citation exacte de la source, et refus explicite
sur le hors-corpus plutôt qu'une invention.
Test d'intégration réel (Mistral + Qdrant Cloud, pas de mock) — c'est
justement la fiabilité du LLM free tier sur ces deux consignes qui est
le risque identifié dans l'ADR 0001, pas mesurable avec des réponses
simulées. Nécessite `.env` rempli et le corpus déjà indexé.
"""

import pytest
from dotenv import load_dotenv

load_dotenv()

from data.reference_questions import HORS_CORPUS_QUESTIONS, REFERENCE_QUESTIONS  # noqa: E402
from generation.generator import DOCUMENT_LABELS, REFUS_HORS_CORPUS, generate_answer  # noqa: E402
from indexation.qdrant_index import get_client  # noqa: E402
from retrieval.retriever import search  # noqa: E402

# Tests d'intégration réels : consomment du quota Mistral/Qdrant et exigent le
# corpus indexé. Exclus par défaut (pyproject.toml), lancés par `pytest -m reseau`.
pytestmark = pytest.mark.reseau

TOP_K = 5


def test_citation_exacte_sur_le_jeu_de_questions_de_reference():
    """Chaque réponse à une question du corpus doit citer le bon document
    (libellé lisible) et le bon numéro d'article/fiche, et ne pas se
    replier sur le refus hors-corpus alors que la question est couverte."""
    client = get_client()
    echecs = []

    for expected in REFERENCE_QUESTIONS:
        chunks = search(client, expected["question"], top_k=TOP_K)
        answer = generate_answer(expected["question"], chunks)

        label = DOCUMENT_LABELS[expected["document"]]
        citation_correcte = label in answer and str(expected["numero"]) in answer
        refus_a_tort = REFUS_HORS_CORPUS in answer

        if not citation_correcte or refus_a_tort:
            echecs.append((expected["question"], answer))

    assert not echecs, f"citations incorrectes ou refus à tort : {echecs}"


def test_refus_explicite_sur_le_hors_corpus():
    """Sur une question hors périmètre V1 (cadrage §1), la réponse doit
    être le refus explicite exact, jamais une réponse inventée à partir
    de connaissances générales sur la réglementation européenne."""
    client = get_client()
    echecs = []

    for question in HORS_CORPUS_QUESTIONS:
        chunks = search(client, question, top_k=TOP_K)
        answer = generate_answer(question, chunks)
        if REFUS_HORS_CORPUS not in answer:
            echecs.append((question, answer))

    assert not echecs, f"réponse inventée au lieu du refus explicite : {echecs}"
