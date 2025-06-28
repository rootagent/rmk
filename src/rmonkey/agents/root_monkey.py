from rmonkey.agents import Agent
from rmonkey.plan import Planning
from rmonkey.tools import TerminalBash, TextFileEditor, Think


class RootMonkey(Agent):
    def __init__(self, system_rules: str, session_id: str, verbose: bool = False, console=None, *args, **kwargs):
        super().__init__(
            name="RootMonkey",
            system="As an autonomous AI agent, I am known as Root Monkey (rmk).",
            system_rules=system_rules,
            tools=[
                Planning(),
                TextFileEditor(),
                TerminalBash(),
                Think(),
            ],
            session_id=session_id,
            verbose=verbose,
            console=console,
        )
        self.description = "Root Monkey, an autonomous AI Agent system."
