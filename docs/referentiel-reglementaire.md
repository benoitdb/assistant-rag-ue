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
d'EUR-Lex, de Légifrance et d'europe-en-france ont été lus avant toute
consultation automatisée, comme l'exige l'issue #21 — vérifier plutôt que
supposer.

- **EUR-Lex** autorise les pages `/legal-content/...` et impose un
  `Crawl-delay: 10` ; il interdit notamment `/legal-content/*/TXT/DOC/`,
  `/print-pdf`, `/export-documents` et `/download-notice`. Les consultations
  ci-dessous ont porté sur les pages HTML autorisées, espacées en conséquence.
- **Légifrance** n'interdit que `/download/`, et ne déclare pas de
  `Crawl-delay`.
- **europe-en-france** impose un `Crawl-delay: 10` et interdit `/recherche/`
  ainsi que, par la règle `Disallow: *?`, **toute URL portant des paramètres**.
  La pagination de la liste des ressources réglementaires passant par `?page=`,
  seule la page 1 (25 des 51 entrées) était consultable automatiquement. Le
  blocage n'a pas été contourné : les pages 2 et 3 ont été **récupérées à la
  main** (2026-08-22), ce qui est le mode par défaut assumé de cet inventaire.
  Le sitemap, voie autorisée essayée d'abord, n'expose qu'une poignée de
  `/fr/ressources/` et ne remplaçait pas la pagination.

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

## Règlements spécifiques par fonds

