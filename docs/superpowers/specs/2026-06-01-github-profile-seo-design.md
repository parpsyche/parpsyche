# GitHub Profile README SEO Overhaul — Design Spec

**Date:** 2026-06-01
**Phase:** 1 of 2 (Phase 2: Personal site / GitHub Pages — separate spec)
**Goal:** Make Parth Sachdeva's GitHub profile discoverable by search engines for both name-based queries ("Parth Sachdeva", "parpsyche") and skill-based queries ("Python developer", "AI engineer") while maintaining a visually distinctive terminal-style aesthetic.

---

## Problem

The current profile README stores all meaningful content (name, skills, contact, hobbies, stats) inside SVG images (`dark_mode.svg`, `light_mode.svg`). GitHub renders these as `<img>` tags. Search engines cannot read text inside SVGs rendered as images. The README itself has roughly 15 words of crawlable text. This makes the profile nearly invisible to Google and GitHub search.

## Approach

**Code-block terminal with semantic markdown.** Replace the SVG profile cards with an `ini`-formatted fenced code block that mimics the terminal/neofetch look. Surround the code block with keyword-rich markdown headings and paragraphs that carry full SEO weight. Keep the contribution snake and 30-day stats chart as SVG images (they are supplementary visuals, not text-heavy content).

## Target Keywords

Each keyword appears 2-3 times across the page in natural context. No keyword stuffing.

| Keyword | Placement |
|---|---|
| Parth Sachdeva | H1 heading, bio paragraph, alt text on images |
| parpsyche | H1 heading, bio paragraph, code block, repo description, repo topics |
| Python Developer | H1 heading, bio paragraph, Tech Stack section |
| AI Engineer | H1 heading, bio paragraph, What I'm Building section |
| Full Stack Builder | H1 heading, bio paragraph |

---

## README Structure

The new README has two layers:

1. **Semantic text layer** — Markdown headings (`<h1>`, `<h3>`), paragraphs, and lists. This is what search engines read and rank.
2. **Visual layer** — An `ini`-formatted code block for the terminal aesthetic, plus SVG images for contribution graphs. Crawlable but lower semantic weight.

### Section Order

```
1. H1: "Parth Sachdeva (parpsyche) — Full Stack Builder | Python Developer | AI Engineer"
2. Bio paragraph (2-3 sentences with target keywords)
3. Code block: ini-formatted neofetch-style card
   - [parpsyche] section: name, handle, role
   - [stats] section: repos, stars, followers, following, uptime (auto-updated)
   - [languages] section: programming, markup, spoken
   - [hobbies] section: software, hardware
   - [contact] section: email, LinkedIn, Twitter, GitHub
4. H3: "Tech Stack" — markdown list of languages and tools
5. H3: "What I'm Building" — 2-3 sentences about current focus
6. H3: "Contribution Graph" — snake SVG (from output branch)
7. H3: "Contribution Stats" — 30-day chart SVG (from output branch)
8. H3: "Connect" — markdown links to email, LinkedIn, Twitter, GitHub
```

### Code Block Format

Using `ini` language hint for syntax highlighting:

```ini
; parth@sachdeva ~ $ neofetch
; ─────────────────────────────────────────
[parpsyche]
Name       = Parth Sachdeva
Handle     = parpsyche
Role       = Full Stack Builder | Python Developer | AI Engineer

[stats]
Repos      = 15
Stars      = 12
Followers  = 4
Following  = 7
Uptime     = 25 years, 10 months, 24 days

[languages]
Programming = Python, JavaScript, Go
Markup      = HTML, CSS, JSON, YAML
Spoken      = English, Hindi

[hobbies]
Software   = Android Modding, Beatbox, Drums
Hardware   = Arduino, Raspberry Pi, Bare Metal, NUCs, SFF

[contact]
Personal   = parthsachdeva14@gmail.com
Work       = parth@infiswift.tech
LinkedIn   = parpsyche
Twitter    = parpsyche
GitHub     = parpsyche
```

Values in the `[stats]` section are auto-updated by the GitHub Actions workflow every 6 hours.

---

## SEO Optimizations Beyond README

### Repository Metadata

- **Description:** `"Parth Sachdeva (parpsyche) — Full Stack Builder, Python Developer, AI Engineer. GitHub profile README."`
- **Topics:** `parpsyche`, `parth-sachdeva`, `python-developer`, `ai-engineer`, `profile-readme`, `github-profile`

### Improved Alt Text on SVG Images

| Image | Current alt text | New alt text |
|---|---|---|
| Contribution snake | `github contribution grid snake animation` | `parpsyche GitHub contribution activity snake animation` |
| 30-day stats chart | `Weekly combined tech stats` | `parpsyche 30-day combined contribution stats across GitHub accounts` |

---

## Workflow Changes

### `update-github-stats.yml` — Modified

**Schedule:** Every 6 hours (unchanged: `cron: "0 */6 * * *"`)

**Changes:**
- Remove "Update dark_mode.svg" and "Update light_mode.svg" steps
- Add "Update README.md" step that uses `sed` to replace values in the code block:
  ```bash
  sed -i "s/^Repos      = .*/Repos      = $repos/" README.md
  sed -i "s/^Stars      = .*/Stars      = $stars/" README.md
  sed -i "s/^Followers  = .*/Followers  = $followers/" README.md
  sed -i "s/^Following  = .*/Following  = $following/" README.md
  sed -i "s/^Uptime     = .*/Uptime     = $uptime/" README.md
  ```
- Commit step updated: `git add README.md github-stats.min.json`

### `snake.yml` — No changes

### `combined-stats.yml` — No changes

---

## File Changes Summary

| File | Action |
|---|---|
| `README.md` | Full rewrite |
| `dark_mode.svg` | Delete |
| `light_mode.svg` | Delete |
| `.github/workflows/update-github-stats.yml` | Retarget sed from SVGs to README.md |
| `.github/workflows/snake.yml` | No change |
| `.github/workflows/combined-stats.yml` | No change |
| `scripts/generate_combined_stats.py` | No change |
| `github-stats.min.json` | No change (kept as data artifact) |
| Repo description (via `gh repo edit`) | Set keyword-rich description |
| Repo topics (via `gh repo edit`) | Add SEO-relevant topic tags |

---

## Out of Scope (Phase 2)

- Personal website / GitHub Pages with custom domain
- Schema.org structured data markup
- Google Search Console registration
- Custom domain SEO
