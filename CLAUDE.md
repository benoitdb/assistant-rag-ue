# Assistant RAG UE — instructions pour Claude Code

Les instructions du projet sont communes à tous les assistants de code
(Claude Code, Codex) et vivent dans `AGENTS.md` — **source unique**, à modifier
là et pas ici (issue #32) :

@AGENTS.md

## Propre à Claude Code

- **Hooks `Stop`** (`.claude/settings.json`, scripts dans `.claude/hooks/`) :
  - tests rapides (`tests-rapides.sh`), lancés dès qu'un `.py` est modifié — un
    tour ne peut pas se clore dessus s'ils échouent ;
  - tests lents (`tests-lents.sh`), **en tâche de fond** : le tour se clôt sans
    attendre, et Claude n'est réveillé qu'en cas d'échec. Journal dans
    `/tmp/claude-tests-lents.log` — un succès est autrement invisible.
- **Skill `/ingerer-document`** (`.claude/skills/ingerer-document/`) : invocation
  manuelle uniquement (`disable-model-invocation`), chargé à la demande.
