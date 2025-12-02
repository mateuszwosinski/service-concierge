from concierge.datatypes.chat_types import RoleMessage


class Memory:
    """Simple in-memory storage for conversation histories."""

    def __init__(self, init_with_mock_data: bool = False):
        self.store: dict[str, list[RoleMessage]] = {}
        if init_with_mock_data:
            self.store = {
                "conversation_1": [
                    RoleMessage(role="user", message="Hello!"),
                    RoleMessage(role="assistant", message="Hi there! How can I help you today?"),
                ],
                "conversation_2": [
                    RoleMessage(role="user", message="What's the weather like?"),
                    RoleMessage(role="assistant", message="It's sunny and warm today."),
                ],
            }

    def get_conversation(self, conversation_id: str) -> list[RoleMessage]:
        """Retrieve the conversation history for a given conversation ID.

        Args:
            conversation_id (str): The ID of the conversation.

        Returns:
            list[RoleMessage]: The list of messages in the conversation.
        """
        return self.store.get(conversation_id, [])

    def add_message(self, conversation_id: str, message: RoleMessage) -> None:
        """Add a message to the conversation history.

        Args:
            conversation_id (str): The ID of the conversation.
            message (RoleMessage): The message to add.
        """
        if conversation_id not in self.store:
            self.store[conversation_id] = []
        self.store[conversation_id].append(message)
