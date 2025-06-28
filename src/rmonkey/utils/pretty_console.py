from rich.console import Console
from rich.style import Style

roles_color = {
    "error": "#e32636",
    "user": "#00ffff",
    "system": "#bd33a4",
    "assistant": "#ead9c4",
    "tool": "#318ce7",
    "hint": "#fdee00",
}


class PrettyConsole:
    console = Console()

    def print(self, content: str, key: str = "hint"):
        color = roles_color.get(key)
        self.console.print(f"[{key}]: {content}", style=Style(bgcolor=color))
