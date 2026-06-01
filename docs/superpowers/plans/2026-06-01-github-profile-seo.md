# GitHub Profile SEO Overhaul — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace SVG-based profile content with crawlable markdown + ini code block, update the GitHub Actions workflow to target README.md, and set SEO-optimized repo metadata.

**Architecture:** The README gets a full rewrite: semantic markdown sections (H1, H3, paragraphs, lists) for SEO weight, plus an ini-formatted code block for terminal-style visual appeal. The existing `update-github-stats.yml` workflow is retargeted from SVG files to README.md. SVG files are deleted. Contribution snake and 30-day stats SVGs (on the `output` branch) are kept unchanged.

**Tech Stack:** Markdown, GitHub Actions (YAML), `sed`, `gh` CLI

**Spec:** `docs/superpowers/specs/2026-06-01-github-profile-seo-design.md`

---

### Task 1: Rewrite README.md

**Files:**
- Modify: `README.md` (full rewrite — all 38 lines replaced)

- [ ] **Step 1: Replace README.md with the new SEO-optimized content**

Write the entire new README.md with this exact content:

```markdown
# Parth Sachdeva (parpsyche) — Full Stack Builder | Python Developer | AI Engineer

I'm Parth, also known as **parpsyche** — a full-time builder working at the intersection of AI, IoT, and software engineering. I write Python, JavaScript, and Go, and I'm always building something new.

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

### Tech Stack

**Languages:** Python, JavaScript, Go  
**Markup:** HTML, CSS, JSON, YAML  
**Hardware:** Arduino, Raspberry Pi, NUCs, SFF builds

### What I'm Building

Currently focused on AI engineering and IoT systems at Infiswift. Building tools and side projects in Python and Go.

### 🐍 Contribution Graph

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/parpsyche/parpsyche/output/github-contribution-grid-snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/parpsyche/parpsyche/output/github-contribution-grid-snake.svg">
    <img alt="parpsyche GitHub contribution activity snake animation" src="https://raw.githubusercontent.com/parpsyche/parpsyche/output/github-contribution-grid-snake.svg">
  </picture>
</div>

### 📈 Contribution Stats

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/parpsyche/parpsyche/output/combined-tech-stats-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/parpsyche/parpsyche/output/combined-tech-stats.svg">
    <img alt="parpsyche 30-day combined contribution stats across GitHub accounts" src="https://raw.githubusercontent.com/parpsyche/parpsyche/output/combined-tech-stats.svg">
  </picture>
</div>

### Connect

- **Email:** [parthsachdeva14@gmail.com](mailto:parthsachdeva14@gmail.com)
- **Work:** [parth@infiswift.tech](mailto:parth@infiswift.tech)
- **LinkedIn:** [parpsyche](https://linkedin.com/in/parpsyche)
- **Twitter:** [@parpsyche](https://x.com/parpsyche)
- **GitHub:** [parpsyche](https://github.com/parpsyche)
```

- [ ] **Step 2: Verify the README renders correctly**

Open the README in a markdown previewer or check with:

Run: `cat README.md | head -5`
Expected output:
```
# Parth Sachdeva (parpsyche) — Full Stack Builder | Python Developer | AI Engineer

I'm Parth, also known as **parpsyche** — a full-time builder working at the intersection of AI, IoT, and software engineering. I write Python, JavaScript, and Go, and I'm always building something new.
```

Verify the ini code block is properly fenced (opening ` ```ini ` and closing ` ``` ` both present).

- [ ] **Step 3: Verify SEO keyword presence**

Check that each target keyword appears in crawlable text (not just inside the code block):

Run: `grep -c "Parth Sachdeva" README.md && grep -c "parpsyche" README.md && grep -c "Python" README.md && grep -c "AI" README.md`

Expected: Each count should be >= 2 (keywords appear in heading + bio + code block + sections).

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: rewrite README for SEO — replace SVG profile with markdown + ini code block"
```

---

### Task 2: Update GitHub Actions Workflow

**Files:**
- Modify: `.github/workflows/update-github-stats.yml` (lines 1, 11, 77-99)

- [ ] **Step 1: Update workflow name and job name**

In `.github/workflows/update-github-stats.yml`:

Change line 1 from:
```yaml
name: Update GitHub Stats SVG + JSON
```
to:
```yaml
name: Update GitHub Stats README + JSON
```

Change line 13 (the job name) from:
```yaml
  update_svg:
