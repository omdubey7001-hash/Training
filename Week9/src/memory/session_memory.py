from collections import deque


class SessionMemory:

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages
        self.messages = deque(maxlen=max_messages)

    def add_message(self, role: str, content: str):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_recent(self):

        formatted = []

        for msg in self.messages:
            formatted.append(f"{msg['role']}: {msg['content']}")

        return "\n".join(formatted)

    def clear(self):
        self.messages.clear()