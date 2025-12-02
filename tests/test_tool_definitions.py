"""Tests for dynamic tool definition generation."""

import json

from concierge.tools import execute_tool
from concierge.tools.definitions import TOOL_DEFINITIONS, TOOL_FUNCTIONS


class TestToolDefinitions:
    """Test suite for tool definitions and execution."""

    def test_tool_definitions_generated(self) -> None:
        """Test that tool definitions are generated dynamically."""
        assert len(TOOL_DEFINITIONS) > 0
        assert isinstance(TOOL_DEFINITIONS, list)

    def test_tool_definitions_structure(self) -> None:
        """Test that each tool definition has the correct structure."""
        for tool_def in TOOL_DEFINITIONS:
            assert "type" in tool_def
            assert tool_def["type"] == "function"
            assert "function" in tool_def

            function = tool_def["function"]
            assert "name" in function
            assert "description" in function
            assert "parameters" in function

            parameters = function["parameters"]
            assert parameters["type"] == "object"
            assert "properties" in parameters
            assert "required" in parameters
            assert isinstance(parameters["properties"], dict)
            assert isinstance(parameters["required"], list)

    def test_tool_functions_mapping_exists(self) -> None:
        """Test that tool functions mapping is created."""
        assert len(TOOL_FUNCTIONS) > 0
        assert isinstance(TOOL_FUNCTIONS, dict)

    def test_tool_definitions_match_functions(self) -> None:
        """Test that all tool definitions have corresponding functions."""
        tool_names_in_definitions = {tool["function"]["name"] for tool in TOOL_DEFINITIONS}
        tool_names_in_functions = set(TOOL_FUNCTIONS.keys())

        assert tool_names_in_definitions == tool_names_in_functions

    def test_orders_api_tools_included(self) -> None:
        """Test that Orders API tools are included."""
        tool_names = {tool["function"]["name"] for tool in TOOL_DEFINITIONS}

        expected_orders_tools = {
            "get_order",
            "get_order_status",
            "swap_item",
            "cancel_order",
            "update_order_status",
        }

        assert expected_orders_tools.issubset(tool_names)

    def test_appointments_api_tools_included(self) -> None:
        """Test that Appointments API tools are included."""
        tool_names = {tool["function"]["name"] for tool in TOOL_DEFINITIONS}

        expected_appointments_tools = {
            "get_appointment",
            "get_appointments_by_email",
            "get_appointments_by_phone",
            "schedule_appointment",
            "reschedule_appointment",
            "cancel_appointment",
            "confirm_appointment",
        }

        assert expected_appointments_tools.issubset(tool_names)

    def test_knowledge_api_tools_included(self) -> None:
        """Test that Knowledge API tools are included."""
        tool_names = {tool["function"]["name"] for tool in TOOL_DEFINITIONS}

        expected_knowledge_tools = {
            "search_products",
            "get_product",
            "get_products_by_category",
            "get_available_products",
            "search_policies",
            "get_policy",
            "get_policies_by_category",
        }

        assert expected_knowledge_tools.issubset(tool_names)

    def test_tool_has_description_from_docstring(self) -> None:
        """Test that tool descriptions are extracted from docstrings."""
        # Find the get_order tool
        get_order_tool = next(tool for tool in TOOL_DEFINITIONS if tool["function"]["name"] == "get_order")

        description = get_order_tool["function"]["description"]
        assert len(description) > 0
        assert "order" in description.lower()

    def test_tool_has_parameter_descriptions(self) -> None:
        """Test that parameter descriptions are extracted from docstrings."""
        # Find a tool with parameters
        swap_item_tool = next(tool for tool in TOOL_DEFINITIONS if tool["function"]["name"] == "swap_item")

        properties = swap_item_tool["function"]["parameters"]["properties"]
        assert "order_id" in properties
        assert "description" in properties["order_id"]
        assert len(properties["order_id"]["description"]) > 0

    def test_tool_required_parameters_detected(self) -> None:
        """Test that required parameters are correctly identified."""
        # get_order has only order_id parameter which is required
        get_order_tool = next(tool for tool in TOOL_DEFINITIONS if tool["function"]["name"] == "get_order")

        required = get_order_tool["function"]["parameters"]["required"]
        assert "order_id" in required

    def test_execute_tool_success(self) -> None:
        """Test executing a tool successfully."""
        result_json = execute_tool("get_order", {"order_id": "ORD-001"})
        result = json.loads(result_json)

        assert "order_id" in result
        assert result["order_id"] == "ORD-001"

    def test_execute_tool_with_list_result(self) -> None:
        """Test executing a tool that returns a list."""
        result_json = execute_tool("get_appointments_by_email", {"email": "john.doe@example.com"})
        result = json.loads(result_json)

        assert isinstance(result, list)
        assert len(result) > 0

    def test_execute_tool_not_found(self) -> None:
        """Test executing a non-existent tool."""
        result_json = execute_tool("nonexistent_tool", {})
        result = json.loads(result_json)

        assert "error" in result
        assert "unknown tool" in result["error"].lower()

    def test_execute_tool_with_exception(self) -> None:
        """Test executing a tool with invalid arguments."""
        # Missing required parameter
        result_json = execute_tool("get_order", {})
        result = json.loads(result_json)

        assert "error" in result

    def test_execute_tool_returns_json_serializable(self) -> None:
        """Test that execute_tool always returns valid JSON."""
        # Test with various tools
        tool_calls = [
            ("get_order", {"order_id": "ORD-001"}),
            ("search_products", {"query": "jacket"}),
            ("get_available_products", {}),
        ]

        for tool_name, args in tool_calls:
            result_json = execute_tool(tool_name, args)
            # Should not raise an exception
            json.loads(result_json)

    def test_tool_with_optional_parameter(self) -> None:
        """Test tool definition for function with optional parameters."""
        # schedule_appointment has all required parameters
        schedule_tool = next(tool for tool in TOOL_DEFINITIONS if tool["function"]["name"] == "schedule_appointment")

        required = schedule_tool["function"]["parameters"]["required"]
        properties = schedule_tool["function"]["parameters"]["properties"]

        # All parameters should be present
        assert len(properties) > 0
        # Required should match parameters without defaults
        assert len(required) > 0

    def test_tool_parameter_types(self) -> None:
        """Test that parameter types are correctly converted to JSON schema."""
        get_order_tool = next(tool for tool in TOOL_DEFINITIONS if tool["function"]["name"] == "get_order")

        properties = get_order_tool["function"]["parameters"]["properties"]
        # order_id should be a string type
        assert properties["order_id"]["type"] == "string"
