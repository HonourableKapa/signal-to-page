"""Extracts keyword intent and buyer context from a parsed signal using Claude."""
import json
from pathlib import Path
from typing import Any

import anthropic
from rich.console import Console

console = Console()
_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "intent.txt"


def extract_intent(signal_text: str, mock: bool = False) -> dict[str, Any]:
    """Send the signal text to Claude and extract structured intent data.

    Args:
        signal_text: Clean plain-text signal to analyse.
        mock: If True, return a hardcoded mock response.

    Returns:
        Dict with keys: keyword, intent_type, buyer_persona, business_signal.
    """
    if mock:
        return _mock_intent()

    prompt_template = _PROMPT_PATH.read_text(encoding="utf-8")
    prompt = prompt_template.replace("{{SIGNAL}}", signal_text)

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
        console.print("[yellow]Warning:[/yellow] Claude returned non-JSON intent. Attempting partial parse.")
        return _parse_fallback(raw)


def _mock_intent() -> dict[str, Any]:
    """Return a realistic mock intent response for testing."""
    return {
        "keyword": "revenue operations software for mid-market",
        "intent_type": "commercial investigation",
        "buyer_persona": "VP of Revenue Operations at a 200–500 person B2B SaaS company",
        "business_signal": "Series B funding round to expand RevOps platform",
    }


def _parse_fallback(raw: str) -> dict[str, Any]:
    """Attempt to return a minimal valid structure from malformed Claude output."""
    return {
        "keyword": "",
        "intent_type": "unknown",
        "buyer_persona": "",
        "business_signal": raw[:500],
    }
