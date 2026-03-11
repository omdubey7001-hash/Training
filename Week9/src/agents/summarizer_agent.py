from autogen_agentchat.agents import AssistantAgent
from agents.research_agent import model_client

summarizer_agent = AssistantAgent(
    name="SummarizerAgent",
    model_client=model_client,
    description="Summarizes research text only.",
    system_message="""
You are SummarizerAgent.

ROLE:
- Convert research notes into concise summary.

RULES:
- Do NOT add new information.
- Do NOT produce final answer.
- Keep it short and structured.

OUTPUT:
- Bullet or short summary.
"""
)