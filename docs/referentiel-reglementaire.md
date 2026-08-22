# Référentiel réglementaire — inventaire des textes

Inventaire des textes qui régissent les fonds européens de cohésion : lesquels
existent, lesquels sont en vigueur, où les trouver ([issue #21](https://github.com/benoitdb/assistant-rag-ue/issues/21)).

**Ce document n'est pas une liste d'ingestion.** Savoir qu'un texte existe et
décider de l'indexer sont deux choses : les documents concernés sont trop
nombreux pour être tous ingérés, et l'arbitrage se fait texte par texte, en V2
(voir [roadmap-v2.md](roadmap-v2.md)). L'inventaire sert précisément à instruire
cet arbitrage.

## Comment lire ce document

**Chaque statut est une photographie datée, pas une vérité permanente.** Les
textes de base bougent peu, mais les règlements modificatifs les amendent :
« en vigueur » sans date est une affirmation qui se périme en silence. D'où la
colonne « Constaté le », qui dit quand le statut a été vérifié — et rien après
cette date.

Le cas est déjà concret ici : le règlement (UE) 2021/1060 a connu **sept**
versions consolidées depuis sa publication.

**Collecte manuelle.** Les documents sont récupérés à la main ; ce mode est
assumé, pas subi. Aucun rafraîchissement automatique n'est en place, et la mise
à jour de ce fichier se fait quand il y a une raison de le faire.

**Ce qui a été vérifié pour la consultation** (2026-08-22) : les `robots.txt`
d'EUR-Lex et de Légifrance ont été lus avant toute consultation automatisée,
comme l'exige l'issue #21 — vérifier plutôt que supposer.

- **EUR-Lex** autorise les pages `/legal-content/...` et impose un
  `Crawl-delay: 10` ; il interdit notamment `/legal-content/*/TXT/DOC/`,
  `/print-pdf`, `/export-documents` et `/download-notice`. Les consultations
  ci-dessous ont porté sur les pages HTML autorisées, espacées en conséquence.
- **Légifrance** n'interdit que `/download/`.

Ces constats datent eux aussi : les revérifier avant toute nouvelle campagne de
consultation, et **à plus forte raison** avant d'envisager un rafraîchissement
récurrent, qui reste soumis aux deux conditions de l'issue #21 (autorisation
vérifiée, puis faisabilité démontrée).

## Textes du corpus indexé (V1)

| Intitulé | Référence | Date | Statut | Source | Constaté le |
|---|---|---|---|---|---|
| Règlement portant dispositions communes relatives au FEDER, FSE+, Fonds de cohésion, FTJ et FEAMPA (« RPDC ») | Règlement (UE) 2021/1060 | 24/06/2021 | **En vigueur, modifié** — version consolidée en vigueur au 01/07/2026. Versions consolidées successives : 30/06/2021, 26/10/2022, 01/03/2023, 01/03/2024, 30/06/2024, 25/10/2025, 01/07/2026 | [EUR-Lex, CELEX 32021R1060](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32021R1060) · ELI `http://data.europa.eu/eli/reg/2021/1060/oj` | 2026-08-22 |
| Décret fixant les règles nationales d'éligibilité des dépenses des programmes européens de la politique de cohésion et de la pêche et des affaires maritimes pour 2021-2027 | Décret n° 2022-608 | 21/04/2022 (JORF n° 0095 du 23/04/2022) | **En vigueur** — aucune modification signalée par Légifrance (dernière mise à jour des données : 24/04/2022) | [Légifrance, JORFTEXT000045638719](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045638719) ([version consolidée](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000045638719)) | 2026-08-22 |
| Guide du porteur de projets et du bénéficiaire d'une aide européenne — Programme Centre-Val de Loire et interrégional Loire, FEDER-FSE+ 2021-2027 | *(pas de référence réglementaire — document d'accompagnement régional)* | Exemplaire indexé produit le 27/06/2023 (métadonnées du PDF) | **À confirmer** — un exemplaire est publié sous un chemin daté de mars 2024 : il est possible que l'exemplaire indexé soit **antérieur** à celui en ligne, ce qui n'a pas pu être établi sans télécharger et comparer les deux | [europeocentre-valdeloire.eu](https://www.europeocentre-valdeloire.eu/wp-content/uploads/2024/03/Guide-du-porteur-de-projet-et-du-beneficiaire-dune-aide-europeenne-feder-fse-2021-2027.pdf) | 2026-08-22 |

> **Conséquence directe sur le corpus** : l'exemplaire du règlement 2021/1060
> indexé est la version d'origine du JO du 30/06/2021 (548 pages, en-tête
> « L 231/159 »), pas une version consolidée. L'assistant peut donc citer
> fidèlement un texte qui a été amendé depuis. Suivi en
> [issue #26](https://github.com/benoitdb/assistant-rag-ue/issues/26) — ce n'est
> pas un défaut de l'inventaire, c'est l'inventaire qui l'a révélé.

## Textes identifiés, non acquis

Sous-ensemble déjà arbitré du référentiel, repris de
[roadmap-v2.md §0](roadmap-v2.md).

| Intitulé | Référence | Date | Statut | Source | Constaté le |
|---|---|---|---|---|---|
| Règlement relatif au Fonds social européen plus (FSE+), abrogeant le règlement (UE) n° 1296/2013 | Règlement (UE) 2021/1057 | 24/06/2021 | **En vigueur, modifié** — version consolidée en vigueur au 20/09/2025 (versions antérieures : 30/06/2021, 01/03/2024, 24/12/2024) | [EUR-Lex, CELEX 32021R1057](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32021R1057) · ELI `http://data.europa.eu/eli/reg/2021/1057/oj` | 2026-08-22 |
| Guide administratif et financier FSE+ 2021-2027 | *(document d'accompagnement)* | — | **Non vérifié** — signalé au cadrage comme mis à jour régulièrement, donc un statut daté y sera particulièrement volatil | *à fournir* | — |
| Guide ANCT instruments financiers | *(document d'accompagnement)* | — | **Non vérifié** | *à fournir* | — |

## À compléter

L'inventaire ne prétend pas être exhaustif à ce stade. Manquent notamment, et
volontairement tant que leurs références ne sont pas fournies ou vérifiées :

- les **règlements spécifiques par fonds** autres que le FSE+ — FEDER et Fonds
  de cohésion, FTJ — cités par le RPDC mais non encore relevés ici ;
- les **actes délégués et d'exécution** pris sur le fondement du RPDC ;
- les **textes nationaux** autres que le décret n° 2022-608 (arrêtés,
  instructions, circulaires) ;
- les **guides régionaux** au-delà de Centre-Val de Loire.

**Méthode pour ajouter une ligne** : partir de la source officielle (EUR-Lex,
Légifrance, portail de l'autorité de gestion), relever l'intitulé complet tel
qu'il y figure, et dater le constat du jour où il est fait. Ne pas reconstituer
une URL par analogie avec une autre : un identifiant Légifrance formé « à la
main » plutôt que relevé mène à une page inexistante — c'est arrivé pendant la
constitution de cette première version.
