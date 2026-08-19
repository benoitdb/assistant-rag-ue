# Document de cadrage – Assistant RAG réglementaire fonds européens (Projet 5)

## 1. Objectif et périmètre

- **Objectif** : assistant documentaire permettant d'interroger en langage naturel la réglementation des fonds européens de cohésion (FEDER, FSE+), dans une logique d'aide à l'instruction et à l'audit.
- **Périmètre V1** (volontairement restreint) :
  - Règlement (UE) 2021/1060 portant dispositions communes (FEDER, FSE+, Fonds de cohésion, FTJ, FEAMPA)
  - Décret national n° 2022-608 du 21 avril 2022 (règles nationales d'éligibilité des dépenses 2021-2027)
  - Un seul guide régional, à choisir, pour tester le pipeline sur un contenu plus opérationnel/pédagogique
- **Hors périmètre explicite** (V1) : FEADER/FEAMPA hors volet cohésion, programmation 2014-2020, doctrine interne non publique.
- **Extensions envisageables en V2** : élargissement à d'autres guides régionaux, notes internes (si accès obtenu), programmation 2014-2020 à titre comparatif.

## 2. Corpus et sources

| Document | Niveau | Format | Remarque |
|---|---|---|---|
| Règlement (UE) 2021/1060 | UE | PDF/HTML | Texte juridique stable, articles numérotés |
| Règlement (UE) 2021/1057 (FSE+) | UE | PDF/HTML | Complète le précédent |
| Décret n° 2022-608 | National | PDF | Règles nationales d'éligibilité — PDF officiel disponible sur Légifrance (262 Ko, 10 articles + annexe), mais Légifrance bloque le scraping automatisé (Cloudflare) : téléchargement manuel requis |
| Guide administratif et financier FSE+ 2021-2027 | National | PDF | Mis à jour régulièrement (dernière maj identifiée : juin 2026) – prévoir un mécanisme de rafraîchissement |
| Guide méthodologique régional Île-de-France | Régional | PDF | Décline les règles générales en critères concrets — choisi le 2026-08-19 (cadrage laissait IDF ou Nouvelle-Aquitaine à titre d'exemple) |
| Guide ANCT instruments financiers | National | PDF | Conçu pour auditeurs et gestionnaires – vocabulaire proche du métier cible |

**Point d'attention** : corpus hétérogène (texte juridique dense vs. guides pédagogiques) – la stratégie de découpage doit s'adapter au type de document plutôt qu'être uniforme.

## 3. Architecture technique (proposition de départ)

- **Ingestion** : extraction texte des PDF, en préservant si possible la structure (articles, sections, titres)
- **Découpage (chunking)** : par unité logique (article, section) plutôt que par taille de caractères fixe, pour ne pas couper une règle en deux
- **Indexation** : base vectorielle self-hosted et gratuite (ex. Qdrant)
- **Orchestration RAG** : LangChain ou LlamaIndex
- **Génération** : LLM avec récupération de contexte, réponse contrainte à citer la source exacte (document + article/section)
- **Interface** : à définir selon la stack retenue (cf. échanges précédents sur frontend/hébergement gratuit 24/7)

## 4. Exigences fonctionnelles

- Question/réponse en langage naturel sur le corpus indexé
- Traçabilité systématique : chaque réponse doit citer le document et la référence précise (article, section) utilisés
- Gestion explicite du cas hors-corpus : le système doit répondre qu'il ne sait pas plutôt que d'inventer une règle

## 5. Exigences non fonctionnelles

- Hébergement gratuit, disponibilité 24/7 pour un trafic faible (cohérent avec le choix déjà fait pour le portfolio : Hugging Face Spaces / Render / Fly.io)
- Temps de réponse : pas de contrainte de charge, cible "démo fluide"

## 6. Critères de succès du POC

- Réponse correcte à un jeu de questions test, avec citation exacte de la source
- Absence de réponse inventée sur les questions hors-corpus ("je ne sais pas" plutôt qu'une hallucination)

## 7. Risques et limites identifiés

- **Fiabilité réglementaire** : une erreur sur une règle d'éligibilité a un impact réel pour un futur usage – le système doit être positionné comme outil d'aide, non comme source faisant foi
- **Fragmentation des sources** : redondances ou nuances entre les niveaux UE / national / régional, à surveiller dans les réponses générées
