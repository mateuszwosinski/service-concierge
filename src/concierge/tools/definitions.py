"""Tool definitions for OpenAI function calling with mock APIs."""

import inspect
from typing import Any, Callable

from concierge.external_systems import appointments_api, knowledge_api, orders_api, users_api

from .utils import _parse_docstring, _python_type_to_json_schema


def _generate_tool_definition(func: Callable[..., Any], name_prefix: str = "") -> dict[str, Any]:
    """Generate OpenAI tool definition from a function.

    Args:
        func: The function to generate a tool definition for
        name_prefix: Optional prefix for the tool name

    Returns:
        OpenAI tool definition dictionary
    """
    func_name = f"{name_prefix}{func.__name__}" if name_prefix else func.__name__
    docstring = inspect.getdoc(func) or ""
    description, param_descriptions = _parse_docstring(docstring)

    # Get function signature
    sig = inspect.signature(func)

    # Build parameters schema
    properties = {}
    required = []

    for param_name, param in sig.parameters.items():
        # Skip 'self' parameter
        if param_name == "self":
            continue

        # Get parameter type
        param_type = param.annotation if param.annotation != inspect.Parameter.empty else str
        json_type = _python_type_to_json_schema(param_type)

        # Get parameter description from docstring
        param_desc = param_descriptions.get(param_name, f"The {param_name} parameter")

        properties[param_name] = {
            **json_type,
            "description": param_desc,
        }

        # Check if parameter is required (no default value)
        if param.default == inspect.Parameter.empty:
            required.append(param_name)

    return {
        "type": "function",
        "function": {
            "name": func_name,
            "description": description or f"Call the {func_name} function",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        },
    }


def _get_api_methods(api_instance: Any) -> list[tuple[str, Callable[..., Any]]]:
    """Get all public methods from an API instance.

    Args:
        api_instance: The API instance to inspect

    Returns:
        List of (method_name, method_callable) tuples
    """
    methods = []
    for name in dir(api_instance):
        # Skip private methods and special methods
        if name.startswith("_"):
            continue

        attr = getattr(api_instance, name)
        if callable(attr):
            methods.append((name, attr))

    return methods


# Dynamically generate tool definitions from mock APIs
def _generate_all_tool_definitions() -> list[dict[str, Any]]:
    """Generate all tool definitions from the mock APIs.

    Returns:
        List of OpenAI tool definitions
    """
    tool_definitions = []

    # Generate tools for each API
    for api_instance in [orders_api, appointments_api, knowledge_api, users_api]:
        methods = _get_api_methods(api_instance)
        for _, method in methods:
            tool_def = _generate_tool_definition(method)
            tool_definitions.append(tool_def)

    return tool_definitions


# Generate tool definitions on module import
TOOL_DEFINITIONS = _generate_all_tool_definitions()


# Dynamically build tool function mapping from API instances
def _build_tool_functions() -> dict[str, Callable[..., Any]]:
    """Build mapping of tool names to functions from API instances.

    Returns:
        Dictionary mapping tool names to callable functions
    """
    tool_functions = {}

    for api_instance in [orders_api, appointments_api, knowledge_api, users_api]:
        methods = _get_api_methods(api_instance)
        for method_name, method in methods:
            tool_functions[method_name] = method

    return tool_functions


# Tool function mapping
TOOL_FUNCTIONS: dict[str, Callable[..., Any]] = _build_tool_functions()
