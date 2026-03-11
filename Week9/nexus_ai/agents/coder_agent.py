from autogen_core.models import UserMessage


class CoderAgent:

    def __init__(self, llm):
        self.llm = llm

    async def run(self, task):

        prompt = f"""
You are Nexus AI Technical Architect.

TASK:
{task}

Provide:

- System architecture
- Tech stack suggestions
- Scalability design
- APIs / services breakdown
- Deployment approach

Return concise structured technical design.

FORMAT:

Architecture Overview:
Tech Stack:
Components:
Scalability Strategy:
Deployment:
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()
