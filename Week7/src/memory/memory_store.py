import json
from pathlib import Path
from datetime import datetime

MEMORY_PATH = Path("src/logs/CHAT_LOGS.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)


class MemoryStore:
    def __init__(self, max_history=5):
        self.max_history = max_history

        if not MEMORY_PATH.exists():
            MEMORY_PATH.write_text("[]")

    def _load(self):
        try:
            return json.loads(MEMORY_PATH.read_text())
        except:
            return []

    def _save(self, data):
        MEMORY_PATH.write_text(json.dumps(data, indent=2))

    def add(self, user_query, answer, chunks=None):
        history = self._load()

        history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_query,
            "assistant": answer,
            "sources": chunks
        })

        history = history[-self.max_history:]
        self._save(history)

    def get_context(self):
        history = self._load()

        if not history:
            return ""

        context = "Conversation History:\n"
        for h in history:
            context += f"User: {h['user']}\n"
            context += f"Assistant: {h['assistant']}\n"

        return context

    def clear(self):
        self._save([])
