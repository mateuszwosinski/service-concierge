from concierge.datatypes.chat_types import RoleMessage


class Memory:
    """Simple in-memory storage for conversation histories."""

    def __init__(self) -> None:
        self.store: dict[str, list[RoleMessage]] = {}

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
