import os

from autogen_ext.agents.file_surfer import FileSurfer
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.tools import FunctionTool

from config.model_config import model_client


BASE_PATH = "src"


def write_file(path: str, content: str) -> str:
    """
    Create or overwrite a file with content
    """

    full_path = os.path.join(BASE_PATH, path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File written successfully at {full_path}"


write_file_tool = FunctionTool(
    func=write_file,
    description="Create or overwrite a file with given content"
)


def append_file(path: str, content: str) -> str:
    """
    Append content to existing file
    """

    full_path = os.path.join(BASE_PATH, path)

    with open(full_path, "a", encoding="utf-8") as f:
        f.write(content)

    return f"Content appended to {full_path}"


append_file_tool = FunctionTool(
    func=append_file,
    description="Append content to a file"
)


def list_files(directory: str = "") -> str:

    full_path = os.path.join(BASE_PATH, directory)

    if not os.path.exists(full_path):
        return "Directory not found"

    files = os.listdir(full_path)

    return "\n".join(files)


list_files_tool = FunctionTool(
    func=list_files,
    description="List files inside a directory"
)


def create_file_surfer_tool():

    file_surfer_agent = FileSurfer(
        name="file_browser",
        model_client=model_client,
        base_path=BASE_PATH
    )

    return AgentTool(
        agent=file_surfer_agent,
        return_value_as_last_message=True
    )


async def run_file_query(user_query: str):

    file_surfer_tool = create_file_surfer_tool()

    agent = AssistantAgent(
        name="filesystem_agent",
        model_client=model_client,
        tools=[
            file_surfer_tool,
            write_file_tool,
            append_file_tool,
            list_files_tool
        ],
        system_message=(
            "You are a filesystem agent.\n"
            "You can browse directories, read files, create files, "
            "write content and append to files.\n"
            "Use the available tools to perform file operations.\n"
        )
    )

    result = await agent.run(task=user_query)

    return result.messages[-1].content


async def file_agent(query: str):
    return await run_file_query(query)