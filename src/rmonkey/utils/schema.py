from enum import Enum

from openai.types.chat import ChatCompletionMessageToolCall
from pydantic import BaseModel, Field


class Role(str, Enum):
    """LLM API message roles"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

    def __repr__(self) -> str:
        return str.__repr__(self.value)


class Message(BaseModel):
    id: str | None = None
    role: Role = Field(default=Role.USER)
    content: str | None = Field(default=None)
    tool_calls: list[ChatCompletionMessageToolCall] | None = Field(default=None)
    tool_call_id: str | None = Field(default=None)

    def json(self, **kwargs):  # type: ignore
        exclude_none = kwargs.pop("exclude_none", False)
        return self.model_dump(exclude_none=exclude_none)
