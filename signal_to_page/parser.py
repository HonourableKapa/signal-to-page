"""Ingests signals from URLs or raw text and returns clean plain text."""
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from rich.console import Console

console = Console()


def parse_signal(url: Optional[str] = None, text: Optional[str] = None) -> str:
    """Parse a signal from a URL or raw text and return clean plain text.

    Args:
        url: URL to scrape for signal content.
        text: Raw text signal to use directly.

    Returns:
        Clean plain text string with no HTML artifacts.

    Raises:
        ValueError: If neither url nor text is provided.
    """
    if url:
        return _scrape_url(url)
    if text:
        return _clean_text(text)
    raise ValueError("Either url or text must be provided.")


def _scrape_url(url: str) -> str:
    """Scrape a URL and return its visible text content."""
    try:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=15.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; signal-to-page/0.1)"},
        )
        response.raise_for_status()
    except httpx.HTTPError as e:
        console.print(f"[red]Error fetching URL:[/red] {e}")
        raise

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    return _clean_text(soup.get_text(separator=" ", strip=True))


def _clean_text(text: str) -> str:
    """Normalise whitespace and strip empty lines from text."""
    lines = (line.strip() for line in text.splitlines())
    return "\n".join(line for line in lines if line)
