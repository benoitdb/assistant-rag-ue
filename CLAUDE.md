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

Cadrage et choix de stack terminés (voir [ADR 0001](docs/decisions/0001-stack-technique-v1.md)
— pas de framework RAG, Qdrant Cloud, pdfplumber, Mistral pour embeddings et
génération, Streamlit sur Hugging Face Spaces). Aucun code écrit. Prochaine
étape : premier pipeline d'ingestion sur le Règlement (UE) 2021/1060.
Suivi détaillé des grandes étapes (cochables) : [docs/roadmap.md](docs/roadmap.md).

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
