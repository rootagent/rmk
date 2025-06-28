from ._base import Tool


class Think(Tool):
    name: str = "think"
    description: str = "Used for self-think about something."
    parameters: dict = {
        "type": "object",
        "properties": {
            "thought": {
                "type": "string",
                "description": "Thinking and summary.",
            }
        },
        "required": ["thought"],
    }

    def execute(self, thought: str) -> str:
        return "Thinking completed."
