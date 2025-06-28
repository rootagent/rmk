from ._base import Tool


class AskHuman(Tool):
    name: str = "ask_human"
    description: str = "Ask human for help and get a response from human."
    parameters: dict = {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question to ask the human.",
            }
        },
        "required": ["question"],
    }

    def execute(self, **kwargs) -> str:
        question = kwargs.get("question", "")
        human_input = input(f"rMonkey: {question}\nYou: ").strip()
        if not human_input:
            return "No response provided by human."
        return human_input
