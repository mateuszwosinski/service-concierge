import re
from typing import Any, Union, get_args, get_origin


def _parse_docstring(docstring: str) -> tuple[str, dict[str, str]]:
    """Parse Google-style docstring to extract description and parameter descriptions.

    Args:
        docstring: The function docstring to parse

    Returns:
        Tuple of (main_description, param_descriptions_dict)
    """
    if not docstring:
        return "", {}

    # Split into lines and clean up
    lines = [line.strip() for line in docstring.split("\n")]

    # Extract main description (everything before Args:)
    description_lines = []
    param_descriptions = {}
    current_section = "description"
    current_param = None

    for line in lines:
        if line.startswith("Args:"):
            current_section = "args"
            continue
        if line.startswith("Returns:") or line.startswith("Raises:") or line.startswith("Business Logic:"):
            current_section = "other"
            continue

        if current_section == "description" and line:
            description_lines.append(line)
        elif current_section == "args":
            # Match parameter lines like "param_name: Description"
            param_match = re.match(r"(\w+):\s*(.+)", line)
            if param_match:
                current_param = param_match.group(1)
                param_descriptions[current_param] = param_match.group(2)
            elif current_param and line:
                # Continuation of previous parameter description
                param_descriptions[current_param] += " " + line

    description = " ".join(description_lines)
    return description, param_descriptions


def _python_type_to_json_schema(python_type: Any) -> dict[str, Any]:  # noqa: PLR0911
    """Convert Python type annotation to JSON schema type.

    Args:
        python_type: Python type annotation

    Returns:
        JSON schema type definition
    """
    # Handle Optional types
    origin = get_origin(python_type)
    if origin is type(None) or python_type is type(None):  # noqa: E721
        return {"type": "null"}

    # Handle Union types (including Optional)
    if origin is Union:
        args = get_args(python_type)
        # Filter out None type
        non_none_types = [arg for arg in args if arg is not type(None)]  # noqa: E721
        if len(non_none_types) == 1:
            return _python_type_to_json_schema(non_none_types[0])
        # For other unions, default to string
        return {"type": "string"}

    # Handle basic types
    if python_type is str or python_type == "str":
        return {"type": "string"}
    if python_type is int or python_type == "int":
        return {"type": "integer"}
    if python_type is float or python_type == "float":
        return {"type": "number"}
    if python_type is bool or python_type == "bool":
        return {"type": "boolean"}

    # Handle list types
    if origin is list:
        return {"type": "array"}

    # Handle dict types
    if origin is dict:
        return {"type": "object"}

    # Default to string for unknown types
    return {"type": "string"}
