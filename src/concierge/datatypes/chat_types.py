from enum import StrEnum

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Represents a request to the chat system."""

    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    """Represents a response from the chat system."""

    response: str


class Role(StrEnum):
    """Represents the role of a message sender."""

    USER = "user"
    ASSISTANT = "assistant"


class RoleMessage(BaseModel):
    """Represents a message with an associated role."""

    role: Role
    message: str
