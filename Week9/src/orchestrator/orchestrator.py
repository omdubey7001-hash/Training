import json
import re
from typing import Dict, List, Any

from pydantic import BaseModel

from autogen_agentchat.agents import AssistantAgent

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

You ONLY create execution plans.
You NEVER execute tasks.
You NEVER write python code.
You NEVER call tools.

AGENT RESPONSIBILITIES:

file → locate, browse, or read existing files
db → query structured database tables
code → generate data, create csv/files, run python analysis


PLANNING RULES:

- Create csv / random data / computation → use code agent
- Find / list / locate files → use file agent
- Database question → use db agent
- For file analysis → first file step then code step

Return STRICT JSON:

{
 "steps":[
   {
     "agent":"file | db | code",
     "task":"clear instruction",
     "input_keys":[],
     "output_key":"result"
   }
 ]
}

Return ONLY JSON.
"""

planner_agent = AssistantAgent(
    name="ORCHESTRATOR",
    model_client=model_client,
    system_message=SYSTEM_PROMPT,
    tools=[],
    max_tool_iterations=1
)



db = create_db_agent(
    name="DB_AGENT",
    db_path="database/sample.db",
    model_client=model_client
)


def safe_parse_plan(raw: str) -> ExecutionPlan:

    if not raw:
        raise RuntimeError("Planner returned empty response")

    raw = raw.strip()

    raw = raw.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", raw, re.DOTALL)

    if not match:
        raise RuntimeError(f"Planner returned invalid JSON:\n{raw}")

    json_str = match.group(0)

    data = json.loads(json_str)

    return ExecutionPlan.model_validate(data)


async def run_orchestration(user_query: str) -> Dict[str, Any]:

    print("\n===== GENERATING PLAN =====\n")

    plan = None

    for attempt in range(3):

        plan_response = await planner_agent.run(task=user_query)

        raw_plan = plan_response.messages[-1].content

        print("RAW PLAN:\n", raw_plan)

        try:
            plan = safe_parse_plan(raw_plan)
            break
        except Exception as e:
            print(f"Planner parse failed (attempt {attempt+1})")

    if not plan:
        raise RuntimeError("Planner failed after retries")

    context: Dict[str, Any] = {}

    for step in plan.steps:

        if step.agent not in ["file", "db", "code"]:
            raise RuntimeError(f"Invalid agent in plan: {step.agent}")

        print(f"\n>>> Running Step [{step.agent}]")
        print(f"Task → {step.task}")

        step_context = {
            k: context[k] for k in step.input_keys if k in context
        }

        try:

            enriched_task = step.task

            if step_context:
                enriched_task += f"\nContext:\n{json.dumps(step_context, indent=2)}"

            if step.agent == "file":
                output = await file_agent(enriched_task)

            elif step.agent == "db":

                result = await db.run(task=enriched_task)

                output = ""

                for msg in reversed(result.messages):
                    if hasattr(msg, "content") and msg.content:
                        output = msg.content
                        break

                if not output:
                    output = "STEP FAILED: DB returned no result"

            elif step.agent == "code":
                output = await code_executor(enriched_task)

        except Exception as step_error:
            output = f"STEP FAILED: {str(step_error)}"

        print("Output:\n", output)

        context[step.output_key] = output

    return context



def summarize_results(context: Dict[str, Any]) -> str:

    return "\n\n".join([f"{k}:\n{v}" for k, v in context.items()])