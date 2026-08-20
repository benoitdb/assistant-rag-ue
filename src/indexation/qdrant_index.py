"""Indexation des chunks dans Qdrant Cloud.

Un point Qdrant par chunk. L'id est déterministe (UUID5 dérivé de
document + type d'unité + numéro + sous-section) plutôt qu'aléatoire :
ré-indexer le même corpus met à jour les points existants (upsert) au
lieu d'en créer des doublons — choix non trivial documenté dans
l'issue #8 sur benoitdb/assistant-rag-ue.
"""

import os
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from chunking.chunker import Chunk

COLLECTION_NAME = "assistant_rag_ue"
EMBEDDING_SIZE = 1024  # dimension des vecteurs mistral-embed
POINT_ID_NAMESPACE = uuid.UUID("f3c1b2a0-7e4d-4a2b-9c3d-8a1e6f0b2c7d")


def chunk_point_id(chunk: Chunk) -> str:
    key = f"{chunk.document}:{chunk.type_unite}:{chunk.numero}:{chunk.sous_section or 0}"
    return str(uuid.uuid5(POINT_ID_NAMESPACE, key))


def chunk_payload(chunk: Chunk) -> dict:
    """Métadonnées nécessaires à la citation exacte de la source (cadrage
    §4 : document + article/section) au moment de la génération."""
    return {
        "document": chunk.document,
        "type_unite": chunk.type_unite,
        "numero": chunk.numero,
        "titre": chunk.titre,
        "sous_section": chunk.sous_section,
        "page_debut": chunk.page_debut,
        "texte": chunk.texte,
    }


def get_client(url: str | None = None, api_key: str | None = None) -> QdrantClient:
    return QdrantClient(
        url=url or os.environ["QDRANT_URL"],
        api_key=api_key or os.environ["QDRANT_API_KEY"],
    )


def ensure_collection(client: QdrantClient) -> None:
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=EMBEDDING_SIZE, distance=Distance.COSINE),
        )


def index_chunks(client: QdrantClient, chunks: list[Chunk], vectors: list[list[float]]) -> int:
    """Indexe des chunks déjà vectorisés. Retourne le nombre de points indexés."""
    if len(chunks) != len(vectors):
        raise ValueError("chunks et vectors doivent avoir la même longueur")

    points = [
        PointStruct(id=chunk_point_id(chunk), vector=vector, payload=chunk_payload(chunk))
        for chunk, vector in zip(chunks, vectors, strict=True)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)
