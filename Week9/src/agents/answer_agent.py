from autogen_agentchat.agents import AssistantAgent
from agents.research_agent import model_client

answer_agent = AssistantAgent(
    name="AnswerAgent",
    model_client=model_client,
    description="Creates final user-ready answer.",
    system_message="""
You are AnswerAgent.

ROLE:
- Produce final answer from summary.

RULES:
- Do NOT add new research.
- Explain clearly for user.

OUTPUT:
- Final polished answer.
"""
)