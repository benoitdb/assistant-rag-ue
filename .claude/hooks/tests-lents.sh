#!/usr/bin/env bash
# Hook Stop asynchrone : les deux fichiers de tests qui parsent des PDF.
#
# Complément exact de tests-rapides.sh, sans recouvrement :
#   - tests-rapides.sh (bloquant, 7 s)  -> 35 tests
#   - ce script (asynchrone, ~133 s)    -> les 10 autres
# Ensemble : la couverture de la suite hors réseau complète, sans faire attendre.
#
# Lancé en tâche de fond (`async` dans settings.json) : le tour se clôt
# immédiatement. En cas d'échec, sortie 2 — `asyncRewake` réveille alors Claude
# avec le message ci-dessous. Un succès est totalement silencieux, d'où le
# journal dans /tmp : c'est le seul moyen de constater que le hook a tourné.
#
# `-p no:cacheprovider` : ce script tourne en parallèle de tests-rapides.sh,
# deux pytest concurrents ne doivent pas se disputer .pytest_cache.

set -uo pipefail

JOURNAL=/tmp/claude-tests-lents.log

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

if [ -z "$(git status --porcelain -- '*.py' 2>/dev/null)" ]; then
  echo "$(date '+%F %T') ignoré (aucun .py modifié)" >> "$JOURNAL"
  exit 0
fi

# --tb=short et --show-capture=no : sans ça, le message de réveil est noyé sous
# les avertissements pdfminer capturés (des dizaines de lignes par test).
sortie=$(venv/bin/python -m pytest -q -p no:cacheprovider --tb=short --show-capture=no \
  tests/test_articles.py tests/test_guide_regional.py 2>&1)
statut=$?

if [ "$statut" -ne 0 ]; then
  echo "$(date '+%F %T') ÉCHEC" >> "$JOURNAL"
  echo "Tests lents en échec (extraction des articles / guide régional) —"
  echo "non couverts par le hook bloquant, détectés en tâche de fond :"
  echo
  echo "$sortie"
  exit 2
fi

echo "$(date '+%F %T') OK" >> "$JOURNAL"
exit 0
