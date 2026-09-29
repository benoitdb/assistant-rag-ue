# Assistant RAG réglementaire — fonds européens (Projet 5)

Instructions du projet, communes à tous les assistants de code (Claude Code,
Codex) — source unique. `CLAUDE.md` l'importe et ne garde que ce qui est propre
à Claude Code (hooks, skill).

## Pourquoi

Assistant documentaire qui répond en langage naturel sur la réglementation
des fonds européens de cohésion (FEDER, FSE+), pour l'aide à l'instruction
et à l'audit. Portfolio / démo, pas un outil de production.

Cadrage complet : [cadrage-projet5-rag-reglementaire.md](cadrage-projet5-rag-reglementaire.md)
— objectif, périmètre V1, corpus, architecture proposée, critères de succès,
risques. Ne pas dupliquer ce contenu ici ; le mettre à jour là-bas si le
cadrage évolue.

## État actuel

Pipeline RAG complet de bout en bout (voir [ADR 0001](docs/decisions/0001-stack-technique-v1.md)
et [ADR 0002](docs/decisions/0002-strategie-chunking.md)) : extraction,
chunking, indexation (278 chunks dans Qdrant Cloud), retrieval (rappel
100%) et génération (mistral-small-latest). Les deux exigences non
négociables du cadrage sont vérifiées automatiquement contre le vrai
modèle : citation exacte (9/9) et refus explicite hors-corpus (4/4) —
voir [issue #12](https://github.com/benoitdb/assistant-rag-ue/issues/12).
Projet fonctionnellement terminé. Interface Streamlit déployée sur
Hugging Face Spaces (SDK Docker, cf. issue #17) mais bloquée par un bug
de quota côté plateforme HF (issue #18, ticket support envoyé,
pas d'urgence à relancer). Suivi détaillé des grandes
étapes (cochables) : [docs/roadmap.md](docs/roadmap.md). Extensions
envisagées (nouvelles sources, pas commencées) :
[docs/roadmap-v2.md](docs/roadmap-v2.md).

**Point de vigilance** : le LLM de génération (Mistral free tier) doit être
testé en priorité contre les deux exigences non négociables ci-dessous —
voir le risque documenté dans l'ADR 0001.

## Quoi (repo map)

- `cadrage-projet5-rag-reglementaire.md` — document de cadrage de référence
- `docs/decisions/` — ADR (Architecture Decision Records), un fichier par
  décision structurante (ex. choix du vector store, stratégie de chunking)
- `docs/referentiel-reglementaire.md` — inventaire des textes du champ :
  référence, statut **daté**, source officielle. Savoir qu'un texte existe n'est
  pas décider de l'indexer : l'arbitrage d'ingestion se fait texte par texte
  (roadmap-v2). Chaque statut y est une photographie datée — le corriger suppose
  de le reconstater, pas de le supposer stable.
- `.claude/skills/ingerer-document/SKILL.md` — procédure complète d'ajout d'un
  document au corpus, dans l'ordre. Écrite comme skill Claude Code, elle se lit
  comme une procédure par tout outil. Elle écrit dans Qdrant et consomme du
  quota : ne jamais la dérouler sans demande explicite.

## Commandes

Environnement : `venv/` à la racine. Dépendances applicatives épinglées dans
`requirements.txt`, outillage de développement dans `requirements-dev.txt`
(c'est ce dernier qu'installe la CI). Variables requises dans `.env` (modèle
`.env.example`) : `QDRANT_URL`, `QDRANT_API_KEY`, `MISTRAL_API_KEY`.

- **Tests** : `venv/bin/python -m pytest -q` — 45 tests, ~2 min. Les 5 tests
  marqués `reseau` sont **exclus par défaut** (`addopts` du `pyproject.toml`).
- **Tests réseau** : `venv/bin/python -m pytest -q -m reseau` — **IMPORTANT** :
  ces 5 tests (dans `test_app.py`, `test_generation.py` et `test_retrieval.py`)
  appellent réellement l'API Mistral et Qdrant Cloud, consomment du quota et
  exigent le corpus déjà indexé. Ce sont eux qui vérifient les deux exigences
  non négociables du cadrage, donc **à lancer localement avant de fusionner une
  PR touchant le retrieval ou la génération** — la CI ne peut pas les exécuter.
  Un nouveau test appelant le réseau doit porter ce marqueur.
- **Lint et formatage** : `venv/bin/ruff check .` et `venv/bin/ruff format .`
  (config dans `pyproject.toml`). Les deux tournent en CI sur chaque PR.
- **Tests rapides** (35 tests, 7 s) : la suite ci-dessus moins `test_articles.py`
  et `test_guide_regional.py`, qui parsent des PDF et pèsent à eux seuls 80 % des
  140 s : `venv/bin/python -m pytest -q --ignore=tests/test_articles.py
  --ignore=tests/test_guide_regional.py`.
- **Tests lents** (10 tests, ~135 s) : `test_articles.py` et
  `test_guide_regional.py`, qui parsent des PDF :
  `venv/bin/python -m pytest -q tests/test_articles.py tests/test_guide_regional.py`.

Les deux lots se partagent la suite hors réseau **sans recouvrement** (35 + 10 =
45). La CI décide de la fusion.
- **Indexer le corpus** : `venv/bin/python scripts/index_corpus.py` (extraction →
  chunking → embeddings → indexation ; ré-indexer le même corpus fait un upsert,
  pas de doublon)
- **Lancer l'app** : `venv/bin/streamlit run app.py --server.port 8502`
  (8501 est occupé par le dashboard Cartographie FESI)
- **Déploiement** : `Dockerfile` (Hugging Face Spaces, SDK Docker, port 7860
  imposé par la plateforme — ne pas changer)

## Comment travailler ici

**Langue** : français dans le code (docs, commentaires, noms de variables
métier) comme dans les échanges, cohérent avec le cadrage.

**Exigences non négociables issues du cadrage** (§4-6) :
- Toute réponse générée doit citer sa source exacte (document + article/section)
- Cas hors-corpus → réponse explicite "je ne sais pas", jamais d'invention
- Ces deux points sont les critères de succès du POC : toute évolution du
  pipeline doit être testée contre eux avant d'être considérée terminée

**Tests** : un pipeline RAG se casse silencieusement (mauvais chunk récupéré,
citation fausse, hallucination) — les tests s'écrivent avec le code.
- Jeu de questions-réponses de référence (issu du cadrage §6) versionné dans
  le repo et exécuté comme suite de tests, pas comme vérification manuelle
  ponctuelle
- Tester séparément : extraction/chunking (déterministe, testable strictement),
  retrieval (mesurable par précision/rappel sur le jeu de questions),
  génération (nécessite les deux garde-fous ci-dessus)

**Décisions d'architecture** : ADR courtes dans `docs/decisions/` (contexte,
options, choix, pourquoi) — vector store, framework d'orchestration, stratégie de
chunking, hébergement.

**PR** : branches `feat/...`, `fix/...`. Une PR qui touche l'extraction, le
chunking, le retrieval ou la génération n'est pas prête à fusionner sans test
qui couvre le changement.

**Périmètre** : le cadrage fait foi. Un écart entre l'implémentation et le
cadrage est signalé (issue) et arbitré par l'utilisateur, jamais réglé en
silence, ni en retouchant le code ni en retouchant le cadrage.

**Sujets sensibles** : réglementation fonds européens = fiabilité critique.
Toujours positionner l'outil comme aide, jamais comme source faisant foi
(cf. cadrage §7).
