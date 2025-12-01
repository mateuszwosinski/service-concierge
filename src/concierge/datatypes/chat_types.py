from enum import StrEnum
from pydantic import BaseModel

class ChatRequest(BaseModel):
    conversation_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


class RoleMessage(BaseModel):
    role: Role
    message: str