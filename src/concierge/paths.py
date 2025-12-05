from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent.absolute()
PROMPTS_PATH = PROJECT_PATH / "prompts"

AGENT_PROMPT_PATH = PROMPTS_PATH / "agent_prompt.j2"

APPOINTMENTS_DATA_PATH = PROJECT_PATH / "data" / "appointments.json"
PRODUCTS_DATA_PATH = PROJECT_PATH / "data" / "products.json"
POLICIES_DATA_PATH = PROJECT_PATH / "data" / "policies.json"
ORDERS_DATA_PATH = PROJECT_PATH / "data" / "orders.json"
USERS_DATA_PATH = PROJECT_PATH / "data" / "users.json"
