# History - plab-resolve-open-items

| Version | Date | Release | Type | Summary |
|---|---|---|---|---|
| 1.0.0 | 2026-10-08 | unreleased | added | First version. Walks the open questions, decisions and tasks of the current session, or of one named document, takes a one-line answer, writes each answer back to its one home, and writes a walk record that `walk-check.py` verifies. |

## 1.0.0 - 2026-10-08

**Added: the in-session walk.** A walk gathers open items from the conversation and from the "Open Questions / Decisions" sections of documents the session has touched, or from one document the maintainer names. It presents them as D (a decision between lettered options), Q (a question only the maintainer can answer) and T (a task only the maintainer can perform), and reads a one-line reply such as `D1 A, D2 B, Q1: the NAS`.

Silence is never acceptance. An omitted decision is left as found, an omitted question proceeds on its stated default and is recorded as assumed, and only an explicit `ok` or `accept the rest` applies recommendations. A reply with doubt is recorded as `Provisional`, with the maintainer's words verbatim. A reply that asks for more, or makes no choice, re-presents the item in a further round.

Each answer is written to its item's one home document, on the three surfaces `references/decisions-section.md` defines, with a `Follow-up` line naming the work the decision causes. Every other copy of the item gets a pointer to the home. A document on another branch is never written; the intended edit is printed instead.

`scripts/walk-check.py` checks each write-back and each walk record, and CI runs it against a committed sample.

Specified by WD-01 (resolve open items) in `docs/internal/release-plans/_unassigned/WD-01_resolve-open-items/spec.md`. The design came out of two hand-run walks, whose reply shapes are the worked examples in `references/answer-line.md`.
