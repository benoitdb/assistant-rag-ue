# Roadmap — pipeline RAG (Projet 5)

Grandes étapes du pipeline, dans l'ordre où elles doivent fonctionner
pour obtenir un POC de bout en bout. Chaque étape est cochée une fois
livrée et testée (pas juste "commencée") — voir cadrage §6 pour les
critères de succès attendus à la fin. Détail des décisions et des
gotchas rencontrés en cours de route : [ADR](decisions/) et issues
GitHub sur `benoitdb/assistant-rag-ue`, pas dupliqué ici.

## 0. Cadrage

- [x] Document de cadrage (objectif, périmètre V1, corpus, critères de succès)
- [x] ADR 0001 — choix de stack technique (pas de framework RAG, Qdrant Cloud, pdfplumber, Mistral, Streamlit/HF Spaces)

## 1. Extraction

- [x] Récupérer le Règlement (UE) 2021/1060 en local (source EUR-Lex)
- [x] Valider la stratégie de détection des articles (police italique 9.6, plus robuste qu'une regex texte — [issue #1](https://github.com/benoitdb/assistant-rag-ue/issues/1))
- [ ] Décider du traitement des annexes à texte pivoté (52% du document, [issue #2](https://github.com/benoitdb/assistant-rag-ue/issues/2)) — bloquant tant que les annexes restent dans le périmètre
- [ ] Écrire le script d'extraction pour de vrai (`src/`) : texte + repérage structure (Titre/Chapitre/Article) sur le corps des articles
- [ ] Étendre au Décret n° 2022-608 et au guide régional choisi (corpus hétérogène, cf. cadrage §2)
- [ ] Tests d'extraction (déterministes — cf. CLAUDE.md "tester séparément")

## 2. Chunking

- [ ] ADR sur la stratégie de découpage précise (granularité par article, gestion des articles très longs/courts — prévu en fin d'ADR 0001)
- [ ] Implémentation + tests

## 3. Indexation (Qdrant)

- [ ] Setup Qdrant Cloud (free tier)
- [ ] Génération des embeddings (Mistral Embed)
- [ ] Script d'indexation + vérification (nombre de chunks, métadonnées de citation présentes)

## 4. Retrieval

- [ ] Requête vectorielle + reranking éventuel
- [ ] Mesure précision/rappel sur le jeu de questions de référence (cadrage §6, à versionner dans le repo)

## 5. Génération

- [ ] Prompt contraignant la citation exacte (document + article/section)
- [ ] Gestion explicite du hors-corpus ("je ne sais pas", jamais d'invention)
- [ ] Test contre les deux exigences non négociables (cadrage §4) — priorité haute, cf. risque noté dans l'ADR 0001 sur la fiabilité du LLM gratuit

## 6. Interface (Streamlit)

- [ ] Interface de question/réponse + affichage des citations sources
- [ ] Déploiement Hugging Face Spaces

---

**État actuel (2026-08-19)** : étape 1 en cours — stratégie de détection
des articles validée, mais deux limites du corpus source découvertes en
cours de route (voir issues #1 et #2) restent à trancher avant d'écrire
le code d'extraction définitif.
