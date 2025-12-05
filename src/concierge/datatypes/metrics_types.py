from datetime import datetime

from pydantic import BaseModel


class MessageMetrics(BaseModel):
    """Metrics for a single message processing event."""

    timestamp: datetime
    conversation_id: str
    latency_ms: float
    tools_used: list[str]
    num_iterations: int
    guardrail_blocked: bool


class ConversationMetrics(BaseModel):
    """Aggregated metrics for a conversation."""

    conversation_id: str
    total_messages: int
    avg_latency_ms: float
    total_tool_calls: int
    tools_usage: dict[str, int]
    guardrail_blocks: int


class GlobalMetrics(BaseModel):
    """Aggregated global metrics across all conversations."""

    total_conversations: int
    total_messages: int
    avg_latency_ms: float
    total_tool_calls: int
    tools_usage: dict[str, int]
    guardrail_blocks: int
