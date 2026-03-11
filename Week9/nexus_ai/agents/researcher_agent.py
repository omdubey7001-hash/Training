from autogen_core.models import UserMessage


class ResearcherAgent:

    def __init__(self, llm):
        self.llm = llm

    async def run(self, task):

        prompt = f"""
You are Nexus AI Research Agent.

TASK:
{task}

Your job:
- Provide domain knowledge
- Market trends
- existing solutions
- best practices
- risks

Return concise structured research.

FORMAT:

Research Summary:
Key Insights:
Risks:
Opportunities:
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()
