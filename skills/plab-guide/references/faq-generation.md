# FAQ Generation Reference

How to derive useful FAQ categories and questions for a topic. Quality gate G-3 enforces volume and categorization.

## Use when

- Drafting Section 9 (Frequently Asked Questions) of either MD variant
- Auditing whether a draft FAQ is too generic
- Deciding whether to add another category or another Q/A pair

## Required properties

| Property | Rule |
|----------|------|
| Categorized | >=3 categories. Each gets its own H3 (or `### N.M.` in ADHD variant). |
| Volume | >=8 Q/A pairs total. No category has fewer than 2. |
| Friction-driven | At least 50% of questions correspond to real friction (issues from troubleshooting docs, common SO questions, GitHub issue labels). |
| Non-generic | Banned shapes (see below). |
| Traceable | Each Q has at least one implicit or explicit source in `_work/research.md`. Un-sourced Qs are dropped, not fabricated. |

## Category derivation

Categories are **topic-derived**, not templated. Look at:

1. **What the troubleshooting docs cover.** If the project has a `troubleshooting/` directory or section, those are the friction points.
2. **What the GitHub issue labels are.** Repos with `bug`, `installation`, `performance`, `compatibility` labels reveal what users actually ask about.
3. **What the README's "Common questions" or "FAQ" section already covers.** If the project has one, mine it; don't ignore it.
4. **What the topic's audience splits into.** If a topic serves "users + developers" (like memsearch), categories often split that way.

### Typical categories by topic type

| Topic type | Likely categories |
|------------|-------------------|
| repo-url (plugin / library) | Adoption & Setup, Storage & Backend, Recall / Workflow, Customization & Extension, Troubleshooting |
| tool (CLI / build tool) | Configuration, Performance, CI integration, Troubleshooting, Migrations |
| concept (methodology / pattern) | Mental model, Edge cases, Related concepts, Practical application, Common misconceptions |

These are starting points only. Always pick categories that match the topic, not the template.

## Banned question shapes

| Shape | Why banned |
|-------|-----------|
| `What is X?` | Already answered by the Surface Layer (and the title). |
| `Why should I use X?` | Already answered by the Executive Summary. |
| `How do I install X?` | Already answered by the Getting Started section. |
| `Is X better than Y?` | Subjective; belongs in Similar Tools, not FAQ. |
| Any Q with a 1-sentence A | The Q isn't load-bearing enough to deserve a slot. |

If a draft FAQ contains a banned shape, drop the Q and reuse the slot for something friction-driven.

## Q/A length

- **Q:** one sentence, phrased as a real question. Avoid leading questions.
- **A:** 2-5 sentences. Cite source(s). End with a forward pointer if there's deeper material.

The 1-sentence-A rule is hard. If your A is 1 sentence, the Q is too shallow; rewrite or drop.

## Friction-driven question recipe

A friction-driven Q has these properties:

1. **Specific.** "How does X handle Y when Z?" not "How does X work?"
2. **Actionable answer.** The A points the reader at a specific path forward.
3. **Sourceable.** A class-A or class-B source covers the friction (or you can mark `[unverified]` honestly).
4. **Phrased like a real user.** Not "What is the optimal configuration for memory consumption?" but "My memory usage is high. What do I do?"

Looking at troubleshooting docs is the highest-yield path. If the project has a troubleshooting page, every section there is a candidate Q.

## Worked examples

### memsearch (repo-url, library + plugin)

5 categories (matches the audience split + troubleshooting):
1. **Adoption & Setup**: questions a first-time user asks
2. **Storage & Backend**: Milvus Lite vs Cloud, where data lives
3. **Recall Behavior**: what triggers recall, how the 3 layers work
4. **Customization & Extension**: building custom integrations
5. **Troubleshooting**: what to do when it breaks

11 Q/A pairs total, distributed 3/3/3/3/3 except Storage which got 4 (real-world Storage questions are common in the issue tracker).

### superpowers (repo-url, methodology plugin)

5 categories (matches the workflow phases + troubleshooting):
1. **Adoption & Setup**: multi-host install, integration with existing IDE
2. **Workflow Discipline**: when does brainstorming end, what counts as a typo
3. **Multi-Agent & Worktrees**: concurrency safety
4. **Customization & Extension**: disabling skills, adding new ones
5. **Troubleshooting**: fixing false-completion claims, agreement reflex

10 Q/A pairs distributed 3/3/2/3/3.

## Anti-patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| Templated categories ("Setup, Usage, Conclusion") | Categories don't match topic | Re-derive from troubleshooting docs / issues |
| All-positive Qs ("How great is X at Y?") | FAQ reads as marketing | Rewrite around friction |
| Lopsided distribution (1 category has 6 Qs, others have 1) | Imbalanced coverage | Either rebalance or merge categories |
| Generic Qs ("What's a good practice for using X?") | A is necessarily generic | Replace with specific friction-driven Q |
| Repeating Surface Layer content | "What is X?" / "X is..." | Drop the Q; the title and Surface already answer it |
| Single-sentence answer | "Q: How big is the index? A: It depends." | Either expand A with specifics or drop Q |
| Fabricated friction | Q invented because the slot needed filling | Drop the slot; better to have 8 real Qs than 12 with 4 invented |

## Output shape (markdown)

```markdown
## Frequently Asked Questions

### Adoption & Setup

**Q: <Specific friction-driven question>**

A: <2-5 sentences. Cite source.> [S1]

**Q: <Another question>**

A: <Answer.> [S1]

### <Next category>
...
```

In the ADHD variant: numbered subsections (`### 9.1. Adoption & Setup`) plus a clickable [QUICK NAV] block at the top of section 9.
