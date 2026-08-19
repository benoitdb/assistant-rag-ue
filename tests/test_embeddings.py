import pytest

from indexation.embeddings import BATCH_SIZE, embed_texts


class FakeResponse:
    def __init__(self, vectors):
        self._vectors = vectors

    def raise_for_status(self):
        pass

    def json(self):
        return {"data": [{"embedding": v} for v in self._vectors]}


def test_embed_texts_retourne_un_vecteur_par_texte_dans_l_ordre(monkeypatch):
    def fake_post(url, headers, json, timeout):
        return FakeResponse([[float(len(t))] for t in json["input"]])

    monkeypatch.setattr("indexation.embeddings.requests.post", fake_post)

    vectors = embed_texts(["ab", "abcd"], api_key="fake-key")

    assert vectors == [[2.0], [4.0]]


def test_embed_texts_decoupe_par_lots(monkeypatch):
    calls = []

    def fake_post(url, headers, json, timeout):
        calls.append(json["input"])
        return FakeResponse([[0.0] for _ in json["input"]])

    monkeypatch.setattr("indexation.embeddings.requests.post", fake_post)

    texts = [f"texte {i}" for i in range(BATCH_SIZE + 5)]
    vectors = embed_texts(texts, api_key="fake-key")

    assert len(vectors) == len(texts)
    assert len(calls) == 2
    assert calls[0] == texts[:BATCH_SIZE]
    assert calls[1] == texts[BATCH_SIZE:]


def test_embed_texts_leve_une_erreur_si_l_api_repond_en_erreur(monkeypatch):
    class FailingResponse(FakeResponse):
        def raise_for_status(self):
            raise RuntimeError("erreur API")

    monkeypatch.setattr(
        "indexation.embeddings.requests.post",
        lambda *a, **k: FailingResponse([]),
    )

    with pytest.raises(RuntimeError):
        embed_texts(["texte"], api_key="fake-key")
