import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination


from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.answer_agent import answer_agent


async def main():

    team = RoundRobinGroupChat(
        participants=[
            research_agent,
            summarizer_agent,
            answer_agent
        ],
        termination_condition = MaxMessageTermination(4)
    )

    task = "Explain Agentic AI in simple terms."

    await Console(team.run_stream(task=task))


asyncio.run(main())