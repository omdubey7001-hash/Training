from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken


class ValidatorAgent:

    def __init__(self, model_client):

        self.agent = AssistantAgent(
            name="validator",
            system_message="Validate the answer and return the final improved result.",
            model_client=model_client,
        )

    async def run(self, text):

        cancellation = CancellationToken()

        response = await self.agent.on_messages(
            [TextMessage(content=text, source="reflector")],
            cancellation
        )

        return response.chat_message.content