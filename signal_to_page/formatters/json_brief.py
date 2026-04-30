"""Serialises brief output to clean JSON for downstream tooling."""
import json
from pathlib import Path
from typing import Any, Optional

from rich.console import Console

console = Console()


def format_brief(
    brief: dict[str, Any],
    output_path: Optional[Path] = None,
) -> str:
    """Serialise a brief dict to formatted JSON.

    Args:
        brief: Content brief dict from generator.py.
        output_path: If provided, write JSON to this file path.

    Returns:
        Formatted JSON string.
    """
    output = json.dumps(brief, indent=2, ensure_ascii=False)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(output, encoding="utf-8")
        console.print(f"[green]Brief written to:[/green] {output_path}")

    return output
