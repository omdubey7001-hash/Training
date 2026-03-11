import uuid
import json
import re

from autogen_core.models import UserMessage

from .session_memory import SessionMemory
from .vector_store import VectorStore
from .long_term_store import LongTermMemory


SIM_THRESHOLD = 0.80
DUP_THRESHOLD = 0.93


def clean_llm_json(text: str):
    if not text:
        return ""
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    return text.strip()


def safe_json_list(text: str):
    try:
        text = clean_llm_json(text)
        match = re.search(r"\[.*\]", text, re.S)
        if match:
            return json.loads(match.group())
    except:
        pass
    return []


def safe_json_obj(text: str):
    try:
        text = clean_llm_json(text)
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group())
    except:
        pass
    return {}


class MemoryManager:

    def __init__(self, model_client):
        self.session = SessionMemory()
        self.vector = VectorStore()
        self.long_term = LongTermMemory()
        self.llm = model_client

    def _generate_id(self):
        return str(uuid.uuid4())

    async def summarize(self, text: str):

        prompt = f"""
Extract long-term USER facts.

Return STRICT JSON list.

Format:
[
  {{"fact": "...", "category": "...", "importance": 0-1}}
]

Conversation:
{text}
"""

        try:
            response = await self.llm.create(
                messages=[UserMessage(content=prompt, source="user")]
            )

            facts = safe_json_list(response.content)

            if not isinstance(facts, list):
                return []

            return facts

        except Exception as e:
            print("Summarize error:", e)
            return []

    async def store_interaction(self, user_msg, agent_msg):

        self.session.add_message("User", user_msg)
        self.session.add_message("Agent", agent_msg)

        conversation = f"USER: {user_msg}\nAGENT: {agent_msg}"

        facts = await self.summarize(conversation)

        for fact in facts:
            if isinstance(fact, dict) and "fact" in fact:
                await self.reconcile_and_store(fact)

    def retrieve_context(self, query):

        session_context = self.session.get_recent() or ""

        results = self.vector.search(query, k=3) or []

        memory_ids = [mem_id for mem_id, _ in results]

        facts = self.long_term.get_by_ids(memory_ids) if memory_ids else []

        if not facts:
            facts = self.long_term.get_identity_facts()

        return f"""
SESSION MEMORY:
{session_context}

LONG TERM MEMORY:
{facts}
"""

    async def reconcile_memory(self, old_fact: str, new_fact: str):

        prompt = f"""
Compare facts.

OLD: {old_fact}
NEW: {new_fact}

Return JSON:
{{
 "relation": "...",
 "final_fact": "..."
}}
"""

        try:
            response = await self.llm.create(
                messages=[UserMessage(content=prompt, source="user")]
            )

            return safe_json_obj(response.content)

        except Exception as e:
            print("Reconcile error:", e)
            return {}

    async def reconcile_and_store(self, fact_obj):

        new_fact = fact_obj.get("fact")
        if not new_fact:
            return

        candidates = self.vector.search(new_fact, k=3) or []

        if not candidates:
            self._store_new_fact(fact_obj)
            return

        for mem_id, score in candidates:

            if score < SIM_THRESHOLD:
                continue

            if score > DUP_THRESHOLD:
                return

            old_fact_list = self.long_term.get_by_ids([mem_id])
            if not old_fact_list:
                continue

            old_fact = old_fact_list[0]

            decision = await self.reconcile_memory(old_fact, new_fact)

            relation = decision.get("relation")
            final_fact = decision.get("final_fact")

            if relation == "DUPLICATE":
                return

            if relation in {"CONTRADICTS", "UPDATES", "MERGEABLE"}:

                self.vector.delete(mem_id)
                self.long_term.delete(mem_id)

                updated = dict(fact_obj)
                if final_fact:
                    updated["fact"] = final_fact

                self._store_new_fact(updated)
                return

        self._store_new_fact(fact_obj)

    def _store_new_fact(self, fact_obj):

        importance = float(fact_obj.get("importance", 0))

        if importance < 0.5:
            return

        fact_text = fact_obj.get("fact")
        if not fact_text:
            return

        memory_id = self._generate_id()

        self.vector.add_text(memory_id, fact_text)

        self.long_term.store(
            memory_id,
            fact_text,
            fact_obj.get("category", "general"),
            importance,
        )