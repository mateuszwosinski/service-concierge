from concierge.datatypes.chat_types import RoleMessage
from concierge.datatypes.metrics_types import ConversationMetrics, GlobalMetrics, MessageMetrics


class Memory:
    """Simple in-memory storage for conversation histories."""

    def __init__(self) -> None:
        self.store: dict[str, list[RoleMessage]] = {}
        self.metrics: list[MessageMetrics] = []

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

    def add_metrics(self, metrics: MessageMetrics) -> None:
        """Add message metrics.

        Args:
            metrics (MessageMetrics): The metrics to add.
        """
        self.metrics.append(metrics)

    def get_conversation_metrics(self, conversation_id: str) -> ConversationMetrics:
        """Get aggregated metrics for a conversation.

        Args:
            conversation_id (str): The ID of the conversation.

        Returns:
            ConversationMetrics: Aggregated metrics for the conversation.
        """
        conversation_metrics = [m for m in self.metrics if m.conversation_id == conversation_id]

        if not conversation_metrics:
            return ConversationMetrics(
                conversation_id=conversation_id,
                total_messages=0,
                avg_latency_ms=0.0,
                total_tool_calls=0,
                tools_usage={},
                guardrail_blocks=0,
            )

        total_messages = len(conversation_metrics)
        avg_latency_ms = sum(m.latency_ms for m in conversation_metrics) / total_messages
        total_tool_calls = sum(len(m.tools_used) for m in conversation_metrics)
        guardrail_blocks = sum(1 for m in conversation_metrics if m.guardrail_blocked)

        tools_usage: dict[str, int] = {}
        for metric in conversation_metrics:
            for tool in metric.tools_used:
                tools_usage[tool] = tools_usage.get(tool, 0) + 1

        return ConversationMetrics(
            conversation_id=conversation_id,
            total_messages=total_messages,
            avg_latency_ms=avg_latency_ms,
            total_tool_calls=total_tool_calls,
            tools_usage=tools_usage,
            guardrail_blocks=guardrail_blocks,
        )

    def get_global_metrics(self) -> GlobalMetrics:
        """Get aggregated global metrics.

        Returns:
            GlobalMetrics: Aggregated metrics across all conversations.
        """
        if not self.metrics:
            return GlobalMetrics(
                total_conversations=0,
                total_messages=0,
                avg_latency_ms=0.0,
                total_tool_calls=0,
                tools_usage={},
                guardrail_blocks=0,
            )

        unique_conversations = len({m.conversation_id for m in self.metrics})
        total_messages = len(self.metrics)
        avg_latency_ms = sum(m.latency_ms for m in self.metrics) / total_messages
        total_tool_calls = sum(len(m.tools_used) for m in self.metrics)
        guardrail_blocks = sum(1 for m in self.metrics if m.guardrail_blocked)

        tools_usage: dict[str, int] = {}
        for metric in self.metrics:
            for tool in metric.tools_used:
                tools_usage[tool] = tools_usage.get(tool, 0) + 1

        return GlobalMetrics(
            total_conversations=unique_conversations,
            total_messages=total_messages,
            avg_latency_ms=avg_latency_ms,
            total_tool_calls=total_tool_calls,
            tools_usage=tools_usage,
            guardrail_blocks=guardrail_blocks,
        )
