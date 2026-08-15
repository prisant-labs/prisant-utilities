# Analysis Lenses Reference

A catalog of analytical frameworks for use in Section 3 (Structural Analysis) and Section 4 (Approaches). Not every lens applies to every topic. Select lenses that add genuine insight; do not apply frameworks mechanically.

---

## Core Lenses (Always Available)

These are the default lenses used in every Strategy Primer document.

### Strengths / Benefits
What is genuinely good about the direction, idea, or current state? Focus on concrete, specific benefits rather than abstract positives.

### Weaknesses / Limitations
Honest downsides and structural constraints. Distinguish between fixable weaknesses and inherent limitations.

### Cautions, Risks, and Failure Modes
What could go wrong? Consider:
- **Probability vs. severity:** A likely-but-minor risk differs from an unlikely-but-catastrophic one
- **Internal vs. external risks:** Things within the user's control vs. things that depend on others
- **Known unknowns vs. unknown unknowns:** Risks you can name vs. categories of surprise

### Open Questions
Specific, answerable questions that need resolution before a decision. Good open questions are:
- Scoped (not "what should we do about everything?")
- Answerable (someone could actually go find the answer)
- Consequential (the answer would change the recommendation)

### Concerns
Gut-level unease that has not been fully articulated. This lens gives permission to express intuition. Useful phrasings: "Something about X feels fragile..." or "The assumption that Y seems under-examined..."

---

## Situational Lenses (Use When Relevant)

### JTBD (Jobs to Be Done)
Best for: Product decisions, tool selection, workflow design.
- What "job" is the user hiring this solution to do?
- What are the functional, emotional, and social dimensions of the job?
- What does the user currently "hire" to do this job? What are its shortcomings?

### Stakeholder Mapping
Best for: Organizational decisions, communication strategy, change management.
- Who is affected by this decision?
- Who has decision authority vs. influence vs. information needs?
- Whose buy-in is required vs. nice-to-have?

### Opportunity Cost
Best for: Prioritization decisions, resource allocation.
- What are you NOT doing if you pursue this?
- What is the value of the best alternative use of the same time/effort/money?

### Reversibility Assessment
Best for: High-stakes decisions, architecture choices, organizational changes.
- Type 1 (irreversible, one-way door): Requires careful analysis
- Type 2 (reversible, two-way door): Bias toward action and learning
- How expensive is it to undo this decision in 3 months? 12 months?

### Scalability Check
Best for: Technical architecture, process design, organizational design.
- Does this approach work at 2x current scale? 10x? 100x?
- Where are the bottlenecks or breaking points?
- Is the approach designed for current needs or future growth?

### Dependencies and Prerequisites
Best for: Implementation planning, project sequencing.
- What must be true or in place before this can work?
- Which dependencies are within your control vs. external?
- What is the critical path?

### Constraint Analysis
Best for: Problems that feel unsolvable or stuck.
- What constraints are real vs. assumed?
- Which constraints are negotiable?
- What would change if you relaxed the tightest constraint?

### Second-Order Effects
Best for: Policy decisions, system changes, cultural shifts.
- If this works as intended, what happens next?
- What behaviors does this incentivize (intended and unintended)?
- What feedback loops does this create?

### Build vs. Buy vs. Adopt
Best for: Tool selection, technical decisions, process design.
- Build: Maximum control, highest effort, ongoing maintenance burden
- Buy: Faster start, ongoing cost, vendor dependency
- Adopt (open source / community): Low cost, variable quality, community dependency
- Hybrid: Which components should be built, bought, or adopted?

### Effort-to-Value Ratio
Best for: Prioritization, approach comparison, 80/20 analysis.
- Map each option on a 2x2 of effort (low/high) and value (low/high)
- High-value, low-effort items are the 80/20 sweet spot
- High-effort, low-value items should be eliminated
- High-value, high-effort items may be worth phasing

### Time Horizon Analysis
Best for: Strategic decisions, investments, long-term planning.
- What does this look like in 1 week? 1 month? 6 months? 1 year?
- Does the value increase or decrease over time?
- Is there a window of opportunity that closes?

---

## Domain-Specific Lenses

### Product Management
- **MoSCoW:** Must have / Should have / Could have / Won't have
- **RICE:** Reach, Impact, Confidence, Effort
- **Customer Segment Impact:** How does this affect SME / MM / ENT differently?
- **Platform vs. Domain:** Is this a platform capability or a domain-specific feature?

### Technical Architecture
- **Complexity Budget:** How much complexity does this add to the system?
- **Coupling Assessment:** How tightly does this connect previously independent components?
- **Migration Path:** How do you get from current state to proposed state without breaking things?

### Personal Productivity / Knowledge Management
- **Friction Analysis:** Where are the high-friction points in the current workflow?
- **Automation Readiness:** What parts are ripe for automation vs. require human judgment?
- **Sustainability Test:** Will this process still be followed in 3 months when motivation fades?

---

## Selecting Lenses

1. Always apply the 5 core lenses
2. Scan the situational lenses and pick 2-4 that add genuine insight
3. If a domain-specific lens set applies, include 1-2 from it
4. If a lens would produce only generic observations, skip it
5. If the user's input specifically mentions a framework (e.g., "what are the JTBD here?"), always include that lens
