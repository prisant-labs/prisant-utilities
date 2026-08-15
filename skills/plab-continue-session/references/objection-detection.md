# Objection Detection

How to detect and surface a stated objection that justifies a lighter-than-verbose continuation prompt.

## Why this matters

plab-wrap-session v1.1.0 defaults the continuation prompt to the verbose / deep form in every mode. The only path to a lighter prompt is for the wrapping agent to state a specific objection (per the comply-or-explain rule in `plab-wrap-session/SKILL.md` § "Default verbosity").

When `/plab-continue-session` reads a log and finds a lighter prompt, it should look for and surface the objection so the resuming user understands why the prompt is sparse.

## Where the objection appears

In a well-formed v1.1.0+ log with a lighter prompt, the objection is recorded in the body just before or after the `## Continuation Prompt` section. Common locations:

- A `## Continuation Prompt - lighter (objection: <reason>)` heading
- A short note above the fenced code block: `> Lighter prompt - <reason>.`
- An entry in `## Outstanding Issues` referencing the prompt verbosity

## Detection rules

A continuation prompt is considered "verbose" when it includes (at minimum):

- Task context paragraph (what was being worked on)
- Current state summary
- Immediate next action (specific, named)
- At least one ordered secondary step
- Relevant file paths
- Branch name

A prompt missing two or more of these is "lighter." Treat anything ambiguous as verbose - false positives on "lighter" are noisier than false negatives.

## How to surface

When a lighter prompt is detected:

```markdown
### Continuation prompt (lighter than verbose)

> The wrapping agent recorded an objection: <objection text from log>.

<fenced code block with the actual prompt>
```

If no objection is recorded but the prompt is detectably lighter:

```markdown
### Continuation prompt (lighter than verbose; no objection recorded)

> Heads up: the wrapping agent emitted a lighter-than-verbose prompt without recording why.
> The cold-start handoff may lack context. Skim the log file directly before proceeding.

<fenced code block with the actual prompt>
```

The user decides whether to proceed despite the gap.

## Do not infer reasons

If no objection is stated, don't invent one ("looks like a quick fix, probably trivial"). Report honestly that no objection was recorded. Inference here is worse than absence.

## Logs from plab-wrap-session v1.0.0

v1.0.0 logs predate the verbose-by-default rule. A v1.0.0 quick-mode log legitimately has a minimal prompt. Treat any log with `date` before 2026-05-28 (the v1.1.0 ship date) as exempt from this detection - present its prompt as-is without lighter/verbose annotation.
