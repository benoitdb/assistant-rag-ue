import pdfplumber
import pytest

from conftest import GUIDE_REGIONAL_PDF
from extraction.guide_regional import extract_fiches, find_fiche_headings


@pytest.fixture(scope="module")
def pdf():
    with pdfplumber.open(GUIDE_REGIONAL_PDF) as opened:
        yield opened


@pytest.fixture(scope="module")
def fiches():
    return extract_fiches(str(GUIDE_REGIONAL_PDF))


def test_trouve_les_10_fiches(pdf):
    headings = find_fiche_headings(pdf)
    numeros = sorted(h.numero for h in headings)
    assert numeros == list(range(1, 11))


def test_fiche_1_titre_et_corps(fiches):
    fiche_1 = next(f for f in fiches if f.numero == 1)
    assert fiche_1.titre == "L’ORGANISATION DU PROGRAMME ET LES OUTILS CLÉS"
    assert "MAQUETTE FINANCIÈRE" in fiche_1.texte


def test_fiche_multi_pages_reste_continue(fiches):
    """La fiche 6 (éligibilité des dépenses) s'étend sur plusieurs pages
    (14 à 23 environ) : le texte doit rester continu malgré la coupure."""
    fiche_6 = next(f for f in fiches if f.numero == 6)
    assert len(fiche_6.texte) > 1000


def test_derniere_fiche_va_jusqu_a_la_fin_du_document(fiches):
    fiche_10 = next(f for f in fiches if f.numero == 10)
    assert len(fiche_10.texte) > 0
