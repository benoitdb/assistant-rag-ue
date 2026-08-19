"""Extraction des fiches du Guide du porteur de projet Centre-Val de Loire.

Troisième structure de document rencontrée dans le corpus (voir cadrage
§2 : "corpus hétérogène... la stratégie de découpage doit s'adapter au
type de document"), différente du règlement UE (src/extraction/
articles.py) et du décret (src/extraction/decret.py) : le guide est
organisé en "FICHE N°X – Titre", pas en articles. Le titre est isolé sur
sa propre ligne (comme le règlement UE), en police grasse — pas de
piège de mise en page particulier détecté ici (aucun texte pivoté sur ce
document, contrairement au règlement UE).
"""

import re
from dataclasses import dataclass

import pdfplumber

from extraction.articles import group_words_by_line

FICHE_BOLD_FONT_PREFIX = "Calibri-Bold"
FICHE_HEADING_RE = re.compile(r"^FICHE N°(\d+)\s*–\s*(.*)$")


@dataclass
class FicheHeading:
    page: int
    top: int
    numero: int
    titre: str


@dataclass
class Fiche:
    numero: int
    titre: str
    texte: str
    page_debut: int


def _is_bold(fonts: set) -> bool:
    return any(FICHE_BOLD_FONT_PREFIX in f for f in fonts)


def find_fiche_headings(pdf: pdfplumber.PDF) -> list[FicheHeading]:
    """Repère les lignes "FICHE N°X – Titre", par police grasse."""
    headings = []
    for page_index, page in enumerate(pdf.pages):
        for top, text, fonts in group_words_by_line(page):
            match = FICHE_HEADING_RE.match(text.strip())
            if not match:
                continue
            if not _is_bold(fonts):
                continue
            headings.append(
                FicheHeading(
                    page=page_index,
                    top=top,
                    numero=int(match.group(1)),
                    titre=match.group(2).strip(),
                )
            )
    return headings


def extract_fiches(pdf_path: str) -> list[Fiche]:
    """Extrait les 10 fiches du guide : numéro, titre, corps du texte."""
    with pdfplumber.open(pdf_path) as pdf:
        headings = find_fiche_headings(pdf)
        fiches = []
        for i, heading in enumerate(headings):
            if i + 1 < len(headings):
                end_page, end_top = headings[i + 1].page, headings[i + 1].top
            else:
                end_page, end_top = len(pdf.pages) - 1, float("inf")

            texte_lines = []
            for page_index in range(heading.page, end_page + 1):
                page = pdf.pages[page_index]
                for top, text, _ in group_words_by_line(page):
                    if page_index == heading.page and top <= heading.top:
                        continue
                    if page_index == end_page and top >= end_top:
                        continue
                    texte_lines.append(text)

            fiches.append(
                Fiche(
                    numero=heading.numero,
                    titre=heading.titre,
                    texte="\n".join(texte_lines),
                    page_debut=heading.page,
                )
            )
        return fiches
