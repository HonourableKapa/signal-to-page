# How signal-to-page Works

signal-to-page is a five-stage pipeline that converts a real-world GTM signal into a publish-ready SEO page or content brief.

---

## The Pipeline

```
Signal Input → Parser → Intent → Research → Generator → Scorer → Formatter → Output
```

### Stage 1: Parse (`parser.py`)

The tool accepts either a URL or raw text as input.

- **URL mode**: httpx fetches the page, BeautifulSoup strips navigation, scripts, and boilerplate, and the visible text is returned as a clean blob.
- **Text mode**: The input is normalised (whitespace collapsed, empty lines removed) and returned directly.

Output: a plain-text string with no HTML artifacts.

---

### Stage 2: Extract Intent (`intent.py`)

The cleaned signal text is sent to Claude with a structured prompt (`prompts/intent.txt`). Claude returns a JSON object identifying:

- **keyword** — a 4–7 word long-tail phrase the ideal buyer would search
- **intent_type** — informational / commercial investigation / transactional / navigational
- **buyer_persona** — role, company stage, and problem context
- **business_signal** — one-sentence summary of what the GTM signal reveals

---

### Stage 3: Competitive Research (`research.py`)

The extracted keyword is passed to the DataForSEO SERP API (or mock data in mock mode). This returns:

- **serp_results** — top 10 organic results with URL, title, and description
- **paa_questions** — People Also Ask questions from the SERP
- **avg_word_count** — average word count of top-ranking pages
- **content_gaps** — topics present in the SERP but missing from competitors

If DataForSEO credentials are absent, the tool automatically falls back to mock SERP data.

---

### Stage 4: Generate Content (`generator.py`)

The keyword, intent data, and research data are interpolated into a prompt template and sent to Claude.

- **Page mode** (`prompts/page.txt`): Claude writes a full markdown article — H1, intro, 3–5 H2 sections, FAQ section — targeting the buyer persona and addressing content gaps.
- **Brief mode** (`prompts/brief.txt`): Claude returns a structured JSON brief for use in content workflows.

---

### Stage 5: Score (`scorer.py`)

In page mode, the generated markdown is evaluated against four SEO signals:

| Signal | Pass Condition |
|--------|---------------|
| word_count | ≥ 1000 words |
| h2_count | ≥ 3 H2 headings |
| keyword_in_title | keyword appears in H1 |
| paa_coverage | ≥ 50% of PAA questions addressed |

---

### Stage 6: Format and Output (`formatters/`)

**Page mode** (`formatters/markdown.py`):
- Prepends YAML frontmatter (title, meta description, keyword, date)
- Appends a JSON-LD Article schema block
- Appends an HTML comment with the SEO scorecard

**Brief mode** (`formatters/json_brief.py`):
- Serialises the brief dict to pretty-printed JSON

Both formatters write to a file if `--output` is provided, or print to stdout.

---

## Data Flow Diagram

```
CLI (cli.py)
  │
  ├── parser.parse_signal(url | text)
  │     └── returns: str
  │
  ├── intent.extract_intent(signal_text)
  │     └── returns: {keyword, intent_type, buyer_persona, business_signal}
  │
  ├── research.run_research(keyword)
  │     └── returns: {serp_results, paa_questions, avg_word_count, content_gaps}
  │
  ├── generator.generate_page/brief(keyword, intent, research)
  │     └── returns: str (page) | dict (brief)
  │
  ├── scorer.score_page(markdown, keyword, paa_questions)   [page mode only]
  │     └── returns: {word_count, h2_count, keyword_in_title, paa_coverage, overall}
  │
  └── formatters.format_page/brief(...)
        └── returns: str, optionally writes to file
```
