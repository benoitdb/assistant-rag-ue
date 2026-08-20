import pytest

from chunking.chunker import Chunk
from indexation.qdrant_index import chunk_payload, chunk_point_id, index_chunks


class FakeClient:
    def __init__(self):
        self.upserted = []

    def upsert(self, collection_name, points):
        self.upserted.append((collection_name, points))


def make_chunk(**overrides):
    base = dict(
        document="reglement_ue_2021_1060",
        type_unite="reglement_article",
        numero=1,
        titre="Objet et champ d’application",
        texte="texte",
        page_debut=0,
        sous_section=None,
    )
    base.update(overrides)
    return Chunk(**base)


def test_chunk_point_id_est_stable_pour_le_meme_chunk():
    assert chunk_point_id(make_chunk(numero=1)) == chunk_point_id(make_chunk(numero=1))


def test_chunk_point_id_distingue_deux_articles_differents():
    assert chunk_point_id(make_chunk(numero=1)) != chunk_point_id(make_chunk(numero=2))


def test_chunk_point_id_distingue_les_sous_chunks_d_un_meme_article():
    assert chunk_point_id(make_chunk(sous_section=1)) != chunk_point_id(make_chunk(sous_section=2))


def test_chunk_payload_contient_les_metadonnees_de_citation():
    chunk = make_chunk(numero=19, titre="Mesures...", sous_section=2, page_debut=10)
    payload = chunk_payload(chunk)
    assert payload == {
        "document": "reglement_ue_2021_1060",
        "type_unite": "reglement_article",
        "numero": 19,
        "titre": "Mesures...",
        "sous_section": 2,
        "page_debut": 10,
        "texte": "texte",
    }


def test_index_chunks_upsert_un_point_par_chunk_avec_le_bon_vecteur():
    client = FakeClient()
    chunks = [make_chunk(numero=1), make_chunk(numero=2)]
    vectors = [[0.1, 0.2], [0.3, 0.4]]

    count = index_chunks(client, chunks, vectors)

    assert count == 2
    _collection_name, points = client.upserted[0]
    assert len(points) == 2
    assert [p.vector for p in points] == vectors


def test_index_chunks_rejette_des_longueurs_differentes():
    client = FakeClient()
    with pytest.raises(ValueError):
        index_chunks(client, [make_chunk()], [])
