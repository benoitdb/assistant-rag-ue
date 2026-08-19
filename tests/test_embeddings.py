import pytest

from indexation.embeddings import BATCH_SIZE, embed_texts


class FakeResponse:
    def __init__(self, vectors, status_code=200):
        self._vectors = vectors
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"erreur API {self.status_code}")

    def json(self):
        return {"data": [{"embedding": v} for v in self._vectors]}


def test_embed_texts_retourne_un_vecteur_par_texte_dans_l_ordre(monkeypatch):
    def fake_post(url, headers, json, timeout):
        return FakeResponse([[float(len(t))] for t in json["input"]])

    monkeypatch.setattr("mistral_http.requests.post", fake_post)

    vectors = embed_texts(["ab", "abcd"], api_key="fake-key")

    assert vectors == [[2.0], [4.0]]


def test_embed_texts_decoupe_par_lots(monkeypatch):
    calls = []

    def fake_post(url, headers, json, timeout):
        calls.append(json["input"])
        return FakeResponse([[0.0] for _ in json["input"]])

    monkeypatch.setattr("mistral_http.requests.post", fake_post)

    texts = [f"texte {i}" for i in range(BATCH_SIZE + 5)]
    vectors = embed_texts(texts, api_key="fake-key")

    assert len(vectors) == len(texts)
    assert len(calls) == 2
    assert calls[0] == texts[:BATCH_SIZE]
    assert calls[1] == texts[BATCH_SIZE:]


def test_embed_texts_leve_une_erreur_si_l_api_repond_en_erreur_non_transitoire(monkeypatch):
    monkeypatch.setattr(
        "mistral_http.requests.post",
        lambda *a, **k: FakeResponse([], status_code=400),
    )

    with pytest.raises(RuntimeError):
        embed_texts(["texte"], api_key="fake-key")
