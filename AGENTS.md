# AGENTS.md

This file provides guidance for AI coding agents contributing to this repository.

## Project purpose

`pragmatic-scripts` is a collection of standalone Python scripts intended to improve productivity for developers, ops, DevOps, architects, managers, admins, and anyone who can run Python.

The repository favors scripts that are:

- standalone and easy to run after cloning the repo;
- easy to integrate in Bash scripts and CI pipelines;
- grouped by domain under `scripts/`;
- explicit, pragmatic, and low-coupling;
- easy for contributors to copy, adapt, and extend.

## Repository structure

```text
scripts/                 # Executable standalone Python scripts, grouped by domain
  confluence/
  gitlab/
  jira/
  plantuml/
templates/               # Templates for new scripts
examples/bash/           # Bash integration examples
docs/                    # Contributor documentation and conventions
requirements.txt         # Python dependencies
.env.example             # Example environment variables
Makefile                 # Common commands
```

## Setup commands

Use Python 3.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill `.env` only when a script requires credentials or API URLs.

## Common commands

```bash
make install      # install Python dependencies
make list         # list available Python scripts
make chmod        # make scripts executable
```

Validate Python syntax before committing:

```bash
python3 -m py_compile scripts/*/*.py templates/script_template.py
```

Run a script help page:

```bash
python scripts/jira/list_issues.py --help
python scripts/gitlab/list_merge_requests.py --help
python scripts/plantuml/render_plantuml.py --help
```

## Coding conventions for scripts

Follow `docs/CONVENTIONS.md`.

Minimum expectations for every script:

- It must be executable standalone with `python path/to/script.py`.
- Use `argparse` for CLI parameters.
- Use a `main() -> int` function and `raise SystemExit(main())`.
- Do not hardcode project-specific URLs, tokens, IDs, spaces, JQL, or usernames.
- Read configuration from CLI arguments and, when relevant, environment variables.
- If environment variables are supported, load `.env` with `python-dotenv`.
- Print normal output to `stdout`.
- Print errors to `stderr`.
- Return explicit exit codes:
  - `0`: success;
  - `1`: runtime/API error;
  - `2`: invalid arguments or missing configuration.
- Add `--json` when output may be consumed by Bash, CI, or another tool.
- Keep scripts independent. Avoid shared internal imports unless there is a strong reason.

## Adding a new script

1. Choose or create a domain directory under `scripts/<domain>/`.
2. Copy `templates/script_template.py` as a starting point.
3. Name the script with an action-oriented name, e.g.:
   - `list_issues.py`
   - `render_plantuml.py`
   - `publish_markdown_plantuml.py`
   - `cleanup_merged_branches.py`
4. Add `--help` friendly descriptions for all CLI options.
5. Add `--json` if the output can be automated.
6. Update `README.md` when the script introduces a new domain or common workflow.
7. Add or update an example in `examples/bash/` when useful.
8. Run syntax validation before committing.

## Secrets and credentials

- Never commit real tokens, passwords, cookies, private keys, internal URLs, or client data.
- Use `.env.example` for documenting expected variables.
- Use `.env` locally only; it must stay ignored by Git.
- Prefer CLI arguments for explicit automation and environment variables for secrets.

## Bash and CI integration

Scripts should be easy to compose from Bash:

```bash
#!/usr/bin/env bash
set -euo pipefail

python scripts/gitlab/list_merge_requests.py --project-id "$PROJECT_ID" --json > merge_requests.json
```

When adding scripts, consider whether output should be human-readable, machine-readable, or both.

## Dependencies

- Add Python dependencies to `requirements.txt` only when necessary.
- Avoid heavy dependencies for simple tasks.
- Prefer standard library modules when they are enough.

## Commit guidance

Before committing, run:

```bash
git status --short
python3 -m py_compile scripts/*/*.py templates/script_template.py
```

Use concise commit messages describing the user-facing change, for example:

```text
Add Jira issue export script
Improve PlantUML render CLI
Document script conventions
```
