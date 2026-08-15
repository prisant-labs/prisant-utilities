# Section Guide: Detailed Authoring Instructions

This reference provides detailed guidance for writing each section of a Strategy Primer document. Read this when you need more specificity than the SKILL.md overview provides.

---

## Section 1: Input Mirror

**Goal:** Confirm understanding before investing in analysis.

**Structure options (pick the best fit):**
- Bullet list of restated threads (best for multi-topic inputs)
- 2-3 short paragraphs of narrative restatement (best for single-topic with nuance)
- A "What I hear you saying" framing followed by organized points

**What to include:**
- The core question or problem, restated clearly
- Sub-problems or threads identified in the raw input
- Implicit assumptions the user is making (surface these explicitly)
- Gaps, contradictions, or ambiguities in the input
- Emotional tone acknowledgment if present (e.g., frustration, excitement, fatigue)

**What to avoid:**
- Parroting the input back verbatim
- Adding analysis at this stage (save it for later sections)
- Making the mirror longer than the original input
- Correcting typos or grammar in a way that changes meaning

**Length:** 100-300 words. This section should be scannable in under 30 seconds.

---

## Section 2: Problem Space Expansion

**Goal:** Widen the aperture so the user sees dimensions they may have missed.

**Core questions to address:**
- Why does this matter now? What is the forcing function or urgency?
- What does "solved" look like? (Desired outcomes, measurable where possible)
- What is the desired impact? (On the user, their team, their users, their business)
- Who are the stakeholders affected? (Even if the user did not mention them)
- What adjacent or upstream problems exist? (Problems that, if solved, would make this problem easier or irrelevant)
- What is the JTBD framing? (What "job" is the user hiring this solution to do?)

**Expansion techniques:**
- "Zoom out": Place the specific problem in its broader context
- "Zoom in": Identify the specific, concrete manifestation of a vague concern
- "Time shift": What happens if this is not addressed in 3 months? 12 months?
- "Stakeholder shift": How does this look from a different role's perspective?
- "Inversion": What would actively making this worse look like? (Reveals hidden assumptions)

**Length:** 200-500 words. Scale with complexity.

---

## Section 3: Structural Analysis

**Goal:** Evaluate the idea, direction, or problem through multiple analytical lenses.

**Required lenses (always include):**
- **Strengths / benefits:** What is genuinely good about the direction or idea? Be specific.
- **Weaknesses / limitations:** What are the honest downsides? Include structural limitations, not just risks.
- **Cautions, risks, and failure modes:** What could go wrong? What are the failure scenarios? Distinguish between likely risks and catastrophic-but-unlikely risks.
- **Open questions:** Things that need answers before a decision can be made. Frame as specific, answerable questions.
- **Concerns:** Things that feel wrong but are not fully articulated. This is the "gut check" section. It is okay to express intuition here.

**Optional lenses (include when relevant):**
- **Dependencies and prerequisites:** What must be true or in place before this can work?
- **Opportunity cost:** What are you NOT doing if you pursue this?
- **Reversibility:** How easy is it to undo this decision if it turns out to be wrong?
- **Scalability:** Does this approach work at 10x the current scale?

See `analysis-lenses.md` for additional specialized frameworks.

**Formatting:** Use prose paragraphs or short bullet clusters. Avoid giant bullet lists with single-sentence items; the analysis should have enough depth that each point is 2-4 sentences minimum.

**Length:** 300-800 words.

---

## Section 4: Approaches

**Goal:** Present genuinely distinct paths forward with honest tradeoff analysis.

**How to generate good approaches:**
- Each approach should represent a fundamentally different strategy, not just a different intensity level of the same strategy
- Consider approaches along different dimensions: build vs. buy, incremental vs. big-bang, solo vs. collaborative, technical vs. process-based
- If the user's raw input already contains approach ideas, include those and add alternatives they have not considered
- Include at least one "surprisingly simple" approach if one exists

**For each approach, include:**

1. **Name and high-level summary** (1-2 sentences, scannable)
2. **Detailed breakdown:** What does this actually look like in practice? Walk through the steps or components.
3. **Pros:** Specific to THIS approach (not generic benefits)
4. **Cons:** Specific to THIS approach (not generic risks)
5. **Key risks:** The 1-3 things most likely to derail this approach
6. **Effort / delivery complexity:** Use relative terms (low/medium/high) or time estimates if the domain allows. Note dependencies.
7. **Commentary:** Your honest, opinionated assessment. "This is the approach I would lean toward because..." or "This looks appealing but has a hidden complexity in..." This is not neutral analysis; this is a trusted colleague's take.

**How many approaches:**
- Minimum: 2 (there is always at least one alternative)
- Maximum: 4 (more than 4 creates decision paralysis)
- Typical: 2-3
- If only 1 viable approach exists, present it alongside 1 rejected alternative and explain why the alternative fails

**Length:** 400-1,200 words total across all approaches.

---

## Section 5: The 80/20 Recommendation

**Goal:** Cut through analysis paralysis with a clear, actionable recommendation.

**This section must contain:**

1. **The recommendation:** One clear statement of what to do. If it is a hybrid of approaches from Section 4, explain the hybrid. If it is a single approach, name it.
2. **Why this is the 80/20:** Explain what 80% of the value is and why this path captures it with minimal effort.
3. **Concrete next steps:** 1-3 specific, actionable steps. Not "think more about X" but "create a draft of X" or "send Y to Z for feedback."
4. **What to defer:** Explicitly name what the user should NOT do right now, even if it seems important. This is as valuable as the recommendation itself.
5. **Confidence and caveats:** State your confidence level and the key assumption that, if wrong, would change the recommendation.

**Voice:** Direct, warm, opinionated. Think "trusted colleague at a whiteboard" not "management consultant delivering a deck." Use "I" and "you" naturally.

**Common failure modes:**
- "It depends" without naming what it depends on
- Recommending "more research" as the 80/20 (research is sometimes correct, but it should be specific research with a defined question, not open-ended exploration)
- Hedging so much that the recommendation has no clear direction
- Ignoring the user's constraints (time, energy, resources, context)

**Length:** 150-400 words. This section should be the most information-dense section in the document.

---

## Section 6: Evidence & Source Map

**Goal:** Enable traceability and follow-up.

**Categories to include:**

- **External sources:** Articles, documentation, tools, standards referenced. Include URLs where available.
- **Prior conversations:** If chat search was used to pull in context, link to the relevant conversations.
- **Data points:** Specific statistics, benchmarks, or facts cited in the analysis.
- **Frameworks referenced:** If you used JTBD, MoSCoW, or other frameworks, cite the canonical source.
- **Evidence gaps:** Explicitly note what you could not find or verify. This is more valuable than padding with weak sources.

**Formatting:** A simple list or table. This section is a reference appendix, not prose.

**If no external sources were used:** Say so. "This analysis is based on reasoning from the provided context and general domain knowledge. No external sources were consulted. The following areas would benefit from external validation: [list]."

**Length:** Variable. As long as it needs to be, as short as it can be.

---

## Section 7: Uncertainties & Open Items

**Goal:** Close with intellectual honesty and set up the next conversation.

**Include:**
- What you (Claude) are uncertain about, with confidence labels
- What requires the user's domain-specific judgment
- What would benefit from additional research (with suggested search queries or research prompts)
- Potential follow-up outputs: "Would you like me to generate a deep research prompt for X?" or "I can draft a spec / decision document / action plan based on this analysis."

**Voice:** Honest, not self-deprecating. "I don't have enough context to evaluate X" is better than "I'm sorry I couldn't do better on X."

**Length:** 100-300 words.
