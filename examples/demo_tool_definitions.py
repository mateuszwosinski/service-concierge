"""Demo script to show dynamically generated tool definitions."""

import json

from concierge.tools.definitions import TOOL_DEFINITIONS, TOOL_FUNCTIONS


def demo_tool_definitions() -> None:
    """Show the dynamically generated tool definitions."""
    print("\n=== DYNAMICALLY GENERATED TOOL DEFINITIONS ===\n")

    print(f"Total tools generated: {len(TOOL_DEFINITIONS)}\n")

    # Show a few examples
    print("Example tool definitions:\n")
    for i, tool in enumerate(TOOL_DEFINITIONS[:3], 1):
        print(f"{i}. {tool['function']['name']}")
        print(f"   Description: {tool['function']['description']}")
        print(f"   Parameters: {list(tool['function']['parameters']['properties'].keys())}")
        print(f"   Required: {tool['function']['parameters']['required']}\n")

    print("\n=== TOOL FUNCTION MAPPING ===\n")
    print(f"Total functions mapped: {len(TOOL_FUNCTIONS)}\n")
    print("Available tool functions:")
    for i, tool_name in enumerate(sorted(TOOL_FUNCTIONS.keys()), 1):
        print(f"{i:2d}. {tool_name}")

    # Show full definition of one tool as JSON
    print("\n=== FULL DEFINITION EXAMPLE ===\n")
    print("get_order tool definition:")
    for tool in TOOL_DEFINITIONS:
        if tool["function"]["name"] == "get_order":
            print(json.dumps(tool, indent=2))
            break


if __name__ == "__main__":
    demo_tool_definitions()
