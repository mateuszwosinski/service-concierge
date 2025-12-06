"""Rule-based input guardrails for filtering off-topic queries."""

import re
from dataclasses import dataclass

from loguru import logger


@dataclass
class GuardrailResult:
    """Result of guardrail check."""

    is_allowed: bool
    reason: str | None = None


class InputGuardrails:
    """Fast, rule-based guardrails to filter queries not related to the agent's scope."""

    # Topics the agent CAN handle
    ALLOWED_TOPICS = {
        # Product-related
        "product",
        "products",
        "item",
        "items",
        "clothing",
        "apparel",
        "jacket",
        "coat",
        "sweater",
        "shirt",
        "pants",
        "trousers",
        "dress",
        "suit",
        "bag",
        "accessory",
        "accessories",
        "leather",
        "wool",
        "cashmere",
        "merino",
        "collection",
        "catalog",
        "inventory",
        "stock",
        "size",
        "color",
        "style",
        "fashion",
        "wear",
        "outfit",
        "wardrobe",
        # Order-related
        "email",
        "order",
        "orders",
        "purchase",
        "buy",
        "bought",
        "ordered",
        "cart",
        "checkout",
        "payment",
        "shipping",
        "delivery",
        "cancel",
        "modify",
        "change",
        "update",
        "swap",
        "replace",
        "return",
        "refund",
        "exchange",
        "like",
        # Appointment-related
        "appointment",
        "appointments",
        "schedule",
        "reschedule",
        "booking",
        "book",
        "meeting",
        "session",
        "consultation",
        "fitting",
        "tailoring",
        "styling",
        "stylist",
        "alteration",
        "alterations",
        "custom",
        "personalized",
        # Policy-related
        "policy",
        "policies",
        "warranty",
        "guarantee",
        "terms",
        "privacy",
        "vip",
        "membership",
        "loyalty",
        "program",
        # General service terms
        "help",
        "assist",
        "show",
        "find",
        "search",
        "look",
        "looking",
        "need",
        "want",
        "interested",
        "available",
        "recommend",
        "recommendation",
        "suggest",
        "status",
        "check",
        "view",
        "browse",
        "price",
        "cost",
        "expensive",
        "affordable",
        "luxury",
        "premium",
        "quality",
        "brand",
        "account",
        "profile",
        "preferences",
    }

    # Patterns that clearly indicate OFF-TOPIC queries
    BLOCKED_PATTERNS = [
        # General knowledge/trivia
        (
            r"\b(what|who|when|where|why|how)\s+(is|are|was|were|did)\s+(the\s+)?(capital|president|population|history|war|battle)",
            re.IGNORECASE,
        ),
        (
            r"\b(tell me about|explain|describe)\s+(the\s+)?(history|geography|politics|science|biology|chemistry|physics|quantum|astronomy|geology|anthropology|sociology|psychology)",
            re.IGNORECASE,
        ),
        # Math/calculations
        (r"\b(calculate|compute|solve|what is|what's)\s+\d+\s*[\+\-\*/]\s*\d+", re.IGNORECASE),
        (r"\bmath(ematics)?\s+(problem|equation|formula)", re.IGNORECASE),
        # Programming/technical
        (r"\b(python|javascript|java|code|programming|function|algorithm|debug)", re.IGNORECASE),
        (r"\b(how to (write|program|code)|syntax error)", re.IGNORECASE),
        # Medical/health
        (
            r"\b(medical|doctor|disease|symptom|diagnosis|treatment|medicine|drug|prescription|health issue)",
            re.IGNORECASE,
        ),
        # Legal
        (r"\b(legal advice|lawyer|attorney|lawsuit|contract|sue|litigation)", re.IGNORECASE),
        # News/current events
        (r"\b(latest news|current events|breaking news|headlines)", re.IGNORECASE),
        # Unrelated shopping
        (r"\b(car|auto|vehicle|insurance|real estate|house|property|mortgage|loan)", re.IGNORECASE),
        (r"\b(grocery|groceries|food delivery|restaurant|recipe)", re.IGNORECASE),
        (r"\b(electronics|computer|laptop|phone|smartphone|tablet|gaming)", re.IGNORECASE),
        # Entertainment (unless related to events/styling)
        (r"\b(movie|film|tv show|series|netflix|music|song|album|concert)\s+(recommendation|review)", re.IGNORECASE),
        # Personal advice
        (r"\b(relationship|dating|breakup|marriage|divorce|personal problem)", re.IGNORECASE),
        # Travel (unless related to appointments)
        (r"\b(flight|hotel|vacation|travel package|tourism|tourist)", re.IGNORECASE),
        # Education
        (r"\b(homework|essay|thesis|dissertation|study|quiz)", re.IGNORECASE),
    ]

    @classmethod
    def check_query(cls, query: str) -> GuardrailResult:  # noqa: PLR0911
        """
        Check if a query is within the agent's scope.

        Args:
            query: The user's input query

        Returns:
            GuardrailResult indicating if query is allowed and reason if not
        """
        if not query or not query.strip():
            return GuardrailResult(is_allowed=False, reason="Empty query")

        query_lower = query.lower().strip()

        # Check against blocked patterns first
        for pattern, _ in cls.BLOCKED_PATTERNS:
            if re.search(pattern, query_lower):
                logger.warning(f"Query blocked by guardrails: {pattern}")
                return GuardrailResult(is_allowed=False, reason="Query topic is outside our service scope")

        # Extract words from query
        words = re.findall(r"\b\w+\b", query_lower)

        # If query is very short (1-2 words), be more lenient
        if len(words) <= 2:
            return GuardrailResult(is_allowed=True)

        # Check if at least one allowed topic word is present
        # This ensures the query has some relevance to our domain
        has_allowed_topic = any(word in cls.ALLOWED_TOPICS for word in words)

        if has_allowed_topic:
            return GuardrailResult(is_allowed=True)

        # If query is longer and has no allowed topics, it might be off-topic
        # But we want to avoid false positives, so check if it's a natural conversational query
        conversational_starters = {"hi", "hello", "hey", "thanks", "thank", "yes", "no", "ok", "okay", "sure"}
        if any(word in conversational_starters for word in words[:3]):  # Check first 3 words
            return GuardrailResult(is_allowed=True)

        # If no allowed topics found in a longer query, it's likely off-topic
        if len(words) > 5:
            logger.warning("Query blocked by guardrails: No allowed topics found in a longer query")
            return GuardrailResult(
                is_allowed=False,
                reason="Query doesn't appear to be about products, orders, appointments, or our services",
            )

        # Default: allow (to avoid false positives)
        return GuardrailResult(is_allowed=True)


def check_input_guardrails(query: str) -> GuardrailResult:
    """
    Check if a query passes input guardrails.

    Args:
        query: User's input query

    Returns:
        GuardrailResult with is_allowed flag and optional reason
    """
    return InputGuardrails.check_query(query)
