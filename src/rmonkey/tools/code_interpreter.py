from rmonkey.tools._base import Tool


class CodeInterpreter(Tool):
    name: str = "code_interpreter"
    description: str = "Executes a Python code snippet and returns the print statement output."
    parameters: dict = {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The Python script to execute.",
            },
        },
        "required": ["code"],
    }

    def execute(self, code: str, language: str = "python") -> str:
        assert language == "python", "Only Python code is supported."
        try:
            local_scope = {}
            exec(code, {}, local_scope)
            return str(local_scope)
        except Exception as e:
            return f"Error executing code: {str(e)}"
