import pdfplumber
import pytest

from conftest import REGLEMENT_PDF
from extraction.annexes import find_annexe_on_page

# Annexe I : titre en texte droit (page "L 231/252", pas de rotation).
ANNEXE_I_PAGE_UPRIGHT_TITLE = 93

# Annexe II : titre lui-même pivoté à 90°, comme le reste de son contenu.
ANNEXE_II_PAGE_ROTATED_TITLE = 123

# Annexe IV : idem, titre pivoté (corrige une mauvaise identification
# initiale en "Annexe VI" faite à partir de texte scramblé non fiable,
# voir la correction sur l'issue #2).
ANNEXE_IV_PAGE_ROTATED_TITLE = 162

# Page 100 : suite de l'Annexe I (tableau 4), pas de nouveau titre dessus.
ANNEXE_I_MID_PAGE_NO_TITLE = 100

# Page 84 : corps de l'article 104, qui référence "l'annexe XXV" dans une
# phrase — ne doit pas être pris pour un titre d'annexe isolé.
ARTICLE_PAGE_WITH_ANNEXE_CROSS_REFERENCE = 84


@pytest.fixture(scope="module")
def pdf():
    with pdfplumber.open(REGLEMENT_PDF) as opened:
        yield opened


def test_titre_annexe_en_texte_droit(pdf):
    assert find_annexe_on_page(pdf.pages[ANNEXE_I_PAGE_UPRIGHT_TITLE]) == "I"


def test_titre_annexe_en_texte_pivote(pdf):
    assert find_annexe_on_page(pdf.pages[ANNEXE_II_PAGE_ROTATED_TITLE]) == "II"


def test_titre_annexe_iv_pivote_pas_confondu_avec_annexe_vi(pdf):
    assert find_annexe_on_page(pdf.pages[ANNEXE_IV_PAGE_ROTATED_TITLE]) == "IV"


def test_page_sans_nouveau_titre_ne_retourne_rien(pdf):
    assert find_annexe_on_page(pdf.pages[ANNEXE_I_MID_PAGE_NO_TITLE]) is None


def test_reference_croisee_dans_une_phrase_n_est_pas_prise_pour_un_titre(pdf):
    page = pdf.pages[ARTICLE_PAGE_WITH_ANNEXE_CROSS_REFERENCE]
    assert "annexe" in (page.extract_text() or "").lower()
    assert find_annexe_on_page(page) is None
