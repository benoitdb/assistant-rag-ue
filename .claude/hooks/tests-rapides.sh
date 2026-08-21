#!/usr/bin/env bash
# Hook Stop : empêche de clore un tour sur des tests rapides en échec.
#
# Périmètre : la suite hors réseau, moins les deux fichiers qui parsent des PDF
# (test_articles.py et test_guide_regional.py). Mesuré : 7 s pour 35 tests,
# contre 140 s pour les 45 — 80% du temps vient de ces deux fichiers seuls.
#
# C'est un DÉTECTEUR DE FUMÉE, pas le gardien. L'extraction des 119 articles
# n'est pas couverte ici ; c'est la CI qui vérifie tout, au moment du merge.
#
# Ne tourne que si des fichiers .py sont modifiés dans l'arbre de travail : un
# tour de pure conversation ne paie pas les 7 s. Le critère est `git status`,
# pas une liste de chemins maintenue à la main — il ne peut donc pas dériver
# quand un nouveau module apparaît.

set -uo pipefail

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

# Rien de modifié côté Python → rien à vérifier.
if [ -z "$(git status --porcelain -- '*.py' 2>/dev/null)" ]; then
  exit 0
fi

sortie=$(venv/bin/python -m pytest -q \
  --ignore=tests/test_articles.py \
  --ignore=tests/test_guide_regional.py 2>&1)
statut=$?

if [ "$statut" -ne 0 ]; then
  jq -n --arg r "$sortie" '{
    decision: "block",
    reason: ("Tests rapides en échec — corrige avant de clore le tour.\n\n" + $r +
             "\n\nSuite complète (140 s) : venv/bin/python -m pytest -q")
  }'
fi

exit 0
