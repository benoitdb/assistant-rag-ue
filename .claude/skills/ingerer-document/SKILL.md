---
name: ingerer-document
description: Ajouter un document au corpus RAG — extraction, chunking, indexation Qdrant, questions de référence et vérification des deux exigences non négociables. Procédure complète, dans l'ordre.
disable-model-invocation: true
---

# Ingérer un nouveau document dans le corpus

Procédure complète pour ajouter un document au corpus interrogeable. Chaque
étape référence le code réel — vérifier ces emplacements plutôt que supposer.

**Invocation manuelle uniquement** (`/ingerer-document`) : cette procédure écrit
dans Qdrant Cloud et consomme du quota Mistral. Elle ne doit pas se déclencher
d'elle-même.

## 0. Avant de commencer : ce document doit-il être ingéré ?

L'ingestion n'est pas automatique parce qu'un document existe. Le corpus est
arbitré **texte par texte** — voir
[issue #21](https://github.com/benoitdb/assistant-rag-ue/issues/21). Vérifier :

- Le document est-il dans le périmètre du cadrage (§1-2) ? Les extensions V2
  identifiées sont listées dans [`docs/roadmap-v2.md`](../../../docs/roadmap-v2.md) §0.
- Est-il **stable** ? Un document « mis à jour régulièrement » (ex. Guide
  administratif et financier FSE+) demande un mécanisme de rafraîchissement qui
  **n'existe pas** : `scripts/index_corpus.py` suppose un corpus figé, sans
  détection de version ni ré-indexation différentielle (roadmap-v2 §3).
  Ingérer un document mouvant sans ça, c'est servir du périmé en silence.

Si le document sort du périmètre, s'arrêter ici et le signaler.

## 1. Choisir l'identifiant, poser le PDF

L'identifiant du document (`reglement_ue_2021_1060`, `decret_2022_608`…) est une
**clé qui doit être identique partout** : nom du fichier PDF, `DOCUMENT_LABELS`,
`reference_questions.py`, payload des chunks. Une divergence casse la citation
sans lever d'erreur.

Poser le PDF dans `docs/sources/<identifiant>.pdf`.

⚠️ `docs/sources/` **est versionné** dans ce dépôt (contrairement à FESI) — les
tests hors réseau en dépendent, et la CI aussi.

## 2. Inspecter la structure AVANT d'écrire du code

C'est l'étape qu'on est tenté de sauter, et c'est celle qui coûte le plus cher
si on la saute.

Les trois modules d'extraction existants ont chacun une logique **différente**,
parce que les documents ont des structures différentes :

| Module | Document | Détection |
|---|---|---|
| `src/extraction/articles.py` | Règlement UE | police `EUAlbertina-ReguItal` + regex |
| `src/extraction/decret.py` | Décret | regex sur le texte |
| `src/extraction/guide_regional.py` | Guide régional | fiches, structure propre |

Ouvrir le PDF avec `pdfplumber`, regarder les polices et la mise en page réelles
des titres. **Ne pas supposer qu'un nouveau document suit un motif déjà vu**
(cf. docstring de `decret.py`).

Deux pièges déjà rencontrés, à vérifier systématiquement :

- **Texte pivoté à 90°** — l'Annexe VI du règlement était illisible
  ([issue #2](https://github.com/benoitdb/assistant-rag-ue/issues/2)),
  voir `src/extraction/rotated_tables.py`.
- **La dernière unité qui absorbe la suite** — l'article 119 engloutissait tout
  le texte des annexes faute de borne
  ([issue #6](https://github.com/benoitdb/assistant-rag-ue/issues/6)). Toujours
  vérifier ce qui **borne** la dernière unité.

## 3. Écrire le module d'extraction, avec ses tests

Un module dédié par structure réelle dans `src/extraction/`. **Pas de
généralisation par anticipation** : factoriser seulement quand deux documents
partagent réellement une structure.

Les tests d'extraction sont **déterministes et hors réseau** — les écrire en même
temps que le code, pas après (règle TDD du `CLAUDE.md`). Ajouter le chemin du PDF
dans `tests/conftest.py` à côté des trois existants.

⚠️ Un test qui parse un PDF est **lent** (`test_articles.py` : 113 s à lui seul).
Si le nouveau test dépasse quelques secondes, l'ajouter à la liste de
`.claude/hooks/tests-lents.sh` et le retirer de `tests-rapides.sh`, pour garder
le hook bloquant sous le seuil de perception.

## 4. Chunking : une entrée, pas une refonte

`src/chunking/chunker.py` est déjà générique par type de document. Ajouter une
entrée dans `MARKER_RE_BY_TYPE` pour le nouveau `type_unite` — une regex de
découpage secondaire, utilisée seulement pour les unités dépassant
`LONG_UNIT_THRESHOLD` (4000, cf. ADR 0002).

**Vérifier que le seuil reste pertinent** sur la distribution de longueur réelle
du nouveau document avant de le réutiliser tel quel. Un document aux unités
courtes ne déclenchera jamais le découpage ; un document aux unités très longues
produira des chunks trop gros pour un retrieval précis.

## 5. Libellé lisible — sinon les citations sont fausses

Ajouter une entrée dans `DOCUMENT_LABELS` (`src/generation/generator.py`).

Ce n'est pas cosmétique : sans libellé, le modèle **reformate l'identifiant
technique à sa façon** dans ses citations, et l'exigence de citation exacte tombe
([issue #12](https://github.com/benoitdb/assistant-rag-ue/issues/12)).

## 6. Brancher dans le pipeline d'indexation

Dans `scripts/index_corpus.py`, `build_corpus_chunks()` : importer l'extracteur
et ajouter un `chunk_units("<identifiant>", "<type_unite>", <unités>)` à la
concaténation.

## 7. Questions de référence — ancrées sur le contenu réel

Étendre `tests/data/reference_questions.py` avec des questions couvrant le
nouveau document. Chaque entrée associe une question en langage naturel à
l'unité (`document`, `type_unite`, `numero`) qui doit remonter.

**Écrire les questions en lisant le texte extrait**, pas à partir du titre de
l'unité — sinon le test mesure la correspondance de titres, pas la capacité du
retrieval à relier une question à un passage.

Si le document élargit le corpus vers un domaine jusque-là hors-corpus, revoir
`HORS_CORPUS_QUESTIONS` : élargir le corpus **change la frontière du refus**, et
peut casser silencieusement l'exigence de refus hors-corpus (roadmap-v2 §4).

## 8. Indexer

```
venv/bin/python scripts/index_corpus.py
```

Le script vérifie lui-même que le nombre de points indexés correspond au nombre
de chunks produits et que chaque chunk porte ses métadonnées de citation.

Ré-indexer le même corpus fait un **upsert** (id déterministe UUID5,
[issue #8](https://github.com/benoitdb/assistant-rag-ue/issues/8)) — pas de
doublon, on peut relancer sans nettoyer.

## 9. Vérifier les deux exigences non négociables

```
venv/bin/python -m pytest -q            # 45 tests hors réseau
venv/bin/python -m pytest -q -m reseau  # citation exacte + refus hors-corpus
```

⚠️ Les tests `reseau` appellent réellement Mistral et Qdrant et consomment du
quota free tier. **Ce sont eux qui valident le travail** : un document ingéré
dont les citations sont fausses n'est pas ingéré, il est nuisible.

Tant que ces deux tests ne passent pas, l'ingestion n'est pas terminée.

## 10. Mettre la documentation à jour

- `CLAUDE.md`, section « État actuel » : nombre de chunks indexés, liste du corpus
- `docs/roadmap-v2.md` §0 : cocher le document acquis
- Le cadrage si le périmètre a bougé — c'est lui la source de vérité
- Une issue GitHub pour tout choix non trivial pris en chemin (seuil, découpage,
  approche d'extraction retenue contre une alternative)

## Checklist

- [ ] Document dans le périmètre, et **stable**
- [ ] Identifiant identique partout
- [ ] PDF dans `docs/sources/`
- [ ] Structure inspectée avant d'écrire du code
- [ ] Module d'extraction + tests déterministes
- [ ] Test lent ? → basculé dans `tests-lents.sh`
- [ ] Entrée dans `MARKER_RE_BY_TYPE`, seuil vérifié
- [ ] Entrée dans `DOCUMENT_LABELS`
- [ ] Branché dans `build_corpus_chunks()`
- [ ] Questions de référence écrites depuis le texte extrait
- [ ] `HORS_CORPUS_QUESTIONS` revu si la frontière bouge
- [ ] Indexation lancée et vérifiée
- [ ] `pytest -m reseau` au vert
- [ ] Documentation et issues à jour
