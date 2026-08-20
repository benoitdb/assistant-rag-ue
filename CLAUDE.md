# Assistant RAG réglementaire — fonds européens (Projet 5)

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
- `.claude/skills/` — procédures répétées une fois qu'elles existent
  (ex. procédure d'ingestion d'un nouveau document, checklist de review)

Structure de code à ajouter au fur et à mesure (`src/`, `tests/`, etc.) —
ne pas préparer d'arborescence vide par anticipation.

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

**Qualité et TDD** :
- Un pipeline RAG se casse silencieusement (mauvais chunk récupéré, citation
  fausse, hallucination) — écrire les tests avant ou en même temps que le
  code, pas après
- Jeu de questions-réponses de référence (issu du cadrage §6) versionné dans
  le repo et exécuté comme suite de tests, pas comme vérification manuelle
  ponctuelle
- Tester séparément : extraction/chunking (déterministe, testable strictement),
  retrieval (mesurable par précision/rappel sur le jeu de questions),
  génération (nécessite les deux garde-fous ci-dessus)

**Décisions d'architecture** : toute décision structurante (vector store,
framework d'orchestration, stratégie de chunking, hébergement) va dans
`docs/decisions/` sous forme d'ADR courte (contexte, options, choix, pourquoi).
Ne pas laisser ces choix implicites dans le code ou dans une conversation.

**GitHub issues — AI-driven dev, pas du vibe-coding** : toute limitation
connue, gotcha, idée d'évolution, ou choix technique non trivial pris de
façon autonome (algorithme/lib retenu, seuil choisi, approche préférée à une
alternative) est loggé comme issue GitHub sur `benoitdb/assistant-rag-ue`
(ou commentaire sur une issue liée existante) — par défaut, sans attendre
que ça soit demandé. Objectif : que l'utilisateur reste le décideur qui peut
toujours expliquer et ré-arbitrer un choix plus tard (entretien, revue de
projet), pas qu'il découvre après coup ce qui a été fait. Un ADR documente
une décision d'architecture retenue ; une issue GitHub trace une piste
ouverte, une limite connue, ou un choix d'implémentation ponctuel.

**Branches et tests** : travail non trivial sur une branche dédiée
(`feat/...`, `fix/...`), fusionnée dans `main` via PR une fois les tests
concernés au vert — pas de commit direct sur `main` pour du code (les
corrections de doc/typo peuvent aller directement sur `main`). Une PR sans
test qui couvre le changement n'est pas prête à fusionner tant que le code
touche à l'extraction, au chunking, au retrieval ou à la génération.

**Documentation** : le cadrage reste la source de vérité sur le périmètre.
Si l'implémentation s'en écarte, mettre à jour le cadrage plutôt que de
laisser diverger code et doc.

**Sujets sensibles** : réglementation fonds européens = fiabilité critique.
Toujours positionner l'outil comme aide, jamais comme source faisant foi
(cf. cadrage §7).
