#!/usr/bin/env python3
"""List Jira issues matching a JQL query.

Env vars supported via shell or .env:
  JIRA_URL, JIRA_TOKEN
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from dotenv import load_dotenv
from jira import JIRA


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List Jira issues using JQL.")
    parser.add_argument("--url", default=os.getenv("JIRA_URL"), help="Jira base URL")
    parser.add_argument("--token", default=os.getenv("JIRA_TOKEN"), help="Jira API token / PAT")
    parser.add_argument("--jql", required=True, help="JQL query, e.g. 'project = ABC order by updated desc'")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of issues")
    parser.add_argument("--json", action="store_true", help="Print JSON output for scripting")
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    if not args.url or not args.token:
        print("ERROR: provide --url/--token or JIRA_URL/JIRA_TOKEN", file=sys.stderr)
        return 2

    jira = JIRA(server=args.url, token_auth=args.token)
    issues = jira.search_issues(args.jql, maxResults=args.limit)
    rows = [
        {
            "key": issue.key,
            "summary": issue.fields.summary,
            "status": issue.fields.status.name,
            "updated": issue.fields.updated,
            "url": f"{args.url.rstrip('/')}/browse/{issue.key}",
        }
        for issue in issues
    ]

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        for row in rows:
            print(f"{row['key']} [{row['status']}] {row['summary']}")
            print(f"  updated={row['updated']} {row['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
