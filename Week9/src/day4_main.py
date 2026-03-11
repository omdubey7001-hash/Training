import asyncio

from config.model_config import model_client
from memory.memory_manager import MemoryManager

from autogen_core.models import UserMessage, SystemMessage


async def main():

    print("\n===== MEMORY AGENT SYSTEM =====\n")

    memory = MemoryManager(model_client)

    while True:

        user = input("User: ")

        if user.lower() in ["exit", "quit"]:
            print("\nSession ended.")
            break

        # retrieve memory context
        context = memory.retrieve_context(user)

        response = await model_client.create(
            messages=[
                SystemMessage(
                    content=context,
                    source="system"
                ),
                UserMessage(
                    content=user,
                    source="user"
                )
            ]
        )

        agent_reply = response.content

        print("Agent:", agent_reply)

        # store interaction in memory
        await memory.store_interaction(user, agent_reply)


if __name__ == "__main__":
    asyncio.run(main())