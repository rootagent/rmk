from typing import Any

from pydantic import BaseModel


class Tool(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any] | None = None

    def __call__(self, **kwargs) -> Any:
        return self.execute(**kwargs)

    def execute(self, **kwargs) -> str:
        """Execute the tool with provided parameters."""
        raise NotImplementedError("Tool subclasses must implement execute method")

    async def aexecute(self, **kwargs) -> str:
        """Execute the tool with provided parameters."""
        raise NotImplementedError("Tool subclasses must implement execute method")

    def schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
