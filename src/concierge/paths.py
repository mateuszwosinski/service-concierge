from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent.absolute()
PROMPTS_PATH = PROJECT_PATH / "prompts"

AGENT_PROMPT_PATH = PROMPTS_PATH / "agent_prompt.j2"
