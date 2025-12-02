"""Demo script showing the Understanding module with tool calling."""

from dotenv import load_dotenv

load_dotenv()

from concierge.agent.understanding import Understanding  # noqa: E402


def demo_tool_calling() -> None:
    """Demonstrate the Understanding module with tool calling capabilities."""
    understanding = Understanding()

    print("\n=== UNDERSTANDING MODULE WITH TOOL CALLING DEMO ===\n")

    # Test 1: Search for products
    print("1. User: 'Show me merino wool products'")
    print("   Processing...")
    response = understanding.process("Show me merino wool products available in your store")
    print(f"   Response: {response}\n")

    # Test 2: Check order status
    print("2. User: 'What's the status of order ORD-001?'")
    print("   Processing...")
    response = understanding.process("What's the status of order ORD-001?")
    print(f"   Response: {response}\n")

    # Test 3: Look up appointments
    print("3. User: 'Show me appointments for john.doe@example.com'")
    print("   Processing...")
    response = understanding.process("Show me all appointments for john.doe@example.com")
    print(f"   Response: {response}\n")

    # Test 4: Search for policy information
    print("4. User: 'What is your return policy?'")
    print("   Processing...")
    response = understanding.process("What is your return policy?")
    print(f"   Response: {response}\n")

    # Test 5: Get available products
    print("5. User: 'What luxury items are currently in stock?'")
    print("   Processing...")
    response = understanding.process("What luxury items are currently in stock?")
    print(f"   Response: {response}\n")

    print("=== DEMO COMPLETE ===\n")


if __name__ == "__main__":
    demo_tool_calling()
