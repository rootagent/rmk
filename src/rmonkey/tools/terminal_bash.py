import subprocess

from ._base import Tool


class TerminalBash(Tool):
    name: str = "bash"
    description: str = "Execute a command in the terminal and return the output."
    parameters: dict = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Command to execute in the bash shell.",
            },
        },
        "required": ["command"],
    }

    def execute(self, **kwargs) -> str:
        command = kwargs.get("command", "")
        if not command:
            return "No command provided."

        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout.strip() or "Command executed successfully with no output."
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr.strip()}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
