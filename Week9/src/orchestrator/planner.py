import asyncio
import json
from typing import List, Literal, Dict

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

from pydantic import BaseModel, field_validator

from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectorAgent
from agents.validator import ValidatorAgent


planner_msg = """
You are a planner that creates a DAG for solving a task.

Rules:

1. Create MULTIPLE worker nodes (w1, w2, w3...).
2. All workers must have NO dependencies.
3. Workers must run in parallel.
4. A single reflector node must depend on ALL workers.
5. A single validator node must depend on the reflector.

Return ONLY JSON.

Example:

{
 "nodes":[
  {"id":"w1","role":"worker","task":"task1","deps":[]},
  {"id":"w2","role":"worker","task":"task2","deps":[]},
  {"id":"w3","role":"worker","task":"task3","deps":[]},
  {"id":"r1","role":"reflector","task":"combine results","deps":["w1","w2","w3"]},
  {"id":"v1","role":"validator","task":"validate answer","deps":["r1"]}
 ]
}
"""


class DAGNode(BaseModel):

    id: str
    role: Literal["worker", "reflector", "validator"]
    task: str
    deps: List[str]

    @field_validator("id")
    def validate_id(cls, v):

        if not v.strip():
            raise ValueError("id empty")

        return v


class Planner:

    def __init__(self, model_client):

        self.model_client = model_client

        self.planner_agent = AssistantAgent(
            name="planner",
            system_message=planner_msg,
            model_client=model_client,
        )

    async def create_plan(self, query):

        cancellation = CancellationToken()

        response = await self.planner_agent.on_messages(
            [TextMessage(content=query, source="user")],
            cancellation
        )

        output = response.chat_message.content

        raw = json.loads(output)

        nodes = [DAGNode(**n) for n in raw["nodes"]]

        workers = [n for n in nodes if n.role == "worker"]
        worker_ids = [w.id for w in workers]

        for w in workers:
            w.deps = []

        # reflector must depend on all workers
        for n in nodes:
            if n.role == "reflector":
                n.deps = worker_ids

        return nodes

    async def run(self, query):

        nodes = await self.create_plan(query)

        print("\nORCHESTRATOR PLAN\n")

        for n in nodes:
            print(f"{n.id} | role={n.role} | deps={n.deps} | task={n.task}")

        results: Dict[str, str] = {}

        print("\nPARALLEL EXECUTION STARTED\n")

        pending = {n.id: n for n in nodes}

        while pending:

            ready = [
                n for n in pending.values()
                if all(dep in results for dep in n.deps)
            ]

            tasks = []

            for node in ready:

                if node.role == "worker":

                    agent = WorkerAgent(
                        node.id,
                        node.task,
                        self.model_client
                    )

                    tasks.append(
                        asyncio.create_task(
                            self._run_worker(agent, node, query)
                        )
                    )

                elif node.role == "reflector":

                    agent = ReflectorAgent(self.model_client)

                    inputs = "\n\n".join(results[d] for d in node.deps)

                    tasks.append(
                        asyncio.create_task(
                            self._run_reflector(agent, node, inputs)
                        )
                    )

                elif node.role == "validator":

                    agent = ValidatorAgent(self.model_client)

                    inputs = results[node.deps[0]]

                    tasks.append(
                        asyncio.create_task(
                            self._run_validator(agent, node, inputs)
                        )
                    )

            outputs = await asyncio.gather(*tasks)

            for node_id, output in outputs:

                results[node_id] = output

                del pending[node_id]

        final_node = next(n.id for n in nodes if n.role == "validator")

        return results[final_node]

    async def _run_worker(self, agent, node, query):

        print(f"\nWORKER STARTED → {node.id}")
        print(f"Task: {node.task}\n")

        out = await agent.run(query)

        print(f"WORKER FINISHED → {node.id}\n")

        return node.id, out["output"]

    async def _run_reflector(self, agent, node, text):

        print("\nREFLECTION AGENT RUNNING\n")

        out = await agent.run(text)

        print("\nREFLECTION COMPLETE\n")

        return node.id, out

    async def _run_validator(self, agent, node, text):

        print("\nVALIDATOR CHECKING FINAL OUTPUT\n")

        out = await agent.run(text)

        print("\nVALIDATION COMPLETE\n")

        return node.id, out