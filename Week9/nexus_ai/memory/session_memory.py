from collections import deque


class SessionMemory:

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)

    def add_message(self, role: str, content: str):

        if not content:
            return

        role = role.capitalize() if role else "User"

        self.messages.append({
            "role": role,
            "content": str(content)
        })

    def get_recent(self, limit: int | None = None):

        if not self.messages:
            return ""

        msgs = list(self.messages)

        if limit:
            msgs = msgs[-limit:]

        formatted = []

        for msg in msgs:
            role = msg.get("role", "User")
            content = msg.get("content", "")
            formatted.append(f"{role}: {content}")

        return "\n".join(formatted)

    def size(self):
        return len(self.messages)

    def clear(self):
        self.messages.clear()