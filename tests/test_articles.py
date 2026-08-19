import pdfplumber
import pytest

from conftest import REGLEMENT_PDF
from extraction.articles import extract_articles, find_article_headings


@pytest.fixture(scope="module")
def pdf():
    with pdfplumber.open(REGLEMENT_PDF) as opened:
        yield opened


@pytest.fixture(scope="module")
def articles():
    return extract_articles(str(REGLEMENT_PDF))


def test_finds_all_119_articles_including_the_source_typo(pdf):
    """Le règlement va de l'article premier à l'article 119, sans trou.

    L'article 105 est écrit "Articles 105" (pluriel, coquille du texte
    officiel) dans le PDF source — sans la détection par police (plutôt
    qu'une regex stricte sur le texte), il serait manqué.
    """
    headings = find_article_headings(pdf)
    numeros = sorted(h.numero for h in headings)
    assert numeros == list(range(1, 120))


def test_article_premier_titre_et_debut_du_texte(articles):
    article_1 = next(a for a in articles if a.numero == 1)
    assert article_1.titre == "Objet et champ d’application"
    assert article_1.texte.startswith("1. Le présent règlement arrête:")


def test_article_105_malgre_la_coquille_du_texte_source(articles):
    article_105 = next(a for a in articles if a.numero == 105)
    assert article_105.titre == "Principes et règles de dégagement"
    assert "dégagement" in article_105.texte.lower()


def test_aucune_ligne_d_en_tete_de_page_dans_le_texte(articles):
    """Les lignes "Journal officiel de l'Union européenne" (répétées sur
    chaque page, parfois corrompues à l'extraction, cf. issue #2) ne
    doivent jamais polluer le corps d'un article."""
    for article in articles:
        assert "Journal" not in article.texte


def test_article_multi_pages_reste_continu(articles):
    """L'article 104 (corrections financières) s'étend sur plusieurs
    pages du PDF (84 à 85) : le texte doit rester continu malgré la
    coupure de page."""
    article_104 = next(a for a in articles if a.numero == 104)
    assert "correction financière" in article_104.texte.lower()
    assert len(article_104.texte) > 1500
