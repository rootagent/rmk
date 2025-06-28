import json

from rmonkey.tools import Tool


class ToolAction:
    def __init__(self, tools: list[Tool] | None = None):
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}

    def execute(self, name: str, arguments: str, **kwargs) -> str:
        tool = self.tool_map.get(name, None)
        if not tool:
            return f"Tool {name} is not available."
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError:
            return f"Invalid arguments for tool {name}."

        try:
            return tool(**arguments)
        except Exception as e:
            return str(e)
