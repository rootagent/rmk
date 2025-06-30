import re
from pathlib import Path

from ._base import Tool

_description = """
Text file tool for viewing, creating and editing.

* view will return the content of a file, optionally within a specified line range.
* create will create a new file with the specified content.
* edit will apply diff edits to an existing file.

Note: The diff format is a series of SEARCH/REPLACE blocks, every block must use this format:
1. The start of search block: <<<<<<< SEARCH
2. A contiguous chunk of lines to search for in the existing file
3. The dividing line: =======
4. The lines to replace into the source file
5. The end of replace block: >>>>>>> REPLACE
""".strip()  # noqa: E501


def parse_diff_blocks(diff: str) -> list:
    pattern = r"<<<<<<< SEARCH\n(.*?)\n=======\n(.*?)\n>>>>>>> REPLACE"
    matches = re.findall(pattern, diff, re.DOTALL)
    blocks = []
    for s, r in matches:
        blocks.append((s, r))
    return blocks


class TextFileEditor(Tool):
    name: str = "text_file_editor"
    description: str = _description
    parameters: dict = {
        "type": "object",
        "properties": {
            "operation": {
                "description": "File operation to perform.",
                "type": "string",
                "enum": ["view", "create", "edit"],
            },
            "path": {
                "description": "Absolute file path.",
                "type": "string",
            },
            "content": {
                "description": "Plain text content. Required for `create`.",
                "type": "string",
            },
            "diff": {
                "description": "Diff content (a series of SEARCH/REPLACE blocks). Required for `edit`.",
                "type": "string",
            },
            "view_range": {
                # `sed -n 'start_line,end_linep' file.txt`
                "description": "Line range to view (start and end line numbers). Optional for `view`.",
                "type": "array",
                "items": {"type": "integer"},
            },
            "line_number": {
                "description": "If True, line numbers will be displayed for each line. Optional for 'view'.",
                "type": "boolean",
                "default": False,
            }
        },
        "required": ["operation", "path"],
    }

    def execute(self, **kwargs) -> str:
        operation = kwargs.get("operation")
        path = kwargs.get("path")

        if operation == "view":
            view_range = kwargs.get("view_range")
            return self.view(path, view_range)
        elif operation == "create":
            content = kwargs.get("content")
            line_number = kwargs.get("line_number", False)
            return self.create(path, content, line_number)
        elif operation == "edit":
            diff = kwargs.get("diff")
            return self.edit(path, diff)
        else:
            return f"{self.name}: {operation} is unsupported."

    def view(self, path: str, view_range: list[int] = None, line_number: bool = False) -> str:
        _path = Path(path)
        if not _path.exists():
            return f"{self.name}: File not found: {path}"
        if view_range and (len(view_range) != 2 or not all(isinstance(i, int) for i in view_range)):
            return f"{self.name}: Invalid `view_range`: {view_range}."
        try:
            file_content = _path.read_text(encoding="utf-8")
            _lines = file_content.splitlines()
            if not _lines:
                return ""
            
            if line_number:
                max_line_num = len(_lines)
                width = len(str(max_line_num))
                lines = [f"{i:>{width}} {line}" for i, line in enumerate(_lines, start=1)]
            else:
                lines = _lines
            if not view_range:
                return "\n".join(lines)
            else:
                start, end = view_range
                start = int(start)
                end = int(end)
                if start < 1 or start > end:
                    return f"{self.name}: Invalid `view_range`: {view_range}."
                return "\n".join(lines[start - 1 : end])
        except Exception as e:
            return f"{self.name}: Error reading file: {e}"

    def create(self, path: str, content: str) -> str:
        _path = Path(path)
        if _path.exists():
            return f"{self.name}: File already exists: {path}"
        try:
            _path.write_text(content, encoding="utf-8")
            return f"created: {path}"
        except Exception as e:
            return f"{self.name}: Error creating file: {e}"

    def edit(self, path: str, diff: str) -> str:
        _path = Path(path)
        if not _path.exists():
            return f"{self.name}: File not found: {path}"
        try:
            file_content = _path.read_text(encoding="utf-8")
            blocks = parse_diff_blocks(diff)
            for old_str, new_str in blocks:
                file_content = file_content.replace(old_str, new_str)

            _path.write_text(file_content)
            return "edited the file."
        except Exception as e:
            return f"{self.name}: Error editing file: {e}"
