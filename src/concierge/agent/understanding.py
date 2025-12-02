import json

from jinja2 import Environment, FileSystemLoader
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

    def process(self, input_text: str, max_iterations: int = 10) -> str:
        """Process the input text using the language model with tool calling support.

        Args:
            input_text: User input to process
            max_iterations: Maximum number of tool calling iterations
        Returns:
            Final response from the language model after executing any necessary tools
        """
        prompt = self._understanding_prompt_template.render(input_text=input_text)
        prompt = "\n".join(line.strip() for line in prompt.split("\n") if line.strip())

        # Initialize conversation with user input
        messages: list[ChatCompletionMessageParam] = [{"content": prompt, "role": "user"}]

        iteration = 0
        while iteration < max_iterations:
            # Call the model with tools
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message

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

            iteration += 1

        # If we've reached max iterations, return the last assistant message
        return "Maximum tool calling iterations reached. Please try simplifying your request."
