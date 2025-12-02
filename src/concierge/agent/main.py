from concierge.agent.understanding import Understanding
from concierge.datatypes.chat_types import Role, RoleMessage
from concierge.memory.internal import Memory


class Agent:
    """Main agent class that integrates memory and understanding components."""

    def __init__(self) -> None:
        self.memory = Memory(init_with_mock_data=True)
        self.understanding = Understanding()

    def process_message(self, conversation_id: str, message: str) -> str:
        """Process an incoming message and return a response.

        Args:
            conversation_id (str): The ID of the conversation.
            message (str): The incoming user message.

        Returns:
            str: The agent's response.
        """
        self.memory.add_message(conversation_id, RoleMessage(role=Role.USER, message=message))

        answer = self.understanding.process(message)

        self.memory.add_message(conversation_id, RoleMessage(role=Role.ASSISTANT, message=answer))
        return answer
