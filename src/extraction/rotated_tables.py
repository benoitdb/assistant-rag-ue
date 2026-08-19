"""Reconstruction du texte des tableaux pivotés (annexes du règlement).

Beaucoup d'annexes du Règlement (UE) 2021/1060 sont des tableaux larges
dont le texte est pivoté à 90° dans le PDF (52% des pages du document,
voir issue #2 sur benoitdb/assistant-rag-ue). L'extraction naïve
(`page.extract_text()`) produit du texte inversé et illisible.

Approche validée par exploration :
1. `page.find_tables()` repère les cellules via les traits du PDF —
   indépendant de la rotation du texte à l'intérieur.
2. Pour chaque cellule, on regroupe ses caractères par colonne (x0) et on
   trie chaque colonne par position verticale (`top`) DÉCROISSANTE — sens
   déduit de la matrice de transformation des caractères pivotés
   (`(0, +b, -c, 0, ...)`, rotation +90°, vérifié sur 100% des ~200 000
   caractères pivotés du document, aucune exception).

Le sens de rotation (+90°, jamais -90°) est donc codé en dur : coder une
détection dynamique du signe ajouterait de la complexité pour un cas qui
ne s'est jamais présenté dans ce document.
"""

from collections import defaultdict

import pdfplumber

ROTATED_PAGE_THRESHOLD = 0.3


def is_rotated_page(page: pdfplumber.page.Page) -> bool:
    """Une page où la majorité du texte est pivoté (tableau en rotation)."""
    chars = page.chars
    if not chars:
        return False
    n_rotated = sum(1 for c in chars if not c["upright"])
    return (n_rotated / len(chars)) > ROTATED_PAGE_THRESHOLD


def reconstruct_rotated_cell(chars: list) -> str:
    """Reconstruit le texte d'une cellule de tableau en texte pivoté +90°.

    Regroupe les caractères par colonne (x0 arrondi) puis trie chaque
    colonne par `top` décroissant — l'axe de lecture réel du texte pivoté.
    Plusieurs colonnes dans une même cellule (rare) sont jointes par " | ".
    """
    if not chars:
        return ""
    columns = defaultdict(list)
    for c in chars:
        columns[round(c["x0"], 1)].append(c)
    lines = []
    for x0 in sorted(columns):
        column_chars = sorted(columns[x0], key=lambda c: -c["top"])
        lines.append("".join(c["text"] for c in column_chars))
    return " | ".join(lines)


def extract_rotated_tables_from_page(page: pdfplumber.page.Page) -> list[list[list[str]]]:
    """Toutes les tables d'une page pivotée, reconstruites cellule par cellule.

    Retourne une liste de tables ; chaque table est une liste de lignes ;
    chaque ligne est une liste de textes de cellule (None -> chaîne vide
    pour une cellule fusionnée/absente).
    """
    tables = []
    for table in page.find_tables():
        rows_out = []
        for row in table.rows:
            cells_out = []
            for cell_bbox in row.cells:
                if cell_bbox is None:
                    cells_out.append("")
                    continue
                cropped = page.crop(cell_bbox)
                cells_out.append(reconstruct_rotated_cell(cropped.chars))
            rows_out.append(cells_out)
        tables.append(rows_out)
    return tables
