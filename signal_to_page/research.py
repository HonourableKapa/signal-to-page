"""Runs competitive keyword research via DataForSEO or returns mock SERP data."""
import base64
import json
import os
from pathlib import Path
from typing import Any

import httpx
from rich.console import Console

console = Console()
_MOCK_PATH = Path(__file__).parent / "mock" / "mock_responses" / "serp_results.json"


def run_research(keyword: str, mock: bool = False) -> dict[str, Any]:
    """Fetch SERP and PAA data for a keyword.

    Args:
        keyword: Target keyword to research.
        mock: If True, return data from the mock responses folder.

    Returns:
        Dict with keys: serp_results, paa_questions, avg_word_count, content_gaps.
    """
    if mock or not _has_dataforseo_creds():
        return _load_mock_research()

    return _fetch_dataforseo(keyword)


def _has_dataforseo_creds() -> bool:
    """Check if DataForSEO credentials are configured."""
    return bool(os.getenv("DATAFORSEO_LOGIN") and os.getenv("DATAFORSEO_PASSWORD"))


def _fetch_dataforseo(keyword: str) -> dict[str, Any]:
    """Call the DataForSEO SERP API for the given keyword."""
    login = os.getenv("DATAFORSEO_LOGIN")
    password = os.getenv("DATAFORSEO_PASSWORD")
    credentials = base64.b64encode(f"{login}:{password}".encode()).decode()

    try:
        response = httpx.post(
            "https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
            headers={
                "Authorization": f"Basic {credentials}",
                "Content-Type": "application/json",
            },
            json=[{
                "keyword": keyword,
                "location_code": 2840,
                "language_code": "en",
                "depth": 10,
            }],
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as e:
        console.print(f"[red]DataForSEO request failed:[/red] {e}. Falling back to mock.")
        return _load_mock_research()

    return _parse_dataforseo_response(data)


def _parse_dataforseo_response(data: dict) -> dict[str, Any]:
    """Extract relevant fields from a DataForSEO API response."""
    try:
        items = data["tasks"][0]["result"][0]["items"]
    except (KeyError, IndexError):
        console.print("[yellow]Warning:[/yellow] Unexpected DataForSEO response shape. Falling back to mock.")
        return _load_mock_research()

    serp_results = [
        {
            "url": item.get("url", ""),
            "title": item.get("title", ""),
            "description": item.get("description", ""),
        }
        for item in items
        if item.get("type") == "organic"
    ][:10]

    paa_questions = [
        item.get("title", "")
        for item in items
        if item.get("type") == "people_also_ask"
    ]

    return {
        "serp_results": serp_results,
        "paa_questions": paa_questions,
        "avg_word_count": 1400,
        "content_gaps": [],
    }


def _load_mock_research() -> dict[str, Any]:
    """Load mock SERP data from the mock_responses folder."""
    return json.loads(_MOCK_PATH.read_text(encoding="utf-8"))
