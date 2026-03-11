import asyncio
import json
import os
from datetime import datetime

from nexus_ai.memory.memory_manager import MemoryManager

from nexus_ai.agents.planner_agent import PlannerAgent
from nexus_ai.agents.researcher_agent import ResearcherAgent
from nexus_ai.agents.coder_agent import CoderAgent
from nexus_ai.agents.analyst_agent import AnalystAgent
from nexus_ai.agents.critic_agent import CriticAgent
from nexus_ai.agents.optimizer_agent import OptimizerAgent
from nexus_ai.agents.validator_agent import ValidatorAgent
from nexus_ai.agents.reporter_agent import ReporterAgent


# ===== SAFE LOG PATH =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "..", "logs", "system.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log(event, data=None):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} | {event} | {data}\n")


class MasterOrchestrator:

    def __init__(self, model_client):

        self.memory = MemoryManager(model_client)

        self.planner = PlannerAgent(model_client)

        self.researcher = ResearcherAgent(model_client)
        self.coder = CoderAgent(model_client)
        self.analyst = AnalystAgent(model_client)

        self.critic = CriticAgent(model_client)
        self.optimizer = OptimizerAgent(model_client)
        self.validator = ValidatorAgent(model_client)
        self.reporter = ReporterAgent(model_client)

    async def run_agent(self, agent_name, task):

        if agent_name == "researcher":
            return await self.researcher.run(task)

        if agent_name == "coder":
            return await self.coder.run(task)

        if agent_name == "analyst":
            return await self.analyst.run(task)

        return f"Unknown agent {agent_name}"

    async def execute_dag(self, plan):

        steps = {s["step_id"]: s for s in plan["steps"]}
        pending = set(steps.keys())
        completed = set()
        outputs = {}

        while pending:

            ready = [
                sid for sid in pending
                if all(dep in completed for dep in steps[sid].get("depends_on", []))
            ]

            if not ready:
                raise Exception("DAG execution failed — circular dependency")

            log("dag_batch_start", {"steps": ready})

            tasks = []

            for sid in ready:
                step = steps[sid]
                agent = step["agent"]
                task = step["task"]

                tasks.append(
                    asyncio.create_task(
                        self.run_agent(agent, task)
                    )
                )

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for sid, result in zip(ready, results):
                outputs[sid] = str(result)
                completed.add(sid)
                pending.remove(sid)

            log("dag_batch_complete", {"completed": list(completed)})

        return outputs

    async def run(self, user_task):

        log("task_received", {"task": user_task})

        # ===== MEMORY =====
        context = self.memory.retrieve_context(user_task)

        # ===== PLANNER =====
        plan = await self.planner.plan(user_task, context)

        log("plan_generated", {
            "steps": len(plan.get("steps", []))
        })

        # ===== DAG EXECUTION =====
        step_outputs = await self.execute_dag(plan)

        combined_output = "\n\n".join(step_outputs.values())

        log("workers_completed", {
            "steps_executed": len(step_outputs)
        })

        # ===== REFLECTION =====
        critique = await self.critic.review(combined_output)

        improved_output = await self.optimizer.improve(
            combined_output,
            critique
        )

        validated_output = await self.validator.validate(
            improved_output
        )

        final_report = await self.reporter.generate(
            validated_output
        )

        # ===== MEMORY STORE =====
        await self.memory.store_interaction(
            user_task,
            final_report
        )

        log("memory_updated")

        return final_report
