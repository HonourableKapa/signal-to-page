# signal-to-page

A Python CLI tool that converts a real-world GTM signal into a keyword-targeted SEO page or content brief — in a single command.

---

## The problem

Most content teams write pages based on keyword lists built months ago. Most GTM teams monitor signals but do nothing with them from a content angle.

The gap between _"this company just posted a VP of Sales Enablement role"_ and _"we should own the keyword those buyers are searching right now"_ is currently a manual, slow, expensive process — if it happens at all.

`signal-to-page` closes that gap.

---

## How it works

```
Signal in → Parse → Intent mapping → Keyword research → Content out
```

1. You pass in a signal: a job posting URL, a block of LinkedIn text, or a funding announcement
2. Claude extracts the business context and infers keyword intent
3. The tool runs a competitive research pipeline against that keyword (live or mock)
4. Output is either a full publish-ready SEO page draft or a structured JSON brief

---

## Install

```bash
git clone https://github.com/yourusername/signal-to-page.git
cd signal-to-page
pip install -e .
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env
```

---

## Usage

```bash
# From a job posting URL — output a full page
signal-to-page --url "https://jobs.lever.co/example/vp-sales-enablement" --page

# From pasted text — output a content brief
signal-to-page --text "Acme Corp just raised $40M Series B..." --brief

# Save output to file
signal-to-page --url "..." --page --output ./output/draft.md

# Run without any API keys (mock mode)
signal-to-page --url "..." --page --mock
```

---

## Output formats

### `--page`
Full markdown file with YAML frontmatter, structured body, FAQ section, JSON-LD schema, and a quality scorecard.

```yaml
---
title: "Best Sales Enablement Software for Enterprise Teams"
meta_description: "..."
target_keyword: "sales enablement software enterprise"
date: 2025-01-15
---
```

### `--brief`
Minimal JSON for piping into Clay, n8n, or any downstream workflow.

```json
{
  "target_keyword": "sales enablement software enterprise",
  "intent": "commercial investigation",
  "buyer_persona": "VP of Sales / RevOps lead at 200-500 person company",
  "recommended_word_count": 1600,
  "paa_questions": [...],
  "content_gaps": [...],
  "suggested_title": "..."
}
```

---

## Signal types supported

| Signal | Input method |
|--------|-------------|
| Job posting | `--url` (scraped automatically) |
| LinkedIn company update | `--text` (paste the post body) |
| Funding announcement | `--url` or `--text` |
| Any B2B business event | `--text` |

---

## Mock mode

Run the full pipeline without any API keys. Useful for testing, demos, and development.

```bash
signal-to-page --url "..." --page --mock
```

Mock mode uses sample signals and pre-built SERP responses from `signal_to_page/mock/`.

See [docs/mock-mode.md](docs/mock-mode.md) for details.

---

## API keys

```bash
# .env
ANTHROPIC_API_KEY=your_key_here
DATAFORSEO_LOGIN=optional        # falls back to mock if absent
DATAFORSEO_PASSWORD=optional
```

If DataForSEO credentials are missing, the research layer runs in mock mode automatically.

---

## Who it's for

- **GTM engineers** running signal-based or ABM outreach who want content that matches the buyer's moment
- **Growth marketers** who want to move faster on topical authority
- **SEO teams** who want to tie content production directly to market activity
- **Agencies** who want to pipe briefs into existing Clay or n8n workflows

---

## Examples

See [examples/](examples/) for sample outputs from each signal type:
- [Job posting → page draft](examples/job-posting-example.md)
- [Funding announcement → brief](examples/funding-announcement-example.md)
- [LinkedIn update → page draft](examples/linkedin-update-example.md)

---

## Tech stack

- Python 3.11+
- [Typer](https://typer.tiangolo.com/) — CLI
- [httpx](https://www.python-httpx.org/) + [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — scraping
- [Anthropic Python SDK](https://github.com/anthropic-ai/sdk-python) — signal parsing + content generation
- [DataForSEO API](https://dataforseo.com/) — live SERP and keyword data (optional)
- [Rich](https://github.com/Textualize/rich) — terminal output

---

## Roadmap

- [ ] Batch mode — process multiple signals from a CSV
- [ ] Clay HTTP action integration (webhook endpoint)
- [ ] Competitor gap scoring against live URLs
- [ ] Support for G2 review signals
- [ ] Slack/n8n webhook output

---

## License

MIT
