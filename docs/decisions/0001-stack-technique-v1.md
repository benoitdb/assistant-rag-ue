# ADR 0001 — Stack technique V1

Date : 2026-08-19
Statut : Retenu

## Contexte

Le cadrage (§3 Architecture technique) laissait plusieurs choix ouverts
("LangChain ou LlamaIndex", "ex. Qdrant", interface "à définir"). Décisions
prises pour lancer l'implémentation de la V1.

## Décisions

| Brique | Choix | Pourquoi |
|---|---|---|
| Orchestration RAG | Aucun framework — appels directs API + code fait main pour chunking/retrieval | Corpus V1 restreint (3 documents), et le point critique du cahier des charges (citer la source exacte) demande un contrôle fin sur ce qui est récupéré et pourquoi. Un framework ajoute une couche d'abstraction qui complique ce debug sans apporter de valeur à cette échelle. |
| Vector store | Qdrant, sur Qdrant Cloud (free tier) | Choisi explicitement malgré la recommandation initiale (Chroma embarqué, plus simple pour un POC à 3 documents). Le mode Cloud évite de porter la disponibilité d'un service self-hosted, cohérent avec l'exigence 24/7 sans serveur dédié. |
| Extraction PDF | pdfplumber | Bonne préservation de la mise en page/structure (utile pour repérer articles/sections), léger. |
| Embeddings | Mistral Embed (API) | Même fournisseur que la génération (une seule clé API), bon sur le vocabulaire juridique/administratif français. |
| LLM de génération | Mistral API (free tier) | Cohérent avec la contrainte d'hébergement gratuit du cadrage. Modèles français, potentiellement plus à l'aise sur le vocabulaire juridique/administratif FR que des modèles généralistes US. |
| Interface | Streamlit | Cohérence avec Cartographie FESI (mêmes réflexes), contrôle fin nécessaire pour afficher réponse + citations sources proprement. |
| Hébergement app | Hugging Face Spaces | Gratuit, pensé pour les démos IA/portfolio, bonne intégration Streamlit. |

## Risque identifié à surveiller

Le choix d'un LLM gratuit (Mistral free tier) plutôt qu'un modèle plus
robuste type Claude a été fait en priorisant la contrainte "gratuit" du
cadrage sur la fiabilité de suivi de consignes. Or les deux exigences non
négociables du cadrage (citation exacte systématique, refus explicite sur le
hors-corpus) dépendent directement de cette fiabilité. À vérifier en premier
lors des tests contre le jeu de questions du POC (cadrage §6) : si le modèle
peine à respecter ces consignes de façon fiable, reconsidérer ce choix avant
d'aller plus loin sur le reste du pipeline.

## Prochaine décision à trancher

Stratégie de chunking précise (granularité par article/section, gestion des
articles très longs ou très courts) — à documenter dans un ADR séparé une
fois le premier pipeline d'ingestion testé sur le Règlement 2021/1060.
