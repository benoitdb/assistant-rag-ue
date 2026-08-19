from dataclasses import dataclass

from chunking.chunker import LONG_UNIT_THRESHOLD, chunk_unit, chunk_units


def test_unite_courte_reste_un_seul_chunk():
    chunks = chunk_unit(
        document="reglement_ue_2021_1060",
        type_unite="reglement_article",
        numero=1,
        titre="Objet et champ d’application",
        texte="1. Le présent règlement arrête ses dispositions communes.",
        page_debut=0,
    )
    assert len(chunks) == 1
    assert chunks[0].texte == "1. Le présent règlement arrête ses dispositions communes."
    assert chunks[0].sous_section is None
    assert chunks[0].numero == 1
    assert chunks[0].titre == "Objet et champ d’application"


def test_unite_longue_decoupee_sur_la_numerotation_des_paragraphes():
    """Un article au-delà du seuil, avec plusieurs paragraphes numérotés
    ("1.", "2.", ...), doit être découpé un chunk par paragraphe — chaque
    sous-chunk garde le numéro/titre de l'article parent."""
    paragraphes = [f"{i}. " + ("x" * 2000) for i in range(1, 4)]
    texte = "\n".join(paragraphes)
    assert len(texte) > LONG_UNIT_THRESHOLD

    chunks = chunk_unit(
        document="reglement_ue_2021_1060",
        type_unite="reglement_article",
        numero=19,
        titre="Mesures établissant un lien...",
        texte=texte,
        page_debut=10,
    )

    assert len(chunks) == 3
    for i, chunk in enumerate(chunks, start=1):
        assert chunk.sous_section == i
        assert chunk.numero == 19
        assert chunk.titre == "Mesures établissant un lien..."
        assert chunk.texte.startswith(f"{i}. ")


def test_unite_longue_decoupee_sur_les_sous_sections_de_fiche():
    sous_sections = [f"{i} – SOUS-SECTION\n" + ("x" * 2000) for i in range(1, 3)]
    texte = "\n".join(sous_sections)
    assert len(texte) > LONG_UNIT_THRESHOLD

    chunks = chunk_unit(
        document="guide_regional_centre_val_de_loire",
        type_unite="fiche_guide",
        numero=6,
        titre="L'éligibilité des dépenses",
        texte=texte,
        page_debut=5,
    )

    assert len(chunks) == 2
    assert chunks[0].texte.startswith("1 – SOUS-SECTION")
    assert chunks[1].texte.startswith("2 – SOUS-SECTION")


def test_unite_longue_sans_marqueur_repli_par_lignes_sans_couper_une_ligne():
    """Aucun marqueur de numérotation détectable (texte non structuré) :
    le fallback doit tout de même découper le contenu, sans jamais
    couper une ligne en deux ni perdre de contenu."""
    lignes = [f"ligne {i} " + ("x" * 300) for i in range(20)]
    texte = "\n".join(lignes)
    assert len(texte) > LONG_UNIT_THRESHOLD

    chunks = chunk_unit(
        document="reglement_ue_2021_1060",
        type_unite="reglement_article",
        numero=42,
        titre="",
        texte=texte,
        page_debut=1,
    )

    assert len(chunks) > 1
    reconstitue = "\n".join(chunk.texte for chunk in chunks)
    assert reconstitue == texte
    for chunk in chunks:
        for ligne in chunk.texte.split("\n"):
            assert ligne in lignes


def test_chunk_units_gere_les_unites_sans_titre():
    """`DecretArticle` n'a pas d'attribut `titre` (voir src/extraction/decret.py)
    — chunk_units doit fonctionner sans lever d'erreur, titre="" par défaut."""

    @dataclass
    class FauxArticleDecret:
        numero: int
        texte: str
        page_debut: int

    units = [FauxArticleDecret(numero=1, texte="Texte court.", page_debut=0)]
    chunks = chunk_units("decret_2022_608", "decret_article", units)

    assert len(chunks) == 1
    assert chunks[0].titre == ""
    assert chunks[0].numero == 1