```
to:
```yaml
  update_readme:
```

- [ ] **Step 2: Replace SVG update steps with README update step**

Remove the two steps "Update dark_mode.svg" (lines 77-83) and "Update light_mode.svg" (lines 85-91).

Replace them with a single step:

```yaml
      - name: Update README.md
        run: |
          sed -i "s/^Repos      = .*/Repos      = $repos/" README.md
          sed -i "s/^Stars      = .*/Stars      = $stars/" README.md
          sed -i "s/^Followers  = .*/Followers  = $followers/" README.md
          sed -i "s/^Following  = .*/Following  = $following/" README.md
          sed -i "s/^Uptime     = .*/Uptime     = $uptime/" README.md
```

- [ ] **Step 3: Update the commit step**

Change the commit step from:

```yaml
      - name: Commit changes if any
        run: |
          if ! git diff --quiet; then
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add github-stats.min.json dark_mode.svg light_mode.svg
            git commit -m "Update GitHub stats + SVGs [skip ci]"
            git push
          else
            echo "No changes to commit"
          fi
```

to:

```yaml
      - name: Commit changes if any
        run: |
          if ! git diff --quiet; then
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add README.md github-stats.min.json
            git commit -m "Update GitHub stats [skip ci]"
            git push
          else
            echo "No changes to commit"
          fi
```

- [ ] **Step 4: Verify the final workflow YAML is valid**

Run: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/update-github-stats.yml'))" && echo "YAML valid"`

Expected: `YAML valid`

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/update-github-stats.yml
git commit -m "feat: retarget stats workflow from SVG files to README.md"
```

---

### Task 3: Delete SVG Profile Files

**Files:**
- Delete: `dark_mode.svg`
- Delete: `light_mode.svg`

- [ ] **Step 1: Remove the SVG files**

```bash
git rm dark_mode.svg light_mode.svg
```

- [ ] **Step 2: Verify no remaining references to deleted files**

Run: `grep -r "dark_mode.svg\|light_mode.svg" . --include="*.md" --include="*.yml" --include="*.yaml"`

Expected: No output (no references remain). The README rewrite in Task 1 already removed the `<picture>` block that referenced these files. The workflow rewrite in Task 2 already removed the `sed` commands and `git add` references.

- [ ] **Step 3: Commit**

```bash
git commit -m "chore: remove obsolete SVG profile cards"
```

---

### Task 4: Set Repository Metadata

**Files:** None (GitHub API via `gh` CLI)

- [ ] **Step 1: Set repo description**

```bash
gh repo edit parpsyche/parpsyche --description "Parth Sachdeva (parpsyche) — Full Stack Builder, Python Developer, AI Engineer. GitHub profile README."
```

Expected: No error output.

- [ ] **Step 2: Add repo topics**

```bash
gh repo edit parpsyche/parpsyche --add-topic parpsyche --add-topic parth-sachdeva --add-topic python-developer --add-topic ai-engineer --add-topic profile-readme --add-topic github-profile
```

Expected: No error output.

- [ ] **Step 3: Verify metadata was set**

```bash
gh repo view parpsyche/parpsyche --json description,repositoryTopics
```

Expected output should include the description and all 6 topics.

---

### Task 5: Final Verification

- [ ] **Step 1: Verify git status is clean**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

- [ ] **Step 2: Review the commit log**

```bash
git log --oneline -5
```

Expected: Three commits from this work:
```
<hash> chore: remove obsolete SVG profile cards
<hash> feat: retarget stats workflow from SVG files to README.md
<hash> feat: rewrite README for SEO — replace SVG profile with markdown + ini code block
```

- [ ] **Step 3: Push to remote**

```bash
git push origin main
```

- [ ] **Step 4: Verify the profile renders on GitHub**

Visit `https://github.com/parpsyche` in a browser and confirm:
1. The H1 heading shows with keywords
2. The ini code block renders with syntax highlighting
3. The contribution snake SVG loads
4. The 30-day stats SVG loads
5. The Connect section has working links
