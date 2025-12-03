from loguru import logger
from openai.types.chat import ChatCompletionMessageParam

from concierge.agent.understanding import Understanding
from concierge.datatypes.chat_types import Role, RoleMessage
from concierge.memory.internal import Memory


class Agent:
    """Main agent class that integrates memory and understanding components."""

    def __init__(self) -> None:
        self.memory = Memory()
        self.understanding = Understanding()

    def process_message(self, conversation_id: str, message: str) -> str:
        """Process an incoming message and return a response.

        Args:
            conversation_id (str): The ID of the conversation.
            message (str): The incoming user message.

        Returns:
            str: The agent's response.
        """
        logger.info(f"Received message for conversation {conversation_id}: {message}")

        # Get conversation history BEFORE adding current message
        conversation = self.memory.get_conversation(conversation_id)
        previous_messages = self._get_messages_from_conversation(conversation)

        # Add current user message to memory
        self.memory.add_message(conversation_id, RoleMessage(role=Role.USER, message=message))

        # Process with Understanding agent
        answer = self.understanding.process(message, previous_messages)

        self.memory.add_message(conversation_id, RoleMessage(role=Role.ASSISTANT, message=answer))
        return answer

    @staticmethod
    def _get_messages_from_conversation(conversation: list[RoleMessage]) -> list[ChatCompletionMessageParam]:
        return [{"role": msg.role.value, "content": msg.message} for msg in conversation]
