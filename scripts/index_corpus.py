"""Pipeline complet d'indexation du corpus V1 dans Qdrant.

Extraction -> chunking -> embeddings -> indexation, sur les 3 documents
du corpus V1 (règlement UE, décret, guide régional). Vérifie à la fin
que le nombre de points indexés correspond au nombre de chunks produits
et que chaque chunk porte les métadonnées de citation attendues
(cadrage §4) — pas juste une exécution silencieuse.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
load_dotenv(ROOT / ".env")

from chunking.chunker import Chunk, chunk_units  # noqa: E402
from extraction.articles import extract_articles  # noqa: E402
from extraction.decret import extract_articles as extract_decret_articles  # noqa: E402
from extraction.guide_regional import extract_fiches  # noqa: E402
from indexation.embeddings import embed_texts  # noqa: E402
from indexation.qdrant_index import (  # noqa: E402
    chunk_payload,
    ensure_collection,
    get_client,
    index_chunks,
)

SOURCES = ROOT / "docs" / "sources"
CITATION_FIELDS = ("document", "type_unite", "numero", "page_debut")


def build_corpus_chunks() -> list[Chunk]:
    reglement = extract_articles(str(SOURCES / "reglement_ue_2021_1060.pdf"))
    decret = extract_decret_articles(str(SOURCES / "decret_2022_608.pdf"))
    fiches = extract_fiches(str(SOURCES / "guide_regional_centre_val_de_loire.pdf"))

    return (
        chunk_units("reglement_ue_2021_1060", "reglement_article", reglement)
        + chunk_units("decret_2022_608", "decret_article", decret)
        + chunk_units("guide_regional_centre_val_de_loire", "fiche_guide", fiches)
    )


def verify_citation_metadata(chunks: list[Chunk]) -> None:
    for chunk in chunks:
        payload = chunk_payload(chunk)
        missing = [f for f in CITATION_FIELDS if payload.get(f) in (None, "")]
        if missing:
            raise AssertionError(f"chunk sans métadonnée de citation {missing}: {chunk}")


def main() -> None:
    chunks = build_corpus_chunks()
    print(f"{len(chunks)} chunks produits sur les 3 documents du corpus.")

    vectors = embed_texts([c.texte for c in chunks])

    client = get_client()
    ensure_collection(client)
    indexed_count = index_chunks(client, chunks, vectors)

    if indexed_count != len(chunks):
        raise AssertionError(f"{indexed_count} points indexés pour {len(chunks)} chunks produits")
    verify_citation_metadata(chunks)

    print(
        f"{indexed_count} points indexés dans la collection Qdrant, "
        "métadonnées de citation vérifiées."
    )


if __name__ == "__main__":
    main()
