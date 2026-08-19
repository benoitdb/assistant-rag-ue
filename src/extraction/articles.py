"""Extraction des articles du Règlement (UE) 2021/1060 depuis le PDF.

Stratégie validée par exploration (voir issue #1 sur benoitdb/assistant-rag-ue) :
les titres "Article X" sont repérables de façon fiable par leur police
(italique, taille 9.6), pas par une regex sur le texte seul — le texte
source contient au moins une coquille ("Articles 105" au pluriel) qu'une
regex stricte manquerait.
"""

import re
from dataclasses import dataclass

import pdfplumber

ARTICLE_FONT = "EUAlbertina-ReguItal"
ARTICLE_FONT_SIZE = 9.6
ARTICLE_HEADING_RE = re.compile(r"^Articles?\s+(premier|\d+)$")


@dataclass
class ArticleHeading:
    page: int
    top: float
    numero: int


@dataclass
class Article:
    numero: int
    titre: str
    texte: str
    page_debut: int


def _group_words_by_line(page):
    """Regroupe les mots d'une page par ligne (position verticale arrondie).

    Retourne une liste de (top, texte_ligne, {polices utilisées}) triée
    par position sur la page.
    """
    words = page.extract_words(extra_attrs=["fontname", "size"])
    lines = {}
    for w in words:
        key = round(w["top"], 1)
        lines.setdefault(key, []).append(w)
    result = []
    for top, line_words in lines.items():
        text = " ".join(w["text"] for w in line_words)
        fonts = {w["fontname"] for w in line_words}
        result.append((top, text, fonts))
    return sorted(result, key=lambda item: item[0])


def find_article_headings(pdf: pdfplumber.PDF) -> list[ArticleHeading]:
    """Repère toutes les lignes "Article X" du document, par police.

    Une ligne est retenue seulement si tous ses mots sont dans la police
    et la taille attendues (ARTICLE_FONT / ARTICLE_FONT_SIZE) — ça exclut
    les mentions de "Article X" dans la table des matières (police
    différente) ou en corps de texte (référence croisée à un autre
    article, jamais seule sur sa ligne dans ce cas).
    """
    headings = []
    for page_index, page in enumerate(pdf.pages):
        for top, text, fonts in _group_words_by_line(page):
            match = ARTICLE_HEADING_RE.match(text.strip())
            if not match:
                continue
            if fonts != {ARTICLE_FONT}:
                continue
            raw_numero = match.group(1)
            numero = 1 if raw_numero == "premier" else int(raw_numero)
            headings.append(ArticleHeading(page=page_index, top=top, numero=numero))
    return headings


def _is_header_noise(line_text: str) -> bool:
    """Ligne d'en-tête de page répétée (numéro de page, "Journal officiel...").

    Le mot "Journal" survit même quand le reste de la ligne est corrompu
    par un problème d'encodage du PDF (cf. issue #2) — filtre robuste aux
    deux cas.
    """
    return "Journal" in line_text


def _collect_lines_between(
    pdf: pdfplumber.PDF, start: ArticleHeading, end: ArticleHeading | None
) -> list[tuple[int, float, str, set]]:
    """Toutes les lignes du document entre deux frontières d'article (bornes incluses)."""
    end_page = end.page if end else len(pdf.pages) - 1
    end_top = end.top if end else float("inf")

    collected = []
    for page_index in range(start.page, end_page + 1):
        page = pdf.pages[page_index]
        for top, text, fonts in _group_words_by_line(page):
            if page_index == start.page and top < start.top:
                continue
            if page_index == end_page and top >= end_top:
                continue
            if _is_header_noise(text):
                continue
            collected.append((page_index, top, text, fonts))
    return collected


def extract_articles(pdf_path: str) -> list[Article]:
    """Extrait tous les articles du règlement : numéro, titre, corps du texte.

    Le titre est la première ligne suivant l'en-tête "Article X" (police
    grasse, EUAlbertina-Bold) ; tout le reste jusqu'à l'article suivant
    est le corps.
    """
    with pdfplumber.open(pdf_path) as pdf:
        headings = find_article_headings(pdf)
        articles = []
        for i, heading in enumerate(headings):
            next_heading = headings[i + 1] if i + 1 < len(headings) else None
            lines = _collect_lines_between(pdf, heading, next_heading)

            # la ligne "Article X" elle-même est la première ligne collectée
            body_lines = lines[1:]
            titre = ""
            texte_lines = []
            if body_lines:
                titre = body_lines[0][2]
                texte_lines = [text for _, _, text, _ in body_lines[1:]]

            articles.append(
                Article(
                    numero=heading.numero,
                    titre=titre,
                    texte="\n".join(texte_lines),
                    page_debut=heading.page,
                )
            )
        return articles
