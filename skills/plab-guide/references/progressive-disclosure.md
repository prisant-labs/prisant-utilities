# Progressive Disclosure Reference

The In-Depth Breakdown section uses four explicit layers, each addressing a different reader question. This is the heart of the explanatory MD guide.

## Use when

- Drafting Section 8 (In-Depth Breakdown) of either MD variant
- Auditing whether content is in the right layer
- Triaging "the breakdown feels disorganized" complaints

## The four layers

Each layer gets its own H3 inside the `## In-Depth Breakdown` H2.

| Layer | Reader question | Length | Reads like |
|-------|----------------|--------|-----------|
| Surface | "What is this thing?" | 200-400 words | An orientation paragraph |
| Structural | "How is this organized?" | 600-1000 words | A guided tour of named parts |
| Mechanical | "How does it actually work?" | 1000-2000 words | A phase-by-phase walkthrough |
| Expert | "What's non-obvious?" | 400-800 words | A list of "things you only learn after using it" |

Length targets are guidelines, not hard caps. Shallow topics produce shorter sections; deep topics produce longer ones. The longest sub-section is always Mechanical; the shortest is usually Surface.

## Layer headings: canonical vs topic-specific

The four layers can render their H3 headings in either of two styles. Both are spec-compliant; pick whichever reads more naturally for the topic.

**Canonical (default for software topics):**
```markdown
### Surface Layer - What It Is
### Structural Layer - How It's Organized
### Mechanical Layer - How It Works
### Expert Layer - What's Non-Obvious
```

**Topic-specific (recommended for non-software topics):**
```markdown
### What OKRs Are                         (Surface logic)
### The Anatomy of an OKR                 (Structural logic)
### Running an OKR Cycle in Practice      (Mechanical logic)
### Common Misuses and Subtleties         (Expert logic)
```

The *layer logic* is mandatory; the *layer labels* are flexible. Gate G-1 enforces the four-layer structure (four H3s in order under the In-Depth Breakdown H2), not specific names.

### When to use which

| Topic shape | Recommended label style | Example |
|-------------|------------------------|---------|
| Software repo / library / plugin | Canonical | superpowers, memsearch, glow |
| Software tool with rich docs | Canonical | jq |
| Software concept | Canonical | eventual consistency, idempotency |
| Methodology / framework (non-software) | Topic-specific | OKRs, design thinking |
| Practice / discipline (non-software) | Topic-specific | bullet journaling, journaling, productivity systems |
| Domain knowledge | Topic-specific | Christian heresies, Bible literature, AI principles |

### Picking topic-specific labels

The headings should:
- Use the topic's own vocabulary (the "Anatomy of an OKR", not "Structural Layer")
- Read as a natural progression (orient -> parts -> mechanics -> subtleties)
- Be parsable as the layer they represent (a reader skimming should be able to identify which layer is which without explicit labels)

Patterns that work for the four layers:
- Surface: "What X Is", "X Defined", "Introducing X"
- Structural: "The Anatomy of X", "Components of X", "How X Is Organized", "The Building Blocks of X"
- Mechanical: "How X Works in Practice", "Running X End-to-End", "X in Action", "The X Cycle"
- Expert: "Common Misuses of X", "Subtleties of X", "What's Non-Obvious About X", "Hard-Won Lessons in X"

## Layer 1: Surface - "What it is"

**Reader:** Total newcomer.
**Goal:** Orient them in 200-400 words. Name the category, the authors, the audience, the value proposition.

