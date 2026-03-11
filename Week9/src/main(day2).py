import asyncio

from config.model_config import model_client
from orchestrator.planner import Planner


async def main():

    planner = Planner(model_client)

    result = await planner.run(
        "Explain Agentic AI in simple terms and its benifit in student life"
    )

    print("\nFINAL OUTPUT\n")

    print(result)


asyncio.run(main())