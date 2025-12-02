from jinja2 import Environment, FileSystemLoader
from litellm import completion

from concierge.paths import AGENT_PROMPT_PATH
from concierge.settings import settings


class Understanding:
    """Class to handle understanding of user input using a language model."""

    def __init__(self) -> None:
        self._model = settings.AGENT_MODEL
        self._api_key = settings.OPENAI_API_KEY

        self._understanding_prompt_template = Environment(
            loader=FileSystemLoader(searchpath="/"), autoescape=True
        ).get_template(str(AGENT_PROMPT_PATH))

    def process(self, input_text: str) -> str:
        """Process the input text to extract understanding using the language model."""
        prompt = self._understanding_prompt_template.render(input_text=input_text)
        prompt = "\n".join(line.strip() for line in prompt.split("\n") if line.strip())

        response = completion(
            model=self._model,
            messages=[{"content": prompt, "role": "user"}],
            # response_format=response_format,
        )

        return response.choices[0].message.content
