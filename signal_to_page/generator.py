"""Generates SEO page drafts or content briefs using Claude."""
import json
from pathlib import Path
from typing import Any

import anthropic
from rich.console import Console

console = Console()
_PAGE_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "page.txt"
_BRIEF_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "brief.txt"


def generate_page(
    keyword: str,
    intent: dict[str, Any],
    research: dict[str, Any],
    mock: bool = False,
) -> str:
    """Generate a full markdown SEO page draft.

    Args:
        keyword: Target keyword for the page.
        intent: Structured intent data from intent.py.
        research: SERP and PAA data from research.py.
        mock: If True, return a hardcoded mock page.

    Returns:
        Raw markdown string for the page draft.
    """
    if mock:
        return _mock_page(keyword)

    prompt = _build_prompt(_PAGE_PROMPT_PATH, keyword, intent, research)
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_brief(
    keyword: str,
    intent: dict[str, Any],
    research: dict[str, Any],
) -> dict[str, Any]:
    """Generate a structured content brief.

    Args:
        keyword: Target keyword for the brief.
        intent: Structured intent data from intent.py.
        research: SERP and PAA data from research.py.

    Returns:
        Dict matching the brief JSON schema.
    """
    prompt = _build_prompt(_BRIEF_PROMPT_PATH, keyword, intent, research)
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        console.print("[yellow]Warning:[/yellow] Claude returned non-JSON brief output.")
        return {"raw": raw}


def _build_prompt(path: Path, keyword: str, intent: dict, research: dict) -> str:
    """Interpolate keyword, intent, and research data into a prompt template."""
    template = path.read_text(encoding="utf-8")
    return (
        template
        .replace("{{KEYWORD}}", keyword)
        .replace("{{INTENT}}", json.dumps(intent, indent=2))
        .replace("{{RESEARCH}}", json.dumps(research, indent=2))
    )


def _mock_page(keyword: str) -> str:
    """Return a minimal mock page draft for testing."""
    return f"""# The Complete Guide to {keyword.title()}

Everything B2B revenue teams need to know about {keyword}.

## What Is {keyword.title()}?

Placeholder section content covering the definition and core concepts.

## Why It Matters for Growing Teams

Placeholder section content covering business impact and ROI.

## How to Get Started

Placeholder section content covering implementation steps.

## Choosing the Right Tools

Placeholder section content covering evaluation criteria.

## FAQ

### What does a {keyword} team do?

Placeholder answer covering day-to-day responsibilities.

### How is {keyword} different from sales operations?

Placeholder answer covering the distinction.

### What tools do {keyword} teams use?

Placeholder answer covering the tech stack.
"""
