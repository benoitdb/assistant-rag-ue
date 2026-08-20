import pdfplumber
import pytest

from conftest import DECRET_PDF
from extraction.decret import extract_articles, find_article_headings


@pytest.fixture(scope="module")
def pdf():
    with pdfplumber.open(DECRET_PDF) as opened:
        yield opened


@pytest.fixture(scope="module")
def articles():
    return extract_articles(str(DECRET_PDF))


def test_trouve_les_10_articles(pdf):
    headings = find_article_headings(pdf)
    numeros = sorted(h.numero for h in headings)
    assert numeros == list(range(1, 11))


def test_article_premier_corps_du_texte(articles):
    article_1 = next(a for a in articles if a.numero == 1)
    assert article_1.texte.startswith("Conformément à l’article 63.1 du règlement (UE) 2021/1060")
    assert "période 2021-2027" in article_1.texte


def test_article_court_sur_une_seule_ligne_a_son_corps_sur_la_ligne_suivante(articles):
    """Art. 2. – n'a rien après le tiret sur sa propre ligne : le corps
    commence à la ligne suivante, pas de perte de texte."""
    article_2 = next(a for a in articles if a.numero == 2)
    assert article_2.texte.startswith("Pour l’application du présent décret")


def test_reference_croisee_en_minuscule_non_prise_pour_un_marqueur(articles):
    """Le texte contient de nombreuses références croisées en minuscule
    ("son article 63.1", "l'article 65.1"...) qui ne doivent jamais être
    prises pour un nouveau marqueur d'article (toujours "Art." majuscule
    + gras dans ce document)."""
    numeros = sorted(a.numero for a in articles)
    assert numeros == list(range(1, 11))


def test_dernier_article_ne_deborde_pas_sur_l_annexe(articles):
    article_10 = next(a for a in articles if a.numero == 10)
    assert "RÈGLES PARTICULIÈRES" not in article_10.texte
