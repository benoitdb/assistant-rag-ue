import pdfplumber
import pytest

from conftest import REGLEMENT_PDF
from extraction.rotated_tables import (
    extract_rotated_tables_from_page,
    is_rotated_page,
    reconstruct_rotated_cell,
)

# Page d'index pdfplumber 165 (numérotée "L 231/324" dans le JO) : une
# page de l'Annexe IV, tableau des conditions thématiques favorisantes,
# entièrement en texte pivoté à 90° (voir issue #2).
ANNEXE_IV_PAGE = 165

# Page d'index 21 : corps de l'article premier, texte droit normal.
ARTICLE_PAGE = 21


@pytest.fixture(scope="module")
def pdf():
    with pdfplumber.open(REGLEMENT_PDF) as opened:
        yield opened


def test_annexe_iv_page_est_detectee_comme_pivotee(pdf):
    assert is_rotated_page(pdf.pages[ANNEXE_IV_PAGE]) is True


def test_page_article_n_est_pas_detectee_comme_pivotee(pdf):
    assert is_rotated_page(pdf.pages[ARTICLE_PAGE]) is False


def test_reconstruction_cellule_vide():
    assert reconstruct_rotated_cell([]) == ""


def test_tables_de_l_annexe_iv_sont_lisibles_apres_reconstruction(pdf):
    page = pdf.pages[ANNEXE_IV_PAGE]
    tables = extract_rotated_tables_from_page(page)

    assert len(tables) >= 1

    all_cell_texts = [cell for table in tables for row in table for cell in row]
    joined = " ".join(all_cell_texts)

    # en-têtes de colonnes attendus du tableau des conditions favorisantes
    assert "Nom de la condition" in joined
    assert "favorisante" in joined
    assert "Critères de réalisation" in joined

    # aucune cellule ne doit contenir le scramble caractéristique du bug
    # d'extraction naïve (mots lus à l'envers, ex. "noitidnoc")
    assert not any("noitidnoc" in cell for cell in all_cell_texts)
