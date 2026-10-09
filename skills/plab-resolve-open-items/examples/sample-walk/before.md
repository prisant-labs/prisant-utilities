# Spec: sync between the laptop and the archive

A committed sample for `scripts/walk-check.py writeback`. `before.md` is this document before a walk wrote to it, and `after.md` is the same document after. In that walk, D1 was answered "A", D2 was skipped, and Q1 was skipped, so it proceeded on its default.

## Purpose

Keep a working copy on the laptop and an archive copy on the network drive in step, without a person deciding each conflict by hand.

## Open Questions / Decisions

Three items are open. D1 and D2 are decisions; Q1 needs a fact only the maintainer has.

| ID | Title | Resolution | Status | Updated |
|----|-------|------------|--------|---------|
| D1 | Sync authority | (none) | Open | (none) |
| D2 | Conflict log location | (none) | Open | (none) |
| Q1 | Archive drive name | (none) | Needs info | (none) |

### D1: Sync authority (Open)

**Summary.** When both copies changed, which one wins?

**Context.** Conflicts are rare, about one a month, but each one currently stops the sync until someone looks.

**Desired outcome.** A conflict never stops the sync, and nothing is lost.

**Options / approaches.**

* **Option A:** The laptop wins, and the archive's version is kept beside it with a suffix.
* **Option B:** The archive wins, and the laptop's version is kept beside it with a suffix.

**Recommendation.** Option A. The laptop is where edits happen, so its copy is the likelier intent.

**Confidence:** High.

---

> **Maintainer decision:** _(pending)_
>
> * **Status:** Open
> * **Choice:** (none)
> * **Reasoning:** (none)
> * **Decided by / date:** (none)

### D2: Conflict log location (Open)

**Summary.** Where is each resolved conflict recorded?

**Context.** A resolved conflict should be findable later, in case the losing copy mattered.

**Desired outcome.** One place to look, that survives a laptop rebuild.

**Options / approaches.**

* **Option A:** A log file on the archive drive.
* **Option B:** A log file on the laptop.

**Recommendation.** Option A. It survives a laptop rebuild.

**Confidence:** Medium.

---

> **Maintainer decision:** _(pending)_
>
> * **Status:** Open
> * **Choice:** (none)
> * **Reasoning:** (none)
> * **Decided by / date:** (none)

### Q1: Archive drive name (Needs info)

**Summary.** What is the archive drive called on the network?

**Context.** The sync needs the share name to mount it.

**Default if skipped.** `archive`, the name in the setup notes.

---

> **Maintainer decision:** _(pending)_
>
> * **Status:** Needs info
> * **Choice:** (none)
> * **Reasoning:** (none)
> * **Decided by / date:** (none)

## Sources

- The setup notes for the network drive.
