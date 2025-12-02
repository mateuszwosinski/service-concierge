"""Tests for the Orders API."""

from concierge.external_systems import orders_api


class TestOrdersAPI:
    """Test suite for Orders API functionality."""

    def test_get_order_success(self) -> None:
        """Test retrieving an existing order."""
        order = orders_api.get_order("ORD-001")

        assert order is not None
        assert order.order_id == "ORD-001"
        assert order.status == "shipped"
        assert order.total_amount == 975.00
        assert len(order.items) == 2

    def test_get_order_not_found(self) -> None:
        """Test retrieving a non-existent order."""
        order = orders_api.get_order("ORD-999")
        assert order is None

    def test_get_order_status_success(self) -> None:
        """Test getting order status."""
        status = orders_api.get_order_status("ORD-002")
        assert status == "processing"

    def test_get_order_status_not_found(self) -> None:
        """Test getting status of non-existent order."""
        status = orders_api.get_order_status("ORD-999")
        assert status is None

    def test_swap_item_success(self) -> None:
        """Test swapping an item in a pending order."""
        result = orders_api.swap_item("ORD-004", "PROD-006", "PROD-001", "Merino Wool Performance Jacket")

        assert result["success"] == "true"
        assert "swapped" in result["message"].lower()

    def test_swap_item_shipped_order_fails(self) -> None:
        """Test that swapping items in a shipped order fails."""
        result = orders_api.swap_item("ORD-001", "PROD-002", "PROD-005", "Lightweight Down Vest")

        assert result["success"] == "false"
        assert "cannot modify" in result["message"].lower()

    def test_swap_item_order_not_found(self) -> None:
        """Test swapping item in non-existent order."""
        result = orders_api.swap_item("ORD-999", "PROD-001", "PROD-002", "New Item")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()

    def test_swap_item_item_not_found(self) -> None:
        """Test swapping non-existent item in order."""
        result = orders_api.swap_item("ORD-004", "PROD-999", "PROD-001", "New Item")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()

    def test_cancel_order_success(self) -> None:
        """Test canceling a pending order."""
        # First get the order to verify it exists
        order = orders_api.get_order("ORD-005")
        assert order is not None
        assert order.status == "pending"

        # Cancel it
        result = orders_api.cancel_order("ORD-005")

        assert result["success"] == "true"
        assert "cancelled" in result["message"].lower()

        # Verify status changed
        order = orders_api.get_order("ORD-005")
        assert order is not None
        assert order.status == "cancelled"

    def test_cancel_order_shipped_fails(self) -> None:
        """Test that canceling a shipped order fails."""
        result = orders_api.cancel_order("ORD-003")

        assert result["success"] == "false"
        assert "cannot cancel" in result["message"].lower()

    def test_cancel_order_not_found(self) -> None:
        """Test canceling non-existent order."""
        result = orders_api.cancel_order("ORD-999")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()

    def test_update_order_status_success(self) -> None:
        """Test updating order status."""
        result = orders_api.update_order_status("ORD-002", "shipped")

        assert result["success"] == "true"
        assert "updated" in result["message"].lower()

        # Verify status changed
        order = orders_api.get_order("ORD-002")
        assert order is not None
        assert order.status == "shipped"

    def test_update_order_status_invalid(self) -> None:
        """Test updating order status with invalid status."""
        result = orders_api.update_order_status("ORD-001", "invalid_status")

        assert result["success"] == "false"
        assert "invalid status" in result["message"].lower()

    def test_update_order_status_not_found(self) -> None:
        """Test updating status of non-existent order."""
        result = orders_api.update_order_status("ORD-999", "shipped")

        assert result["success"] == "false"
        assert "not found" in result["message"].lower()
