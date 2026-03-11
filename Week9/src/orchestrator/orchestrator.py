import os
import json
from typing import Dict, List, Any

from dotenv import load_dotenv
from pydantic import BaseModel

from autogen_agentchat.agents import AssistantAgent

# tools
from tools.file_agent import file_agent
from tools.code_executor import code_executor
from tools.db_agent import create_db_agent

from config.model_config import model_client


class PlanStep(BaseModel):

    agent: str
    task: str
    input_keys: List[str] = []
    output_key: str


class ExecutionPlan(BaseModel):

    steps: List[PlanStep]



SYSTEM_PROMPT = """
You are an orchestration planner.

Your job is ONLY to produce an execution plan.

Code execution steps are stateless.

Do NOT pass variables like DataFrames between steps.

If analysis is required, perform it in a SINGLE code step.

Return JSON in this format:

{
  "steps": [
    {
      "agent": "file | db | code",
      "task": "description",
      "input_keys": [],
      "output_key": "result_name"
    }
  ]
}

Rules:
- file agent → find files
- db agent → query database
- code agent → perform python analysis

Return ONLY JSON.
"""



planner_agent = AssistantAgent(
    name="ORCHESTRATOR",
    model_client=model_client,
    system_message=SYSTEM_PROMPT,
)


db = create_db_agent(
    name="DB_AGENT",
    db_path="database/sample.db",
    model_client=model_client
)


async def run_orchestration(user_query: str) -> Dict[str, Any]:

    print("\n--- Generating Execution Plan ---\n")

    plan_response = await planner_agent.run(task=user_query)

    plan_json = plan_response.messages[-1].content

    print("RAW PLAN:")
    print(plan_json)

    plan = ExecutionPlan.model_validate(json.loads(plan_json))

    context: Dict[str, Any] = {}

    for step in plan.steps:

        step_context = {
            k: context[k] for k in step.input_keys if k in context
        }

        print(f"\nRunning Step → {step.agent}")
        print(f"Task → {step.task}")


        if step.agent == "file":
            output = "src/data/sales.csv"


        elif step.agent == "db":

            enriched_task = step.task

            if step_context:
                enriched_task += f"\nContext:\n{json.dumps(step_context,indent=2)}"

            result = await db.run(task=enriched_task)

            output = result.messages[-1].content

        elif step.agent == "code":

            enriched_task = step.task

            if step_context:
                enriched_task += f"\nContext:\n{json.dumps(step_context,indent=2)}"

            output = await code_executor(enriched_task)

        else:

            raise ValueError(f"Unknown agent type: {step.agent}")

        print("Output:")
        print(output)

        context[step.output_key] = output

    return context


def summarize_results(context: Dict[str, Any]) -> str:

    summary = []

    for key, value in context.items():
        summary.append(f"{key}:\n{value}")

    return "\n\n".join(summary)