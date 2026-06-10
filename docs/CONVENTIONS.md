# Conventions pragmatic-scripts

## Philosophie

Chaque script doit pouvoir être lancé seul avec `python path/to/script.py` et intégré dans un script Bash ou une CI.

## Règles

- Utiliser `argparse` pour les paramètres.
- Utiliser `load_dotenv()` seulement si le script accepte des variables d'environnement.
- Ne pas hardcoder d'URL, token, projet, espace ou JQL spécifique.
- Mettre les erreurs dans `stderr`.
- Retourner un code explicite :
  - `0` : succès ;
  - `1` : erreur runtime/API ;
  - `2` : configuration ou arguments invalides.
- Prévoir `--json` dès qu'une sortie peut être consommée par Bash/CI.
- Éviter les imports internes au repo pour garder le script standalone.

## Nommage

Format recommandé : `verbe_objet.py`

Exemples :
- `list_issues.py`
- `render_plantuml.py`
- `publish_markdown_plantuml.py`
- `cleanup_merged_branches.py`
