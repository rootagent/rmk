from rmonkey.agents import Agent
from rmonkey.plan import Planning
from rmonkey.tools import CodeInterpreter, TerminalBash, TextFileEditor, Think


class SWEAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="SWEAgent",
            system="You are an autonomous AI software engineer.",
            tools=[
                Planning(),
                TextFileEditor(),
                TerminalBash(),
                CodeInterpreter(),
                Think(),
            ],
        )
        self.description = "an autonomous AI Software Engineer agent."
