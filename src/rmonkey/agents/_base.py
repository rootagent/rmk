import os
from contextlib import ExitStack
from pathlib import Path

from rmonkey.action import ToolAction
from rmonkey.llm import OpenAIHandler
from rmonkey.memory import Memory
from rmonkey.tools import Tool, Toolset
from rmonkey.utils.pretty_console import PrettyConsole
from rmonkey.utils.schema import Message, Role
from rmonkey.utils.util import generate_session_id


class Agent:
    # attributes
    name: str = "BaseAgent"
    description: str = "This is a base agent that does nothing."

    # https://lilianweng.github.io/posts/2023-06-23-agent/
    # agent key components: LLM, Memory, Tools, Planning, Action

    llm_handler: OpenAIHandler = None
    system: str = None
    system_rules: str = None

    memory: Memory = None
    tools: Toolset = None
    action: ToolAction = None
    planning: str = None

    # runtime settings
    session_id: str | None = None
    max_turns: int = 30
    run_step: int = 0
    run_state = None

    def __init__(
        self,
        name: str,
        system: str = None,
        tools: list[Tool] | None = None,
        provider: str = "openai",
        model: str = "gpt-4.1",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        session_id: str | None = None,
        verbose: bool = False,
        console: PrettyConsole = None,
        **kwargs,
    ):
        self.name = name
        if system is not None:
            self.system = system
        self.system_rules = kwargs.get("system_rules")
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        if tools:
            self.tools = Toolset(tools=tools)
            self.action = ToolAction(tools=tools)

        self.init_llm_handler(provider)

        self.session_id = session_id if session_id else generate_session_id()
        self.memory = Memory(id=self.session_id)
        if self.system:
            system_content = self.system
            if self.system_rules:
                system_content = f"{system_content}\n\n<system>\n{self.system_rules}\n</system>"
            self.memory.add_message(role=Role.SYSTEM, content=system_content)
        self.verbose = verbose
        self.console = console

    @classmethod
    def create(cls, **kwargs) -> "Agent":
        return cls(**kwargs)

    def init_llm_handler(self, provider: str = "openai"):
        if provider == "openai":
            self.llm_handler = OpenAIHandler(
                base_url=os.getenv("BASE_URL", None),
                api_version=os.getenv("API_VERSION", None),
                api_key=os.getenv("OPENAI_API_KEY", None),
                model=os.getenv("OPENAI_MODEL", self.model),
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _llm_with_tool(self, prompt: str) -> Message:
        """process a prompt and handle tool calls in a loop"""

        self.memory.add_message(role=Role.USER, content=prompt)
        if self.verbose:
            self.console.print(prompt, Role.USER)
        while True:
            result: Message = self.llm_handler.call(
                self.memory.get_messages(),
                self.tools.schema() if self.tools else None,
            )
            self.memory.add_message(result)
            if result.tool_calls:
                if self.verbose and result.content:
                    self.console.print(result.content, result.role)
                for tool_call in result.tool_calls:
                    if self.verbose:
                        self.console.print(tool_call, result.role)
                        input("Press Enter to continue with the tool call...")
                    name = tool_call.function.name
                    arguments = tool_call.function.arguments
                    tool_call_output = self.action.execute(name=name, arguments=arguments)
                    self.memory.add_message(role=Role.TOOL, content=tool_call_output, tool_call_id=tool_call.id)
                    if self.verbose:
                        self.console.print(tool_call_output, Role.TOOL)
            else:
                if self.verbose:
                    self.console.print(result.content, result.role)
                return result

    def run(self, prompt: str) -> str:
        agent_result = None

        with ExitStack() as stack:
            try:
                step_response = self._llm_with_tool(prompt)
                agent_result = step_response.content
            except Exception as e:
                print(f"Agent Sys Error: {e}")
        return agent_result

    def save(self, save_dir: str) -> str:
        if not Path(save_dir).exists():
            Path(save_dir).mkdir(parents=True)
        save_file = Path(save_dir) / f"{self.session_id}.jsonl"
        self.memory.save(save_file)
        return str(save_file)
