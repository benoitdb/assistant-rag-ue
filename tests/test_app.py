"""Test de l'interface Streamlit (`app.py`) sans navigateur, via `AppTest`.

Test d'intégration réel comme `test_retrieval.py`/`test_generation.py` :
c'est le comportement de bout en bout (saisie -> retrieval -> génération
-> affichage) qui compte, pas mockable sans perdre l'intérêt du test.
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = Path(__file__).resolve().parent.parent / "app.py"


def test_question_du_corpus_affiche_une_reponse_avec_sources():
    at = AppTest.from_file(str(APP_PATH), default_timeout=60)
    at.run()
    at.text_input[0].input("Quel est l'objet du règlement (UE) 2021/1060 ?").run()

    assert not at.exception
    markdown_text = "\n".join(m.value for m in at.markdown)
    assert "Article 1" in markdown_text
    assert "Sources consultées" in [e.label for e in at.expander]


def test_question_hors_corpus_affiche_le_refus_sans_sources():
    at = AppTest.from_file(str(APP_PATH), default_timeout=60)
    at.run()
    at.text_input[0].input("Quelle est la capitale de la France ?").run()

    assert not at.exception
    markdown_text = "\n".join(m.value for m in at.markdown)
    assert "ne sais pas" in markdown_text.lower()
    assert len(at.expander) == 0
