"""Détection des titres d'annexe ("ANNEXE <romain>") pour attribuer un
tableau reconstruit à son annexe précise (voir issue #3 sur
benoitdb/assistant-rag-ue).

Piège découvert en construisant cette détection : le titre d'une annexe
peut être en texte droit (ex. Annexe I, VI) ou en texte pivoté à 90°
comme le reste de son contenu (ex. Annexe II, IV) — selon l'annexe. Les
deux cas doivent être vérifiés. Une détection naïve sur le texte brut
scramblé (`page.extract_text()` sur une page pivotée) a d'ailleurs
produit une fausse identification une première fois (page attribuée à
"Annexe VI" alors qu'il s'agissait de l'Annexe IV) — corrigée en
repassant systématiquement par la reconstruction validée plutôt que par
une lecture visuelle du texte scramblé.

Un titre d'annexe est repéré seulement s'il est ISOLÉ (seul sur sa ligne
ou sa colonne) — ça exclut les références croisées noyées dans une
phrase ("conformément à l'annexe XXV"), qui ne matchent jamais le motif
seules sur leur ligne/colonne.
"""

import re
from collections import defaultdict

import pdfplumber

from extraction.articles import group_words_by_line
from extraction.rotated_tables import reconstruct_rotated_cell

ANNEXE_HEADING_RE = re.compile(r"^ANNEXE\s+([IVXLCM]+)$")


def _find_upright_annexe(page: pdfplumber.page.Page) -> str | None:
    upright_page = page.filter(
        lambda obj: obj.get("object_type") != "char" or obj.get("upright", True)
    )
    for _, text, _ in group_words_by_line(upright_page):
        match = ANNEXE_HEADING_RE.match(text.strip())
        if match:
            return match.group(1)
    return None


def _find_rotated_annexe(page: pdfplumber.page.Page) -> str | None:
    rotated_chars = [c for c in page.chars if not c["upright"]]
    columns = defaultdict(list)
    for c in rotated_chars:
        columns[round(c["x0"], 1)].append(c)
    for x0 in sorted(columns):
        text = reconstruct_rotated_cell(columns[x0])
        for part in text.split(" | "):
            match = ANNEXE_HEADING_RE.match(part.strip())
            if match:
                return match.group(1)
    return None


def find_annexe_on_page(page: pdfplumber.page.Page) -> str | None:
    """Numéro romain de l'annexe dont le titre apparaît sur cette page, sinon None.

    Vérifie le texte droit puis le texte pivoté — une page n'a jamais les
    deux à la fois dans ce document, mais l'ordre n'a pas d'importance.
    """
    return _find_upright_annexe(page) or _find_rotated_annexe(page)
