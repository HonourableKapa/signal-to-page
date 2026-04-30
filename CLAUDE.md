# CLAUDE.md — signal-to-page

## What this project does

`signal-to-page` is a Python CLI tool that takes a real-world GTM signal — a job posting URL,
a LinkedIn company update, or a funding announcement — and converts it into either a full
publish-ready SEO page draft or a structured content brief.

It connects signal monitoring → keyword intent → competitive research → content production
in a single command.

---

## Module responsibilities

| File | What it does |
|------|--------------|
| `cli.py` | Entry point. Typer app. Accepts signal input (URL or text), output format flag (`--page` / `--brief`), optional `--output` path, and `--mock` flag. |
| `parser.py` | Ingests the signal. If a URL is passed, scrapes it with httpx + BeautifulSoup. If text is passed, uses it directly. Returns a clean text blob. |
| `intent.py` | Sends the parsed signal to Claude API. Extracts: company context, inferred buyer persona, business motion, and a single target keyword with supporting rationale. |
| `research.py` | Takes the target keyword and runs competitive research. In live mode: DataForSEO API. In mock mode: returns realistic fake SERP data from `mock/mock_responses/`. |
| `generator.py` | Sends keyword + research data to Claude API. Produces either a full markdown SEO page or a minimal JSON brief, depending on the mode. |
| `scorer.py` | Evaluates the generated page output against basic SEO quality signals (word count, heading structure, PAA coverage, keyword presence). Returns a scorecard dict. |
| `formatters/markdown.py` | Wraps the page draft in YAML frontmatter + JSON-LD schema. Writes or prints final markdown. |
| `formatters/json_brief.py` | Serialises the brief output to clean JSON for piping into Clay, n8n, or other tools. |
| `mock/` | Sample signals (job posting, LinkedIn update, funding announcement) and fake SERP/keyword API responses. Used when `--mock` flag is passed or API keys are absent. |

---

## Tech stack

- Python 3.11+
- `typer` — CLI framework
- `httpx` — HTTP requests for URL scraping
- `beautifulsoup4` — HTML parsing
- `anthropic` — Claude API client (signal parsing, content generation)
- `python-dotenv` — API key management from `.env`
- `rich` — terminal output formatting

---

## API keys

Stored in `.env` at project root. See `.env.example`.

```
ANTHROPIC_API_KEY=your_key_here
DATAFORSEO_LOGIN=optional
DATAFORSEO_PASSWORD=optional
```

If `DATAFORSEO_LOGIN` is absent, the tool automatically falls back to mock mode for research.

---

## CLI usage

```bash
# From a URL
signal-to-page --url "https://jobs.lever.co/example/vp-sales-enablement" --page

# From pasted text
signal-to-page --text "Acme Corp just raised $40M Series B to expand their RevOps platform..." --brief

# Write to file
signal-to-page --url "..." --page --output ./output/page-draft.md

# Force mock mode (no API keys needed)
signal-to-page --url "..." --page --mock
```

---

## Output formats

### `--page` (default)
Full markdown file with:
- YAML frontmatter (title, meta description, target keyword, date)
- H1, intro, body sections (structured around SERP gaps)
- FAQ section using People Also Ask data
- JSON-LD schema block
- Quality scorecard comment at end of file

### `--brief`
Minimal JSON:
```json
{
  "target_keyword": "...",
  "intent": "...",
  "buyer_persona": "...",
  "recommended_word_count": 1400,
  "competitor_urls": [...],
  "paa_questions": [...],
  "content_gaps": [...],
  "suggested_title": "..."
}
```

---

## Coding conventions

- All functions have docstrings
- Errors are caught at module boundaries and surfaced with `rich` console messages — never silent failures
- Mock mode is toggled via `MOCK=true` in `.env` or `--mock` CLI flag
- No global state — each module is a pure function or class that takes inputs and returns outputs
- Keep Claude prompts in a separate `prompts/` folder as `.txt` files — do not hardcode them inline
- Type hints on all function signatures

---

## What "done" looks like per module

- `parser.py` — given any URL or text blob, returns clean plain text, no HTML artifacts
- `intent.py` — returns a structured dict with `keyword`, `intent_type`, `buyer_persona`, `business_signal`
- `research.py` — returns a dict with `serp_results`, `paa_questions`, `avg_word_count`, `content_gaps`
- `generator.py` — returns raw markdown string (page mode) or dict (brief mode)
- `scorer.py` — returns dict with pass/fail scores for: word count, h2 count, keyword in title, PAA coverage
- `formatters/` — writes or returns final output with no side effects beyond the intended file write
