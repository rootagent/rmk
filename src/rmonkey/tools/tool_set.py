from rmonkey.tools._base import Tool


class Toolset:
    def __init__(self, tools: list[Tool] | None = None):
        self.tools = tools if tools is not None else []

    def add_tool(self, tool: Tool) -> None:
        self.tools.append(tool)

    def get_tool(self, name: str) -> Tool | None:
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None

    def schema(self) -> list[dict]:
        return [tool.schema() for tool in self.tools]

    def save(self, filepath: str):
        import json

        with open(filepath, "w") as f:
            json.dump(self.schema(), f, indent=2)
