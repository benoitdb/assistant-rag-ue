"""Extraction des articles du Décret n° 2022-608 du 21 avril 2022.

Structure différente du Règlement (UE) 2021/1060 (voir src/extraction/
articles.py) : le marqueur "Art. X." n'est pas seul sur sa ligne, le
corps du texte enchaîne directement après ("Art. 1er. – Conformément
à..."), et il n'y a pas de titre d'article séparé. D'où un module dédié
plutôt qu'une généralisation d'articles.py sur la base d'un seul contre-
exemple (cf. issue de conception discutée en session).

Le marqueur est en gras (UniversLTStd-Bold), le corps en romain
(TimesLTStd-Roman) — même principe de détection par police que pour le
règlement UE, mais le test porte sur le début de ligne, pas sur la ligne
entière.
"""

import re
from dataclasses import dataclass

import pdfplumber

from extraction.articles import group_words_by_line

ARTICLE_BOLD_FONT = "KFCODB+UniversLTStd-Bold"
ARTICLE_HEADING_RE = re.compile(r"^Art\.\s*(\d+)(?:er)?\.\s*[–-]\s*(.*)$")
ANNEXE_MARKER_RE = re.compile(r"^ANNEXE$")


@dataclass
class DecretArticleHeading:
    page: int
    top: float
    numero: int
    reste_de_ligne: str


@dataclass
class DecretArticle:
    numero: int
    texte: str
    page_debut: int


def find_article_headings(pdf: pdfplumber.PDF) -> list[DecretArticleHeading]:
    """Repère les lignes "Art. X. – ..." du décret, par police du marqueur.

    Le marqueur doit être en gras — ça exclut toute mention de "article X"
    en minuscule dans une référence croisée (jamais capitalisée "Art."
    dans ce document).
    """
    headings = []
    for page_index, page in enumerate(pdf.pages):
        for top, text, fonts in group_words_by_line(page):
            match = ARTICLE_HEADING_RE.match(text.strip())
            if not match:
                continue
            if ARTICLE_BOLD_FONT not in fonts:
                continue
            headings.append(
                DecretArticleHeading(
                    page=page_index,
                    top=top,
                    numero=int(match.group(1)),
                    reste_de_ligne=match.group(2),
                )
            )
    return headings


def _find_annexe_start(pdf: pdfplumber.PDF) -> tuple[int, float] | None:
    """Position (page, top) du marqueur "ANNEXE", pour borner le dernier article."""
    for page_index, page in enumerate(pdf.pages):
        for top, text, _ in group_words_by_line(page):
            if ANNEXE_MARKER_RE.match(text.strip()):
                return (page_index, top)
    return None


def extract_articles(pdf_path: str) -> list[DecretArticle]:
    """Extrait les articles du décret : numéro et corps du texte.

    Le dernier article inclut, en fin de texte, les formules de
    signature ("Fait le 21 avril 2022...") qui précèdent l'annexe dans
    le document — imperfection mineure, non traitée ici (le contenu
    normatif reste correct, seul un bruit de fin de texte s'ajoute).
    """
    with pdfplumber.open(pdf_path) as pdf:
        headings = find_article_headings(pdf)
        annexe_start = _find_annexe_start(pdf)

        articles = []
        for i, heading in enumerate(headings):
            if i + 1 < len(headings):
                end_page, end_top = headings[i + 1].page, headings[i + 1].top
            elif annexe_start:
                end_page, end_top = annexe_start
            else:
                end_page, end_top = len(pdf.pages) - 1, float("inf")

            texte_lines = [heading.reste_de_ligne] if heading.reste_de_ligne else []
            for page_index in range(heading.page, end_page + 1):
                page = pdf.pages[page_index]
                for top, text, _ in group_words_by_line(page):
                    if page_index == heading.page and top <= heading.top:
                        continue
                    if page_index == end_page and top >= end_top:
                        continue
                    texte_lines.append(text)

            articles.append(
                DecretArticle(
                    numero=heading.numero,
                    texte=" ".join(texte_lines),
                    page_debut=heading.page,
                )
            )
        return articles
