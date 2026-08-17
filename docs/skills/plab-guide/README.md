# plab-guide

**Version:** 1.6.0
**Source:** [`skills/plab-guide/`](../../../skills/plab-guide/)

Generate a paired guide bundle (standard MD + ADHD MD + quick-reference HTML + 2-page PDF) for any topic. Works for software repos, tools, methodologies, frameworks, or domain knowledge.

---

## Getting Started

### Quick Start

Invoke the skill with a topic:

```
/plab-guide https://github.com/zilliztech/memsearch
/plab-guide jq
/plab-guide OKRs
/plab-guide systems thinking
```

The skill produces four artifacts in a dated output directory:

```
_output/plab-guide/<slug>-<YYYY-MM-DD>/
├── <slug>_guide-standard.md          # Technical-reference MD guide
├── <slug>_guide-adhd.md              # ADHD-optimized MD guide
├── <slug>_quick-reference.html       # 2-page HTML operator card
├── <slug>_quick-reference.pdf        # 2-page PDF (rendered locally; no LLM tokens)
└── MANIFEST.yaml                     # Machine-readable manifest
```

Plus `_work/` (intermediate research, outline) by default.

### Installation

Install via the prisant-labs marketplace:

```bash
/plugin marketplace add prisant-labs/agent-plugins
/plugin install prisant-utilities@agent-plugins
```

### Prerequisites

- A Chromium-based browser (Google Chrome, Chromium, or Microsoft Edge) for PDF rendering. Without one, the skill still produces the three text/HTML artifacts and emits an install hint for the PDF step.
- Optional: `pdfinfo` (poppler-utils) for page-count enforcement.

---

## When to Use

- A teammate or stakeholder needs to learn a new topic from scratch (a tool, a framework, a methodology).
- You want a printable, two-page operator card for a topic you reference often.
- You want to lock down what you currently know about a topic in a structured artifact you can update later.
- You're onboarding to a new repo or tool and want to absorb it efficiently with both depth and a quick-reference.

## When NOT to Use

- The topic has no authoritative sources (the skill marks `confidence: low-confidence draft` and produces an honest but thin guide).
- You want a one-paragraph summary; the skill produces a full bundle.
- You want creative or persuasive writing; the skill writes structured technical-reference prose.

---

## Three Input Types

| Input | Examples | Notes |
|-------|----------|-------|
| `repo-url` | `https://github.com/owner/repo`, `git@github.com:owner/repo` | The skill fetches README and primary docs |
| `tool` | `jq`, `pandas`, `kubectl` | The skill searches for the tool's official docs |
| `concept` | `OKRs`, `eventual consistency`, `bullet journaling`, `systems thinking` | The skill searches for canonical sources (books, papers, well-known sites) |

If classification is ambiguous (e.g., "Claude Code hooks" - is that a tool or concept?), the skill asks for confirmation. Override with `--type repo-url|tool|concept`.

---

## What's Inside Each Artifact

### Standard MD Guide

12 mandatory sections in fixed order:
1. At a Glance (8-12 row Field/Value table)
2. Table of Contents
3. Executive Summary (250-500 words, written last)
4. Official Resources (5-15 row link table)
5. 80/20 - High-Leverage Practices (5-7 numbered practices)
6. Getting Started (mental model + first step + first-session expectations)
7. Key Terms (8-20 term glossary)
8. In-Depth Breakdown (4 progressive-disclosure layers)
9. Frequently Asked Questions (>=3 categories, >=8 Q/A)
10. Similar Tools & Alternatives (comparison table)
11. Additional & Third-Party Resources
12. Sources & Evidence (citations + traceability + gaps)

Total: 1,500-6,000 words depending on topic depth.

### ADHD MD Guide

Same content as the standard guide with visual scaffolding:
- Numbered headings with `.` separator (`## 5. 80/20 - ...`, `### 5.1. ...`)
- `[TL;DR]` callout at the top of every section
- `[BOTTOM LINE]` at the end of every section
- Clickable `[QUICK NAV]` blocks in long sections
- Inline emoji-tagged callouts (📌 [KEY], 💡 [INSIGHT], ⚠️ [WARNING/GOTCHA], ⏹️ [STOP])
- Section confidence emoji (🟢 high, 🟠 medium, 🔴 low)
- Horizontal rules only before `##` (no decorative dividers)

### Quick-Reference HTML

Two-page operator card with:
- 6-column grid; cards span 3 columns by default (half-page)
- Semantic card classes: default (white), `.ref` (left accent rule for lookup tables), `.span-6 .summary` (full-width closing banner)
- 6.75pt body, Segoe UI / Consolas typeface stack
- Print-safe single accent color (configurable via CSS custom properties)

### Quick-Reference PDF

Rendered locally via `scripts/render-pdf.sh` using headless Chrome / Chromium / Edge. Exactly 2 pages (gate G-8 enforces). **Zero LLM tokens** are spent on rendering; the script invokes a local browser binary.

---

## Theming the Quick Reference

All visual configuration of the HTML/PDF lives in a `:root` block of CSS custom properties at the top of the HTML template. Edit any variable to change the appearance globally:

