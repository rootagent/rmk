import logging
from typing import Any

from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI, OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage

from rmonkey.utils.schema import Message, Role

logger = logging.getLogger(__name__)


class OpenAIHandler:
    base_url: str = None
    api_version: str = None
    api_key: str = None
    model: str = "gpt-4.1"
    max_tokens: int = 1024 * 8
    temperature: float = 0.7

    client: AzureOpenAI | OpenAI = None
    aclient: AsyncAzureOpenAI | AsyncOpenAI = None

    def __init__(
        self, base_url: str, api_version: str, api_key: str, model: str, max_tokens: int, temperature: float, **kwargs
    ):
        self.base_url = base_url
        self.api_version = api_version
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

        if api_version and "azure.com" in base_url:
            self.aclient = AsyncAzureOpenAI(
                azure_endpoint=base_url,
                api_version=api_version,
                api_key=api_key,
            )
            self.client = AzureOpenAI(
                azure_endpoint=base_url,
                api_version=api_version,
                api_key=api_key,
            )
        else:
            self.aclient = AsyncOpenAI(
                api_key=api_key,
            )
            self.client = OpenAI(
                api_key=api_key,
            )

    def call(
        self,
        messages: list[dict],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
        stream: bool = False,
        top_p: float | None = None,
    ) -> Message:
        if stream and tools:
            logger.warning("Streaming is not supported for tool calls. Disabling streaming.")
            stream = False

        _config = {
            "model": model if model else self.model,
            "messages": messages,
            "max_tokens": max_tokens if max_tokens else self.max_tokens,
            "temperature": temperature if temperature else self.temperature,
            "top_p": top_p if top_p else 0.95,
        }
        if tools:
            _config["tools"] = tools

        if not stream:
            response: ChatCompletion = self.client.chat.completions.create(**_config)
            if not response.choices or not response.choices[0].message:
                raise ValueError(f"Invalid response from LLM {_config['model']}")
            _message: ChatCompletionMessage = response.choices[0].message
            response_content = _message.content
            tool_calls = _message.tool_calls
            return Message(role=Role.ASSISTANT, content=response_content, tool_calls=tool_calls)
        else:
            _config["stream"] = True
            response = self.client.chat.completions.create(**_config)
            chunks = []

            for chunk in response:
                chunk_text = chunk.choices[0].delta.content or ""
                chunks.append(chunk_text)
                print(chunk_text, end="", flush=True)
            response_content = "".join(chunks)
            return Message(role=Role.ASSISTANT, content=response_content)

    async def acall(
        self,
        messages: list[dict],
        tools: list[dict[str, Any]] | None = None,
        config: dict[str, Any] | None = None,
    ) -> Message:
        stream = config.get("stream", False)
        if stream and tools:
            logger.warning("Streaming is not supported for tool calls. Disabling streaming.")
            stream = False

        _config = {
            "model": config.get("model", "gpt-4.1"),
            "messages": messages,
            "max_tokens": config.get("max_tokens", 1024 * 8),
            "temperature": config.get("temperature", 0.7),
            "top_p": config.get("top_p", 0.95),
        }
        if tools:
            _config["tools"] = tools

        if not stream:
            response: ChatCompletion = await self.aclient.chat.completions.create(**_config)
            if not response.choices or not response.choices[0].message:
                raise ValueError(f"Invalid response from LLM {_config['model']}")
            _message: ChatCompletionMessage = response.choices[0].message
            response_content = _message.content
            tool_calls = _message.tool_calls
            return Message(role=Role.ASSISTANT, content=response_content, tool_calls=tool_calls)
        else:
            _config["stream"] = True
            chunks = []
            async for chunk in self.aclient.chat.completions.create(**_config):
                chunk_text = chunk.choices[0].delta.content or ""
                chunks.append(chunk_text)
                print(chunk_text, end="", flush=True)
            response_content = "".join(chunks)
        return Message(role=Role.ASSISTANT, content=response_content)


def mock_openai_call(
    messages: list[dict],
    tools: list[dict[str, Any]] | None = None,
    **kwargs,
) -> Message:
    from openai.types.chat import ChatCompletionMessageToolCall
    from openai.types.chat.chat_completion_message_tool_call import Function

    mock_tool_calls = None
    if tools:
        mock_tool_calls = [
            ChatCompletionMessageToolCall(
                id="call_xxx",
                type="function",
                function=Function(
                    name="get_weather",
                    arguments='{"location":"Paris, France"}',
                ),
            )
        ]
    return Message(
        role=Role.ASSISTANT,
        content="This is a mock response.",
        tool_calls=mock_tool_calls,
    )
