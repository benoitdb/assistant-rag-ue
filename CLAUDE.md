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

## Directives comportementales générales

Behavioral guidelines to reduce common LLM coding mistakes. Merge with
project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For
trivial tasks, use judgment.

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If
yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make
it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in
diffs, fewer rewrites due to overcomplication, and clarifying questions
come before implementation rather than after mistakes.
