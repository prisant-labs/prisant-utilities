# Section Presets by Document Type

Default review dimensions for each document type. The skill selects the appropriate preset based on auto-detection or `--type`. Users can override with custom sections.

For `doc` type (generic), the LLM reads the document and proposes 5-7 custom dimensions, confirmed with the user before generating.

---

## plan

**Focus:** Executability - can this be built as written?

| # | Dimension | What's at risk |
|---|-----------|---------------|
| 1 | Plan Traceability | Goals, requirements, and work items don't connect end-to-end |
| 2 | Work Item Completeness | Tasks lack clear acceptance criteria or definition |
| 3 | Dependency/Ordering | Task dependencies missed, sequencing unsound |
| 4 | Decision Log Coherence | Decisions internally inconsistent or unsupported |
| 5 | File Inventory Accuracy | Referenced files, paths, or structures don't exist |
| 6 | Success Criteria | Completion conditions unmeasurable or ambiguous |
| 7 | Scope Risks | Likely expansion areas without containment strategy |

---

## brief

**Focus:** Decision quality - is the thinking rigorous?

| # | Dimension | What's at risk |
|---|-----------|---------------|
| 1 | Problem Framing | Problem framed too narrowly, constraining solutions |
| 2 | Evidence Quality | Claims not backed by data, examples, or credible sources |
| 3 | Approach Viability | Recommended approach infeasible given real constraints |
| 4 | Recommendation Strength | Recommendations hedged, vague, or not actionable |
| 5 | Stakeholder Coverage | Affected parties not identified, concerns unaddressed |
| 6 | Risk Assessment | Risks not identified with likelihood, impact, mitigation |
| 7 | Assumptions | Unstated assumptions not surfaced or tested |

---

## spec

**Focus:** Completeness - is this testable and unambiguous?

Also triggered by `prd`.

| # | Dimension | What's at risk |
|---|-----------|---------------|
| 1 | Requirements Completeness | Requirements missing or only implicitly stated |
| 2 | Acceptance Criteria | Requirements not testable with clear pass/fail conditions |
| 3 | Scope Boundaries | What's NOT included is unstated, inviting scope creep |
| 4 | Dependency Identification | External dependencies not identified, no fallback plans |
| 5 | Priority Coherence | Priorities don't reflect actual business value or constraints |
| 6 | User Story Coverage | User personas or scenarios underrepresented |

---

## rfc

**Focus:** Technical soundness - is the proposal correct?

| # | Dimension | What's at risk |
|---|-----------|---------------|
| 1 | Problem Definition | Problem not clearly stated, no evidence of real need |
| 2 | Solution Architecture | Proposed solution technically unsound or incomplete |
| 3 | Trade-offs | Alternatives not honestly considered, rationale unclear |
| 4 | Edge Cases | Boundary conditions, failure modes, unusual inputs missed |
| 5 | Integration Points | Interfaces with other systems poorly defined |
| 6 | Migration Path | No plan for transitioning existing systems |
| 7 | Open Questions | Acknowledged unknowns not tracked with resolution plans |

---

## doc

**Focus:** LLM-selected - analyze document and propose custom dimensions.

No preset. When type is `doc` (or auto-detect isn't confident):

1. Read the document fully
2. Identify 5-7 dimensions most relevant to this specific document
3. Propose dimensions to the user with one-line justification each
4. Confirm before generating the review document
