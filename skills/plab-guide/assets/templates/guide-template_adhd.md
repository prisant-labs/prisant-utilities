<!--
================================================================================
GUIDE TEMPLATE v2 (ADHD / SKIM-OPTIMIZED) / plab-guide / explanatory artifact
================================================================================

This is a visually-optimized variant of the canonical guide template. Use when
the audience benefits from:
- Aggressive skim paths (TL;DRs, bottom-lines, bold lead phrases)
- Predictable visual rhythm (consistent callout tags, numbered sections)
- Chunked content (no long paragraphs, lots of tables/lists)
- Front-loaded summaries (every section says its takeaway up front)

Use v1-expanded for technical / reference-style readers who want flowing prose.
Use this v2 for operators who skim, hop, and re-enter the document multiple times.

================================================================================
DESIGN PRINCIPLES
================================================================================

1. EVERY SECTION HAS THE SAME SHAPE (predictable pattern):
   - Numbered H2 heading using "." separator (e.g., "## 5. 80/20 - High-Leverage Practices")
   - [TL;DR] callout (one sentence)
   - Mini-TOC if section has >=4 sub-sections (must be clickable - markdown links)
   - Content
   - [BOTTOM LINE] callout (one sentence takeaway)
   - **Section confidence:** line with confidence emoji (high 🟢 / medium 🟠 / low 🔴)
   - --- horizontal rule (only before the NEXT ## - not between H3s or H4s)

2. CALLOUT TAGS (use consistently with their emojis):
   - [TL;DR]       one-sentence summary at top of section (no emoji)
   - [BOTTOM LINE] one-sentence takeaway at end of section (no emoji)
   - [QUICK NAV]   clickable mini-TOC for sections >=4 sub-sections (no emoji)
   - [ACTION]      specific thing the reader should do (no emoji - tag is enough)
   - 📌 [KEY]      the single most important point in the section
   - 💡 [INSIGHT]  non-obvious thing worth pausing on
   - ⚠️ [WARNING]  common mistake or gotcha to avoid
   - ⚠️ [GOTCHA]   edge case or trap (same emoji as WARNING; the tag distinguishes)
   - ⏹️ [STOP]     do not do this (rare; use only for hard-stop rules)
   - ⭐            inline emphasis on a pull quote or starred takeaway

   EMOJI RULE: every callout that "warns / informs / pins" gets one of the five
   emojis. Don't double up (no "📌 💡 [KEY]"). Don't put emojis on [TL;DR],
   [BOTTOM LINE], [QUICK NAV], or [ACTION] - they already read as structural.

3. BOLD LEAD PHRASES on every prose chunk so the eye lands on the load-bearing word.

4. TABLES OVER PROSE wherever the content is comparison-shaped or lookup-shaped.
   EXCEPTION: a 2-row table is always a list. Tables exist to compare across rows;
   2 rows do not compare. Tables also REQUIRE column headers - never use a
   header-less 2-column table for "Field / Value" pairs.

5. NUMBERED EVERYTHING (sections, sub-sections, list items, phases). Use "." as
   the separator after the number, not "/". So "## 5. Foo", not "## 5 / Foo".

6. NO PARAGRAPH LONGER THAN 3 SENTENCES. Break it up.

7. HORIZONTAL RULES (---) ONLY BEFORE H2 SECTIONS. Do NOT put --- between
   adjacent H3s or H4s - that breaks the visual rhythm and adds noise. The H3
   or H4 heading is its own visual break.

8. MINI-TOCs at start of long sections so the reader can hop. Mini-TOCs
   (a.k.a. [QUICK NAV] blocks) MUST use clickable markdown links, not plain
   text bullets. Format: "- [5.1. Trust the brainstorming pass](#51-trust-the-brainstorming-pass)".

9. SECTION CONFIDENCE EMOJIS: every "**Section confidence: <level>.**" line
   must end with the matching emoji - 🟢 for high, 🟠 for medium, 🔴 for low.

10. NO MARKETING PROSE. Same voice rules as v1-expanded apply.

11. PROSE DENSITY: any #### sub-section under Mechanical Layer or Structural
    Layer needs >=2 paragraphs of prose (100-200 words minimum). One-line
    phases are too sparse and were explicitly flagged in v1.0.0 review. If a
    phase is genuinely a single sentence, fold it into an adjacent phase.

================================================================================
WRITING ORDER (DO NOT WRITE TOP-TO-BOTTOM)
================================================================================

  1.  Frontmatter (placeholder values; finalize at the end)
  2.  At a Glance + Official Resources
  3.  Key Terms (mark as you go)
  4.  In-Depth Breakdown (heart of the document; four progressive layers)
  5.  Frequently Asked Questions
  6.  Similar Tools & Alternatives
  7.  Additional & Third-Party Resources
  8.  80/20 - High-Leverage Practices (synthesize)
  9.  Getting Started (synthesize)
  10. Executive Summary (LAST)
  11. All TL;DR + BOTTOM LINE callouts (write last - they summarize each section)
  12. Sources & Evidence (audit)
  13. Final frontmatter pass

================================================================================
VOICE AND TONE (same as v1-expanded)
================================================================================

DO:
- Lead with the claim, support with citation. ("X happens. [S1]")
- Direct, declarative sentences.
- Show failure modes, not just features.
- Bold the load-bearing word in every paragraph.
- Mark inferences ([inferred]) and speculation ([unverified]).

DON'T:
- Marketing prose ("powerful", "elegant", "intuitive").
- Hedge with "might possibly". Use [unverified] when uncertain.
- Cite obvious common knowledge.
- Use em-dashes (-) or en-dashes (-).
- Write paragraphs longer than 3 sentences.
- Use list-bullet padding ("Also...", "Additionally...").

================================================================================
CITATION PATTERN EXAMPLES
================================================================================

  Direct quote:        Foo behaves as bar: "<quoted text>" [S1].
  Paraphrase:          Foo behaves as bar [S1].
  Multiple sources:    Foo behaves as bar [S1, S3].
  Inference:           Foo likely behaves as bar [inferred from <source/principle>].
  Speculation:         Foo may behave as bar [unverified, <reason>].
  Section confidence:  **Section confidence: high 🟢.** All claims cited [S1].
                       **Section confidence: medium 🟠.** Mix of cited + inferred.
                       **Section confidence: low 🔴.** Mostly inference.

================================================================================
SECTION CONFIDENCE LADDER
================================================================================

  high 🟢  - every claim in the section is cited from a primary source.
  medium 🟠 - >=1 inferred or unverified claim, but core claims are sourced.
  low 🔴   - half or more of claims are inference or unverified.

  Always include the matching emoji directly after the level word in the
  Section confidence line.

================================================================================
FRONTMATTER VALIDATION CHEATSHEET
================================================================================

  title:           "<Topic> - Guide"
  slug:            kebab-case lowercase
  type:            always "explanatory"
  generated:       YYYY-MM-DD (today)
  last-verified:   YYYY-MM-DD (today on first run)
  source-count:    integer count of fetched sources
  confidence:      "high" (>=3 sources, >=1 class A, <=2 unverified body claims)
                   "medium" (1-2 sources, >=1 class A, <=5 unverified body claims)
                   "low-confidence draft" (0 verified sources OR all class C)
  audience:        one-line description
  maturity:        "experimental" | "active development" | "stable v1.x" |
                   "maintenance" | "deprecated"
  license:         SPDX OR "proprietary" OR "n/a"

================================================================================
TOPIC-TYPE ADAPTERS
================================================================================

  repo:    a GitHub URL. Has owners, license, README, docs.
  tool:    a named tool / library / CLI. Has install command, package.
  concept: an idea, methodology, pattern. No package, no command.

================================================================================
END HEADER. SECTION-BY-SECTION CONTENT BEGINS BELOW.
================================================================================
-->

<!--
================================================================================
SECTION 0: FRONTMATTER
PURPOSE: standardized machine-readable metadata.
[KEY] always populate all 10 fields. Use "n/a" only if genuinely unknown.
================================================================================
-->
---
title: <Topic> - Guide
slug: <slug>
type: explanatory
generated: <YYYY-MM-DD>
last-verified: <YYYY-MM-DD>
source-count: <n>
confidence: high | medium | low-confidence draft
audience: <one-line audience description>
maturity: experimental | active development | stable v1.x | maintenance | deprecated
license: <SPDX or "proprietary" or "n/a">
---

<!--
================================================================================
SECTION 0.5: STATUS BANNER (CONDITIONAL)
[ACTION] Insert ONLY if confidence != high. Delete entirely if confidence == high.
[WARNING] Don't use the literal "low-confidence draft" wording when you have
fetched sources - adapt to "medium-confidence draft".
================================================================================
-->
> **Status:** <medium-confidence draft | low-confidence draft>. <One-sentence honest reason>. See Sources & Evidence for the per-section breakdown.

# <Topic> - Guide

---

<!--
================================================================================
SECTION 1 / AT A GLANCE
PURPOSE: 5-second skim. Reader knows what this is and whether to keep reading.
LENGTH: 8-12 table rows. No prose.
[KEY] This is the most-read section. Make every row count.
[WARNING] Don't put marketing fluff in the Stance row.
================================================================================
-->
## 1. At a Glance

> **[TL;DR]** <One-sentence description that captures what the topic is and who it's for.>

| Field | Value |
|-------|-------|
| **What** | <one-sentence description of the topic> |
| **Category** | <topic class/family> |
| **Who built it** | <author / org / origin> |
| **License** | <license> |
| **Source** | <repo URL or canonical reference> |
| **Audience** | <one-line audience> |
| **Cost** | <free / paid / etc.> |
| **Maturity** | <status> |
| **Stance** | <project's one-liner if memorable> |

> **[BOTTOM LINE]** <Single sentence: what kind of reader benefits from this topic.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 2 / TABLE OF CONTENTS
PURPOSE: navigation. Numbered to match section numbering.
[ACTION] Regenerate after final section reorder.
================================================================================
-->
## 2. Table of Contents

> **[TL;DR]** Jump to any section by number. Sections 5 (80/20) and 8 (Breakdown) are the highest-utility deep-reads.

- [3. Executive Summary](#3-executive-summary)
- [4. Official Resources](#4-official-resources)
- [5. 80/20 - High-Leverage Practices](#5-8020---high-leverage-practices)
- [6. Getting Started](#6-getting-started)
- [7. Key Terms](#7-key-terms)
- [8. In-Depth Breakdown](#8-in-depth-breakdown)
    - [8.1. Surface Layer - What It Is](#81-surface-layer---what-it-is)
    - [8.2. Structural Layer - How It's Organized](#82-structural-layer---how-its-organized)
    - [8.3. Mechanical Layer - How It Works](#83-mechanical-layer---how-it-works)
    - [8.4. Expert Layer - What's Non-Obvious](#84-expert-layer---whats-non-obvious)
- [9. Frequently Asked Questions](#9-frequently-asked-questions)
- [10. Similar Tools & Alternatives](#10-similar-tools--alternatives)
- [11. Additional & Third-Party Resources](#11-additional--third-party-resources)
- [12. Sources & Evidence](#12-sources--evidence)

---

<!--
================================================================================
SECTION 3 / EXECUTIVE SUMMARY
PURPOSE: complete summary the reader can stop after.
LENGTH: 250-500 words. 3-6 paragraphs + Key Takeaways callout.
[KEY] Write this LAST - it summarizes the actual document.
[WARNING] Don't repeat headings ("In the Surface Layer below..."). Standalone read.
================================================================================
-->
## 3. Executive Summary

> **[TL;DR]** <One-sentence summary of the topic + its load-bearing innovation.>

<Paragraph 1: What the topic is, who built it, and the headline framing. Cite primary source.>

<Paragraph 2: The structural innovation or core mechanic. What makes this distinct from adjacent options.>

<Paragraph 3: The failure modes the topic addresses or the problem space it occupies.>

<Paragraph 4: Practical operator impact. What changes when adopted.>

> **[KEY TAKEAWAYS]**
>
> 1. **<Sharp claim>.** <One-line elaboration with citation> [S1].
> 2. **<Sharp claim>.** <One-line elaboration> [S1].
> 3. **<Sharp claim>.** <One-line elaboration> [S1].
> 4. **<Sharp claim>.** <One-line elaboration> [S1].
> 5. **<Sharp claim>.** <One-line elaboration> [S1].

> **[BOTTOM LINE]** <One sentence: when this topic is the right answer.>

**Section confidence: <high | medium | low>.** <One-line justification.>

---

<!--
================================================================================
SECTION 4 / OFFICIAL RESOURCES
PURPOSE: canonical links bookmarked at the top.
LENGTH: 5-10 table rows.
[ACTION] Include only OFFICIAL sources here. Community goes to section 11.
================================================================================
-->
## 4. Official Resources

> **[TL;DR]** Bookmark these. Everything authoritative starts at one of these URLs.

| Resource | URL | Use for |
|----------|-----|---------|
| <name of resource> | `<url>` | <when reader would click this> |
| <e.g., Source repo> | `<github.com/org/repo>` | Code, README, docs |

> **[BOTTOM LINE]** <One sentence pointing to the single most useful resource for a beginner.>

**Section confidence: <high | medium | low>.** <One-line justification.>

---

<!--
================================================================================
SECTION 5 / 80/20 - HIGH-LEVERAGE PRACTICES
PURPOSE: 5-7 actions that deliver disproportionate value.
LENGTH: ~600-1000 words. 5-7 numbered practices.
[KEY] This is the highest-utility section. Place near top, write with care.
[WARNING] Don't list every feature. Pick the disproportionate-impact subset.
================================================================================
-->
## 5. 80/20 - High-Leverage Practices

> **[TL;DR]** These <n> practices deliver most of <topic>'s value. Adopting them faithfully matters more than learning every feature.

> **[QUICK NAV]**
>
> 1. [<Practice 1 short label>](#51-practice-1-slug)
> 2. [<Practice 2 short label>](#52-practice-2-slug)
> 3. [<Practice 3 short label>](#53-practice-3-slug)
> 4. [<Practice 4 short label>](#54-practice-4-slug)
> 5. [<Practice 5 short label>](#55-practice-5-slug)

### 5.1. <Practice phrased as an action / verb>

> **[ACTION]** <One-sentence imperative restating the practice.>

<1-3 sentences explaining what to do and why it works. Cite primary source.>

- **Impact:** <what failure mode this prevents or what gain this captures>.
- **Effort:** <trivial / marginal / moderate / heavy>.

### 5.2. <Practice phrased as an action / verb>

> **[ACTION]** <One-sentence imperative.>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

### 5.3. <Practice phrased as an action / verb>

> ⚠️ **[WARNING]** <If the practice is "do not do X", use WARNING; otherwise ACTION.>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

### 5.4. <Practice phrased as an action / verb>

> **[ACTION]** <One-sentence imperative.>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

### 5.5. <Practice phrased as an action / verb>

> 💡 **[INSIGHT]** <If the practice is more "realize this" than "do this", use INSIGHT.>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

> 💡 **[INSIGHT]** <One sentence that synthesizes the practices into a single observation.>

> **[BOTTOM LINE]** <One sentence: which 1-2 of these practices to adopt first.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 6 / GETTING STARTED
PURPOSE: orientation from "I just heard of this" to "I have something running".
LENGTH: 200-450 words.
[KEY] Lead with the mental model. Don't reproduce the install guide.
================================================================================
-->
## 6. Getting Started

> **[TL;DR]** <One sentence: the mental model + the first concrete action.>

### 6.1. Mental Model

> 📌 **[KEY]** <One or two sentences capturing the topic's core conceptual move.>

<2-3 sentences elaborating on the mental model. Why this framing, and what it
replaces in the reader's existing model.>

### 6.2. First Concrete Step

> **[ACTION]** Run this:

```
<concrete first command>
```

<2-3 sentences explaining what happens next, citing primary source. Include
multi-host or multi-environment notes if applicable.>

### 6.3. First-Session Expectations

> 💡 **[INSIGHT]** What you'll observe in the first session:

| #   | Expectation                |
| --- | -------------------------- |
| 1   | <observable behavior 1>    |
| 2   | <observable behavior 2>    |
| 3   | <observable behavior 3>    |
| 4   | <observable behavior 4>    |

<1-2 paragraphs commenting on the table. Why these expectations, what they
indicate when they don't hold, and what operators typically report after the
first 1-3 sessions.>

> **[BOTTOM LINE]** <One sentence: how the reader knows things are working.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 7 / KEY TERMS
PURPOSE: glossary of topic-specific vocabulary.
LENGTH: 8-20 terms.
[ACTION] Build this AS YOU WRITE the breakdown. Mark terms as you encounter them.
================================================================================
-->
## 7. Key Terms

> **[TL;DR]** Vocabulary the rest of the document assumes you know.

| Term       | Definition                                                |
| ---------- | --------------------------------------------------------- |
| **<term>** | <one-sentence definition> [S1].                           |
| **<term>** | <one-sentence definition> [S1].                           |
| **<term>** | <one-sentence definition> [inferred, <reason>].           |

> **[BOTTOM LINE]** <One sentence: which 2-3 terms are most load-bearing for this topic.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 8 / IN-DEPTH BREAKDOWN
PURPOSE: heart of the document. Four progressive-disclosure layers.
LENGTH: 2200-4000 words across all four layers.
[KEY] Don't mix layers. Each layer answers a different reader question.
================================================================================
-->
## 8. In-Depth Breakdown

> **[TL;DR]** Four layers of disclosure: surface (what), structural (how organized), mechanical (how works), expert (what's non-obvious).

> **[QUICK NAV]**
>
> - [8.1. Surface Layer - What It Is](#81-surface-layer---what-it-is)
> - [8.2. Structural Layer - How It's Organized](#82-structural-layer---how-its-organized)
> - [8.3. Mechanical Layer - How It Works](#83-mechanical-layer---how-it-works)
> - [8.4. Expert Layer - What's Non-Obvious](#84-expert-layer---whats-non-obvious)

<!--
================================================================================
SUB-SECTION 8.1 / SURFACE LAYER
PURPOSE: answers "What is this thing?" for a total newcomer.
LENGTH: 200-400 words. 2-4 paragraphs.
[INCLUDE] Category framing, authors/license, audience, optional pull quote.
[STOP] Don't go into how it works. That's section 8.3.
================================================================================
-->
### 8.1. Surface Layer - What It Is

> **[TL;DR]** <One-sentence statement of what the topic IS, in its most boring categorical sense.>

<Paragraph 1: Category framing. What family/class does this belong to? What adjacent options exist?>

<Paragraph 2: Authors, license, source. Who built it; under what terms.>

<Paragraph 3: Audience and value proposition. Who benefits and when.>

<Optional pull quote:>

> ⭐ **Pull quote:** "<Memorable framing or quote from the source materials.>"

> **[BOTTOM LINE]** <One sentence: who the topic is for and who it isn't.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SUB-SECTION 8.2 / STRUCTURAL LAYER
PURPOSE: answers "How is this thing organized?"
LENGTH: 600-1000 words. At least one diagram, table, or structured list, plus
real prose framing each axis.
[INCLUDE] Named parts + relationships + workflow/pipeline if applicable.
[STOP] Don't go into runtime mechanics. That's section 8.3.
[ACTION] Open with a multi-sentence framing paragraph naming the 2-4 axes and
explaining how they compose. Tables alone do not explain composition.
================================================================================
-->
### 8.2. Structural Layer - How It's Organized

> **[TL;DR]** <One sentence naming the structure's primary axes (e.g., "Three layers: A, B, C").>

<Opening framing paragraph (3-5 sentences): Name the 2-4 structural axes. Explain how they compose. Stress that the axes are not independent - the topic's mechanism comes from how they fit together.>

#### 8.2.1. Axis 1 - <Sub-heading: components or parts>

<Paragraph (2-4 sentences): What this axis is and why the partition is shaped this way. Frame what the table below shows BEFORE the table.>

| Group      | Item        | One-line role |
| ---------- | ----------- | ------------- |
| <category> | <component> | <role>        |

<Paragraph (2-4 sentences): Closing prose - how the items relate, what an experienced reader takes away from the catalog. Cite primary source.>

#### 8.2.2. Axis 2 - <Sub-heading: workflow or relationships>

<Paragraph (2-3 sentences): What this axis is. Set up the diagram below.>

```
<flow diagram or pipeline>
```

<Paragraph (2-4 sentences): How the diagram maps to the topic's principles or design choices. Cite primary source.>

#### 8.2.3. Axis 3 - <Sub-heading: another structural axis if relevant>

<2-3 paragraphs of prose. The third axis is often the load-bearing one (triggers, configuration, runtime gating). Spend the words to explain not just what it is, but WHEN it fires and what makes it structurally important rather than advisory.>

<Closing synthesis paragraph (2-3 sentences): How all the axes combine to produce the topic's mechanism. This is the bridge to the Mechanical Layer.>

> **[BOTTOM LINE]** <One sentence: the structural axis that matters most for an operator.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SUB-SECTION 8.3 / MECHANICAL LAYER
PURPOSE: answers "How does this thing actually work?"
LENGTH: 1000-2000 words. Numbered phases.
[KEY] Most of the document's depth lives here.
[ACTION] Use #### Phase N - Name format for each phase.
[WARNING] Each phase needs >=2 paragraphs (100-200 words). One-line phases
were flagged in v1.0.0 review as too sparse. Fold any genuinely-one-sentence
phase into an adjacent phase.
================================================================================
-->
### 8.3. Mechanical Layer - How It Works

> **[TL;DR]** <One sentence describing the end-to-end mechanic.>

> **[QUICK NAV]**
>
> - [8.3.1. Phase 1 - <name>](#831-phase-1---name-slug)
> - [8.3.2. Phase 2 - <name>](#832-phase-2---name-slug)
> - [8.3.3. Phase 3 - <name>](#833-phase-3---name-slug)
> - <continue for all phases>

<2-3 sentence introduction: name what "running this thing" actually means and how many phases the mechanics break into.>

#### 8.3.1. Phase 1 - <Phase name>

> 📌 **[KEY]** <One sentence: what this phase accomplishes.>

<2-4 paragraphs covering: (1) what triggers this phase, (2) the internal steps it runs, (3) the artifact / state change it produces, (4) which failure mode it exists to address. Cite primary source for each load-bearing claim.>

#### 8.3.2. Phase 2 - <Phase name>

> 📌 **[KEY]** <One sentence.>

<2-4 paragraphs in the same shape. Don't skimp - if a phase only needs one sentence, fold it into an adjacent phase instead.>

#### 8.3.3. Phase 3 - <Phase name>

> 📌 **[KEY]** <One sentence.>

<2-4 paragraphs.>

<...continue for all phases...>

> ⭐ **Pull quote:** "<Pull quote that captures the operating principle.>"

> **[BOTTOM LINE]** <One sentence: which phase is the load-bearing one.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SUB-SECTION 8.4 / EXPERT LAYER
PURPOSE: answers "What's non-obvious about this?"
LENGTH: 400-800 words. 5-10 sub-points with bold lead phrases.
[KEY] Almost exclusively from class A or B sources. Mark inferences clearly.
[WARNING] Don't repeat structural content with longer paragraphs.
================================================================================
-->
### 8.4. Expert Layer - What's Non-Obvious

> **[TL;DR]** Things that only become visible after working with <topic> for a while.

> **[QUICK NAV]**
>
> - [8.4.1. <insight 1 short label>](#841-insight-1-slug)
> - [8.4.2. <insight 2 short label>](#842-insight-2-slug)
> - [8.4.3. <insight 3 short label>](#843-insight-3-slug)
> - <continue for 5-10>

#### 8.4.1. <Insight phrased as a sentence>

> 💡 **[INSIGHT]** <One sentence stating the insight bluntly.>

<1-2 paragraphs explaining why it matters and how it manifests. Bold the load-bearing word.>

#### 8.4.2. <Insight phrased as a sentence>

> 💡 **[INSIGHT]** <One sentence.>

<1-2 paragraphs.>

#### 8.4.3. <Insight phrased as a sentence>

> ⚠️ **[GOTCHA]** <One sentence stating the gotcha or trap.>

<1-2 paragraphs.>

<...continue for 5-10 insights...>

> **[BOTTOM LINE]** <One sentence: the single most non-obvious thing on this list.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 9 / FREQUENTLY ASKED QUESTIONS
PURPOSE: answer the questions a reader will actually have.
LENGTH: ~5 categories, ~10 Q/A pairs total.
[REQUIRED] >=3 categories, >=8 Q/A pairs, >=2 per category.
[BANNED] "What is X?", "Why use X?", "How install X?", any answer <=1 sentence.
================================================================================
-->
## 9. Frequently Asked Questions

> **[TL;DR]** Friction-driven Q/A. Categories derived from real questions, not templated.

> **[QUICK NAV]**
>
> - [9.1. <Category 1 label>](#91-category-1-slug)
> - [9.2. <Category 2 label>](#92-category-2-slug)
> - [9.3. <Category 3 label>](#93-category-3-slug)
> - [9.4. <Category 4 label>](#94-category-4-slug)
> - [9.5. <Category 5 label>](#95-category-5-slug)

### 9.1. <Category 1: e.g., Adoption & Setup>

**Q: <Specific, friction-driven question>**

A: <Substantive answer of 2-5 sentences. Cite source.> [S1]

**Q: <Another question>**

A: <Answer.> [S1]

### 9.2. <Category 2: e.g., Workflow Discipline>

**Q: <Question>**

A: <Answer.> [S1]

**Q: <Question>**

A: <Answer.> [S1]

**Q: <Question>**

A: <Answer.> [S1]

### 9.3. <Category 3: e.g., Multi-Agent / Concurrency / Scale>

**Q: <Question>**

A: <Answer.> [S1]

**Q: <Question>**

A: <Answer.> [S1]

### 9.4. <Category 4 (optional): e.g., Customization & Extension>

**Q: <Question>**

A: <Answer.> [S1]

**Q: <Question>**

A: <Answer.> [unverified, <reason>]

### 9.5. <Category 5 (optional): e.g., Troubleshooting>

**Q: <Question>**

A: <Answer.> [S1]

**Q: <Question>**

A: <Answer.> [S1]

> **[BOTTOM LINE]** <One sentence: which 1-2 questions get asked most often.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 10 / SIMILAR TOOLS & ALTERNATIVES
PURPOSE: position the topic in its competitive/adjacent landscape.
LENGTH: ~250-450 words. 1 comparison table + 2 short bullet lists.
[KEY] The trade-off column is the value. Don't skip it.
================================================================================
-->
## 10. Similar Tools & Alternatives

> **[TL;DR]** <One-sentence positioning: where this topic sits relative to alternatives.>

### 10.1. Comparison

| Approach | What it is | Best for | Trade-off vs. <topic> |
|----------|-----------|----------|----------------------|
| **<Alternative 1>** | <one-line description> | <when to use it> | <how it differs from the topic> |
| **<Alternative 2>** | <one-line description> | <when to use it> | <difference> |
| **<Alternative 3>** | <one-line description> | <when to use it> | <difference> |

### 10.2. When to Choose <topic>

- <Situation 1 where this is the right choice.>
- <Situation 2.>
- <Situation 3.>

### 10.3. When <topic> May Be Overkill

- <Situation 1 where simpler options suffice.>
- <Situation 2.>

> **[BOTTOM LINE]** <One sentence: the single decisive factor for choosing this over alternatives.>

**Section confidence: <high 🟢 | medium 🟠 | low 🔴>.** <One-line justification.>

---

<!--
================================================================================
SECTION 11 / ADDITIONAL & THIRD-PARTY RESOURCES
PURPOSE: deeper resource library beyond the canonical Official Resources table.
LENGTH: >=5 total entries across the four sub-sections.
[ACTION] Use the four required sub-sections in this order.
================================================================================
-->
## 11. Additional & Third-Party Resources

> **[TL;DR]** Where to go after the official resources stop being enough.

### 11.1. Official

- `<url or identifier>` / <one-line description> [S1]
- `<url>` / <description> [S1]

### 11.2. Community & Tutorials

- <Resource name> / <description> [S1 or unverified]
- <Resource name> / <description>

### 11.3. Deep-Dive / Advanced

- <Resource name> / <description> [S1]
- <Resource name> / <description> [unverified, <reason>]

### 11.4. Related Tools

- **<Tool name>** / <one-line description>
- **<Tool name>** / <description>

> **[BOTTOM LINE]** <One sentence: the single most useful resource for a deep-dive.>

---

<!--
================================================================================
SECTION 12 / SOURCES & EVIDENCE
PURPOSE: full traceability for every claim in the document.
LENGTH: variable. ~250-500 words.
[REQUIRED] Primary Sources, Confidence Markers Used, Unverified Claims,
Source-to-Section Traceability, Gaps. Supporting Sources optional.
================================================================================
-->
## 12. Sources & Evidence

> **[TL;DR]** Every claim in this document traces here. Use this section to extend, audit, or update the guide.

### 12.1. Primary Sources

- **[S1]** <Title>, retrieved <YYYY-MM-DD> from `<URL>`. Credibility <A | B | C>. <One-line note.>
- **[S2]** <Title>, retrieved <YYYY-MM-DD>. Credibility <A | B | C>.

### 12.2. Supporting Sources

<!-- Omit this sub-section if no class-B/C corroborating sources exist. -->

- **[S3]** <Title>, retrieved <YYYY-MM-DD>. Credibility B. <Note.>

### 12.3. Confidence Markers Used

| Marker | Meaning |
|--------|---------|
| `[S1]`, `[S2]`, ... | Directly cited or quoted from the numbered source. |
| `[inferred]` | Derived from documented architecture, not stated explicitly. |
| `[unverified]` | Model knowledge or speculation. Verify before relying on. |
| **Section confidence: high 🟢** | All claims directly sourced from primary materials. |
| **Section confidence: medium 🟠** | Mix of sourced and inferred claims. |
| **Section confidence: low 🔴** | Mostly speculative or inferred. |

### 12.4. Unverified Claims

| Claim | Where it appears | Why it's unverified |
|-------|------------------|---------------------|
| "<exact text of the claim>" | <Section name> | <Why this is not directly sourced.> |
| "<claim>" | <Section> | <Reason.> |

### 12.5. Source-to-Section Traceability

| Section | Primary Sources | Inferred / Unverified |
|---------|-----------------|----------------------|
| 1. At a Glance | <Sn> | <inferences> |
| 4. Official Resources | <Sn> | <inferences> |
| 3. Executive Summary | <Sn> | <inferences> |
| 5. 80/20 | <Sn> | <inferences> |
| 6. Getting Started | <Sn> | <inferences> |
| 7. Key Terms | <Sn> | <inferences> |
| 8.1. Surface Layer | <Sn> | <inferences> |
| 8.2. Structural Layer | <Sn> | <inferences> |
| 8.3. Mechanical Layer | <Sn> | <inferences> |
| 8.4. Expert Layer | <Sn> | <inferences> |
| 9. FAQ | <Sn> | <inferences> |
| 10. Similar Tools | <Sn or "interpretive"> | <inferences> |
| 11. Resources | <Sn> | <inferences> |

### 12.6. Gaps

> 💡 **[INSIGHT]** Topics adjacent to this guide that the available sources did not cover.

| Gap | Where to look |
|-----|---------------|
| <topic the sources missed> | <suggested investigation path> |
| <gap> | <where to look> |

> **[BOTTOM LINE]** <One sentence: the single biggest gap in current source coverage.>

---

<!--
================================================================================
CROSS-ARTIFACT REFERENCES

The guide is one of three artifacts the skill produces:
  - <slug>_guide.md     - this explanatory guide
  - <slug>_quickref.md  - operator-only quick reference
  - <slug>_quickref.pdf - 2-page rendered PDF

Link to companions from the resources section or from getting-started.

================================================================================
-->

<!--
================================================================================
FINAL CHECKLIST (REMOVE BEFORE SHIPPING)
================================================================================

VISUAL SCAFFOLDING
- [ ] Every section has [TL;DR] callout at top
- [ ] Every section has [BOTTOM LINE] callout at end
- [ ] Section confidence line at end of every major section, with matching emoji (🟢 / 🟠 / 🔴)
- [ ] Horizontal rules (---) ONLY before ## sections - never between H3s or H4s
- [ ] Numbered sections use "." separator (## 1. Foo, not ## 1 / Foo)
- [ ] Sub-sections use "." separator (### 5.1. Foo, #### 8.2.1. Foo)
- [ ] Quick-nav blocks at start of long sections (5, 8, 9) and they are CLICKABLE markdown links
- [ ] Tags used consistently with emojis: 📌 [KEY], 💡 [INSIGHT], ⚠️ [WARNING], ⚠️ [GOTCHA], ⏹️ [STOP]
- [ ] [TL;DR], [BOTTOM LINE], [QUICK NAV], [ACTION] use NO emoji (structural tags)
- [ ] Pull quotes use ⭐ prefix
- [ ] No paragraph longer than 3 sentences
- [ ] Bold lead phrases on prose chunks
- [ ] No 2-row tables - if you only have two rows, use a bullet list
- [ ] Tables always have column headers (header-less 2-column key/value pairs are banned)
- [ ] Mechanical Layer phases: each phase >= 2 paragraphs (one-line phases are too sparse)

FRONTMATTER
- [ ] All 10 fields populated
- [ ] confidence value matches source-count and unverified-claim count
- [ ] last-verified is today

STRUCTURE
- [ ] Section reorder applied: At a Glance / TOC / Executive Summary / Official Resources
- [ ] All required H2 sections present and numbered
- [ ] Confidence banner present iff confidence != high

CONTENT
- [ ] Executive Summary written LAST
- [ ] At a Glance: 8-12 rows
- [ ] Official Resources: 5-10 rows, OFFICIAL only
- [ ] 80/20: 5-7 practices, each with [ACTION]/[WARNING]/[INSIGHT] callout + Impact/Effort BULLET LIST (not table)
- [ ] Getting Started: 3 sub-sections (Mental Model, First Step, Expectations)
- [ ] Key Terms: 8-20 terms with citations
- [ ] All four PD layers have [TL;DR], substantive content, [BOTTOM LINE]
- [ ] Mechanical Layer uses #### Phase N format
- [ ] Expert Layer has 5-10 [INSIGHT] / [GOTCHA] sub-sections
- [ ] FAQ: >=3 categories, >=8 Q/A, >=2 per category
- [ ] No banned FAQ shapes
- [ ] No FAQ answer is <=1 sentence
- [ ] Similar Tools: comparison table + when-to-choose + when-overkill

SOURCING
- [ ] Every cited [Sn] appears in Sources & Evidence
- [ ] Every [unverified] flag in body has a row in Unverified Claims
- [ ] Source-to-Section Traceability covers all sections (1-11)
- [ ] Gaps reflect real gaps, not filler

WRITING
- [ ] No em-dashes or en-dashes
- [ ] No marketing prose
- [ ] All HTML comments removed
- [ ] All <placeholder> tokens replaced
- [ ] Word count between 1,500 and 6,000 (target: 3,500-5,500 for ADHD-optimized
      since visual scaffolding adds bytes without adding read-time)

CROSS-ARTIFACT
- [ ] Linked to companion quick-ref artifact if one exists
- [ ] Slug matches frontmatter and filename

================================================================================
END OF TEMPLATE
================================================================================
-->
