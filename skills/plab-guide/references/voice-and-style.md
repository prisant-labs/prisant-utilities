# Voice & Style Reference

Voice and style rules that apply to **all four artifacts** (standard MD guide, ADHD MD guide, quick-reference HTML, quick-reference PDF). The skill must conform to these rules before write; gate G-11 enforces the em-dash ban via grep verification (no auto-rewrite script).

> **Note:** This reference file contains literal em-dash and en-dash characters in its rule documentation (the table that lists the codepoints) and in two "before" examples that demonstrate LLM-default bad prose. The G-11 gate applies to *output* artifacts (the four generated files), not to the skill's own reference material. The em-dashes here are sanctioned because they document or demonstrate the rule.

## Use when

- Drafting any artifact section
- Reviewing the output of a fill phase before moving to the next
- Triaging "this output reads like a generic LLM summary" complaints

## DO

- **Lead with the claim, support with citation.** "X happens. [S1]" not "Per the documentation, it appears that X may happen."
- **Direct, declarative sentences.** Not "this can be useful when" but "use this when".
- **Show failure modes, not just features.** Operators care more about what breaks than what works.
- **Bold the load-bearing word** in every paragraph. Helps skim-readers find the substantive claim.
- **Mark inferences (`[inferred]`)** when a claim is derived from documented architecture rather than directly sourced.
- **Mark speculation (`[unverified]`)** when a claim is model knowledge or plausible inference without a source.
- **Use ASCII hyphens (`-`) and forward slashes (`/`) as separators** instead of em-dashes or en-dashes.

## DON'T

- **Marketing prose.** Words to avoid: "powerful", "elegant", "intuitive", "seamless", "robust", "next-generation", "cutting-edge".
- **Hedging.** "Might possibly happen" -> use `[unverified]` if you mean "I'm not sure".
- **Cite obvious common knowledge.** Don't write `Git is a version control system [S1]`.
- **Em-dashes (`—`, U+2014) or en-dashes (`–`, U+2013).** Anywhere. Author writes them as ASCII from the start; G-11 grep catches any that slip in.
- **Paragraphs longer than 3 sentences.** Break them up.
- **List-bullet padding.** "Also...", "Additionally...", "Furthermore..." add no information.

## Em-dash / en-dash ban (G-11)

Strict, written-discipline rule. No auto-rewrite script: writing em-dashes and then sweeping them is a workflow that masks the underlying habit. Author writes ASCII from the start; verification is by grep.

**Substitution guidance** (use these as you write, not as a post-hoc replacement):

| Character | Codepoint | Substitute with |
|-----------|-----------|-----------------|
| em-dash `—` | U+2014 | ` - ` (space-hyphen-space), OR restructure with a comma, colon, semicolon, or sentence break (usually better) |
| en-dash `–` | U+2013 | `-` (hyphen) |

**Verification at G-11:** `grep -P '[\x{2013}\x{2014}]' <output-file>` must return zero matches. Run this manually before declaring an artifact done. If matches are found, fix the underlying sentence (do not just substitute), then re-run the grep.

**Why this rule exists:** em-dashes signal LLM authorship to most readers. Rephrasing forces clearer sentence structure. The two locked reference outputs (`superpowers_*`, `memsearch_*`) pass this rule with zero violations.

## Citation pattern examples

| Pattern | Example |
|---------|---------|
| Direct quote | `Foo behaves as bar: "<quoted text>" [S1].` |
| Paraphrase | `Foo behaves as bar [S1].` |
| Multiple sources | `Foo behaves as bar [S1, S3].` |
| Inference | `Foo likely behaves as bar [inferred from <source/principle>].` |
| Speculation | `Foo may behave as bar [unverified, <reason>].` |
| Section confidence | `**Section confidence: high.** All claims cited [S1].` |

## Bold lead phrase pattern

Every paragraph that introduces a substantive claim should bold the load-bearing word. The pattern is "topic-claim-evidence":

> **Memsearch is a cross-platform semantic memory plugin and library** built and maintained by Zilliz, the company behind the Milvus vector database. It is published under the MIT license and distributed on PyPI as the `memsearch` package [S1].

The eye lands on the bold phrase first; the rest of the paragraph elaborates. Used consistently, this gives every section a scannable summary embedded in its prose.

## Paragraph length

Maximum 3 sentences per paragraph. If a paragraph hits 4+ sentences, find a logical break and split it. The ADHD variant amplifies this rule (every paragraph must read in <= 10 seconds); the standard variant tolerates it more loosely but still caps at 3 sentences.

## Anti-patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Marketing fluff | "memsearch is a powerful, elegant, cross-platform memory layer" | "memsearch is a cross-platform semantic memory plugin" |
| Hedging | "memsearch can probably be used to..." | "memsearch is used to..." (or `[unverified]` if uncertain) |
| Em-dash signal | "Three axes — skills, workflows, triggers — compose..." | "Three axes (skills, workflows, triggers) compose..." or "Three axes: skills, workflows, triggers." |
| Long paragraph | One block of 7 sentences | Break into 2-3 paragraphs at logical boundaries |
| Generic open | "memsearch is interesting because..." | "memsearch's design choice that gives it shape is..." |
| Unsourced claim | "memsearch is the most popular memory plugin" | Either cite or drop |

## Worked example

**Before** (LLM-default prose):
> Memsearch is a powerful and elegant cross-platform memory plugin that can be used by AI coding agents to remember conversations across sessions — it's truly a game-changer for the agent ecosystem. It supports a wide variety of platforms and offers many features like hybrid search, progressive recall, and live sync.

**After** (voice-and-style applied):
> **Memsearch is a cross-platform semantic memory plugin for AI coding agents.** It treats markdown as the source of truth and Milvus as a rebuildable shadow index [S1]. Four plugins (Claude Code, OpenClaw, OpenCode, Codex CLI) install with one command; a Python API and CLI expose the same engine for developers building custom agents [S1].

The "before" reads as marketing; the "after" reads as an operator's summary.
