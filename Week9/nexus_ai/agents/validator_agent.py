from autogen_core.models import UserMessage


class ValidatorAgent:

    def __init__(self, llm):
        self.llm = llm

    async def validate(self, text):

        text = str(text)[:4000]

        prompt = f"""
You are Nexus AI Final Solution Validator.

Validate the solution.

Check:

- Logical consistency
- Technical feasibility
- Missing critical components
- Unrealistic claims
- Clarity of execution plan

Return structured validation.

FORMAT:

Validation Status: PASS or NEEDS_IMPROVEMENT

Critical Issues:
- ...

Minor Issues:
- ...

Validated Solution Summary:

Solution:
{text}
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()
