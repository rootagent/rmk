import re
from pathlib import Path

from rmonkey.tools import Tool

_description = """
This planning tool helps you view, create, manage, and break down highly complex tasks into manageable sub-tasks, making intricate problem-solving more efficient.
**Only employ this tool when you encounter a task that is exceptionally difficult and complex**
""".strip()  # noqa: E501


def parse_diff_blocks(diff: str) -> list:
    pattern = r"<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE"
    matches = re.findall(pattern, diff, re.DOTALL)
    blocks = []
    for s, r in matches:
        blocks.append((s, r))
    return blocks


class Planning(Tool):
    name: str = "planning"
    description: str = _description

    parameters: dict = {
        "type": "object",
        "properties": {
            "operation": {
                "description": "The operation to perform.",
                "enum": [
                    "view",
                    "create",
                    "update",
                    "decompose",
                ],
                "type": "string",
            },
            "path": {
                "description": "The absolute file path for storing the plan.",
                "type": "string",
            },
            "content": {
                "description": "The Markdown-formatted overall plan to achieve the goal. Required for `create`.",
                "type": "string",
            },
            "diff_content": {
                "description": (
                    "To update the current plan in the `path`, "
                    "provide the diff content as SEARCH/REPLACE blocks. Required for `update`."
                ),
                "type": "string",
            },
            "subtasks": {
                "description": "The list of tasks or steps to be performed. "
                "Subtasks will be appended to the plan. Required for `decompose`.",
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["command", "path"],
        "additionalProperties": False,
    }

    def execute(self, **kwargs) -> str:
        # valid parameters
        # operation: str, path: str, content: str = None, diff_content: str = None, subtasks: str = None
        operation = kwargs.get("operation")
        path = kwargs.get("path")
        content = kwargs.get("content")
        diff_content = kwargs.get("diff_content")
        subtasks = kwargs.get("subtasks")

        if not operation:
            return f"{self.name}: `operation` is required."
        if not path:
            return f"{self.name}: `path` is required."
        _path = Path(path)
        if not _path.exists():
            return f"{self.name}: File not found: {path}"

        if operation == "view":
            plan_content = Path(path).read_text()
            return plan_content
        elif operation == "create":
            if content is None:
                return f"{self.name}: `content` is need for the `create`."
            Path(path).write_text(content)
            return "created plan."
        elif operation == "update":
            if diff_content is None:
                return f"{self.name}: `diff_content` is need for the `update`."
            try:
                file_content = _path.read_text(encoding="utf-8")
                blocks = parse_diff_blocks(diff_content)
                for old_str, new_str in blocks:
                    file_content = file_content.replace(old_str, new_str)
                _path.write_text(file_content)
                return "updated plan."
            except Exception as e:
                return f"{self.name}: Error updating plan: {e}"
        elif operation == "decompose":
            if subtasks is None:
                return f"{self.name}: `subtasks` is need for the `decompose`."
            subtasks_str = "\n".join([f"[ ] Task-{i}\n{s}" for i, s in enumerate(subtasks, start=1)])
            with open(path, "a") as f:
                f.write("\n" + subtasks_str)
            return "subtasks is added to the plan."
        return f"{self.name}: {operation} is unsupported."
