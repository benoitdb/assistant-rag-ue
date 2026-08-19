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

- [x] Récupérer le Règlement (UE) 2021/1060 en local (source EUR-Lex, committé dans `docs/sources/`)
- [x] Valider la stratégie de détection des articles (police italique 9.6, plus robuste qu'une regex texte — [issue #1](https://github.com/benoitdb/assistant-rag-ue/issues/1))
- [x] Extraction des 119 articles (`src/extraction/articles.py`, 5 tests, corps multi-pages géré, en-têtes de page filtrés)
- [x] Valider et intégrer la reconstruction du texte pivoté des annexes (`src/extraction/rotated_tables.py`, 4 tests — cellule par cellule via `find_tables()` + tri par police/rotation, [issue #2](https://github.com/benoitdb/assistant-rag-ue/issues/2))
- [x] Attribuer chaque tableau reconstruit à son annexe précise (`src/extraction/annexes.py`, 5 tests — titre droit ou pivoté selon l'annexe, [issue #3](https://github.com/benoitdb/assistant-rag-ue/issues/3))
- [x] Récupérer le Décret n° 2022-608 (Légifrance bloque le scraping automatisé — Cloudflare — téléchargement manuel, committé dans `docs/sources/`)
- [x] Extraction des 10 articles du décret (`src/extraction/decret.py`, 5 tests — structure différente du règlement UE, module dédié plutôt qu'une généralisation prématurée ; a révélé un bug dans `group_words_by_line` partagée, corrigé, [issue #4](https://github.com/benoitdb/assistant-rag-ue/issues/4))
- [x] Récupérer et extraire le guide régional Centre-Val de Loire (`src/extraction/guide_regional.py`, 4 tests — structure en "FICHE N°X", troisième type de document du corpus, aucun piège de mise en page détecté)

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

**État actuel (2026-08-19)** : étape 1 terminée — les 3 documents du
corpus V1 (règlement UE, décret, guide régional Centre-Val de Loire)
sont extraits et testés (23 tests). Prochaine étape : chunking (étape 2).
