import os
from dotenv import load_dotenv

from autogen_ext.models.openai import OpenAIChatCompletionClient


load_dotenv()

api_key = os.getenv("GROK_API_KEY")


model_info = {
    "family": "oss",
    "vision": False,
    "function_calling": True,
    "json_output": True,
    "structured_output": True,
    "context_length": 8192,
}


model_client = OpenAIChatCompletionClient(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",

    model_info=model_info,

    temperature=0,
    max_tokens=2000,

    timeout=60,
    max_retries=3,

    parallel_tool_calls=True
)