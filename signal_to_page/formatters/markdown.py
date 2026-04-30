"""Wraps page drafts in YAML frontmatter and JSON-LD schema."""
import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Optional

from rich.console import Console

console = Console()


def format_page(
    draft: str,
    intent: dict[str, Any],
    keyword: str,
    scorecard: dict[str, Any],
    output_path: Optional[Path] = None,
) -> str:
    """Wrap a page draft with YAML frontmatter, JSON-LD schema, and SEO scorecard.

    Args:
        draft: Raw markdown page content from generator.py.
        intent: Structured intent dict for metadata fields.
        keyword: Target keyword for frontmatter.
        scorecard: SEO score dict from scorer.py.
        output_path: If provided, write result to this file path.

    Returns:
        Final markdown string with frontmatter and schema appended.
    """
    frontmatter = _build_frontmatter(draft, keyword, intent)
    schema_block = _build_json_ld(draft, keyword)
    scorecard_comment = _build_scorecard_comment(scorecard)

    final = f"{frontmatter}\n{draft}\n\n{schema_block}\n\n{scorecard_comment}"

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(final, encoding="utf-8")
        console.print(f"[green]Page written to:[/green] {output_path}")

    return final


def _build_frontmatter(draft: str, keyword: str, intent: dict) -> str:
    """Build YAML frontmatter block from intent data."""
    title_match = re.search(r"^# (.+)", draft, re.MULTILINE)
    title = title_match.group(1) if title_match else keyword.title()
    today = date.today().isoformat()
    persona = intent.get("buyer_persona", "")[:80]

    return f"""---
title: "{title}"
meta_description: "A complete guide to {keyword} for {persona}."
target_keyword: "{keyword}"
date: "{today}"
---
"""


def _build_json_ld(draft: str, keyword: str) -> str:
    """Build a JSON-LD Article schema block."""
    title_match = re.search(r"^# (.+)", draft, re.MULTILINE)
    title = title_match.group(1) if title_match else keyword.title()
    today = date.today().isoformat()

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "keywords": keyword,
        "datePublished": today,
        "author": {"@type": "Organization", "name": "signal-to-page"},
    }

    return f"```json-ld\n{json.dumps(schema, indent=2)}\n```"


def _build_scorecard_comment(scorecard: dict) -> str:
    """Format the SEO scorecard as a markdown comment."""
    lines = ["<!-- SEO Scorecard"]
    for key, value in scorecard.items():
        if isinstance(value, dict):
            status = "PASS" if value.get("pass") else "FAIL"
            lines.append(f"  {key}: {value.get('value')} [{status}]")
        else:
            lines.append(f"  overall: {value}")
    lines.append("-->")
    return "\n".join(lines)
