import json

from rmonkey.utils.schema import Message


class Memory:
    id: str = None
    messages: list[Message] = []

    max_messages: int = 100
    context_window_tokens: int = 128_000
    total_tokens: int = 0

    def __init__(self, id: str = None, max_messages: int = 100, context_window_tokens: int = 128_000) -> None:
        self.id = id
        self.max_messages = max_messages
        self.context_window_tokens = context_window_tokens
        self.messages = []
        self.total_tokens = 0

    def set_id(self, session_id: str) -> None:
        self.session_id = session_id

    def add_message(
        self,
        message: Message = None,
        role: str = None,
        content: str = None,
        tool_calls: list[dict] | None = None,
        tool_call_id: str | None = None,
    ) -> None:
        if message is not None and isinstance(message, Message):
            self.messages.append(message)
        else:
            m = Message(role=role, content=content, tool_calls=tool_calls, tool_call_id=tool_call_id)
            self.messages.append(m)

    def clear(self) -> None:
        self.messages.clear()

    def get_messages(self) -> list[dict]:
        return [msg.json() for msg in self.messages]

    def truncate(self) -> None:
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def save(self, save_path: str):
        with open(save_path, "w") as f:
            for msg in self.messages:
                f.write(json.dumps(msg.json(exclude_none=True)) + "\n")
