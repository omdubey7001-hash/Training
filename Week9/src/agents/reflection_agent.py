from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class ReflectorAgent:

    def __init__(self, model_client):

        self.agent = AssistantAgent(
            name="reflector",
            system_message="Improve and refine the provided content.",
            model_client=model_client,
        )

    async def run(self, text):

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=text, source="worker")],
            cancellation
        )

        return response.chat_message.content