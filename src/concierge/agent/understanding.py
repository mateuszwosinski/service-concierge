import json

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

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

        # Initialize conversation with user input
        messages: list[ChatCompletionMessageParam] = [{"content": prompt, "role": "user"}]

        iteration = 0
        while iteration < max_iterations:
            logger.info(f"Tool calling iteration {iteration + 1}")

            # Call the model with tools
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message
            logger.info(f"Assistant message: {assistant_message.content}")

            # Add assistant's response to messages
            messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": assistant_message.tool_calls,
                }
            )

            # Check if the model wants to call tools
            if not assistant_message.tool_calls:
                # No tool calls, return the final response
                return assistant_message.content or ""

            # Execute each tool call
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_arguments = json.loads(tool_call.function.arguments)

                logger.info(f"Executing tool: {tool_name} with arguments: {tool_arguments}")

                # Execute the tool
                tool_result = execute_tool(tool_name, tool_arguments)

                # Add tool result to messages
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result,
                    }
                )
                logger.info(f"Tool result for {tool_name}: {tool_result}")
            iteration += 1

        # If we've reached max iterations, return the last assistant message
        return messages[-1]["content"] or ""
