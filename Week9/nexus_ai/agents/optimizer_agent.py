from autogen_core.models import UserMessage


class OptimizerAgent:

    def __init__(self, llm):
        self.llm = llm

    async def improve(self, text, critique):

        text = str(text)[:4000]
        critique = str(critique)[:2000]

        prompt = f"""
You are Nexus AI Solution Optimizer.

Improve the solution using the critique.

Your job:

- Fix major issues first
- Improve clarity
- Improve feasibility
- Improve scalability logic
- Merge research + analysis + technical design
- Remove redundant content
- Make solution realistic

Return structured improved solution.

FORMAT:

Improved Solution Overview:
Key Enhancements Applied:
Final Refined Plan:

ORIGINAL SOLUTION:
{text}

CRITIQUE:
{critique}
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()
