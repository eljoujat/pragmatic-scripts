#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:?Missing PROJECT_ID}"

python scripts/gitlab/list_merge_requests.py \
  --project-id "$PROJECT_ID" \
  --state merged \
  --limit 20 \
  --json > merge_requests.json

echo "Report generated: merge_requests.json"
