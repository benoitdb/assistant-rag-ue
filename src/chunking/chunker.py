"""Découpage des unités extraites (articles, fiches) en chunks pour l'indexation.

Stratégie validée dans l'ADR 0002 : une unité extraite (article du
règlement/décret, fiche du guide régional) reste un chunk unique en
dessous du seuil `LONG_UNIT_THRESHOLD`. Au-delà, découpage sur la
numérotation interne propre au type de document (paragraphes "1." dans
un article, sous-sections "1 –" dans une fiche), avec repli par
regroupement de lignes si moins de deux marqueurs sont trouvés — pour
ne pas planter sur une structure non anticipée.

Un sous-chunk garde toujours le numéro/titre de l'unité parente en
métadonnée : la citation générée reste au niveau de l'article ou de la
fiche, jamais un numéro de fragment interne.
"""

import re
from dataclasses import dataclass

LONG_UNIT_THRESHOLD = 4000

ARTICLE_PARAGRAPH_RE = re.compile(r"^\d+\.\s")
FICHE_SUBSECTION_RE = re.compile(r"^\d+\s*[–-]\s")

MARKER_RE_BY_TYPE = {
    "reglement_article": ARTICLE_PARAGRAPH_RE,
    "decret_article": ARTICLE_PARAGRAPH_RE,
    "fiche_guide": FICHE_SUBSECTION_RE,
}


@dataclass
class Chunk:
    document: str
    type_unite: str
    numero: int
    titre: str
    texte: str
    page_debut: int
    sous_section: int | None = None


def _split_on_markers(lines: list[str], marker_re: re.Pattern) -> list[list[str]] | None:
    """Découpe une liste de lignes aux lignes qui matchent marker_re.

    Retourne None si moins de deux marqueurs sont trouvés : un seul
    marqueur ne permet pas de découper (tout le texte resterait dans un
    seul groupe), il faut alors passer par le fallback.
    """
    marker_indices = [i for i, line in enumerate(lines) if marker_re.match(line.strip())]
    if len(marker_indices) < 2:
        return None

    groups = []
    for i, start in enumerate(marker_indices):
        end = marker_indices[i + 1] if i + 1 < len(marker_indices) else len(lines)
        groups.append(lines[start:end])

    # les lignes avant le premier marqueur (préambule) sont rattachées au premier groupe
    if marker_indices[0] > 0:
        groups[0] = lines[: marker_indices[0]] + groups[0]
    return groups


def _split_by_line_count(lines: list[str], threshold: int) -> list[list[str]]:
    """Fallback : regroupe les lignes en blocs de taille proche du seuil.

    Ne coupe jamais une ligne en deux — l'unité de découpage est la ligne
    physique déjà produite par l'extraction, pas le caractère.
    """
    groups: list[list[str]] = []
    current: list[str] = []
    current_len = 0
    for line in lines:
        if current and current_len + len(line) > threshold:
            groups.append(current)
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + 1
    if current:
        groups.append(current)
    return groups


def chunk_unit(
    document: str,
    type_unite: str,
    numero: int,
    titre: str,
    texte: str,
    page_debut: int,
) -> list[Chunk]:
    """Découpe une unité extraite en un ou plusieurs chunks.

    `type_unite` détermine la regex de numérotation interne utilisée pour
    le découpage secondaire (voir `MARKER_RE_BY_TYPE`).
    """
    if len(texte) <= LONG_UNIT_THRESHOLD:
        return [Chunk(document, type_unite, numero, titre, texte, page_debut)]

    marker_re = MARKER_RE_BY_TYPE[type_unite]
    lines = texte.split("\n")
    groups = _split_on_markers(lines, marker_re) or _split_by_line_count(
        lines, LONG_UNIT_THRESHOLD
    )

    return [
        Chunk(
            document=document,
            type_unite=type_unite,
            numero=numero,
            titre=titre,
            texte="\n".join(group),
            page_debut=page_debut,
            sous_section=i + 1,
        )
        for i, group in enumerate(groups)
    ]


def chunk_units(document: str, type_unite: str, units: list) -> list[Chunk]:
    """Découpe une liste d'unités extraites (articles ou fiches) en chunks.

    `units` : objets avec attributs `numero`, `texte`, `page_debut`
    (produits par `src/extraction/*.py`) — `titre` est optionnel, absent
    sur `DecretArticle`.
    """
    chunks = []
    for unit in units:
        chunks.extend(
            chunk_unit(
                document=document,
                type_unite=type_unite,
                numero=unit.numero,
                titre=getattr(unit, "titre", ""),
                texte=unit.texte,
                page_debut=unit.page_debut,
            )
        )
    return chunks
