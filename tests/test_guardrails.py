"""Tests for input guardrails."""

import pytest

from concierge.agent.guardrails import InputGuardrails, check_input_guardrails


class TestInputGuardrails:
    """Test the input guardrails functionality."""

    def test_allowed_product_queries(self):
        """Test that product-related queries are allowed."""
        allowed_queries = [
            "Show me winter jackets",
            "I need a new suit",
            "What colors are available for the merino sweater?",
            "Do you have leather bags in stock?",
            "I'm looking for a black dress",
            "What's the price of the cashmere coat?",
        ]

        for query in allowed_queries:
            result = check_input_guardrails(query)
            assert result.is_allowed, f"Query should be allowed: {query}"

    def test_allowed_order_queries(self):
        """Test that order-related queries are allowed."""
        allowed_queries = [
            "I want to cancel my order ORD-001",
            "Can I modify my order?",
            "What's the status of my order?",
            "I'd like to swap an item in my order",
            "When will my order be delivered?",
            "I need to return a product",
        ]

        for query in allowed_queries:
            result = check_input_guardrails(query)
            assert result.is_allowed, f"Query should be allowed: {query}"

    def test_allowed_appointment_queries(self):
        """Test that appointment-related queries are allowed."""
        allowed_queries = [
            "I'd like to schedule a fitting appointment",
            "Can I reschedule my styling session?",
            "Do you have any available appointments next week?",
            "I need to book a wardrobe consultation",
            "Cancel my appointment for tomorrow",
            "What time slots are available?",
        ]

        for query in allowed_queries:
            result = check_input_guardrails(query)
            assert result.is_allowed, f"Query should be allowed: {query}"

    def test_allowed_policy_queries(self):
        """Test that policy-related queries are allowed."""
        allowed_queries = [
            "What's your return policy?",
            "Do you offer a warranty?",
            "Tell me about your shipping options",
            "What are the VIP membership benefits?",
            "What's your privacy policy?",
        ]

        for query in allowed_queries:
            result = check_input_guardrails(query)
            assert result.is_allowed, f"Query should be allowed: {query}"

    def test_allowed_conversational_queries(self):
        """Test that natural conversational queries are allowed."""
        allowed_queries = [
            "Hi",
            "Hello",
            "Thank you",
            "Yes",
            "No",
            "Okay",
            "Sure",
        ]

        for query in allowed_queries:
            result = check_input_guardrails(query)
            assert result.is_allowed, f"Query should be allowed: {query}"

    def test_blocked_general_knowledge(self):
        """Test that general knowledge queries are blocked."""
        blocked_queries = [
            "What is the capital of France?",
            "Who is the president of the United States?",
            "Tell me about the history of World War 2",
            "When was the Declaration of Independence signed?",
        ]

        for query in blocked_queries:
            result = check_input_guardrails(query)
            assert not result.is_allowed, f"Query should be blocked: {query}"
            assert result.reason is not None

    def test_blocked_math(self):
        """Test that math queries are blocked."""
        blocked_queries = [
            "What is 2 + 2?",
            "Calculate 156 * 23",
            "Solve this math problem: 10 / 2",
        ]

        for query in blocked_queries:
            result = check_input_guardrails(query)
            assert not result.is_allowed, f"Query should be blocked: {query}"
            assert result.reason is not None

    def test_blocked_programming(self):
        """Test that programming queries are blocked."""
        blocked_queries = [
            "How do I write a Python function?",
            "Help me debug this JavaScript code",
            "What's the syntax for a for loop?",
        ]

        for query in blocked_queries:
            result = check_input_guardrails(query)
            assert not result.is_allowed, f"Query should be blocked: {query}"
            assert result.reason is not None

    def test_blocked_medical(self):
        """Test that medical queries are blocked."""
        blocked_queries = [
            "I have a headache, what medicine should I take?",
            "Diagnose my symptoms",
            "What treatment is best for diabetes?",
        ]

        for query in blocked_queries:
            result = check_input_guardrails(query)
            assert not result.is_allowed, f"Query should be blocked: {query}"
            assert result.reason is not None

    def test_blocked_legal(self):
        """Test that legal queries are blocked."""
        blocked_queries = [
            "Can I sue my landlord?",
            "I need legal advice about a contract",
            "How do I file a lawsuit?",
        ]

        for query in blocked_queries:
            result = check_input_guardrails(query)
            assert not result.is_allowed, f"Query should be blocked: {query}"
            assert result.reason is not None

    def test_blocked_unrelated_shopping(self):
        """Test that unrelated shopping queries are blocked."""
        blocked_queries = [
            "Where can I buy car insurance?",
            "I need a new laptop",
            "Recommend a good smartphone",
            "Find me the best grocery store",
        ]

        for query in blocked_queries:
            result = check_input_guardrails(query)
            assert not result.is_allowed, f"Query should be blocked: {query}"
            assert result.reason is not None

    def test_empty_query(self):
        """Test that empty queries are blocked."""
        result = check_input_guardrails("")
        assert not result.is_allowed
        assert result.reason == "Empty query"

    def test_edge_cases(self):
        """Test edge cases and borderline queries."""
        # Very short queries should be allowed (lenient)
        result = check_input_guardrails("help")
        assert result.is_allowed

        # Queries with mixed content (on-topic words) should be allowed
        result = check_input_guardrails("I need help finding a jacket for my trip")
        assert result.is_allowed

        # Long off-topic query should be blocked
        result = check_input_guardrails(
            "Tell me everything you know about quantum physics and how it relates to modern computing"
        )
        assert not result.is_allowed
