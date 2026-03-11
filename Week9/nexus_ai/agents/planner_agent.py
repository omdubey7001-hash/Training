import json
import re
from autogen_core.models import UserMessage


class PlannerAgent:

    def __init__(self, llm):
        self.llm = llm

    async def plan(self, task, memory_context):

        memory_context = str(memory_context)[:500]

        prompt = f"""
You are Nexus AI Autonomous Task Planner.

First classify the USER TASK:

EXECUTION TASK examples:
- create file
- write runnable code
- run script
- analyze csv
- query database
- perform computation

REASONING TASK examples:
- design architecture
- research topic
- plan startup
- strategy analysis
- build system design

Planning Rules:

1. If EXECUTION TASK → create SINGLE step using coder agent.
2. If REASONING TASK → create MULTI-STEP DAG plan using researcher → analyst → coder order.
3. Add depends_on field for dependency aware execution.
4. Keep steps between 1 and 4.
5. Tasks must be clear actionable sentences.

Return STRICT JSON only.

FORMAT:

{{
 "goal":"short goal",
 "steps":[
   {{
     "step_id":1,
     "agent":"coder",
     "task":"clear actionable task",
     "depends_on":[]
   }}
 ]
}}

USER TASK:
{task}

MEMORY CONTEXT:
{memory_context}
"""

        response = await self.llm.create(
            messages=[UserMessage(content=prompt, source="user")]
        )

        raw = response.content.strip()

        try:
            plan = json.loads(raw)

        except Exception:
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not match:
                raise ValueError(f"Planner invalid JSON:\n{raw}")
            plan = json.loads(match.group())

        # ===== VALIDATION =====

        if "steps" not in plan:
            raise ValueError("Planner missing steps")

        if len(plan["steps"]) == 0:
            raise ValueError("Planner empty steps")

        # normalize agents + depends
        for s in plan["steps"]:
            s["agent"] = str(s.get("agent", "")).lower().strip()
            if "depends_on" not in s:
                s["depends_on"] = []

        return plan
