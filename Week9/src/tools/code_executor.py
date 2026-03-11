import os

from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import ToolCallSummaryMessage

from config.model_config import model_client


WORKSPACE = "workspace"

os.makedirs(WORKSPACE, exist_ok=True)

_executor = LocalCommandLineCodeExecutor(
    work_dir=WORKSPACE,
    timeout=120
)

_code_tool = PythonCodeExecutionTool(_executor)


python_agent = AssistantAgent(
    name="PYTHON_EXECUTOR_AGENT",
    tools=[_code_tool],
    model_client=model_client,
    system_message=(
        "You are a Python execution agent.\n"
        "You MUST always execute code using the tool.\n"
        "Never simulate outputs.\n"
        "Always print final results.\n"
        "Write full runnable Python scripts.\n"
        "Use relative file paths only.\n"
    )
)


async def code_executor(task: str):

    response = await python_agent.run(task=task)

    tool_outputs = []

    for message in response.messages:
        if isinstance(message, ToolCallSummaryMessage):
            tool_outputs.append(message.content)

    if tool_outputs:
        return "\n\n".join(tool_outputs)

    return response.messages[-1].content