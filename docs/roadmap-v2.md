# Roadmap — V2 (extensions du corpus)

V1 terminée (voir [roadmap.md](roadmap.md)) : pipeline complet, 3
documents indexés, déploiement Streamlit/HF Spaces (bloqué par un bug
de quota côté plateforme, sans lien avec le code — voir issue #18).

Ce document liste les extensions envisagées par le cadrage §1
("Extensions envisageables en V2") sous forme actionnable, pas encore
planifiées dans le temps — pas de code commencé sur ce périmètre.

## 0. Sources identifiées mais pas encore acquises

Le statut et la source de chacun de ces documents sont tenus à jour dans
l'inventaire du référentiel réglementaire
([referentiel-reglementaire.md](referentiel-reglementaire.md), issue #21) —
cette section garde la trace de l'**arbitrage** (quoi acquérir, pourquoi),
l'inventaire porte les **faits** (référence exacte, statut daté, URL).

Trois documents apparaissent dans le tableau "Corpus et sources" du
cadrage (§2) mais étaient explicitement hors périmètre V1 (§1) :

- [ ] **Règlement (UE) 2021/1057** (FSE+) — complète le règlement
  2021/1060 déjà indexé ; à récupérer (EUR-Lex, comme le 2021/1060)
- [ ] **Guide administratif et financier FSE+ 2021-2027** — signalé au
  cadrage comme "mis à jour régulièrement" (dernière maj identifiée :
  juin 2026) : contrairement aux 3 documents V1 (stables), celui-ci
  demande un vrai mécanisme de rafraîchissement, pas juste une
  extraction ponctuelle (cf. §3 ci-dessous)
- [ ] **Guide ANCT instruments financiers** — vocabulaire proche du
  métier cible (auditeurs/gestionnaires), à récupérer

Plus, mentionnés au cadrage §1 sans document précis identifié :
- [ ] **D'autres guides régionaux** (au-delà de Centre-Val de Loire) —
  lesquels reste à décider
- [ ] **Notes internes**, "si accès obtenu" — dépend d'un accès non
  garanti, pas actionnable tant que cet accès n'existe pas
- [ ] **Programmation 2014-2020, à titre comparatif** — voir §4
  ci-dessous, implique une vraie décision de design, pas juste
  l'ajout d'un document

## 1. Extraction

- [ ] Pour chaque nouveau document : vérifier sa structure avant de
  coder — les 3 modules V1 (`articles.py`, `decret.py`,
  `guide_regional.py`) ont chacun une structure différente détectée
  par police/regex ; ne pas supposer qu'un nouveau document suit un
  motif déjà vu. Un module dédié par structure réelle, pas une
  généralisation anticipée (cf. `decret.py`, docstring).

## 2. Chunking

- [ ] `src/chunking/chunker.py` est déjà générique par rapport au type
  de document (`chunk_units(document, type_unite, units)` + une regex
  de numérotation par `type_unite` dans `MARKER_RE_BY_TYPE`) — ajouter
  une entrée dans ce dict pour chaque nouveau `type_unite`, pas de
  refonte du module attendue a priori
- [ ] Vérifier que le seuil `LONG_UNIT_THRESHOLD` (4000, cf. ADR 0002)
  reste pertinent sur la distribution de longueur des nouveaux
  documents avant de le réutiliser tel quel

## 3. Indexation

- [ ] `DOCUMENT_LABELS` (`src/generation/generator.py`) à étendre avec
  un libellé lisible par nouveau document (cf. issue #12 — sans ça, le
  modèle reformate l'identifiant technique dans ses citations)
- [ ] Décider : même collection Qdrant (`assistant_rag_ue`) ou
  collection séparée par version ? Le schéma d'id déterministe
  (`chunk_point_id`, issue #8) n'a pas de collision entre documents
  différents, donc rien ne force une collection séparée techniquement
  — à trancher plutôt sur un critère produit (veut-on pouvoir
  chercher V1-only vs. V1+V2 ?)
- [ ] **Mécanisme de rafraîchissement** pour le Guide administratif et
  financier FSE+ (seul document V2 identifié comme non stable) : pas
  conçu du tout actuellement — `scripts/index_corpus.py` suppose un
  corpus figé, aucune détection de version/date de mise à jour ni de
  ré-indexation différentielle

## 4. Retrieval / génération

- [ ] Étendre `tests/data/reference_questions.py` avec des questions
  couvrant chaque nouveau document (même principe qu'en V1 : ancrées
  sur le contenu réel, pas seulement le titre)
- [ ] **Décision de design à trancher avant de coder** : la
  programmation 2014-2020 "à titre comparatif" est aujourd'hui
  explicitement hors-corpus (le système refuse, cadrage §1 + testé en
  V1, cf. `HORS_CORPUS_QUESTIONS`). L'ajouter en V2 change la nature du
  refus hors-corpus : il faudra soit un mode de réponse comparatif
  explicite (2014-2020 vs 2021-2027, avec citation des deux corpus),
  soit garder le refus par défaut et n'activer la comparaison que sur
  demande explicite de l'utilisateur — sans clarifier ça, on risque de
  casser silencieusement l'exigence non négociable actuelle (refus
  hors-corpus, cadrage §4) en élargissant simplement le corpus indexé

## Hors scope V2 (pas mentionné au cadrage, à ne pas ajouter par anticipation)

FEADER/FEAMPA hors volet cohésion — explicitement hors périmètre même
en V2 selon le cadrage §1 ("hors périmètre explicite").
