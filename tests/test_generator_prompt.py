from generation.generator import DOCUMENT_LABELS, format_context
from retrieval.retriever import RetrievedChunk


def make_chunk(**overrides):
    base = dict(
        document="reglement_ue_2021_1060",
        type_unite="reglement_article",
        numero=1,
        titre="Objet et champ d’application",
        sous_section=None,
        page_debut=0,
        texte="1. Le présent règlement arrête...",
        score=0.9,
    )
    base.update(overrides)
    return RetrievedChunk(**base)


def test_format_context_utilise_le_libelle_lisible_pas_l_id_technique():
    """L'identifiant technique snake_case (chunk.document) ne doit jamais
    apparaître tel quel dans le contexte envoyé au modèle — sinon le
    modèle le reformate spontanément dans sa citation (accents ajoutés),
    ce qui casse la vérification automatique de la citation exacte."""
    chunk = make_chunk(document="reglement_ue_2021_1060")
    context = format_context([chunk])
    assert "reglement_ue_2021_1060" not in context
    assert DOCUMENT_LABELS["reglement_ue_2021_1060"] in context


def test_format_context_distingue_article_et_fiche():
    article = make_chunk(type_unite="reglement_article", numero=1)
    fiche = make_chunk(
        document="guide_regional_centre_val_de_loire", type_unite="fiche_guide", numero=6
    )
    context = format_context([article, fiche])
    assert "Article 1" in context
    assert "Fiche 6" in context
