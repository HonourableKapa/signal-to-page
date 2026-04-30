"""Entry point for the signal-to-page CLI."""
import os
from pathlib import Path
from typing import Optional

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from signal_to_page import parser, intent, research, generator, scorer
from signal_to_page.formatters import markdown as md_formatter
from signal_to_page.formatters import json_brief as brief_formatter

load_dotenv()

app = typer.Typer(help="Convert GTM signals into SEO pages or content briefs.")
console = Console()


@app.command()
def main(
    url: Optional[str] = typer.Option(None, "--url", help="URL of the signal to parse."),
    text: Optional[str] = typer.Option(None, "--text", help="Raw signal text to parse."),
    page: bool = typer.Option(False, "--page", help="Output a full SEO page draft (default)."),
    brief: bool = typer.Option(False, "--brief", help="Output a structured content brief."),
    output: Optional[Path] = typer.Option(None, "--output", help="File path to write output to."),
    mock: bool = typer.Option(False, "--mock", help="Use mock data instead of live APIs."),
) -> None:
    """Convert a GTM signal into an SEO page or content brief."""
    if not url and not text:
        console.print("[red]Error:[/red] Provide either --url or --text.")
        raise typer.Exit(1)

    if page and brief:
        console.print("[red]Error:[/red] Use either --page or --brief, not both.")
        raise typer.Exit(1)

    use_mock = mock or os.getenv("MOCK", "false").lower() == "true"
    output_mode = "brief" if brief else "page"

    with Progress(SpinnerColumn(), TextColumn("{task.description}"), console=console) as progress:
        task = progress.add_task("Parsing signal...", total=None)

        signal_text = parser.parse_signal(url=url, text=text)

        progress.update(task, description="Extracting intent...")
        intent_data = intent.extract_intent(signal_text, mock=use_mock)

        progress.update(task, description="Running competitive research...")
        research_data = research.run_research(intent_data["keyword"], mock=use_mock)

        progress.update(task, description="Generating content...")
        if output_mode == "page":
            draft = generator.generate_page(
                intent_data["keyword"], intent_data, research_data, mock=use_mock
            )
            progress.update(task, description="Scoring output...")
            scorecard = scorer.score_page(
                draft, intent_data["keyword"], research_data.get("paa_questions", [])
            )
            result = md_formatter.format_page(
                draft, intent_data, intent_data["keyword"], scorecard, output_path=output
            )
        else:
            brief_data = generator.generate_brief(
                intent_data["keyword"], intent_data, research_data
            )
            result = brief_formatter.format_brief(brief_data, output_path=output)

        progress.update(task, description="Done.")

    if not output:
        console.print(result)


if __name__ == "__main__":
    app()
