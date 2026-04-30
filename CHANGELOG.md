# Changelog

All notable changes to signal-to-page will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0] — unreleased

### Added
- Initial CLI with `--url`, `--text`, `--page`, `--brief`, `--output`, `--mock` flags
- Signal parser: URL scraping (httpx + BeautifulSoup) and raw text input
- Intent mapping via Claude API
- Mock research layer with realistic SERP/keyword data
- Page generator: full markdown with YAML frontmatter and JSON-LD schema
- Brief generator: minimal JSON output for Clay/n8n piping
- Quality scorecard on page output
- Rich terminal output
- Mock mode — runs full pipeline without any API keys
