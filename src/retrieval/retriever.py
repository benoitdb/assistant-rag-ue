"""Recherche vectorielle sur la collection Qdrant du corpus indexé.

La requête est vectorisée avec le même modèle que l'indexation
(Mistral Embed, cf. `indexation/embeddings.py`), puis les `top_k` chunks
les plus proches en similarité cosinus sont retournés.

Pas de reranking en V1 (le cadrage le laissait "éventuel") : le corpus
est restreint (278 chunks), la similarité cosinus directe est mesurée
suffisante sur le jeu de questions de référence
(`tests/test_retrieval.py`) — à reconsidérer seulement si cette mesure
montre une précision insuffisante.
"""

from dataclasses import dataclass

from qdrant_client import QdrantClient

from indexation.embeddings import embed_texts
from indexation.qdrant_index import COLLECTION_NAME


@dataclass
class RetrievedChunk:
    document: str
    type_unite: str
    numero: int
    titre: str
    sous_section: int | None
    page_debut: int
    texte: str
    score: float


def search(client: QdrantClient, question: str, top_k: int = 5) -> list[RetrievedChunk]:
    vector = embed_texts([question])[0]
    results = client.query_points(collection_name=COLLECTION_NAME, query=vector, limit=top_k).points

    return [
        RetrievedChunk(
            document=r.payload["document"],
            type_unite=r.payload["type_unite"],
            numero=r.payload["numero"],
            titre=r.payload["titre"],
            sous_section=r.payload["sous_section"],
            page_debut=r.payload["page_debut"],
            texte=r.payload["texte"],
            score=r.score,
        )
        for r in results
    ]
