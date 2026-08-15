# Research & Citation Reference

How to gather, classify, and cite sources during Phase 2 (Research & Cite). Output of this phase is `_work/research.md`. Failure modes if skipped: hallucinated URLs, false credibility claims, ungrounded prose throughout the guide.

## Use when

- Phase 2 of the pipeline
- Re-validating citations during Phase 8 (Bundle & Manifest)
- Triaging a guide that has too many `[unverified]` markers and needs more sourcing

## The research manifest

`_work/research.md` is the structured artifact this phase produces. Every fact that will appear in the guide must trace to a source entry here.

### Structure

```markdown
# Research - <topic>

## Summary
<1-2 paragraphs synthesizing what the sources say.>

## Sources
| # | Title | URL | Retrieved | Kind | Credibility |
|---|-------|-----|-----------|------|-------------|
| S1 | <title> | <url> | <YYYY-MM-DD> | official | A | maintainer | B | community | C | third-party |
| S2 | ... | ... | ... | ... | ... |

## Facts
| Fact | Source(s) | Notes |
|------|-----------|-------|
| <fact> | S1, S3 | ... |

## Gaps
- <topic area not covered by sources>

## Model-Knowledge Claims (Unverified)
- <claim carried from model knowledge, no source>
```

The `Facts` table is the working set the guide-fill phases pull from. Every claim in the guide should trace back to a row here.

## Source types & where to find them

| Input type | Primary sources |
|------------|----------------|
| `repo-url` | README, `docs/` directory, top-level config files (`pyproject.toml`, `package.json`), CHANGELOG, project's docs site (often `<owner>.github.io/<repo>` or a dedicated domain) |
| `tool` | Project's official docs site, `man` pages, `--help` output from the tool itself, package registry (PyPI/npm/Crates) |
| `concept` | Originating paper, RFC/spec, well-known textbook, authoritative blog post by domain expert, academic survey |

### Repo-url specifics

For `repo-url` topics, the minimum-viable research:
1. WebFetch the README at `https://raw.githubusercontent.com/<owner>/<repo>/main/README.md` (or `master` if that's the default).
2. If the README references a docs site, WebFetch the docs landing page.
3. Record the commit SHA at the time of fetch (this goes into `MANIFEST.yaml`).

Three sources is the soft minimum for a `confidence: high` repo-url guide. One source is acceptable for `confidence: medium` if the README is the project's authoritative documentation (which is common for small/young repos).

## Credibility classes

Three classes. The skill assigns one when fetching the source.

- **A** - Official or authoritative source. The project's own docs, README, RFC, spec.
- **B** - Maintainer or well-known expert. Maintainer's blog post, conference talk by a maintainer, project's own release announcements.
- **C** - Community reference. Tutorial, Stack Overflow answer, third-party blog post.

### Assignment rules (apply in order; first match wins)

| Source pattern | Class | Examples |
|----------------|-------|----------|
| Project's own README, docs site, hosted documentation under the project's primary domain | **A** | `github.com/zilliztech/memsearch/README.md`, `react.dev`, `docs.python.org` |
| Project's published RFCs, specs, design docs, release notes | **A** | `peps.python.org`, `CHANGELOG.md` in project repo |
| Standards body output | **A** | IETF RFC, W3C spec, ECMA spec |
| Maintainer's personal blog or talk on the project (maintainer named in `AUTHORS` or README) | **B** | `primeradiant.com/superpowers/`, conference talk by a named maintainer |
| Project's official Discord/Slack message from a maintainer (not from a community member) | **B** | Discord message authored by the project lead |
| Recognized industry expert blog where topic is a stated specialty | **B** | A Postgres internals blog post by a Postgres core contributor |
| Stack Overflow accepted answer with high vote count | **C** | accepted answer with >50 votes |
| General tutorials, blog posts by non-maintainers, conference talks by non-maintainers | **C** | Medium article, dev.to post |
| Community wiki, GitHub issue replies from non-maintainers | **C** | community-edited wiki, issue thread |

When the assignment is ambiguous, default to the lower class and let the operator upgrade it later. The full decision tree (forks, deprecated official docs, archived projects, mirrors) is in the spec under "Credibility assignment rules".

### Confidence thresholds

The frontmatter `confidence` field aggregates source counts and quality:

| confidence | Source profile |
|------------|---------------|
| `high` | >=3 sources, >=1 class A, <=2 unverified body claims |
| `medium` | 1-2 sources, >=1 class A, <=5 unverified body claims |
| `low-confidence draft` | 0 verified sources OR all class C |

Below the threshold, the skill demotes the confidence and inserts the status banner under the H1.

## Citation markers

Three inline markers. Use them consistently.

| Marker | Meaning | Example |
|--------|---------|---------|
| `[S1]`, `[S2]`, ... | Directly cited or quoted from numbered source | `Memory files live at .memsearch/memory/YYYY-MM-DD.md [S1].` |
| `[inferred]` | Derived from documented architecture; not stated explicitly | `Switching providers invalidates the index [inferred from how vector spaces work].` |
| `[unverified]` | Model knowledge or speculation | `Most operators report 1-3 sessions of slowdown [unverified, plausible].` |

### Inline citation forms

| Pattern | Use |
|---------|-----|
| End of sentence | `Foo behaves as bar [S1].` |
| Multi-source | `Foo behaves as bar [S1, S3].` |
| Inferred with reason | `Foo likely behaves as bar [inferred from architectural framing].` |
| Unverified with reason | `Foo may behave as bar [unverified, plausible].` |
| Direct quote | `The README says: "<quoted text>" [S1].` |

## Section confidence

Every major section ends with a one-line confidence summary plus justification:

```markdown
**Section confidence: high.** All claims sourced from README [S1].
```

In the ADHD variant, the line includes a colored emoji: `high 🟢`, `medium 🟠`, `low 🔴`.

## Failure modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Hallucinated URL | A `[S1]` cite points at a URL that doesn't load | Re-fetch the source; if it doesn't exist, drop the claim |
| Citation drift | Body has `[S1]` but Sources section lists only S1, S2 (missing claim's actual source) | Re-audit; ensure every cite has a row in Sources |
| Credibility inflation | A Stack Overflow tutorial labeled class A | Re-classify per the assignment rules |
| Over-marking | Every sentence has `[unverified]` | Either fetch more sources or accept that this is a `low-confidence draft` |
| Under-marking | Critical claims have no marker | Re-audit; default conservative (mark `[unverified]` if you're not sure of the source) |

## Anti-patterns

- **Inventing a source URL because the topic is small or niche.** If the topic is genuinely under-documented, mark every claim `[unverified]` and set confidence to `low-confidence draft`. Do not fabricate.
- **Treating the project's GitHub repo description as a source.** The repo description is too short to be cited. Cite the README instead.
- **Citing the absence of something.** "The README doesn't mention X [S1]" is not a citation; it's an inference. Mark `[inferred]` and explain why the absence matters.
