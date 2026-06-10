#!/usr/bin/env python3
"""List GitLab merge requests for a project.

Env vars supported via shell or .env:
  GITLAB_URL, GITLAB_TOKEN
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import gitlab
from dotenv import load_dotenv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List GitLab merge requests for a project.")
    parser.add_argument("--url", default=os.getenv("GITLAB_URL"), help="GitLab base URL")
    parser.add_argument("--token", default=os.getenv("GITLAB_TOKEN"), help="GitLab private access token")
    parser.add_argument("--project-id", required=True, help="GitLab project ID or path")
    parser.add_argument("--state", default="merged", choices=["opened", "closed", "locked", "merged", "all"], help="MR state")
    parser.add_argument("--limit", type=int, default=10, help="Maximum number of MRs")
    parser.add_argument("--json", action="store_true", help="Print JSON output for scripting")
    return parser.parse_args()


def mr_to_dict(mr: Any) -> dict[str, Any]:
    return {
        "iid": mr.iid,
        "title": mr.title,
        "author": mr.author.get("username"),
        "source_branch": mr.source_branch,
        "target_branch": mr.target_branch,
        "state": mr.state,
        "merged_at": getattr(mr, "merged_at", None),
        "updated_at": mr.updated_at,
        "web_url": mr.web_url,
    }


def main() -> int:
    load_dotenv()
    args = parse_args()
    if not args.url or not args.token:
        print("ERROR: provide --url/--token or GITLAB_URL/GITLAB_TOKEN", file=sys.stderr)
        return 2

    gl = gitlab.Gitlab(url=args.url, private_token=args.token, keep_base_url=True)
    project = gl.projects.get(args.project_id, lazy=True)
    mrs = project.mergerequests.list(state=args.state, order_by="updated_at", sort="desc", per_page=args.limit)
    rows = [mr_to_dict(mr) for mr in mrs[: args.limit]]

    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        for row in rows:
            print(f"!{row['iid']} {row['title']}")
            print(f"  author={row['author']} {row['source_branch']} -> {row['target_branch']} updated={row['updated_at']}")
            print(f"  {row['web_url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
