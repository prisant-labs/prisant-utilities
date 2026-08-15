---
name: plab-strategy-brief
description: "Transform messy thinking into structured, decision-ready analysis documents.
  Use when a user provides raw, unstructured thoughts and wants them organized, expanded,
  and turned into an actionable artifact. Triggers on: 'help me think through', 'brain
  dump', 'summarize and expand', 'make sense of this', requests combining pros/cons with
  approaches and recommendations, or any stream-of-consciousness input needing structure.
  Also triggers on 'strategy primer', 'structured analysis', or '80/20 analysis'. Do NOT
  use for simple summarization of existing structured documents, editing polished prose,
  or pure research queries with no raw thinking provided."
version: "1.1.1"
updated: 2026-07-04
argument-hint: "[paste raw thinking]"
license: MIT
---

# Strategy Brief

Transform raw, unstructured thinking into a structured, decision-ready analysis document. This is not summarization - it is thinking amplification. The user arrives with a confused signal and leaves with a structured artifact they can reference, share, and act on.

## When to Use

The user will typically:
- Paste stream-of-consciousness text (often with typos, incomplete sentences)
- Ask a variation of "summarize, expand, polish, analyze, give me approaches, what's the 80/20"
- Combine multiple analytical requests in a single prompt
- Be tired, busy, or mid-thought and want Claude to do the structural heavy lifting

Do NOT use when the user provides clean, structured input (that's editing), asks a simple factual question, or wants only a summary with no expansion.

## Output Format

Always produce a **standalone markdown document** (canvas/artifact). Never inline chat unless explicitly requested. The document should be referenceable and shareable.

## Output Location (v1.0.1+)

Write the brief to `_output/plab-strategy-brief/<slug>-<YYYY-MM-DD>.md` by default, where:

- `<cwd>` is the current working directory at invocation time
- `<slug>` is a kebab-case derivation of the brief's topic (3-6 words)
- `<YYYY-MM-DD>` is today's date

If the user says "output to ...", "write to ...", `--out <path>`, or names an explicit destination, honor that path instead. Common explicit overrides:
- A specific file path: `--out /path/to/brief.md`
- A directory: writes to `<dir>/<slug>-<YYYY-MM-DD>.md`
- "as a chat artifact only" / "do not save": skip disk write

The default `_output/plab-strategy-brief/` convention matches `plab-guide` so output artifacts from this plugin's skills accumulate in one predictable root. The folder is intended to be gitignored at the project level.

## The Seven Sections

Every output follows this structure. Scale sections up or down based on complexity, but all seven must be present. Read `references/section-guide.md` for detailed per-section guidance.

### 1. What I Understand (Input Mirror)
Reflect the input back in organized form. Surface assumptions, identify sub-threads, flag gaps. The user needs to see "yes, that is what I mean" before analysis has value. Keep concise: 100-300 words.

### 2. Problem Space
Go deeper and wider than the raw input. Why does this matter now? What does "solved" look like? Who is affected? What adjacent problems exist? Frame desired outcomes clearly. 200-500 words.

### 3. Analysis
Evaluate through multiple lenses. Always apply the 5 core lenses (strengths, weaknesses, risks, open questions, concerns). Scan situational lenses and pick 2-4 that add genuine insight. See `references/analysis-lenses.md` for the full catalog. 300-800 words.

### 4. Approaches
Generate 2-4 genuinely distinct approaches (not intensity variants of the same strategy). For each: summary, detailed breakdown, pros, cons, key risks, effort/complexity, and honest commentary. Do not pad - if only 2 viable paths exist, present 2. 400-1,200 words total.

### 5. The 80/20 Recommendation
The most important section. Cut through the analysis: which approach gets 80% of value for 20% of effort? Include concrete next steps (1-3 specific actions), what to explicitly defer, and confidence level with reasoning. Be direct and opinionated. 150-400 words.

### 6. Evidence & Source Map
Trace claims to sources. Include external sources, prior conversations, data points, and evidence gaps. If analysis is based primarily on reasoning, say so honestly. A thin evidence map is better than a fabricated one.

### 7. Uncertainties & Open Items
What you're unsure about (with confidence labels). What requires human judgment. What would benefit from additional research. Offer follow-up generation (spec, decision doc, action plan).

## Depth Scaling

| Complexity | Signals | Target Length |
|---|---|---|
| Simple (1 clear question, narrow scope) | Single thread, clear ask | 800-1,500 words |
| Medium (2-3 threads, some ambiguity) | Multiple sub-questions, moderate context | 1,500-2,500 words |
| Complex (4+ threads, broad scope) | Extensive raw input, many unknowns | 2,500-4,000 words |

## Behavioral Guidelines

1. **Do not interrogate.** If input has 2+ substantive threads, begin. If genuinely too vague, ask ONE clarifying question.
2. **Mirror first, then expand.** The mirror step catches misunderstandings before deep analysis.
3. **Be opinionated in Section 5.** "It depends" is not a recommendation. If it depends on a variable, name it and recommend for each value.
4. **Use web search** when the topic involves current tools, market conditions, or verifiable facts.
5. **Offer follow-up generation** at the end - spec, decision doc, action plan, whatever is the logical next step.
6. **Do not pad.** Every sentence earns its place. If a section adds nothing, keep it to 1-2 sentences.

## Common Pitfalls

- **Generic SWOT language.** "High risk but high reward" says nothing. Be specific.
- **Symmetric pros/cons.** If every approach has equal pros and cons, you're forcing balance, not analyzing.
- **Ignoring implicit constraints.** If the user is a solo operator, don't suggest team-of-5 approaches.
- **Burying the 80/20.** Some users skip to Section 5. It must stand alone.

## Integration

- Pairs well with `wrap-session` for logging the output
- Outputs are portable to Obsidian vaults, git repos, or shared documents
- If the user's input references a prior conversation, use chat search to pull in context
