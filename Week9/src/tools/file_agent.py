import os

from autogen_ext.agents.file_surfer import FileSurfer
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.tools import AgentTool
from autogen_core.tools import FunctionTool

from config.model_config import model_client


BASE_PATH = "src"



def _safe_path(path: str) -> str:

    full = os.path.abspath(os.path.join(BASE_PATH, path))
    base = os.path.abspath(BASE_PATH)

    if not full.startswith(base):
        raise ValueError("Invalid path access attempt")

    return full



def find_file_by_name(filename: str) -> str:

    matches = []

    for root, _, files in os.walk(BASE_PATH):
        for f in files:
            if f.lower() == filename.lower():
                matches.append(os.path.join(root, f))

    if not matches:
        return "File not found"

    return "\n".join(matches)


find_file_tool = FunctionTool(
    func=find_file_by_name,
    description="Find file by exact filename and return full path"
)


def write_file(path: str, content: str) -> str:

    full_path = _safe_path(path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"File written at {full_path}"


write_file_tool = FunctionTool(
    func=write_file,
    description="Create or overwrite a file"
)


def append_file(path: str, content: str) -> str:

    full_path = _safe_path(path)

    with open(full_path, "a", encoding="utf-8") as f:
        f.write(content)

    return f"Appended content at {full_path}"


append_file_tool = FunctionTool(
    func=append_file,
    description="Append content to file"
)


def list_files(directory: str = "") -> str:

    root = _safe_path(directory)

    if not os.path.exists(root):
        return "Directory not found"

    results = []

    for r, _, files in os.walk(root):
        for f in files:
            results.append(os.path.join(r, f))

    return "\n".join(results) if results else "No files found"


list_files_tool = FunctionTool(
    func=list_files,
    description="Recursively list files"
)



_file_surfer_agent = FileSurfer(
    name="FILE_BROWSER",
    model_client=model_client,
    base_path=BASE_PATH
)

file_surfer_tool = AgentTool(
    agent=_file_surfer_agent,
    return_value_as_last_message=True
)



filesystem_agent = AssistantAgent(
    name="FILESYSTEM_AGENT",
    model_client=model_client,
    tools=[
        find_file_tool,     
        file_surfer_tool,
        list_files_tool,
        write_file_tool,
        append_file_tool
    ],
    system_message=(
        "You are a filesystem agent.\n"
        "You MUST use tools.\n"
        "If user asks to find specific file → use find_file_by_name.\n"
        "Do NOT list entire directory unless asked.\n"
        "You cannot generate datasets.\n"
        "Always return exact real file paths.\n"
    )
)



async def file_agent(query: str):

    result = await filesystem_agent.run(task=query)

    return result.messages[-1].content

