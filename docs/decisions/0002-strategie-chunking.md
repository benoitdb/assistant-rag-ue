# ADR 0002 — Stratégie de chunking V1

Date : 2026-08-19
Statut : Retenu

## Contexte

L'ADR 0001 renvoyait le choix de la stratégie de chunking à une fois
l'extraction testée (cadrage §3 : "par unité logique plutôt que par
taille fixe, pour ne pas couper une règle en deux"). L'extraction est
terminée sur les 3 documents du corpus V1 : 119 articles (règlement UE),
10 articles (décret), 10 fiches (guide régional Centre-Val de Loire).

Mesure de la distribution réelle des unités extraites (longueur en
caractères) :

| Document | n | médiane | min | max | remarque |
|---|---|---|---|---|---|
| Règlement UE 2021/1060 | 119 | 1 670 | 144 | 484 383 | l'outlier (article 119) est un artefact d'extraction, pas un vrai article long — voir plus bas |
| Décret n° 2022-608 | 10 | ~1 000 | 632 | 1 552 | tous courts, aucun cas limite |
| Guide régional CVL (fiches) | 10 | ~6 500 | 2 649 | 26 814 | plusieurs fiches nettement plus longues qu'un article |

## Décisions

### 1. Granularité de base : une unité extraite = un chunk

Un chunk correspond par défaut à un article (règlement, décret) ou une
fiche (guide régional), pas à une taille fixe de caractères — conforme
au cadrage. Ça garantit qu'une citation générée pointe toujours vers une
unité juridique/pédagogique complète et non ambiguë (document +
numéro), l'exigence non négociable du cadrage §4.

Les unités courtes (12 articles du règlement UE < 500 caractères) ne
sont **pas** fusionnées avec leurs voisines : la densité d'embedding
d'un chunk minuscule est un problème mineur d'optimisation retrieval,
alors que fusionner deux articles casserait la correspondance 1:1
chunk ↔ citation exacte, qui est le critère de succès du POC.

### 2. Unités longues : découpage secondaire sur la numérotation interne

Au-delà d'un seuil de **4 000 caractères**, une unité est découpée en
sous-chunks sur ses marqueurs de numérotation interne plutôt que sur
une taille de caractères arbitraire :
- Articles (règlement/décret) : paragraphes numérotés en tête de ligne
  (`^\d+\.`), motif déjà présent et cohérent dans le corpus (ex.
  article 19, vu en exploration).
- Fiches (guide régional) : sous-sections numérotées (`^\d+\s*[–-]`),
  motif déjà utilisé pour les titres de fiches eux-mêmes (voir
  `guide_regional.py`).

Seuil choisi à 4 000 caractères plutôt que plus bas : la médiane des
articles du règlement UE est 1 670 caractères, donc un seuil plus
agressif découperait inutilement une large part du corpus sans gain de
précision retrieval. Seuls les vrais cas longs (fiche 6 du guide
régional, 26 814 caractères ; quelques articles isolés du règlement)
sont concernés.

**Fallback si aucun marqueur de numérotation n'est détecté** : découpage
par regroupement de lignes (l'unité déjà produite par l'extraction, une
ligne physique du PDF par élément de `texte.split("\n")"), en visant des
sous-chunks proches du seuil sans jamais couper une ligne en deux — pas
de paragraphes séparés par ligne vide dans le format produit par
l'extraction (`"\n".join(texte_lines)` sans ligne vide entre lignes),
donc pas de découpage sur ce motif. Pour ne pas planter sur une
structure non anticipée plutôt que de supposer que tout le corpus suit
un motif de numérotation — cohérent avec l'approche déjà suivie en
extraction (un module dédié par structure de document plutôt qu'une
généralisation prématurée).

Un sous-chunk garde en métadonnée le numéro/titre de l'unité parente
(article ou fiche) : la citation générée reste au niveau de l'unité
("Article 19", "FICHE N°6"), jamais un numéro de fragment interne qui
n'a pas de sens pour l'utilisateur final.

### 3. Correction préalable requise : article 119 du règlement UE

L'article 119 ("Entrée en vigueur") est actuellement mesuré à 484 383
caractères car son extraction (`articles.py`) n'a pas de heading
suivant pour le borner et engloutit tout le texte des annexes qui le
suit dans le PDF — annexes déjà extraites séparément et attribuées par
`annexes.py`/`rotated_tables.py`. Sans correction, le seuil de 4 000
caractères déclencherait un découpage sur du contenu non pertinent
(mélange article + 25 annexes), avec un vrai risque de pollution du
retrieval. Documenté en détail dans
[issue #6](https://github.com/benoitdb/assistant-rag-ue/issues/6) — à
corriger dans `articles.py` avant/pendant l'implémentation du chunking,
pas contourné dans le module de chunking lui-même (la correction est du
ressort de l'extraction, pas du chunking).

### 4. Hors scope V1 : chunking des annexes

Les annexes du règlement UE (tableaux reconstruits, cf. `annexes.py`,
`rotated_tables.py`) ne sont pas encore assemblées en unités citables
complètes (pas d'équivalent `extract_annexes()` retournant des objets
par annexe, seulement des briques page par page). Le chunking V1 porte
donc uniquement sur les articles et fiches. Chunking des annexes
explicitement laissé en dehors de cette itération — à reprendre une
fois un besoin business identifié dessus (le cadrage ne les mentionne
pas comme prioritaires), pas anticipé ici.

### 5. Schéma de métadonnées par chunk

Chaque chunk porte : document source, type d'unité (article règlement /
article décret / fiche guide), numéro, titre (si présent), sous-section
(si découpage secondaire), page de début, texte. Ce schéma est ce qui
permet de respecter l'exigence de citation exacte (cadrage §4) au
moment de la génération — porté par le chunk lui-même plutôt que
reconstruit après coup au moment du retrieval.

## Conséquences

- Un module de chunking par famille de structure n'est pas nécessaire :
  contrairement à l'extraction, la logique de découpage secondaire
  (seuil + regex de numérotation + fallback paragraphe) est la même
  pour les 3 types d'unités, seule la regex de numérotation change en
  paramètre.
- Tests à écrire séparément pour : le seuil de déclenchement (unité
  courte = 1 chunk, longue = plusieurs), la préservation des
  métadonnées de citation sur les sous-chunks, et le fallback
  paragraphe sur une unité longue sans numérotation détectable.
