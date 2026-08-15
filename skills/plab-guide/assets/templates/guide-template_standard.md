<!--
================================================================================
GUIDE TEMPLATE v1 (EXPANDED) / plab-guide / explanatory artifact
================================================================================

This is the canonical markdown template for the explanatory guide artifact
(Artifact 1 in the spec). HTML comments contain instructional guidance.
STRIP ALL HTML COMMENTS BEFORE SHIPPING.

This expanded version adds:
- Worked examples per section (clearly marked for deletion)
- Topic-type adapter notes (repo / tool / concept)
- Anti-patterns per section
- Writing order
- Voice and tone rules
- Length targets per sub-section
- Citation pattern examples
- "When this section doesn't apply" rule
- Frontmatter validation cheatsheet
- Section confidence ladder
- Final checklist enforcement (visible + invisible)
- Cross-artifact references

================================================================================
WRITING ORDER (DO NOT WRITE TOP-TO-BOTTOM)
================================================================================

The document reads top-to-bottom but should be WRITTEN in a different order.
The Executive Summary in particular must be written LAST so it summarizes what
is actually in the document, not what was intended.

Recommended writing order:

  1. Frontmatter (placeholder values; finalize at the end)
  2. At a Glance + Official Resources (build factual foundation first)
  3. Key Terms (mark terms you'll define as you encounter them; fill table after step 5)
  4. In-Depth Breakdown (heart of the document; four progressive layers)
     - Surface Layer
     - Structural Layer
     - Mechanical Layer
     - Expert Layer
  5. Key Terms (now finalize from terms surfaced in step 4)
  6. Frequently Asked Questions (derive from breakdown gaps + research)
  7. Similar Tools & Alternatives (research and position)
  8. Additional & Third-Party Resources (organize)
  9. 80/20 - High-Leverage Practices (synthesize from steps 4-7)
  10. Getting Started (synthesize a beginner path)
  11. Executive Summary (LAST - summarizes the actual document)
  12. Sources & Evidence (audit every citation in body, list every [unverified])
  13. Update frontmatter: source-count, confidence, last-verified

================================================================================
VOICE AND TONE
================================================================================

Goal: a fast-tracked learning document for an operator. Read once, refer back.

DO:
- Lead with the claim, support with citation. ("X happens. [S1]")
- Use direct, declarative sentences.
- Show failure modes, not just features. ("This prevents <specific failure>.")
- Use bold lead phrases so the eye lands on the load-bearing word first.
- Cite specifics ([S1]). Mark inferences ([inferred]). Mark speculation ([unverified]).
- Use bullet lists when 3+ parallel items would otherwise become a comma soup.
- Use tables when content is comparison- or lookup-shaped.

DON'T:
- Use marketing prose ("powerful", "elegant", "intuitive", "best-in-class").
- Hedge unnecessarily ("might possibly", "could potentially").
  Use [unverified] when uncertain - that's honest. Hedging is filler.
- Cite obvious common knowledge.
- Leave a non-obvious specific claim un-cited.
- Use em-dashes (-) or en-dashes (-). Hyphens, slashes, commas, sentence breaks only.
- Write a paragraph longer than 5 sentences. Break it up.
- Use list-bullet padding ("Also...", "Additionally...", "Moreover..."). Each bullet
  should add a distinct fact.

================================================================================
CITATION PATTERN EXAMPLES
================================================================================

  Direct quote:        Foo behaves as bar: "<quoted text>" [S1].
  Paraphrase:          Foo behaves as bar [S1].
  Multiple sources:    Foo behaves as bar across implementations [S1, S3].
  Inference:           Foo likely behaves as bar [inferred from <source/principle>].
  Speculation:         Foo may behave as bar [unverified, <reason>].
  Section confidence:  **Section confidence: high.** All claims cited [S1].

================================================================================
SECTION CONFIDENCE LADDER (END EACH MAJOR SECTION WITH ONE OF THESE)
================================================================================

  high   - every claim in the section is cited from a primary source.
  medium - >=1 inferred or unverified claim, but core claims are sourced.
  low    - half or more of claims are inference or unverified.

Examples:
  **Section confidence: high.** All claims sourced to README [S1].
  **Section confidence: medium.** Core mechanics from [S1]; "X" is inferred.
  **Section confidence: low.** Mostly speculative; verify against upstream.

================================================================================
FRONTMATTER VALIDATION CHEATSHEET
================================================================================

  title:           "<Topic> - Guide" (use plain hyphen, not em-dash)
  slug:            kebab-case lowercase per spec slug rule
                   - repo-url: <owner>-<repo> (lowercased)
                   - tool: lowercase tool name
                   - concept: short kebab-case of the topic
  type:            always "explanatory" for this artifact
  generated:       today's date YYYY-MM-DD
  last-verified:   same as generated for first run; update on later verifications
  source-count:    integer count of independently fetched sources
  confidence:      "high" | "medium" | "low-confidence draft"
                   - high:                3+ sources, >=1 class A, 0-2 unverified body claims
                   - medium:              1-2 sources, >=1 class A, <=5 unverified body claims
                   - low-confidence draft: 0 verified sources OR all class C
  audience:        one-line description of the intended reader
  maturity:        "experimental" | "active development" | "stable v1.x" |
                   "maintenance" | "deprecated"
  license:         SPDX identifier OR "proprietary" OR "n/a" (for concepts)

================================================================================
TOPIC-TYPE ADAPTERS (HOW CONTENT VARIES)
================================================================================

The skill handles three input types: repo, tool, and concept. Sections shift in
character. The per-section guidance below names how each section adapts.

  repo:    a GitHub URL. Has owners, license, README, docs, source files.
  tool:    a named tool / library / CLI. Has install command, version, package.
  concept: an idea, methodology, pattern, principle. No package, no command.

================================================================================
END HEADER. SECTION-BY-SECTION CONTENT BEGINS BELOW.
================================================================================
-->

<!--
================================================================================
SECTION 0: FRONTMATTER
================================================================================

PURPOSE: standardized machine-readable metadata at top of every guide.

INCLUDE: all 10 fields below. Do not omit fields - use "n/a" if truly unknown.

TOPIC-TYPE ADAPTERS:
- repo:    license = SPDX from repo; maturity = read from CHANGELOG / releases.
- tool:    license = SPDX from package metadata.
- concept: license = "n/a"; maturity = "stable" if widely accepted else
           "active development" if evolving.

ANTI-PATTERNS:
- Marking confidence: high without 3+ verified sources.
- Setting last-verified to a future date.
- Using freeform values for `maturity` instead of the enum.
- Forgetting to update last-verified after re-running the skill.
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
================================================================================

PURPOSE: warn the reader when confidence is below high.

WHEN TO INCLUDE: only when confidence != high.
WHEN TO REMOVE: delete the entire blockquote when confidence == high.

LENGTH: 1-2 sentences.

ADAPT THE WORDING:
- "medium-confidence draft" - have at least one fetched primary source
- "low-confidence draft" - no fetched sources OR all class C only

ANTI-PATTERNS:
- Using "low-confidence draft" wording when you have a fetched primary source.
- Skipping the banner because the document looks polished.
- Burying the warning in a paragraph instead of a blockquote.
-->
> **Status:** <medium-confidence draft | low-confidence draft>. <One-sentence honest reason>. See Sources & Evidence for the per-section breakdown.

# <Topic> - Guide

<!--
================================================================================
SECTION 1: AT A GLANCE
================================================================================

PURPOSE: 5-second skim. Reader knows what the topic is and whether to keep reading.
LENGTH: 8-12 table rows. No prose.

INCLUDE (suggested fields, adapt to topic):
- What:         one-sentence description
- Category:     family/class
- Who built it: author / org / origin
- License:      SPDX or n/a
- Source:       repo URL / package / canonical reference
- Cross-platform: list if applicable
- Audience:     one-line
- Cost:         free / freemium / paid / $X/mo / open-source
- Maturity:     status
- Stance:       project's own one-liner if memorable

TOPIC-TYPE ADAPTERS:
- repo:    Source = github.com/...; emphasize cross-platform, license, contributors.
- tool:    Source = package URL; emphasize CLI command, install method, host environments.
- concept: Source = first description / paper / origin moment; replace cross-platform with
           "Adjacent concepts" or "Origin"; replace cost with "Adoption cost".

ANTI-PATTERNS:
- Long prose values that wrap multiple lines (cap at one short line per cell).
- Marketing fluff in the Stance row.
- Including unverifiable values ("100x faster than alternatives") without citation.
- Skipping the section to "save space" - this is a load-bearing skim aid.

WHEN N/A: never. Every guide has facts to surface.

WORKED EXAMPLE (delete after writing your real At a Glance):

| Field | Value |
|-------|-------|
| **What** | Open-source memory infrastructure for AI tools |
| **Category** | Personal infra / shared persistent memory |
| **Who built it** | Nate B. Jones + community |
| **License** | FSL-1.1-MIT |
| **Source** | `github.com/example/example` |
| **Audience** | Operators with multi-tool AI workflows |
| **Cost** | Free (open source) |
| **Maturity** | Active development, public release |
| **Stance** | "Database with vector search and an open protocol" |

END EXAMPLE
-->
## At a Glance

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

<!--
================================================================================
SECTION 2: TABLE OF CONTENTS
================================================================================

PURPOSE: navigation. Auto-generate from H2 / important H3 headings.
LENGTH: ~20-25 lines.

INCLUDE:
- All H2s in document order
- Important H3s nested under their parent H2 (In-Depth Breakdown, FAQ)
- Resources sub-sections optional (they're short)

ANTI-PATTERNS:
- Stale TOC after section renames - regenerate at the end.
- Linking to non-existent anchors. Test in a markdown renderer.
- Including every H3 (clutter; only the ones the reader will jump to).

WHEN N/A: never. Required by spec.
-->
## Table of Contents

- [Executive Summary](#executive-summary)
- [Official Resources](#official-resources)
- [80/20 - High-Leverage Practices](#8020---high-leverage-practices)
- [Getting Started](#getting-started)
- [Key Terms](#key-terms)
- [In-Depth Breakdown](#in-depth-breakdown)
  - [Surface Layer - What It Is](#surface-layer---what-it-is)
  - [Structural Layer - How It's Organized](#structural-layer---how-its-organized)
  - [Mechanical Layer - How It Works](#mechanical-layer---how-it-works)
  - [Expert Layer - What's Non-Obvious](#expert-layer---whats-non-obvious)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Similar Tools & Alternatives](#similar-tools--alternatives)
- [Additional & Third-Party Resources](#additional--third-party-resources)
- [Sources & Evidence](#sources--evidence)

<!--
================================================================================
SECTION 3: EXECUTIVE SUMMARY
================================================================================

PURPOSE: complete summary the reader can stop after. Surfaces the top 3-5 takeaways.

LENGTH: 250-500 words. 3-6 paragraphs. End with a Key Takeaways blockquote (3-5 numbered items).

INCLUDE:
- Paragraph 1: what the topic is + headline framing + cite primary source
- Paragraph 2: the structural innovation or core mechanic that makes this distinct
- Paragraph 3: the failure modes addressed OR the problem space occupied
- Paragraph 4: practical operator impact - what changes when adopted
- Key Takeaways: 3-5 numbered items in a blockquote, each one a sharp claim with citation

WRITING ORDER: WRITE THIS LAST. After the body is complete. The exec summary
summarizes the actual document, not the intended document.

TOPIC-TYPE ADAPTERS:
- repo:    headline framing = README's tagline; takeaways = features that moved
           something for users.
- tool:    headline framing = problem-solution sentence; takeaways = practices.
- concept: headline framing = the key insight; takeaways = applications or implications.

ANTI-PATTERNS:
- Writing this first and never revisiting (will not match the actual body).
- Repeating headings ("In the Surface Layer below..."). The exec summary should
  read as a standalone document.
- Vague takeaways ("It's a useful tool"). Each takeaway should be a sharp,
  surprising or load-bearing claim.
- Marketing tone. Stay descriptive.

WHEN N/A: never.

WORKED EXAMPLE (delete after writing):

> Example is a database-backed personal memory layer for AI assistants. Built on
> PostgreSQL + pgvector, it stores captured thoughts as embeddings and exposes
> them through an MCP server so any compliant client can read or write the same
> persistent memory [S1]. The README's framing is direct: "this isn't a notes
> app, it's a database with vector search and an open protocol" [S1].
>
> The structural innovation is the rejection of middleware chains. Rather than
> stitching together SaaS services, Example collapses the architecture to
> "one database, one protocol, one chat-channel capture surface" [S1]. Capture
> happens through Slack or Discord; storage is Postgres+pgvector you own;
> access is MCP. Every connected AI tool sees the same memory.
>
> [continue for 2-3 more paragraphs]
>
> > **Key takeaways**
> >
> > 1. **It's plumbing, not an app.** Whatever AI client you use is the UI [S1].
> > 2. **Memory is unified through MCP** + a single Postgres+pgvector instance [S1].
> > 3. **Capture is intentionally low-friction** via Slack or Discord [S1].
> > 4. **The license is FSL-1.1-MIT** (delayed-MIT for commercial uses) [S1].
> > 5. **The learning path is the documentation** through six progressive
> >    extensions [S1].

END EXAMPLE
-->
## Executive Summary

<Paragraph 1: What the topic is, who built it, and the headline framing. Cite primary source.>

<Paragraph 2: The structural innovation or core mechanic. What makes this topic distinct from adjacent options.>

<Paragraph 3: The failure modes the topic addresses or the problem space it occupies.>

<Paragraph 4: Practical operator impact. What changes when a user adopts this.>

> **Key takeaways**
>
> 1. **<Sharp claim>.** <One-line elaboration with citation> [S1].
> 2. **<Sharp claim>.** <One-line elaboration> [S1].
> 3. **<Sharp claim>.** <One-line elaboration> [S1].
> 4. **<Sharp claim>.** <One-line elaboration> [S1].
> 5. **<Sharp claim>.** <One-line elaboration> [S1].

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 4: OFFICIAL RESOURCES
================================================================================

PURPOSE: canonical links the reader should bookmark, surfaced near the top so
the reader can jump out to authoritative material immediately.

LENGTH: 5-10 table rows. No prose.

INCLUDE: only OFFICIAL sources here. Community, third-party, or unverified
resources go in the bottom "Additional & Third-Party Resources" section.

3-column table format: Resource | URL | Use for

TOPIC-TYPE ADAPTERS:
- repo:    Source repo, marketplace listing, docs site, community channel,
           issue tracker, dedicated AI helpers if any.
- tool:    Package URL, docs, marketplace listing, GitHub issues, Stack
           Overflow tag if active.
- concept: Original paper / first description, the most-cited textbook,
           authoritative blog by the originator, conference talks.

ANTI-PATTERNS:
- Mixing community resources here.
- Listing every URL in the README - keep to the 5-10 most useful.
- Using opaque labels ("Page 1", "Doc 2"). Each "Use for" should tell the reader
  what they would click for.

WHEN N/A: rare. For a brand-new concept, list 1-2 originating sources at minimum.

WORKED EXAMPLE (delete after writing):

| Resource | URL | Use for |
|----------|-----|---------|
| Source repo | `github.com/example/example` | Code, README, individual docs |
| Marketplace | `github.com/example/marketplace` | Plugin install (alt path) |
| Substack | `example.substack.com` | Author updates, longform context |
| Discord | `discord.gg/abc123` | Real-time community questions |
| Issues | `github.com/example/example/issues` | Bug reports, feature requests |

END EXAMPLE
-->
## Official Resources

| Resource | URL | Use for |
|----------|-----|---------|
| <name of resource> | `<url>` | <when reader would click this> |
| <e.g., Source repo> | `<github.com/org/repo>` | Code, README, docs |

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 5: 80/20 - HIGH-LEVERAGE PRACTICES
================================================================================

PURPOSE: the 5-7 actions or practices that deliver disproportionate value.
This is the highest-utility section for an experienced reader.

LENGTH: 5-7 numbered practices. Each practice = 1-3 sentences + Impact/Effort line.
~600-1000 words total.

EACH PRACTICE FORMAT:
  ### N. <Practice phrased as an imperative>
  <1-3 sentences explaining what to do and why it works. Cite primary source.>

  - **Impact:** <what failure mode this prevents or what gain this captures>.
  - **Effort:** <how hard it is to adopt: trivial / marginal / moderate / heavy>.

NOTE: Impact and Effort MUST be a two-bullet list, not a single inline sentence.
Inline runs together visually and is hard to scan. The bullet form gives the
reader two distinct pieces of information they can compare across practices.

End the section with a "Key insight" pull quote synthesizing the practices.

TOPIC-TYPE ADAPTERS:
- repo:    practices = adoption + day-one operations.
- tool:    practices = usage discipline + integration patterns.
- concept: practices = "if you do nothing else, do these" applications +
           common scenarios where the concept changes a decision.

ANTI-PATTERNS:
- Listing every feature instead of the high-leverage subset.
- Including practices the user already does by default.
- Practices that sound generic (e.g., "Read the docs"). Be specific to the topic.
- Skipping the Impact/Effort bullets - those are the load-bearing decision aid.
- Running Impact and Effort together on one line - always use a two-bullet list.

WHEN N/A: never. Every topic has high-leverage practices, even if they're
"approach with skepticism" or "don't use".

WORKED EXAMPLE (delete after writing):

### 1. Trust the brainstorming pass, even when the request seems clear

The brainstorming step is the cheapest place to catch design errors. Going
through it on a request that turns out to be simple costs ~30 seconds.
Skipping it on a complex request costs hours of rework. The 1% rule is
calibrated for that asymmetry [S1].

- **Impact:** prevents "I built the wrong thing" failures.
- **Effort:** trivial.

[continue for 4-6 more practices]

> **Key insight:** The first three practices prevent failure modes; the last
> two prevent failure-mode-creation. Together they cover most of the gap
> between "agent wrote code" and "agent wrote correct code".

END EXAMPLE
-->
## 80/20 - High-Leverage Practices

<One-line framing: why these matter and how the reader should approach them.>

### 1. <Practice phrased as an action / verb>

<1-3 sentences explaining what to do and why it works. Cite primary source.>

- **Impact:** <what failure mode this prevents or what gain this captures>.
- **Effort:** <how hard it is to adopt>.

### 2. <Practice phrased as an action / verb>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

### 3. <Practice phrased as an action / verb>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

### 4. <Practice phrased as an action / verb>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

### 5. <Practice phrased as an action / verb>

<1-3 sentences.>

- **Impact:** <...>.
- **Effort:** <...>.

> **Key insight:** <One sentence that synthesizes the practices above into a single observation.>

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 6: GETTING STARTED
================================================================================

PURPOSE: orientation for someone new to this topic. From "I just heard of this"
to "I have something running / I can apply this".

LENGTH: 200-450 words.

INCLUDE:
- Minimum-viable mental model (one or two sentences capturing the core)
- One concrete first step (install command for tools/repos; mental exercise
  for concepts)
- "First-session expectations" sub-section: 4-5 bullets describing what the
  user will observe in their first encounter

TOPIC-TYPE ADAPTERS:
- repo:    install command + first run + initial behavior.
- tool:    install command + minimal usage example + expected output.
- concept: minimum mental exercise + first concrete application + how to know
           you've absorbed the model.

ANTI-PATTERNS:
- Reproducing the full install guide. The quick-ref artifact owns that.
- Burying the mental model in prose. Lead with it.
- Skipping "first-session expectations" - this is what tells the reader if
  things are going right.

WHEN N/A: rare. For purely theoretical concepts, replace install with a
one-paragraph "first time you'll see this in the wild" example.

WORKED EXAMPLE (delete after writing):

The minimum-viable mental model: **example turns "what should the agent do
next?" into a question the agent looks up rather than guesses at.**

For Claude Code:

```
/plugin install example@official-marketplace
```

The first conversation after install loads the entry-point skill
automatically [S1]. From there, the agent will:

1. Invoke the brainstorming skill before any code change.
2. Isolate the work in a worktree.
3. Plan tasks at 2-5 minute granularity.
4. Run TDD inside each task.
5. Verify before claiming "done" [S1].

**First-session expectations:**
- The first response feels slower (the agent is brainstorming).
- Work proceeds in 2-5 minute chunks rather than monolithic generations.
- Tests appear before code, not after.
- "Done" claims arrive with verification output.

END EXAMPLE
-->
## Getting Started

The minimum-viable mental model: **<one or two sentences capturing the topic's core conceptual move>**. <Optional follow-up sentence with more detail.>

<For repos/tools, include a concrete install / first-use snippet:>

```
<concrete first command>
```

<Brief explanation of what happens next, citing primary source.>

**First-session expectations:**
- <observable behavior 1>
- <observable behavior 2>
- <observable behavior 3>
- <observable behavior 4>

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 7: KEY TERMS
================================================================================

PURPOSE: glossary of topic-specific vocabulary the reader needs to track.

LENGTH: 8-20 terms. 2-column table.

INCLUDE:
- Domain terms the reader needs to understand the rest of the document.
- Project-specific jargon. Skip terms that any reader will know.
- One-sentence definition per term, citing source or marking [inferred].

WRITING ORDER: build this AS YOU WRITE the In-Depth Breakdown. Note terms
to define when you encounter them; finalize the glossary after the breakdown
is complete.

TOPIC-TYPE ADAPTERS:
- repo:    project-specific names + roles (extensions, plugins, etc.) + adopted
           industry terms used in non-standard ways.
- tool:    CLI flags, configuration keys, named patterns from the docs.
- concept: defined terms from the originating paper + adjacent concepts the
           reader will mix this up with.

ANTI-PATTERNS:
- Defining terms the audience already knows ("Git is a version control system").
- Multi-sentence definitions that reproduce the breakdown. Keep to one sentence.
- Skipping inferences silently - mark [inferred] when the term is general
  knowledge applied to this domain.

WHEN N/A: skip if topic has no domain-specific vocabulary (rare).

WORKED EXAMPLE (delete after writing):

| Term | Definition |
|------|-----------|
| **Skill** | A named, reusable workflow with a triggering condition [S1]. |
| **Trigger description** | The "use when..." text defining when a skill should fire [S1]. |
| **Subagent** | A fresh agent instance dispatched for a specific task [S1]. |
| **Worktree** | A separate working directory checked out from the same Git repo [inferred, standard Git terminology]. |
| **The 1% rule** | "If there's a 1% chance a skill might apply, invoke it" [S1]. |

END EXAMPLE
-->
## Key Terms

| Term | Definition |
|------|-----------|
| **<term>** | <one-sentence definition> [S1]. |
| **<term>** | <one-sentence definition> [S1]. |
| **<term>** | <one-sentence definition> [inferred, <reason>]. |

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 8: IN-DEPTH BREAKDOWN
================================================================================

PURPOSE: the heart of the document. Four progressive-disclosure layers, each
addressing a different reader question and using different content density.

LENGTH: 2200-4000 words total across all four layers. This section is the
single biggest chunk of the document. Lean into prose; do not try to fit the
whole topic into tables.

DO NOT MIX LAYERS. If something belongs to a deeper layer, leave it out of the
shallower layer. The whole point is progressive disclosure.

WRITING ORDER: write Surface, then Structural, then Mechanical, then Expert.
Surface is short; Structural is mid-length; Mechanical is the longest.

PROSE DENSITY RULE: every #### sub-heading inside Structural and Mechanical
gets at least 2-3 paragraphs of prose. One-liners under a heading make the
section feel sparse and harder to read. If you only have one sentence under a
heading, fold it into the parent paragraph instead of giving it its own H4.

TOPIC-TYPE ADAPTERS:
- repo:    Surface = what + audience + license; Structural = directory layout +
           components; Mechanical = how the runtime works end-to-end; Expert =
           edge cases + maintainer wisdom.
- tool:    Surface = what + category; Structural = subsystems + flags;
           Mechanical = invocation lifecycle; Expert = performance gotchas +
           idiomatic usage.
- concept: Surface = what + origin + adjacent concepts; Structural =
           sub-concepts + relationships; Mechanical = how the concept applies
           in practice; Expert = subtle distinctions + common misapplications.
-->
## In-Depth Breakdown

<!--
================================================================================
SUB-SECTION 8.1: SURFACE LAYER
================================================================================

PURPOSE: answers "What is this thing?" for a total newcomer.
LENGTH: 200-400 words. 2-4 paragraphs.

INCLUDE:
- Category framing (what family/class does this belong to?)
- Authors, license, source
- Audience and value proposition
- Optional pull quote with the project's most memorable framing

ANTI-PATTERNS:
- Going into how it works (that's the Mechanical layer).
- Listing components (that's Structural).
- Skipping the category framing - it's the orientation move.

WORKED EXAMPLE (delete after writing):

Example is a **plugin in the agent-skills category**, in the same family as
Anthropic's official Skills system and other community libraries (superpowers,
plugin-dev, claude-mem). It is distinct from those because **it is not a
toolkit for building skills.** It is a curated, opinionated set of finished
skills [S1].

It was built by the Example Project maintainers and is published
under the MIT license [S1]. The source repository is `github.com/example/example`.
Distribution is through plugin marketplaces [...].

The audience is operators running coding agents who have been bitten by the
failure modes the methodology addresses [...]. **If those problems are
theoretical to you, the value proposition is theoretical too.**

> **Pull quote:** "This isn't a notes app or another wrapper. It's a methodology."

END EXAMPLE
-->
### Surface Layer - What It Is

<Paragraph 1: Category framing. What family/class does this belong to? What adjacent options exist?>

<Paragraph 2: Authors, license, source. Who built it; under what terms.>

<Paragraph 3: Audience and value proposition. Who benefits and when.>

<Optional pull quote:>

> **<Memorable framing or quote from the source materials>.**

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SUB-SECTION 8.2: STRUCTURAL LAYER
================================================================================

PURPOSE: answers "How is this thing organized?" for a reader who has decided
to investigate further.

LENGTH: 600-1000 words. At least one diagram, table, or structured list, plus
real prose introducing each axis. Do NOT make this a wall of tables.

STRUCTURE PATTERN:
1. Open with a multi-sentence framing paragraph that names the structural
   axes (typically 2-4) and explains how they compose. Stress that the axes
   are not independent - the topic's mechanism comes from how they fit
   together.
2. Use H4 (####) sub-headings - one per axis - with a numbered prefix
   ("#### Axis 1 / The X", "#### Axis 2 / The Y").
3. Under each H4, write 2-3 paragraphs of prose that contextualize the axis
   BEFORE the table or code block. The table/code block alone is not enough.
4. Close with a 1-2 sentence synthesis paragraph that names what the axes
   produce together.

INCLUDE:
- The named parts (components, modules, sub-systems)
- The relationships among parts (this is the load-bearing piece)
- A pipeline / workflow diagram if applicable

ANTI-PATTERNS:
- Going into runtime mechanics (that's the Mechanical layer).
- Listing parts without relationships - the structure IS the relationships.
- One wall of prose. Use a table for parts, a code block for pipelines.
- One wall of tables. Tables alone do not explain how axes compose.
- Using a single H4 with no other H4s nearby. If only one sub-heading is
  needed, drop the H4 and run the structure as one section.

WORKED EXAMPLE (delete after writing):

Example organizes its work along three axes that compose together. **Skills**
are the units of behavior. **A workflow** is the canonical order in which
skills fire. **A trigger system** is the mechanism that decides which skill
applies. Each axis is necessary; none of them is sufficient on its own. Read
the three subsections below as one composed mechanism, not three independent
features.

#### Axis 1 / The fourteen skills, grouped by function

The first axis is the catalog. Example ships fourteen skills, partitioned
across four functional groups. <Brief framing of what each group covers and
why the partition is shaped this way.>

| Group | Skill | One-line role |
|-------|-------|---------------|
| Testing | `test-driven-development` | RED-GREEN-REFACTOR with anti-patterns |
| ... | ... | ... |

<Closing paragraph: how skills inside a group share assumptions and how skills
across groups compose by handing each other artifacts.>

#### Axis 2 / The sequential workflow

The second axis takes the catalog and orders it. <2-3 sentences naming the
shape of the pipeline and what makes the order intentional.>

```
brainstorming -> using-git-worktrees -> writing-plans -> ...
```

<2-3 sentences mapping the pipeline to the underlying principles. Cite [S1].>

#### Axis 3 / The trigger system

The third axis is what makes the first two load-bearing instead of advisory.
<2-3 paragraphs explaining the trigger mechanic, including the structurally
important detail of WHEN the check fires (e.g., before clarifying questions).>

<Closing synthesis paragraph: how the three axes combine to produce the
mechanism.>

END EXAMPLE
-->
### Structural Layer - How It's Organized

<Opening framing paragraph (3-5 sentences). Name the 2-4 structural axes that
the topic organizes its work along. Explain how they compose - that the axes
are not independent. Set the reader up to read the H4 subsections below as
one composed mechanism.>

#### Axis 1 / <Sub-heading: components or parts>

<Paragraph 1 (2-4 sentences): What this axis is and why it matters. Frame
what the table below shows BEFORE the table.>

| Group | Item | One-line role |
|-------|------|---------------|
| <category> | <component> | <role> |
| <category> | <component> | <role> |

<Paragraph 2 (2-4 sentences): Closing prose - how the items in the table
relate to each other, what the grouping reveals, what an experienced reader
should take away from the catalog. Cite primary source.>

#### Axis 2 / <Sub-heading: workflow or relationships>

<Paragraph 1 (2-3 sentences): What this axis is and why it matters. Set up
the diagram below.>

```
<flow diagram or pipeline>
```

<Paragraph 2 (2-4 sentences): How the diagram maps to the topic's principles
or design choices. Why this order, this composition. Cite primary source.>

#### Axis 3 / <Sub-heading: another structural axis if relevant>

<2-3 paragraphs of prose. The third axis is often the load-bearing one
(triggers, configuration, runtime gating). Spend the words to explain not
just what it is, but WHEN it fires and what makes it structurally important
rather than advisory.>

<Closing synthesis paragraph (2-3 sentences): How all the axes combine to
produce the topic's mechanism. This is the bridge to the Mechanical Layer.>

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SUB-SECTION 8.3: MECHANICAL LAYER
================================================================================

PURPOSE: answers "How does this thing actually work?" for an operator who needs
to use the topic effectively. Most of the document's depth lives here.

LENGTH: 1000-2000 words. Numbered phases or sub-systems with #### sub-headings.
This is the longest sub-section in the document; do not under-spend.

INCLUDE:
- End-to-end mechanics
- Key sub-systems and their interactions
- Data flow / control flow
- Numbered phases if there's a sequence (use #### Phase N - Name format)
- Optional pull quote synthesizing the mechanics

WRITE EACH PHASE/SUB-SYSTEM AS:
  #### Phase N - <Phase name>
  <2-4 paragraphs describing:
   - What triggers the phase (the conditions that cause it to fire)
   - The internal steps the phase runs (its sub-mechanics)
   - The artifact / state change the phase produces
   - Why the phase exists - which failure mode it addresses
   Cite primary source for each load-bearing claim.>

PROSE DENSITY RULE: each phase needs at least 100-200 words. A phase that is
only 1-2 sentences is structurally suspect; either it should be folded into
an adjacent phase, or it needs more detail. The reader is here for depth.

ANTI-PATTERNS:
- Skipping sub-headings (one wall of text is unreadable).
- One-sentence phases (the user explicitly flagged this as too sparse).
- Mixing phases out of order without flagging it.
- Repeating Surface or Structural content.
- Skipping pull quotes - they're cheap punctuation.
- Listing what the phase does without explaining WHY it exists. The "why" is
  what makes the mechanics legible.

WORKED EXAMPLE (delete after writing):

The actual mechanics of running a task under example, phase by phase.

#### Phase 1 - Pre-action skill check

When the user sends a message, the agent's first internal step is "does any
skill apply?" The decision rule is biased aggressively toward "yes" [...] [S1].

#### Phase 2 - Brainstorming

For any creative work, brainstorming fires and runs a Socratic refinement [...].

[...continue for all phases...]

> **Pull quote:** "The skill is rigid by design. Pre-test code gets deleted.
> Performative agreement gets pushed back. Done claims need evidence."

END EXAMPLE
-->
### Mechanical Layer - How It Works

<2-3 sentence introduction: name what "running this thing" actually means and
how many phases the mechanics break into. Set the reader up for the depth
that follows.>

#### Phase 1 - <Phase name>

<2-4 paragraphs. Cover: (1) what triggers this phase, (2) the internal steps
it runs, (3) the artifact / state change it produces, (4) which failure mode
it exists to address. Cite primary source.>

#### Phase 2 - <Phase name>

<2-4 paragraphs in the same shape. Do not skimp - if a phase only needs one
sentence, fold it into an adjacent phase instead.>

#### Phase 3 - <Phase name>

<2-4 paragraphs.>

<...continue for all phases / sub-systems...>

<Optional pull quote synthesizing the mechanics:>

> **<Pull quote that captures the operating principle>.**

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SUB-SECTION 8.4: EXPERT LAYER
================================================================================

PURPOSE: answers "What's non-obvious about this?" for someone who has used the
topic and wants to deepen.

LENGTH: 400-800 words. 5-10 sub-points, each with a bold lead phrase + paragraph.

INCLUDE:
- Edge cases and foot-guns
- Subtle semantics
- Performance characteristics or constraints
- Hidden invariants the maintainers keep in mind
- Critical patterns that operators eventually learn

EACH SUB-POINT FORMAT:
  #### <Insight phrased as a sentence>
  <1-2 paragraphs explaining the insight. Bold the lead phrase.>

CONTENT ALMOST EXCLUSIVELY FROM CLASS A OR B SOURCES. Mark inferences clearly.

ANTI-PATTERNS:
- Repeating Structural content with longer paragraphs.
- Listing surface-level features as "expert insights".
- Skipping citations - this layer especially needs them since insights sound
  authoritative.

WORKED EXAMPLE (delete after writing):

Several things about example only become visible after working with it for
a while.

#### The skill check fires before clarifying questions

This sounds minor but is structurally important. **Superpowers reverses the
naive pattern**: agent receives message, checks skills, the skill might tell
it how to ask the clarifying question [S1].

#### The "1% rule" is about regret asymmetry

Invoking a skill that turns out to be wrong is cheap (the agent just does not
use it). **Not invoking a skill that would have applied is expensive** [...] [S1].

[...continue for 5-10 insights...]

END EXAMPLE
-->
### Expert Layer - What's Non-Obvious

Several things about <topic> only become visible after working with it for a while.

#### <Sub-heading: a non-obvious insight>

<1-2 paragraphs explaining the insight, why it matters, and how it manifests. Bold lead phrase optional.>

#### <Sub-heading: another insight>

<1-2 paragraphs.>

#### <Sub-heading: another insight>

<1-2 paragraphs.>

<...continue for 5-10 insights...>

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 9: FREQUENTLY ASKED QUESTIONS
================================================================================

PURPOSE: answer the questions a reader will actually have, derived from real
friction (issue tracker, Discord, Stack Overflow, the document's own gaps).

LENGTH: ~5 categories, ~10 Q/A pairs total.

REQUIRED:
- >=3 categories, >=8 Q/A total, >=2 per category
- Categories must be derived from the topic, NOT templated

BANNED QUESTION SHAPES:
- "What is <topic>?"
- "Why should I use <topic>?"
- "How do I install <topic>?"
- Any question whose answer is <=1 sentence

EACH Q/A FORMAT:
  **Q: <Specific friction-driven question>**
  A: <2-5 sentence substantive answer with citation> [S1]

TOPIC-TYPE ADAPTERS:
- repo:    Adoption & Setup, Workflow Discipline, Multi-User / Concurrency,
           Customization, Troubleshooting.
- tool:    Adoption, Configuration, Performance, Integration with X, Migration,
           Troubleshooting.
- concept: Mental model, Edge cases, Practical application, Common
           misconceptions, Related concepts.

CATEGORIES MUST FIT THE TOPIC. Don't force a "Performance" category if there's
no performance question to answer.

ANTI-PATTERNS:
- Banned question shapes (definitional/marketing/setup).
- 1-sentence answers (suggests the question shouldn't be there).
- Categories that don't fit (e.g., "Performance" with no real performance
  question, padded with filler).
- Q/As without citation (every answer should have a source or [unverified]).

WHEN N/A: never. Even concepts have FAQ-worthy friction.

WORKED EXAMPLE (delete after writing):

### Adoption & Setup

**Q: Can I run example on Codex CLI as well as Claude Code, and do I get the same skills?**
A: Yes. The README documents installation paths for [...] [S1]. The skill set
is the same across hosts; what changes is the install command [...]. Cross-platform
consistency is a deliberate design goal [S1].

**Q: How long does adoption take in practice?**
A: Install is one command per host. Behavioral change happens on the first
conversation after install. The discipline takes longer to internalize [...]
[unverified, plausible].

[...continue for 4 more categories, 6 more Q/A...]

END EXAMPLE
-->
## Frequently Asked Questions

### <Category 1: e.g., Adoption & Setup>

**Q: <Specific, friction-driven question>**
A: <Substantive answer of 2-5 sentences. Cite source.> [S1]

**Q: <Another question>**
A: <Answer.> [S1]

### <Category 2: e.g., Workflow Discipline>

**Q: <Question>**
A: <Answer.> [S1]

**Q: <Question>**
A: <Answer.> [S1]

**Q: <Question>**
A: <Answer.> [S1]

### <Category 3: e.g., Multi-Agent / Concurrency / Scale>

**Q: <Question>**
A: <Answer.> [S1]

**Q: <Question>**
A: <Answer.> [S1]

### <Category 4 (optional): e.g., Customization & Extension>

**Q: <Question>**
A: <Answer.> [S1]

**Q: <Question>**
A: <Answer.> [unverified, <reason>]

### <Category 5 (optional): e.g., Troubleshooting>

**Q: <Question>**
A: <Answer.> [S1]

**Q: <Question>**
A: <Answer.> [S1]

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 10: SIMILAR TOOLS & ALTERNATIVES
================================================================================

PURPOSE: position the topic in its competitive/adjacent landscape. Help the
reader decide whether the topic fits their situation.

LENGTH: ~250-450 words. 1 comparison table + 2 short bullet lists.

INCLUDE:
- Comparison table: 4 columns (Approach | What it is | Best for |
  Trade-off vs. <topic>). 3-7 rows.
- "When to choose <topic>" bullet list (3-4 items)
- "When <topic> may be overkill" bullet list (2-3 items)

TOPIC-TYPE ADAPTERS:
- repo:    competing repos, vendor SaaS alternatives, hand-rolled options.
- tool:    competing tools at the same layer + adjacent tools that solve
           overlapping problems differently.
- concept: alternative frameworks, predecessor concepts, refinements or
           extensions.

ANTI-PATTERNS:
- Listing alternatives without trade-offs (the trade-off column is the value).
- Marketing the focal topic ("OB1 is best for X" everywhere).
- Skipping "When this may be overkill" - that builds reader trust.

WHEN N/A: rare. For foundational concepts with no direct competitors, write
"n/a for foundational concepts; the closest comparison is between formal and
informal versions of the concept itself" and explain the formal/informal axis.

WORKED EXAMPLE (delete after writing):

| Approach | What it is | Best for | Trade-off vs. example |
|----------|-----------|----------|------------------------|
| **Vanilla agent** | Use the host without a methodology plugin | One-off tasks | Maximum flexibility; no structural guardrails |
| **Other plugin** | Personal skill library | Operators wanting smaller scope | Different category; complements rather than replaces |
| **Hand-rolled rules** | Project-level prompt documents | Teams wanting explicit version-controlled rules | Maintenance burden; weaker enforcement |

### When to choose example

- The team uses 2+ AI clients and wants consistent behavior.
- Past projects have hit failure modes example prevents.
- Operators are willing to slow down at the start in exchange for fewer late-stage rework cycles.

### When example may be overkill

- Tasks are one-off, exploratory, or research-grade.
- Single-operator workflows where cross-platform portability is not valued.

END EXAMPLE
-->
## Similar Tools & Alternatives

| Approach | What it is | Best for | Trade-off vs. <topic> |
|----------|-----------|----------|----------------------|
| **<Alternative 1>** | <one-line description> | <when to use it> | <how it differs from the topic> |
| **<Alternative 2>** | <one-line description> | <when to use it> | <difference> |
| **<Alternative 3>** | <one-line description> | <when to use it> | <difference> |

### When to choose <topic>

- <Situation 1 where this is the right choice.>
- <Situation 2.>
- <Situation 3.>

### When <topic> may be overkill

- <Situation 1 where simpler options suffice.>
- <Situation 2.>

**Section confidence: <high | medium | low>.** <One-line justification.>

<!--
================================================================================
SECTION 11: ADDITIONAL & THIRD-PARTY RESOURCES
================================================================================

PURPOSE: deeper resource library beyond the canonical "Official Resources"
table at the top.

LENGTH: >=5 total entries across the four sub-sections. Use bullet lists.

REQUIRED SUB-SECTIONS (in this order):
- Official (high-quality entries that didn't fit the top table)
- Community & Tutorials
- Deep-Dive / Advanced
- Related Tools

EACH ENTRY FORMAT:
  - `<resource name or url>` / <one-line description> [Sn or unverified]

TOPIC-TYPE ADAPTERS:
- repo:    Official = repo files (CHANGELOG, CONTRIBUTING); Community =
           tutorials, blog posts; Advanced = source code reading paths;
           Related = other plugins/tools.
- tool:    Official = docs, marketplace; Community = SO tags, blog posts;
           Advanced = source / reference impl; Related = competing tools.
- concept: Official = original paper, canonical book; Community = blog
           explainers; Advanced = follow-up papers, extensions; Related =
           adjacent concepts.

ANTI-PATTERNS:
- Duplicating entries that are already in Official Resources at top.
- Listing every tutorial - keep to 2-3 highest-quality.
- Forgetting "Related Tools" - this is where the reader finds adjacent options.

WHEN N/A: rare. For very obscure topics, list 1-2 entries per sub-section minimum.
-->
## Additional & Third-Party Resources

### Official

- `<url or identifier>` / <one-line description> [S1]
- `<url>` / <description> [S1]

### Community & Tutorials

- <Resource name> / <description> [S1 or unverified]
- <Resource name> / <description>

### Deep-Dive / Advanced

- <Resource name> / <description> [S1]
- <Resource name> / <description> [unverified, <reason>]

### Related Tools

- **<Tool name>** / <one-line description>
- **<Tool name>** / <description>

<!--
================================================================================
SECTION 12: SOURCES & EVIDENCE
================================================================================

PURPOSE: full traceability for every claim in the document. The reader who
wants to verify or extend the doc starts here.

LENGTH: variable. ~250-500 words for typical guide.

REQUIRED SUB-SECTIONS:
- Primary Sources (mandatory)
- Supporting Sources (optional - omit if no class-B/C corroborating sources)
- Confidence Markers Used (mandatory)
- Unverified Claims (mandatory if any [unverified] in body)
- Source-to-Section Traceability (mandatory)
- Gaps (mandatory)

CREDIBILITY CLASSES:
- A: official / authoritative (project's own docs, RFC, spec)
- B: maintainer or recognized expert (blog, talk)
- C: community reference (tutorial, SO answer)

ANTI-PATTERNS:
- Listing sources that aren't actually cited in the body.
- Missing entries in Unverified Claims for [unverified] flags in the body.
- "Gaps" section as filler. Should reflect real gaps in the source coverage.
- Misrating credibility (a fan blog is class B if the author is a recognized
  expert; class C otherwise).

WHEN N/A: never. Required by spec.
-->
## Sources & Evidence

### Primary Sources

- **[S1]** <Title>, retrieved <YYYY-MM-DD> from `<URL>`. Credibility <A | B | C>. <One-line note about what this source covers.>
- **[S2]** <Title>, retrieved <YYYY-MM-DD>. Credibility <A | B | C>.

### Supporting Sources

<!-- Omit this sub-section if no class-B/C corroborating sources exist. -->

- **[S3]** <Title>, retrieved <YYYY-MM-DD>. Credibility B. <Note.>

### Confidence Markers Used

| Marker | Meaning |
|--------|---------|
| `[S1]`, `[S2]`, ... | Directly cited or quoted from the numbered source. |
| `[inferred]` | Derived from documented architecture or design principles, not stated explicitly. |
| `[unverified]` | Model knowledge or speculation. Reader should verify before relying on. |
| **Section confidence: high** | All claims directly sourced from primary materials. |
| **Section confidence: medium** | Mix of sourced claims and inferences from documented framing. |
| **Section confidence: low** | Mostly speculative or inferred; verify against current upstream documentation. |

### Unverified Claims

| Claim | Where it appears | Why it's unverified |
|-------|------------------|---------------------|
| "<exact text of the claim>" | <Section name> | <Why this is not directly sourced.> |
| "<claim>" | <Section> | <Reason.> |

### Source-to-Section Traceability

| Section | Primary Sources | Inferred / Unverified |
|---------|-----------------|----------------------|
| At a Glance | <Sn> | <list inferences if any> |
| Official Resources | <Sn> | <inferences> |
| Executive Summary | <Sn> | <inferences> |
| 80/20 Practices | <Sn> | <inferences> |
| Getting Started | <Sn> | <inferences> |
| Key Terms | <Sn> | <inferences> |
| Surface Layer | <Sn> | <inferences> |
| Structural Layer | <Sn> | <inferences> |
| Mechanical Layer | <Sn> | <inferences> |
| Expert Layer | <Sn> | <inferences> |
| FAQ | <Sn> | <inferences> |
| Similar Tools | <Sn or "interpretive"> | <inferences> |
| Resources | <Sn> | <inferences> |

### Gaps

Topics adjacent to this guide that the available sources did not cover.

| Gap | Where to look |
|-----|---------------|
| <topic the sources missed> | <suggested investigation path> |
| <gap> | <where to look> |

<!--
================================================================================
CROSS-ARTIFACT REFERENCES
================================================================================

The guide is one of three artifacts the skill produces. The other two are:

  - <slug>_quickref.md  - operator-only quick reference, ~70% tabular
  - <slug>_quickref.pdf - 2-page rendered PDF of the quick reference

If a quick-ref version of this topic exists, link to it from the Resources
section's "Related" sub-section or from the Getting Started section, e.g.:

  > See also: <slug>_quickref.pdf for a 2-page operator cheat sheet.

Bidirectional linking helps readers move between the explanatory and reference
artifacts based on their need.

================================================================================
-->

<!--
================================================================================
FINAL CHECKLIST (REMOVE BEFORE SHIPPING)
================================================================================

Run through this list before declaring the guide done.

FRONTMATTER
- [ ] All 10 fields populated; no "n/a" except where genuinely unknown
- [ ] confidence value matches the actual source-count and unverified-claim count
- [ ] last-verified is today (or the date of last verification pass)

STRUCTURE
- [ ] All required H2 sections present in canonical order
- [ ] Section reorder applied: At a Glance / TOC / Executive Summary / Official Resources
- [ ] Each major section ends with **Section confidence: ...** line
- [ ] Confidence banner present iff confidence != high
- [ ] Confidence banner wording is accurate to the case

CONTENT
- [ ] Executive Summary written LAST (matches actual body)
- [ ] At a Glance has 8-12 rows
- [ ] Official Resources has 5-10 rows, OFFICIAL only
- [ ] 80/20 has 5-7 practices, each with Impact + Effort
- [ ] Getting Started has mental model + concrete first step + first-session expectations
- [ ] Key Terms has 8-20 terms with citations or [inferred] markers
- [ ] All four PD layers have substantive content (no layer skipped)
- [ ] Mechanical Layer uses #### sub-headings for phases/sub-systems
- [ ] Expert Layer has 5-10 insights with bold lead phrases
- [ ] FAQ has >=3 categories and >=8 Q/A pairs, >=2 per category
- [ ] No banned FAQ shapes ("What is X?", "Why use X?", "How install X?")
- [ ] No FAQ answer is <=1 sentence
- [ ] Similar Tools has comparison table + when-to-choose + when-overkill lists

SOURCING
- [ ] Every cited [Sn] appears in Sources & Evidence
- [ ] Every [unverified] flag in body has a row in Unverified Claims
- [ ] Source-to-Section Traceability table covers all sections
- [ ] Gaps table reflects real gaps, not filler

WRITING
- [ ] No em-dashes or en-dashes (find/replace U+2014 and U+2013)
- [ ] No marketing prose (find/replace "powerful", "elegant", "intuitive", etc.)
- [ ] No paragraphs longer than 5 sentences
- [ ] All HTML comments removed
- [ ] All <placeholder> tokens replaced
- [ ] Word count between 1,500 and 6,000 (target: 3,000-5,500 for comprehensive)

CROSS-ARTIFACT
- [ ] Linked to companion quick-ref artifact if one exists
- [ ] Slug matches frontmatter and filename

================================================================================
END OF TEMPLATE
================================================================================
-->
