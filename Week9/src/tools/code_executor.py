from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ToolCallSummaryMessage

from config.model_config import model_client


def build_code_tool():

    executor = LocalCommandLineCodeExecutor(
        work_dir="workspace",
        timeout=600
    )

    return PythonCodeExecutionTool(executor)


async def run_python_task(prompt: str):

    code_tool = build_code_tool()

    agent = AssistantAgent(
        name="python_agent",
        tools=[code_tool],
        model_client=model_client,
        system_message=(
            "You are a Python execution agent.\n"
            "Write Python code and execute it using the tool.\n"
            "Create files using relative paths.\n"
            "Always print results after execution.\n"
        )
    )

    response = await agent.run(task=prompt)

    for message in reversed(response.messages):
        if isinstance(message, ToolCallSummaryMessage):
            return message.content

    return response.messages[-1].content


async def code_executor(task: str):
    return await run_python_task(task)