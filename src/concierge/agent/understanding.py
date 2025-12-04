import json
from time import sleep

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from concierge.paths import AGENT_PROMPT_PATH
from concierge.settings import settings
from concierge.tools import execute_tool
from concierge.tools.definitions import TOOL_DEFINITIONS


class Understanding:
    """Class to handle understanding of user input using a language model with tool calling."""

    def __init__(self) -> None:
        self._model = settings.AGENT_MODEL
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

        self._understanding_prompt_template = Environment(
            loader=FileSystemLoader(searchpath="/"), autoescape=True
        ).get_template(str(AGENT_PROMPT_PATH))

    def process(
        self,
        latest_user_message: str,
        previous_messages: list[ChatCompletionMessageParam] | None = None,
        max_iterations: int = 10,
    ) -> str:
        """Process the input text using the language model with tool calling support.

        Args:
            latest_user_message: User message to process
            previous_messages: List of previous messages in the conversation
            max_iterations: Maximum number of tool calling iterations
        Returns:
            Final response from the language model after executing any necessary tools
        """
        prompt = self._understanding_prompt_template.render(
            latest_user_message=latest_user_message, previous_messages=previous_messages if previous_messages else []
        )
        prompt = "\n".join(line.strip() for line in prompt.split("\n") if line.strip())

        messages: list[ChatCompletionMessageParam] = [{"content": prompt, "role": "user"}]

        iteration = 0
        while iteration < max_iterations:
            logger.info(f"Tool calling iteration {iteration + 1}")

            response = self._call_llm(messages)

            assistant_message = response.choices[0].message
            logger.info(f"Assistant message: {assistant_message.content}")

            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": assistant_message.tool_calls,
                }
            )

            if not assistant_message.tool_calls:
                return assistant_message.content or ""

            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_arguments = json.loads(tool_call.function.arguments)

                logger.info(f"Executing tool: {tool_name} with arguments: {tool_arguments}")

                tool_result = execute_tool(tool_name, tool_arguments)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    }
                )
                logger.info(f"Tool result for {tool_name}: {tool_result}")
            iteration += 1

        return messages[-1]["content"] or ""

    def _call_llm(self, messages: list[ChatCompletionMessageParam]) -> ChatCompletion:
        for i in range(3):
            try:
                return self._client.chat.completions.create(
                    model=self._model,
                    messages=messages,
                    tools=TOOL_DEFINITIONS,
                    tool_choice="auto",
                )
            except Exception as e:
                logger.warning(f"Error calling LLM: {e}")
                sleep(2**i)
        raise RuntimeError("Failed to call LLM after multiple attempts")
