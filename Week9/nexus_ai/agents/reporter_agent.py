from autogen_core.models import UserMessage


class ReporterAgent:

    def __init__(self, llm):
        self.llm = llm

    async def generate(self, text):

        text = str(text)[:4500]

        prompt = f"""
You are Nexus AI Final Report Generator.

Your job:

- Convert validated solution into clear actionable final output
- Focus on execution plan
- Keep it practical
- Avoid corporate filler
- Avoid generic templates
- Be structured and concise

FORMAT:

Final Solution Summary:
Execution Strategy:
Key Components:
Risks & Mitigation:
Next Steps:

Validated Content:
{text}
"""

        response = await self.llm.create(
            messages=[
                UserMessage(content=prompt, source="user")
            ]
        )

        return response.content.strip()