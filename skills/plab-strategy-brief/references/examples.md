# Examples: Annotated Strategy Primer Outputs

These examples illustrate how raw inputs map to structured outputs across different complexity levels.

---

## Example 1: Simple Input (Single Thread)

### Raw Input
> "I'm thinking about switching from Notion to Todoist for task management. I use Notion for everything but it's getting slow and I never actually check my tasks in it. Thoughts?"

### How to Handle This

**Complexity level:** Simple (1 clear question, narrow scope). Target ~800-1,200 words.

**Section 1 (Mirror):** "You're considering replacing Notion with Todoist specifically for task management. The core trigger is that Notion's all-in-one nature means your tasks get buried alongside notes, docs, and databases, and the friction of opening Notion for a quick task check means you skip it. You're not asking whether to leave Notion entirely; you're asking whether to extract task management into a dedicated tool."

**Key moves:**
- Clarified the scope (task management only, not full Notion replacement)
- Surfaced the real problem (friction and buried tasks, not "Notion is bad")
- Named an assumption (you still want Notion for other things)

**Section 4 (Approaches):** Only 2 needed here. "Switch to Todoist for tasks, keep Notion for everything else" vs. "Fix your Notion setup with a dedicated tasks database and better views." A third approach is not needed; do not pad.

**Section 5 (80/20):** Should be direct. If the user's real problem is friction, a dedicated task app likely wins because no amount of Notion optimization fixes the "I don't open it for quick checks" problem.

---

## Example 2: Medium Input (Multiple Threads)

### Raw Input
> "With the quantity of skills being released at such a rapid pace and the adoption of open claw... I am wondering, is there any repo that reliably tests the security or risks of the skills? Perhaps an open source tool that evaluates skills and outputs some sort of standard risk factor or prioritize risk assessment? What would the factors be? Perhaps a part of it is more about informing the user or affirming what the skill can do or access... Because the user may want the deep access.... But What if they don't know what they don't know? What are the different types of security risks? I wonder what would be involved in creating something like this."

### How to Handle This

**Complexity level:** Medium-to-complex (4+ threads). Target ~2,500-3,500 words.

**Section 1 (Mirror):** Identify the distinct threads:
1. Does a skill security evaluation tool exist today?
2. What would a risk scoring standard look like?
3. How do you handle the user-awareness gap?
4. What would it take to build this?
5. Architecture question: centralized repo vs. evaluation skill vs. something else?

**Key moves:**
- Numbered the threads explicitly so the user can see the scope of their own thinking
- Flagged that thread 3 (user awareness) is a different kind of problem than threads 1-2 (tooling)

**Section 2 (Problem Space):** This is where web search adds value. The analysis should check whether existing tools, standards, or registries address this. Converging trends (rapid skill proliferation, open standards, privileged execution context) belong here.

**Section 4 (Approaches):** 3 approaches warranted:
- A: Lightweight "permissions manifest" standard (low effort, high adoption potential)
- B: Evaluation skill that audits other skills (medium effort, self-contained)
- C: Centralized registry with submission review (high effort, ecosystem-level)

Each approach should address the user-awareness gap differently.

**Section 6 (Evidence Map):** This topic benefits from external source validation. Search for existing security frameworks, MCP security discussions, npm/PyPI security scanning tools as analogues.

---

## Example 3: Complex Input (Organizational / Multi-Stakeholder)

### Raw Input
> A long Slack thread with screenshots, multiple stakeholder opinions, and the user's gut reactions pasted in, asking for help crafting a thoughtful response while also wanting to understand the broader organizational dynamics.

### How to Handle This

**Complexity level:** Complex. Target ~3,000-4,000 words.

**Key differences at this complexity level:**
- Section 1 needs to separate the user's own position from the other stakeholders' positions
- Section 2 should map the stakeholder landscape explicitly
- Section 3 should evaluate each stakeholder's position charitably before analyzing
- Section 4 may include both "what to think" approaches and "what to say" approaches (the user needs both a mental model and a message)
- Section 5 should address the immediate action (the Slack reply) AND the longer-term strategic question

**Common mistake:** Getting lost in the organizational complexity and producing a 5,000-word analysis when the user needs a 200-word Slack message and a 1,000-word mental model. Scale appropriately.

---

## Anti-Examples: What NOT to Do

### Anti-Example 1: Over-Structured Simple Topic

**Input:** "Should I use tabs or spaces?"
**Wrong:** A 3,000-word analysis with 4 approaches, stakeholder analysis, and an evidence map citing coding style research papers.
**Right:** This is not a Strategy Primer input. Answer it directly in chat. The skill should not trigger for simple factual or preference questions.

### Anti-Example 2: Generic Analysis

**Input:** "I'm thinking about starting a newsletter."
**Wrong Section 3:** "Strengths: Newsletters can build an audience. Weaknesses: Newsletters require consistency. Risks: You might run out of content."
**Right Section 3:** "The strongest signal here is that you already produce structured thinking documents regularly: the weekly engineering review you write, the internal wiki pages you keep current, and the incident write-ups your team still cites months later. You have a content engine; you just do not have a distribution channel. The primary risk is not content generation but editorial consistency and the overhead of yet another publishing workflow alongside your existing commitments to [specific things from context]."

The difference: generic analysis could apply to anyone. Good analysis uses the user's specific context.

### Anti-Example 3: Padding Approaches

**Input:** A topic where there are clearly 2 viable approaches.
**Wrong:** Adding a third "hybrid" approach that is just "do a little of both" with no distinct strategy.
**Right:** Present 2 approaches, explain why a hybrid does not make sense (or does, with specifics), and move on.
