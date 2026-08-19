"""Interface Streamlit de l'assistant RAG réglementaire fonds européens.

Positionnement volontaire comme outil d'aide, jamais comme source
faisant foi (cadrage §7 : fiabilité réglementaire critique) — rappelé
directement dans l'interface, pas seulement dans la documentation.
"""

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
load_dotenv(ROOT / ".env")

from generation.generator import DOCUMENT_LABELS, REFUS_HORS_CORPUS, generate_answer  # noqa: E402
from indexation.qdrant_index import get_client  # noqa: E402
from retrieval.retriever import search  # noqa: E402

TOP_K = 5

st.set_page_config(page_title="Assistant RAG réglementaire — fonds européens", page_icon="📘")

st.title("Assistant réglementaire — fonds européens de cohésion")
st.caption(
    "Portfolio / démo — aide à l'instruction et à l'audit sur le règlement (UE) "
    "2021/1060, le décret n° 2022-608 et le guide du porteur de projet "
    "Centre-Val de Loire."
)
st.warning(
    "Cet assistant est un outil d'aide, pas une source faisant foi. "
    "Vérifie toujours une réponse auprès des textes officiels ou d'un "
    "professionnel avant toute décision.",
    icon="⚠️",
)


@st.cache_resource
def _get_client():
    return get_client()


def _document_label(document: str) -> str:
    return DOCUMENT_LABELS.get(document, document)


question = st.text_input("Pose ta question sur la réglementation FEDER / FSE+ :")

if question:
    client = _get_client()
    with st.spinner("Recherche dans le corpus..."):
        chunks = search(client, question, top_k=TOP_K)
    with st.spinner("Génération de la réponse..."):
        answer = generate_answer(question, chunks)

    st.markdown(answer)

    if answer.strip() != REFUS_HORS_CORPUS:
        with st.expander("Sources consultées"):
            for chunk in chunks:
                label = "Article" if "article" in chunk.type_unite else "Fiche"
                titre = f" — {chunk.titre}" if chunk.titre else ""
                st.markdown(
                    f"**{_document_label(chunk.document)} — {label} {chunk.numero}{titre}** "
                    f"(score {chunk.score:.2f})"
                )
                extrait = chunk.texte[:500] + ("…" if len(chunk.texte) > 500 else "")
                st.text(extrait)
