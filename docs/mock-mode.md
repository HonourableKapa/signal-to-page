# Mock Mode

Mock mode lets you run the full signal-to-page pipeline without any API keys. It is designed for development, testing, and demonstrations.

---

## When Mock Mode Activates

Mock mode is triggered by any of three conditions, checked in this order:

1. **`--mock` CLI flag** — explicitly passed by the user
2. **`MOCK=true` in `.env`** — set in your environment file
3. **Missing DataForSEO credentials** — if `DATAFORSEO_LOGIN` is absent, `research.py` automatically falls back to mock SERP data (but Claude calls in `intent.py` and `generator.py` still run unless `--mock` is also set)

---

## What Mock Mode Does

| Module | Mock behaviour |
|--------|---------------|
| `intent.py` | Returns a hardcoded intent dict (RevOps VP persona) |
| `research.py` | Loads `signal_to_page/mock/mock_responses/serp_results.json` |
| `generator.py` | Returns a minimal placeholder markdown page |

The `parser.py`, `scorer.py`, and `formatters/` modules are not affected by mock mode — they always run on real data.

---

## Running in Mock Mode

```bash
# Explicit mock flag
signal-to-page --url "https://example.com/job-posting" --page --mock

# Via environment variable
echo "MOCK=true" >> .env
signal-to-page --url "https://example.com/job-posting" --page

# Using a local sample signal file
signal-to-page --text "$(cat signal_to_page/mock/signal_samples/job_posting.txt)" --page --mock
```

---

## Sample Signal Files

Three sample signals are included in `signal_to_page/mock/signal_samples/`:

| File | Signal type |
|------|------------|
| `job_posting.txt` | VP of Sales Enablement job ad at a Series B RevOps company |
| `linkedin_update.txt` | LinkedIn funding announcement post |
| `funding_announcement.txt` | Formal press release for a $40M Series B |

These cover the three main GTM signal types the tool is designed to handle.

---

## Mock Response Files

`signal_to_page/mock/mock_responses/serp_results.json` contains realistic SERP data for the keyword `revenue operations software for mid-market`, including:

- 5 organic results with URLs, titles, and descriptions
- 5 PAA questions
- Average word count (1850)
- 4 identified content gaps

To test with a different keyword context, edit this file or add additional response files and update the path in `research.py`.

---

## Adding New Mock Responses

To add a new mock scenario:

1. Create a new file in `signal_to_page/mock/mock_responses/`, e.g. `serp_results_sales_ops.json`
2. Match the structure of the existing `serp_results.json`
3. Update `research._load_mock_research()` to select the right file, or add a parameter to `run_research()` to accept a mock file path
