import pytest

from mistral_http import MAX_ATTEMPTS, post_with_retry


class FakeResponse:
    def __init__(self, status_code):
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"erreur API {self.status_code}")


def test_reussit_sans_retry_si_la_premiere_reponse_est_ok(monkeypatch):
    calls = []
    monkeypatch.setattr("mistral_http.time.sleep", lambda _: None)
    monkeypatch.setattr(
        "mistral_http.requests.post",
        lambda *a, **k: (calls.append(1), FakeResponse(200))[1],
    )

    response = post_with_retry("https://example.test")

    assert response.status_code == 200
    assert len(calls) == 1


def test_reessaie_sur_503_puis_reussit(monkeypatch):
    statuses = iter([503, 503, 200])
    monkeypatch.setattr("mistral_http.time.sleep", lambda _: None)
    monkeypatch.setattr("mistral_http.requests.post", lambda *a, **k: FakeResponse(next(statuses)))

    response = post_with_retry("https://example.test")

    assert response.status_code == 200


def test_abandonne_apres_max_attempts_et_leve_l_erreur(monkeypatch):
    monkeypatch.setattr("mistral_http.time.sleep", lambda _: None)
    monkeypatch.setattr("mistral_http.requests.post", lambda *a, **k: FakeResponse(503))

    with pytest.raises(RuntimeError):
        post_with_retry("https://example.test")


def test_ne_reessaie_pas_sur_une_erreur_non_transitoire(monkeypatch):
    calls = []
    monkeypatch.setattr("mistral_http.time.sleep", lambda _: None)
    monkeypatch.setattr(
        "mistral_http.requests.post",
        lambda *a, **k: (calls.append(1), FakeResponse(400))[1],
    )

    with pytest.raises(RuntimeError):
        post_with_retry("https://example.test")

    assert len(calls) == 1  # pas de retry sur une erreur client non transitoire


def test_max_attempts_est_au_moins_deux():
    """Le retry n'a de sens que si au moins un deuxième essai est tenté."""
    assert MAX_ATTEMPTS >= 2