**Include:**
- Category framing ("It is a memory plugin in the same family as OpenClaw")
- Authors, license, source URL
- Audience (who benefits, who doesn't)
- Optional pull quote from the source materials

**Exclude:**
- How it works (that's Mechanical)
- Component listings (that's Structural)
- Anything subtle (that's Expert)

**Anti-pattern:** Skipping the category framing. The reader needs to know what *kind* of thing this is before anything else. Compare:
- Bad: "Memsearch stores memories in markdown files and indexes them in Milvus."
- Good: "**Memsearch is a cross-platform semantic memory plugin and library** in the agent-memory category."

## Layer 2: Structural - "How it's organized"

**Reader:** Decided to investigate further; wants the parts list.
**Goal:** Show the named parts and how they relate, in 600-1000 words.

**Include:**
- The structural axes (typically 2-4) along which the topic organizes work
- A table or list per axis showing components
- A diagram or code block where applicable (pipeline, data flow)
- Prose framing each axis - tables alone do not explain composition

**Exclude:**
- Runtime mechanics (that's Mechanical)
- Subtle gotchas (that's Expert)

**Pattern: "axes that compose"**

Open with a multi-sentence framing paragraph that names the axes and explains how they fit together. Stress that the axes are not independent. Then give each axis its own H4 sub-heading.

```markdown
### Structural Layer - How It's Organized

<Topic> organizes its work along three axes that compose together.
**Skills** are the units of behavior. **A workflow** is the canonical
order. **A trigger system** decides which skill applies. Each axis is
necessary; none is sufficient on its own. Read the three subsections
below as one composed mechanism.

#### Axis 1 / The fourteen skills, grouped by function

<2-3 paragraphs of prose framing the catalog before the table>

| Group | Skill | Role |
|-------|-------|------|
| ...   | ...   | ...  |

<closing prose tying the catalog together>

#### Axis 2 / The sequential workflow
...

#### Axis 3 / The trigger system
...
```

**Anti-patterns:**
- One wall of prose with no tables
- One wall of tables with no prose framing
- A single H4 with no other H4s nearby (drop the H4; run as one section)

## Layer 3: Mechanical - "How it works"

**Reader:** Operator who needs to actually use the topic.
**Goal:** Phase-by-phase end-to-end mechanics, in 1000-2000 words.

**Include:**
- Numbered phases (use `#### Phase N - <name>` headings)
- Each phase covers: trigger, internal steps, artifact produced, failure mode addressed
- Optional pull quote synthesizing the mechanics
- Code blocks where they aid understanding (pipelines, data formats, command sequences)

**Exclude:**
- Surface-level "what is" content
- Architectural framing (that's Structural)
- Subtle gotchas (that's Expert)

**Per-phase shape**

Each phase is 2-4 paragraphs (100-200 words). One-sentence phases are an anti-pattern; fold them into adjacent phases. Cover:

1. **What triggers this phase** (the conditions that cause it to fire)
2. **The internal steps it runs** (its sub-mechanics)
3. **The artifact / state change it produces**
4. **Why the phase exists** (which failure mode it addresses)

```markdown
#### Phase 6 - TDD inside each task

Implementation tasks must run through `test-driven-development`. The
cycle is rigid and is run for each unit of behavior the task introduces:

1. Write a failing test
2. Run it; confirm the failure mode is the one expected
3. Write the minimum code to pass
4. Run the test again; confirm green
5. Refactor with the test as a safety net
6. Commit

Step 2 is often skipped in casual TDD; superpowers calls it out
explicitly. A test that fails for the wrong reason (a typo, a missing
import, a wrong path) is not the test the agent is about to satisfy
[S1]. The skill's enforcement mechanism is unusual: code written before
its test gets deleted [S1].
```

This phase example covers what triggers it (implementation tasks), the steps it runs (the 6-step cycle), the artifact (a tested feature), and the failure mode (retrofitted tests testing what code does, not what the spec required).

## Layer 4: Expert - "What's non-obvious"

**Reader:** Has used the topic; wants the wisdom that took experience to learn.
**Goal:** 5-10 non-obvious points in 400-800 words.

**Include:**
- Subtle interactions, edge cases, foot-guns
- Performance characteristics
- Architectural consequences only visible after running the topic
- Each point gets a short H4 sub-heading and 1-2 paragraphs

**Exclude:**
- Restatement of Mechanical content
- Anything Surface- or Structural-level

**Almost exclusively class-A or class-B sources.** If a claim here can only be supported by class-C material, mark `[unverified]` and lean toward dropping it.

**Pattern**

```markdown
#### The skill check fires before clarifying questions

This sounds minor but is structurally important. A naive implementation
would be: agent receives message, asks clarifying question, user answers,
agent checks for skills. **Superpowers reverses this**: agent receives
message, checks skills, the skill might tell it how to ask the
clarifying question [S1].
```

The bold lead phrase carries the insight. The surrounding prose explains why it matters and how it manifests.

## Layer mixing - the cardinal sin

**Do not mix layers.** If a piece of information belongs to the Mechanical layer, it does not appear in Structural just because it's convenient.

Test: read your section out loud. If you find yourself saying "and this works because..." in the Structural layer, you've drifted into Mechanical. Cut the explanation; move it to the right layer.

## Topic-type adapters

Each layer adapts slightly per input type:

| Layer | repo-url | tool | concept |
|-------|----------|------|---------|
| Surface | What + audience + license | What + category | What + origin + adjacent concepts |
| Structural | Directory layout + components | Subsystems + flags | Sub-concepts + relationships |
| Mechanical | How the runtime works | Invocation lifecycle | How the concept applies in practice |
| Expert | Edge cases + maintainer wisdom | Performance gotchas + idiomatic usage | Subtle distinctions + common misapplications |

## Length budget worked example (memsearch reference)

Looking at `examples/memsearch/memsearch_guide-standard.md`:
- Surface Layer: 4 paragraphs, ~330 words (within 200-400 target)
- Structural Layer: 3 axes, ~840 words (within 600-1000 target)
- Mechanical Layer: 5 phases, ~1080 words (within 1000-2000 target)
- Expert Layer: 9 sub-points, ~720 words (within 400-800 target)

Total breakdown: ~2,970 words across the four layers. Total guide: ~5,750 words. The breakdown is roughly half the document.

## Anti-patterns

| Anti-pattern | Symptom | Fix |
|-------------|---------|-----|
| Single-sentence Mechanical phase | Phase 3 is just "Worktree isolation runs." | Expand to 2-4 paragraphs covering trigger/steps/artifact/why |
| Layer mixing | Structural section explains how the workflow runs end-to-end | Cut the runtime detail; move to Mechanical |
| Tables without prose | Section is a table list with no framing sentences | Add a 2-3 sentence intro and closing per axis |
| Expert layer with no class-A sources | Expert claims are mostly `[unverified]` | Either source or drop |
| Surface layer drift into mechanics | Surface explains how the feature works step-by-step | Surface is *what*, not *how* |
