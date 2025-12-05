from datetime import datetime, timezone

from loguru import logger
from openai.types.chat import ChatCompletionMessageParam

from concierge.agent.guardrails import check_input_guardrails
from concierge.agent.understanding import Understanding
from concierge.datatypes.chat_types import Role, RoleMessage
from concierge.datatypes.metrics_types import MessageMetrics
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
        start_time = datetime.now(timezone.utc)
        guardrail_blocked = False

        try:
            logger.info(f"Received message for conversation {conversation_id}: {message}")

            guardrail_result = check_input_guardrails(message)
            if not guardrail_result.is_allowed:
                guardrail_blocked = True
                response = self._handle_guardrail_violation(conversation_id, message)

                # Record metrics for guardrail violation
                end_time = datetime.now(timezone.utc)
                latency_ms = (end_time - start_time).total_seconds() * 1000
                metrics = MessageMetrics(
                    timestamp=start_time,
                    conversation_id=conversation_id,
                    latency_ms=latency_ms,
                    tools_used=[],
                    num_iterations=0,
                    guardrail_blocked=True,
                )
                self.memory.add_metrics(metrics)

                return response

            conversation = self.memory.get_conversation(conversation_id)
            previous_messages = self._get_messages_from_conversation(conversation)

            self.memory.add_message(conversation_id, RoleMessage(role=Role.USER, message=message))

            result = self.understanding.process(message, previous_messages)

            self.memory.add_message(conversation_id, RoleMessage(role=Role.ASSISTANT, message=result.response))

            # Record metrics
            end_time = datetime.now(timezone.utc)
            latency_ms = (end_time - start_time).total_seconds() * 1000
            metrics = MessageMetrics(
                timestamp=start_time,
                conversation_id=conversation_id,
                latency_ms=latency_ms,
                tools_used=result.tools_used,
                num_iterations=result.num_iterations,
                guardrail_blocked=False,
            )
            self.memory.add_metrics(metrics)

            return result.response
        except Exception as e:
            logger.error(f"Error processing message: {e}")

            # Record metrics for error case
            end_time = datetime.now(timezone.utc)
            latency_ms = (end_time - start_time).total_seconds() * 1000
            metrics = MessageMetrics(
                timestamp=start_time,
                conversation_id=conversation_id,
                latency_ms=latency_ms,
                tools_used=[],
                num_iterations=0,
                guardrail_blocked=guardrail_blocked,
            )
            self.memory.add_metrics(metrics)

            return "I'm sorry, but I encountered an error while processing your request. Please try again later."

    def _handle_guardrail_violation(self, conversation_id: str, message: str) -> str:
        response = (
            "I apologize, but I'm a specialized concierge for our luxury brand, "
            "focused on assisting with products, orders, appointments, and services. "
            "Your question appears to be outside my area of expertise. "
            "Is there anything related to our product catalog, your orders, or scheduling appointments that I can help you with?"
        )
        self.memory.add_message(conversation_id, RoleMessage(role=Role.USER, message=message))
        self.memory.add_message(conversation_id, RoleMessage(role=Role.ASSISTANT, message=response))
        return response

    @staticmethod
    def _get_messages_from_conversation(conversation: list[RoleMessage]) -> list[ChatCompletionMessageParam]:
        return [{"role": msg.role.value, "content": msg.message} for msg in conversation]