Relevés depuis la page « [Règlements européens 2021-2027](https://www.europe-en-france.gouv.fr/fr/ressources/reglements-europeens-2021-2027) »
d'europe-en-france, **statuts constatés sur EUR-Lex**. Le portail national dit
quels textes existent ; il ne dit pas s'ils sont en vigueur.

| Intitulé | Référence | Date | Statut | Source | Constaté le |
|---|---|---|---|---|---|
| Règlement relatif au Fonds européen de développement régional et au Fonds de cohésion | Règlement (UE) 2021/1058 | 24/06/2021 | **En vigueur, modifié** — version consolidée en vigueur au 20/09/2025 (versions antérieures : 30/06/2021, 01/03/2024, 24/12/2024) | [EUR-Lex, CELEX 32021R1058](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32021R1058) · ELI `http://data.europa.eu/eli/reg/2021/1058/oj` | 2026-08-22 |
| Règlement établissant le Fonds pour une transition juste (FTJ) | Règlement (UE) 2021/1056 | 24/06/2021 | **En vigueur, modifié** — version consolidée en vigueur au 20/09/2025 (versions antérieures : 30/06/2021, 01/03/2024) | [EUR-Lex, CELEX 32021R1056](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32021R1056) · ELI `http://data.europa.eu/eli/reg/2021/1056/oj` | 2026-08-22 |
| Règlement portant dispositions particulières relatives à l'objectif « Coopération territoriale européenne » (Interreg) soutenu par le FEDER et les instruments de financement extérieur | Règlement (UE) 2021/1059 | 24/06/2021 | **En vigueur, non modifié** — une seule version consolidée, 30/06/2021 (JO L 231 du 30/06/2021, p. 94-158) | [EUR-Lex, CELEX 32021R1059](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32021R1059) · ELI `http://data.europa.eu/eli/reg/2021/1059/oj` | 2026-08-22 |

> **Le Fonds de cohésion n'a pas de règlement propre** : il est régi par le
> 2021/1058, conjointement avec le FEDER — l'intitulé officiel relevé sur
> EUR-Lex le nomme explicitement. La page d'europe-en-france étiquette ce
> règlement « FEDER » seulement ; c'est le titre à la source qui fait foi.

> **Piège d'ingestion, avant qu'il ne se referme** : europe-en-france héberge
> ces cinq règlements en PDF sous `/sites/default/files/`, mais ce sont les
> versions **du JO de juillet 2021**, pas les consolidées. Ingérer depuis cette
> source reproduirait l'[issue #26](https://github.com/benoitdb/assistant-rag-ue/issues/26)
> sur cinq textes au lieu d'un. Commodité de téléchargement n'est pas fraîcheur
> du texte.

## Textes nationaux d'application

Constatés sur Légifrance. Aucun n'est acquis ni indexé.

| Intitulé | Référence | Date | Statut | Source | Constaté le |
|---|---|---|---|---|---|
| Décret relatif à la gestion des programmes européens de la politique de cohésion et de la pêche et des affaires maritimes pour la période 2021-2027 | Décret n° 2021-1884 | 29/12/2021 (JORF n° 0303 du 30/12/2021) | **En vigueur** — aucune modification signalée (dernière mise à jour des données : 31/12/2021) | [Légifrance, JORFTEXT000044615064](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000044615064) | 2026-08-22 |
| Décret relatif à l'autorité nationale pour les programmes de coopération territoriale européenne pour la période 2021-2027 | Décret n° 2022-579 | 19/04/2022 | **En vigueur** — aucune modification signalée (dernière mise à jour des données : 22/04/2022) | [Légifrance, JORFTEXT000045614686](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000045614686) | 2026-08-22 |
| Décret relatif au comité national Etat-régions et au comité Etat-région régional pour la période 2021-2027 des programmes européens de la politique de cohésion et de la pêche et des affaires maritimes et la période 2023-2027 de la politique de développement rural | Décret n° 2022-580 | 20/04/2022 | **En vigueur, modifié** — articles 1 et 2 modifiés par le décret n° 2022-1051 du 28/07/2022 (dernière mise à jour des données : 30/07/2022) | [Légifrance, JORFTEXT000045614693](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000045614693) | 2026-08-22 |
| Décret relatif à la mise en œuvre des programmes européens de la politique de cohésion, de la pêche et des affaires maritimes, et des migrations et des affaires intérieures pour la période 2021-2027 | Décret n° 2022-713 | 27/04/2022 | **En vigueur** — aucune modification signalée (dernière mise à jour des données : 23/11/2023) | [Légifrance, JORFTEXT000045684059](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000045684059) | 2026-08-22 |
| Arrêté portant désignation des préfets coordonnateurs pour les programmes de coopération territoriale européenne transfrontaliers, transnationaux et régions ultrapériphériques pour la période 2021-2027 | Arrêté du 15/02/2022 (NOR PRMG2202115A) | 15/02/2022 (JORF n° 0040 du 17/02/2022) | **Version initiale** — aucune version ultérieure publiée | [Légifrance, JORFTEXT000045180944](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045180944) | 2026-08-22 |
| Accord de partenariat France 2021-2027 (FEDER, FSE+, FTJ, FEAMPA) | *(pas une norme — document de programmation adopté par la Commission)* | Adopté le 02/06/2022 | **Adopté** — exemplaire publié par europe-en-france le 24/06/2022 ; aucune version ultérieure repérée sur ce portail | [europe-en-france, `ap_fr_version_adoptee_020622.pdf`](https://www.europe-en-france.gouv.fr/sites/default/files/ap_fr_version_adoptee_020622.pdf) | 2026-08-22 |

> **Deux constats que cette passe a produits**, et qui justifient la colonne
> « Constaté le » mieux qu'un argument :
>
> 1. Le décret n° 2022-580 **a été modifié** en juillet 2022. Une liste sans
>    date l'aurait présenté comme intact pendant quatre ans.
> 2. Son intitulé réel, relevé sur Légifrance, couvre aussi la politique de
>    développement rural 2023-2027 — ce que le libellé abrégé du portail
>    national ne laissait pas voir.
>
> **Et un rappel de méthode payé comptant** : le lien du portail national vers
> le décret n° 2021-1884 pointait vers `JORFTEXT000045180944`, qui est en
> réalité l'arrêté du 15 février 2022. Le bon identifiant
> (`JORFTEXT000044615064`) a été retrouvé en parcourant le JORF du 30/12/2021.
> Une source officielle peut se tromper de lien : c'est le texte à l'arrivée
> qu'il faut lire, pas le lien au départ.

## Programmation 2014-2020 — les deux prédécesseurs directs

Retenus à titre **comparatif** (cf. [roadmap-v2.md §4](roadmap-v2.md)) parce
qu'ils sont les prédécesseurs exacts des deux textes normatifs du corpus
indexé : le 1303/2013 précède le RPDC 2021/1060, le décret 2016-279 précède
le décret 2022-608. Le reste du bloc 2014-2020 du portail national n'est pas
repris — voir « À compléter ».

| Intitulé | Référence | Date | Statut | Source | Constaté le |
|---|---|---|---|---|---|
| Règlement portant dispositions communes relatives au FEDER, au FSE, au Fonds de cohésion, au FEADER et au FEAMP | Règlement (UE) n° 1303/2013 | 17/12/2013 | **En vigueur, modifié** — version consolidée en vigueur au 01/03/2024. Toujours en vigueur malgré la fin de la période de programmation | [EUR-Lex, CELEX 32013R1303](https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX%3A32013R1303) · ELI `http://data.europa.eu/eli/reg/2013/1303/oj` | 2026-08-22 |
| Décret fixant les règles nationales d'éligibilité des dépenses dans le cadre des programmes soutenus par les fonds structurels et d'investissement européens pour la période 2014-2020 | Décret n° 2016-279 | 08/03/2016 (JORF n° 0059 du 10/03/2016) | **En vigueur, modifié** — notamment par le décret n° 2019-225 du 22/03/2019 (dernière mise à jour des données : 25/03/2019) | [Légifrance, JORFTEXT000032174265](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000032174265) | 2026-08-22 |

> **Contre-intuitif, et c'est pour cela que c'est écrit** : ces deux textes de
> la période 2014-2020 sont **toujours en vigueur** en 2026. Une période de
> programmation close ne signifie pas des textes abrogés — les opérations en
> cours de clôture continuent d'en relever. Supposer l'inverse aurait produit
> deux lignes fausses.

## Ce que le portail national contient, et ne contient pas

Les 51 ressources réglementaires d'europe-en-france ont été parcourues en
entier (2026-08-22). Répartition constatée, d'après les propres facettes du
portail : 20 taguées « Aides d'État », 10 « 2014-2020 », **8 « 2021-2027 »**.

**Les 8 entrées 2021-2027 sont toutes recensées ci-dessus** — Accord de
partenariat, décrets 2021-1884 / 2022-579 / 2022-580 / 2022-608 / 2022-713,
arrêté du 15/02/2022, et la page « Règlements européens 2021-2027 ». Aucun
texte de la programmation en cours ne manque à l'inventaire du fait de ce
portail.

Les 26 autres entrées relèvent de deux ensembles hors périmètre V1, et
l'arbitrage a été tranché différemment pour chacun :

- le **droit des aides d'État** (RGEC 651/2014, règlements *de minimis*
  1407/2013, 1408/2013, 717/2014, 360/2012, règlements de procédure 659/1999
  et 2015/1589, régime SA.39252, communications de la Commission) — **écarté**
  de l'inventaire : ces textes débordent les fonds de cohésion et forment un
  champ à eux seuls. Décision de périmètre, pas oubli ;
- la **programmation 2014-2020** — **deux textes retenus** à titre comparatif,
  le règlement 1303/2013 et le décret n° 2016-279 (section précédente), parce
  qu'ils précèdent directement les deux textes normatifs du corpus indexé. Le
  reste du bloc (cadre national de développement rural, cadre de suivi PAC,
  charte graphique, stratégie de communication Europ'Act) n'est pas repris.

> **Le portail illustre involontairement la thèse de ce document.** Plusieurs
> de ses fiches affichent une date de fin déjà passée sans que le statut soit
> signalé comme périmé : « Date de fin : 31/12/2018 » pour le règlement
> 360/2012, « 31/12/2020 » pour les règlements 1408/2013 et 717/2014. Une
> liste sans date de constat vieillit en silence ; c'est visible ici à l'œil nu.

## À compléter

L'inventaire ne prétend pas être exhaustif à ce stade. Manquent notamment, et
volontairement tant que leurs références ne sont pas fournies ou vérifiées :

- les **actes délégués et d'exécution** pris sur le fondement du RPDC ;
- les **instructions et circulaires** nationales — les décrets et l'arrêté
  recensés ci-dessus ne couvrent pas la doctrine d'application ;
- les **guides régionaux** au-delà de Centre-Val de Loire.

**Hors périmètre, par décision et non par omission** : le droit des aides
d'État (lignes directrices, *de minimis*, exemptions sectorielles, régimes
notifiés) et le reste de la programmation 2014-2020. Ces textes touchent
l'éligibilité des dépenses sans être propres aux fonds de cohésion ; les
recenser reviendrait à ouvrir un second référentiel. Si ce choix est
réexaminé un jour, le portail national en recense une vingtaine, listés à la
section précédente — le point de départ existe.

**Méthode pour ajouter une ligne** : partir de la source officielle (EUR-Lex,
Légifrance, portail de l'autorité de gestion), relever l'intitulé complet tel
qu'il y figure, et dater le constat du jour où il est fait. Ne pas reconstituer
une URL par analogie avec une autre : un identifiant Légifrance formé « à la
main » plutôt que relevé mène à une page inexistante — c'est arrivé pendant la
constitution de cette première version.
