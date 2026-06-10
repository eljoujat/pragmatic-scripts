#!/usr/bin/env python3
"""Publish a Markdown file to Confluence and render embedded PlantUML references.

PlantUML references use this compact syntax inside markdown:
  ``` plantuml path/to/diagram.puml ```

Env vars supported via shell or .env:
  CONFLUENCE_URL, CONFLUENCE_TOKEN
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import markdown2
from atlassian import Confluence
from dotenv import load_dotenv
from plantweb.render import render_file
from requests.exceptions import HTTPError

PLANTUML_REF_PATTERN = re.compile(r"```\s*plantuml\s+([^`\s]+\.puml)\s*```")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish Markdown with PlantUML images to Confluence.")
    parser.add_argument("--url", default=os.getenv("CONFLUENCE_URL"), help="Confluence base URL")
    parser.add_argument("--token", default=os.getenv("CONFLUENCE_TOKEN"), help="Confluence API token / PAT")
    parser.add_argument("--space", required=True, help="Confluence space key")
    parser.add_argument("--title", required=True, help="Page title")
    parser.add_argument("--markdown", required=True, type=Path, help="Markdown file to publish")
    parser.add_argument("--parent-id", help="Optional Confluence parent page ID for creation")
    return parser.parse_args()


def publish() -> int:
    load_dotenv()
    args = parse_args()
    if not args.url or not args.token:
        print("ERROR: provide --url/--token or CONFLUENCE_URL/CONFLUENCE_TOKEN", file=sys.stderr)
        return 2
    if not args.markdown.exists():
        print(f"ERROR: markdown file not found: {args.markdown}", file=sys.stderr)
        return 2

    confluence = Confluence(url=args.url, token=args.token)
    page = confluence.get_page_by_title(space=args.space, title=args.title)
    if page:
        page_id = page["id"]
    else:
        page = confluence.create_page(space=args.space, title=args.title, body="", parent_id=args.parent_id)
        page_id = page["id"]

    markdown_content = args.markdown.read_text(encoding="utf-8")
    base_dir = args.markdown.parent

    for match in PLANTUML_REF_PATTERN.findall(markdown_content):
        puml_file = (base_dir / match).resolve()
        if not puml_file.exists():
            print(f"ERROR: PlantUML file not found: {puml_file}", file=sys.stderr)
            return 2

        png_file = render_file(
            str(puml_file),
            renderopts={"engine": "plantuml", "format": "png"},
            cacheopts={"use_cache": False},
        )
        attachment = confluence.attach_file(page_id=page_id, filename=png_file)
        attachment_path = urlparse(attachment["_links"]["download"]).path
        markdown_content = markdown_content.replace(
            f"``` plantuml {match} ```",
            f"![PlantUML Image]({attachment_path})",
        )

    html_content = markdown2.markdown(markdown_content)
    confluence.update_page(page_id=page_id, always_update=True, title=args.title, body=html_content, type="page")
    print(f"{args.url.rstrip('/')}{page['_links']['webui']}")
    return 0


def main() -> int:
    try:
        return publish()
    except HTTPError as exc:
        print(f"HTTP error: {exc.response.status_code} - {exc.response.text}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - CLI safety net
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
