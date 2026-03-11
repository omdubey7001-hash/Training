from autogen_agentchat.agents import AssistantAgent
from config.model_config import model_client


research_agent = AssistantAgent(
    name="ResearchAgent",
    model_client=model_client,
    description="Collects factual research information only.",
    system_message="""
You are ResearchAgent.

ROLE:
- Gather detailed factual information.

RULES:
- Do NOT summarize.
- Do NOT generate final answers.
- Provide structured research notes.
- Mention uncertainty if needed.
OUTPUT:
- Detailed information only.
"""
)