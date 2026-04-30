# Output Formats

signal-to-page produces two output formats, selected via CLI flag.

---

## `--page` (default)

A full publish-ready markdown file structured for SEO.

### Structure

```
---
title: "..."
meta_description: "..."
target_keyword: "..."
date: "YYYY-MM-DD"
---

# H1 Title

Intro paragraph...

## Section 1

...

## Section 2

...

## Frequently Asked Questions

### Question from PAA data?

Answer...

```json-ld
{
  "@context": "https://schema.org",
  "@type": "Article",
  ...
}
```

<!-- SEO Scorecard
  word_count: 1423 [PASS]
  h2_count: 4 [PASS]
  keyword_in_title: True [PASS]
  paa_coverage: 0.8 [PASS]
  overall: 4/4
-->
```

### Components

| Component | Source | Description |
|-----------|--------|-------------|
| YAML frontmatter | `formatters/markdown.py` | title, meta_description, target_keyword, date |
| Page body | `generator.py` + Claude | H1, intro, H2 sections, FAQ |
| JSON-LD schema | `formatters/markdown.py` | Article schema with headline, keyword, date |
| SEO scorecard | `scorer.py` + `formatters/markdown.py` | HTML comment with pass/fail signals |

### Scorecard signals

| Signal | What it checks | Pass condition |
|--------|---------------|----------------|
| `word_count` | Total word count of the page body | ≥ 1000 words |
| `h2_count` | Number of H2 headings | ≥ 3 |
| `keyword_in_title` | Whether keyword appears in the H1 | True |
| `paa_coverage` | Fraction of PAA questions addressed | ≥ 50% |

---

## `--brief`

A minimal JSON object for use in content workflows, CRM enrichment, or tools like Clay and n8n.

### Schema

```json
{
  "target_keyword": "revenue operations software for mid-market",
  "intent": "commercial investigation",
  "buyer_persona": "VP of Revenue Operations at a 200–500 person B2B SaaS company",
  "recommended_word_count": 1800,
  "competitor_urls": [
    "https://www.salesforce.com/resources/articles/revenue-operations/",
    "https://www.clari.com/blog/revenue-operations/",
    "https://www.gartner.com/en/sales/insights/revenue-operations",
    "https://www.hubspot.com/revenue-operations",
    "https://revopsco-op.com/what-is-revops/"
  ],
  "paa_questions": [
    "What does a revenue operations team do?",
    "What is the difference between RevOps and sales ops?",
    "How do you structure a RevOps team?",
    "What tools do revenue operations teams use?",
    "Is RevOps the same as business operations?"
  ],
  "content_gaps": [
    "No content covering RevOps for mid-market specifically",
    "Lack of ROI and business case content for RevOps investment",
    "Missing comparison of build vs buy for RevOps tooling",
    "No coverage of RevOps team structure at Series B stage"
  ],
  "suggested_title": "Revenue Operations Software for Mid-Market: The Complete Buyer's Guide"
}
```

### Field reference

| Field | Type | Source |
|-------|------|--------|
| `target_keyword` | string | `intent.py` |
| `intent` | string | `intent.py` |
| `buyer_persona` | string | `intent.py` |
| `recommended_word_count` | integer | `research.py` avg_word_count, rounded |
| `competitor_urls` | string[] | `research.py` serp_results |
| `paa_questions` | string[] | `research.py` |
| `content_gaps` | string[] | `research.py` |
| `suggested_title` | string | `generator.py` + Claude |

---

## Writing to a file

Both formats support the `--output` flag:

```bash
# Write page to file
signal-to-page --url "..." --page --output ./output/my-page.md

# Write brief to file
signal-to-page --url "..." --brief --output ./output/brief.json
```

Parent directories are created automatically if they do not exist.

If `--output` is omitted, the result is printed to stdout.