```css
--accent: #1f4b87;             /* primary brand color */
--font-body: "Segoe UI", ...;  /* body font */
--size-body: 6.75pt;           /* default body size */
--bg-row-even: #e8edf2;        /* table zebra; transparent to drop */
```

The full list of variables (12+ size variables, 12+ color variables, spacing, accent rules) is documented in [`skills/plab-guide/references/quick-ref-theme.md`](../../../skills/plab-guide/references/quick-ref-theme.md).

---

## Confidence Levels

The skill grades every guide and section on a confidence ladder:

| Confidence | Meaning |
|------------|---------|
| `high` | All claims directly cited from primary sources (>=3 sources, >=1 class A) |
| `medium` | Mix of sourced and inferred claims (1-2 sources, >=1 class A) |
| `low-confidence draft` | Mostly speculative or 0 verified sources |

The frontmatter records the overall confidence; each major section ends with a `**Section confidence: <level>.**` line. The ADHD variant adds 🟢 / 🟠 / 🔴 emojis.

If `confidence != high`, the skill inserts a status banner immediately after the H1, naming the limitation.

---

## Examples

Seven calibration topics were used as locked baselines during development. The baseline bundles are not shipped with this plugin; `scripts/regression-test.sh` accepts your own via `PLAB_GUIDE_EXAMPLES_DIR`. The topics were:

| Bundle | Type | Why this fixture |
|--------|------|------------------|
| `superpowers/` | repo-url | Multi-platform plugin with rich workflow surface |
| `memsearch/` | repo-url | Cross-platform memory plugin + library |
| `glow-2026-04-30/` | repo-url | Smaller CLI tool; tests minimum-source-count behavior |
| `okrs-2026-05-01/` | concept | Non-software methodology; tests topic-specific Layer headings |
| `bullet-journaling-2026-05-01/` | concept | Non-software practice; tests creator-driven canon |
| `systems-thinking-2026-05-01/` | concept | Non-software framework; tests multi-source synthesis |
| `jq-2026-05-01/` | tool | CLI tool; tests `tool` input type with rich docs |

Read any of them to see what a finished guide looks like.

---

## Common Operations

### Render a PDF from an existing HTML

```bash
skills/plab-guide/scripts/render-pdf.sh path/to/file.html
```

Validates exactly 2 pages (gate G-8). Exits 3 on overflow with a fix-list.

### Sweep em-dashes from generated text

```bash
skills/plab-guide/scripts/em-dash-sweep.sh path/to/file.md
skills/plab-guide/scripts/em-dash-sweep.sh --dry-run path/to/file.md  # report only
```

Replaces U+2014 (em-dash) with ` - ` (space-hyphen-space) and U+2013 (en-dash) with `-` (hyphen). Enforces gate G-11.

### Validate a MANIFEST.yaml

```bash
python3 skills/plab-guide/scripts/validate-manifest.py path/to/MANIFEST.yaml
```

Validates against the schema (required keys, correct types, artifact files exist).

### Run regression tests against locked baselines

```bash
skills/plab-guide/scripts/regression-test.sh
```

Re-renders all 7 baseline quick-reference HTMLs to PDF and verifies each is exactly 2 pages.

### Check toolchain readiness

```bash
skills/plab-guide/scripts/check-toolchain.sh
```

Detects a Chromium-based browser; prints the resolved path or an install hint.

---

## Failure Modes

| Failure | Behavior |
|---------|----------|
| No browser found | Phase 7 skipped; the other 3 artifacts are produced; install hint printed. |
| PDF overflows 2 pages | Render script exits 3 with a fix-list (tighten longest card, drop a low-value card, reduce padding). |
| Fewer than 3 sources | Mark `confidence: medium` (1-2 sources) or `low-confidence draft` (0 sources). |
| Em-dash leaks past sweep | Gate G-11 fails the run; investigate before unblocking. |
| Existing output directory | Append `-<n>` suffix; never overwrite without `--force`. |
| Network unavailable | Build all artifacts from model knowledge with prominent unverified markers and confidence banner. |

---

## Where to Edit What

| What | Where |
|------|-------|
| Skill body / pipeline | [`skills/plab-guide/SKILL.md`](../../../skills/plab-guide/SKILL.md) |
| Reference material | [`skills/plab-guide/references/`](../../../skills/plab-guide/references/) (8 files) |
| Local scripts | [`skills/plab-guide/scripts/`](../../../skills/plab-guide/scripts/) (5 scripts) |
| Locked output templates | [`skills/plab-guide/assets/templates/`](../../../skills/plab-guide/assets/templates/) (3 files) |
| Quick-ref visual theme | The `:root` block in `quick-reference-template_v1-technical-white.html`; see [`quick-ref-theme.md`](../../../skills/plab-guide/references/quick-ref-theme.md) |
| Spec and plan | Not shipped; they remain in the author's private development repository |

---

## Version History

| Version | Date | Notes |
|---------|------|-------|
| 1.6.0 | 2026-05-10 | Current version. See `skills/plab-guide/HISTORY.md` for full version history. |
| 1.0.0 | 2026-05-01 | Initial release. 7 calibration topics validated; locked templates; parameterized CSS theme; flexible Layer headings for non-software topics. |
