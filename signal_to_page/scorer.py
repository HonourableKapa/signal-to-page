"""Evaluates generated page content against basic SEO quality signals."""
import re
from typing import Any


def score_page(markdown: str, keyword: str, paa_questions: list[str]) -> dict[str, Any]:
    """Score a markdown page against SEO quality signals.

    Args:
        markdown: Raw markdown string of the generated page.
        keyword: Target keyword the page is optimised for.
        paa_questions: List of PAA questions from the research phase.

    Returns:
        Dict with pass/fail scores for each signal and an overall grade.
    """
    word_count = len(markdown.split())
    h2_count = len(re.findall(r"^## .+", markdown, re.MULTILINE))
    keyword_in_title = keyword.lower() in _extract_title(markdown).lower()
    paa_coverage = _calculate_paa_coverage(markdown, paa_questions)

    scores: dict[str, Any] = {
        "word_count": {"value": word_count, "pass": word_count >= 1000},
        "h2_count": {"value": h2_count, "pass": h2_count >= 3},
        "keyword_in_title": {"value": keyword_in_title, "pass": keyword_in_title},
        "paa_coverage": {
            "value": round(paa_coverage, 2),
            "pass": paa_coverage >= 0.5 if paa_questions else True,
        },
    }

    passed = sum(1 for s in scores.values() if s.get("pass"))
    scores["overall"] = f"{passed}/{len(scores)}"
    return scores


def _extract_title(markdown: str) -> str:
    """Extract the first H1 heading from markdown."""
    match = re.search(r"^# (.+)", markdown, re.MULTILINE)
    return match.group(1) if match else ""


def _calculate_paa_coverage(markdown: str, paa_questions: list[str]) -> float:
    """Calculate what fraction of PAA questions appear in the page content."""
    if not paa_questions:
        return 1.0
    covered = sum(1 for q in paa_questions if q.lower()[:40] in markdown.lower())
    return covered / len(paa_questions)
