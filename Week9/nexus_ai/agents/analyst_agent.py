from autogen_core.models import UserMessage


class AnalystAgent:

    def __init__(self, llm):
        self.llm = llm

    async def run(self, task):

        prompt = f"""
You are Nexus AI Strategy Analyst.

TASK:
{task}

Analyze:

- Market feasibility
- Cost factors
- Technical complexity
- Risks
- Scalability potential

Return concise structured analysis.

FORMAT:

Feasibility:
Key Risks:
Cost Factors:
Scalability:
Recommendations:
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()
