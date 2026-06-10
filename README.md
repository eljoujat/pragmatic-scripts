![Visitors](https://api.visitorbadge.io/api/visitors?path=eljoujat%2Fpragmatic-scripts&labelColor=%2337d67a&countColor=%23263759)

# pragmatic-scripts

Collection de scripts Python **standalone** pour automatiser des tâches pragmatiques Dev / Ops / DevOps / Architectes / Managers / Admins.

Objectifs du repo :
- exécuter un script facilement après clone ;
- intégrer chaque script dans un pipeline Bash / CI ;
- ajouter un nouveau script sans comprendre tout le repo ;
- garder des scripts indépendants, explicites et maintenables.

## Structure

```text
pragmatic-scripts/
├── scripts/                 # Scripts exécutables, classés par domaine
│   ├── confluence/
│   ├── gitlab/
│   ├── jira/
│   └── plantuml/
├── templates/               # Template pour créer un nouveau script
├── examples/bash/           # Exemples d'intégration Bash
├── docs/                    # Documentation contributeur / conventions
├── requirements.txt         # Dépendances Python
├── .env.example             # Variables d'environnement attendues
└── Makefile                 # Commandes utiles
```

## Installation rapide

```bash
git clone <repo-url>
cd pragmatic-scripts
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Puis renseigner `.env` si vous utilisez Jira / GitLab / Confluence.

## Exécuter un script

Tous les scripts exposent une aide CLI :

```bash
python scripts/jira/list_issues.py --help
python scripts/gitlab/list_merge_requests.py --help
python scripts/plantuml/render_plantuml.py --help
```

Exemples :

```bash
python scripts/jira/list_issues.py \
  --jql "project = ABC order by updated desc" \
  --limit 5

python scripts/gitlab/list_merge_requests.py \
  --project-id 123 \
  --state merged \
  --json

python scripts/plantuml/render_plantuml.py \
  --input scripts/confluence/seq.puml \
  --output /tmp/seq.png
```

## Utilisation dans Bash / CI

```bash
#!/usr/bin/env bash
set -euo pipefail

python scripts/gitlab/list_merge_requests.py --project-id "$PROJECT_ID" --json > merge_requests.json
```

Voir aussi `examples/bash/run_gitlab_report.sh`.

## Ajouter un nouveau script

1. Choisir ou créer un domaine dans `scripts/<domaine>/`.
2. Copier `templates/script_template.py`.
3. Nommer le fichier avec une action claire : `list_issues.py`, `render_plantuml.py`, `cleanup_branches.py`.
4. Ajouter `argparse`, `main()`, codes retour, `--json` si utile.
5. Documenter un exemple dans le header ou dans `scripts/<domaine>/README.md`.

Convention minimale :
- script autonome ;
- pas de valeur hardcodée projet/client ;
- paramètres via arguments CLI ou variables d'environnement ;
- sortie exploitable par Bash ;
- erreurs sur `stderr` ;
- exit code `0` succès, `1` erreur runtime, `2` mauvais usage/config.

## Commandes utiles

```bash
make install      # installe les dépendances
make list         # liste les scripts Python
make chmod        # rend les scripts exécutables
```
