from autogen_core.models import UserMessage


class CriticAgent:

    def __init__(self, llm):
        self.llm = llm

    async def review(self, text):

        text = str(text)[:4000]

        prompt = f"""
You are Nexus AI Senior Solution Critic.

Review the solution below.

Identify:

- Logical gaps
- Missing components
- Unrealistic assumptions
- Technical risks
- Business risks
- Scalability concerns

Be concise and actionable.

FORMAT:

Overall Quality Score (1-10):

Major Issues:
- ...

Minor Issues:
- ...

Improvement Suggestions:
- ...

Solution:
{text}
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()
