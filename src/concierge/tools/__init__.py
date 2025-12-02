import json
from typing import Any

from .definitions import TOOL_FUNCTIONS


def execute_tool(tool_name: str, tool_arguments: dict[str, Any]) -> str:
    """Execute a tool function and return the result as a JSON string.

    Args:
        tool_name: Name of the tool to execute
        tool_arguments: Arguments to pass to the tool function

    Returns:
        JSON string with the tool execution result
    """
    if tool_name not in TOOL_FUNCTIONS:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})

    try:
        func = TOOL_FUNCTIONS[tool_name]
        result = func(**tool_arguments)

        # Convert result to JSON-serializable format
        if hasattr(result, "model_dump"):  # Pydantic models
            return json.dumps(result.model_dump())
        if isinstance(result, list) and result and hasattr(result[0], "model_dump"):  # List of Pydantic models
            return json.dumps([item.model_dump() for item in result])
        return json.dumps(result)

    except Exception as e:
        return json.dumps({"error": str(e)})
