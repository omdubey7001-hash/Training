from agents.worker_agent import WorkerAgent
from agents.reflection_agent import ReflectorAgent
from agents.validator import ValidatorAgent


AGENT_REGISTRY = {
    "worker": WorkerAgent,
    "reflector": ReflectorAgent,
    "validator": ValidatorAgent,
}