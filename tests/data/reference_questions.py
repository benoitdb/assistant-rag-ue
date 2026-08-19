"""Jeu de questions de référence pour mesurer la précision du retrieval.

Cadrage §6 : "réponse correcte à un jeu de questions test, avec citation
exacte de la source" — chaque entrée associe une question en langage
naturel à l'unité (document + type + numéro) qui doit apparaître dans
les résultats du retrieval. Couvre les 3 documents du corpus V1.

Les questions sont écrites à partir du contenu réel des unités visées
(vérifié en lisant `Article.texte`/`Fiche.texte` extraits), pas
inventées à partir du seul titre — pour que le test mesure vraiment la
capacité du retrieval à faire le lien question -> bon passage.
"""

REFERENCE_QUESTIONS = [
    {
        "question": "Quel est l'objet du règlement (UE) 2021/1060 ?",
        "document": "reglement_ue_2021_1060",
        "type_unite": "reglement_article",
        "numero": 1,
    },
    {
        "question": "Comment le règlement encadre-t-il les corrections financières appliquées par les États membres ?",
        "document": "reglement_ue_2021_1060",
        "type_unite": "reglement_article",
        "numero": 103,
    },
    {
        "question": "Quels sont les principes applicables au dégagement d'office des crédits par la Commission ?",
        "document": "reglement_ue_2021_1060",
        "type_unite": "reglement_article",
        "numero": 105,
    },
    {
        "question": "La Commission peut-elle demander à un État membre de réviser ses programmes pour des motifs de gouvernance économique ?",
        "document": "reglement_ue_2021_1060",
        "type_unite": "reglement_article",
        "numero": 19,
    },
    {
        "question": "À quelle date le règlement (UE) 2021/1060 entre-t-il en vigueur ?",
        "document": "reglement_ue_2021_1060",
        "type_unite": "reglement_article",
        "numero": 119,
    },
    {
        "question": "Quelles sont les conditions générales pour qu'une dépense soit éligible selon le décret n° 2022-608 ?",
        "document": "decret_2022_608",
        "type_unite": "decret_article",
        "numero": 4,
    },
    {
        "question": "Quelles dépenses sont explicitement inéligibles selon le décret n° 2022-608 ?",
        "document": "decret_2022_608",
        "type_unite": "decret_article",
        "numero": 5,
    },
    {
        "question": "Quelles pièces justificatives doivent être présentées à l'autorité de gestion pour une opération ?",
        "document": "decret_2022_608",
        "type_unite": "decret_article",
        "numero": 7,
    },
    {
        "question": "Quelles dépenses de personnel sont éligibles selon le guide du porteur de projet Centre-Val de Loire ?",
        "document": "guide_regional_centre_val_de_loire",
        "type_unite": "fiche_guide",
        "numero": 6,
    },
]

# Questions volontairement hors du périmètre V1 (cadrage §1 : "hors périmètre
# explicite" — FEADER/FEAMPA hors volet cohésion, programmation 2014-2020,
# doctrine interne non publique), plus un cas totalement étranger au domaine.
# Sert à vérifier la deuxième exigence non négociable du cadrage (§4) : refus
# explicite plutôt qu'invention quand le corpus ne couvre pas la question —
# y compris sur des questions "proches" du corpus (mêmes mots-clés,
# réglementation européenne) où l'invention serait la plus tentante pour un LLM.
#
# Attention en ajoutant une question ici : elle doit être vraiment hors
# corpus, pas seulement formulée pour l'être. Une première version testait
# "la procédure interne de contrôle non publique de l'autorité de gestion" en
# pensant tester la doctrine interne — mais l'article 74 du règlement UE
# (dans le corpus) décrit précisément les "vérifications de gestion" de
# l'autorité de gestion, une procédure publique. Le modèle a donc, à raison,
# répondu à partir de cet article plutôt que de refuser (issue #14) —
# ce n'était pas un défaut du modèle, la question était mal calée.
HORS_CORPUS_QUESTIONS = [
    "Quels sont les taux de soutien du FEADER pour les exploitations agricoles ?",
    "Quelles étaient les règles d'éligibilité applicables à la programmation 2014-2020 ?",
    "Quelles consignes internes non publiées la Région Centre-Val de Loire donne-t-elle à ses agents instructeurs pour l'analyse des dossiers FEDER, en dehors du guide du porteur de projet ?",
    "Quelle est la capitale de la France ?",
]
