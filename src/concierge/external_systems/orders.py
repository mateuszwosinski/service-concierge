"""Mock Orders API for managing order queries and modifications."""

from datetime import datetime
from typing import Optional

from concierge.datatypes.general_types import OrderDetails, OrderItem


class OrdersAPI:
    """Mock API for order management operations."""

    def __init__(self) -> None:
        """Initialize the Orders API with mock data."""
        self._orders: dict[str, OrderDetails] = self._initialize_mock_orders()

    @staticmethod
    def _initialize_mock_orders() -> dict[str, OrderDetails]:
        """Create mock order data."""
        return {
            "ORD-001": OrderDetails(
                order_id="ORD-001",
                user_id="user_123",
                items=[
                    OrderItem(product_id="PROD-002", name="Technical Cashmere Sweater", quantity=1, price=485.00),
                    OrderItem(product_id="PROD-007", name="Merino Wool Base Layer Set", quantity=2, price=245.00),
                ],
                total_amount=975.00,
                status="shipped",
                created_at="2025-11-25T10:30:00",
                updated_at="2025-11-26T14:20:00",
            ),
            "ORD-002": OrderDetails(
                order_id="ORD-002",
                user_id="user_456",
                items=[
                    OrderItem(product_id="PROD-001", name="Merino Wool Performance Jacket", quantity=1, price=895.00),
                ],
                total_amount=895.00,
                status="processing",
                created_at="2025-11-28T09:15:00",
                updated_at="2025-11-28T09:15:00",
            ),
            "ORD-003": OrderDetails(
                order_id="ORD-003",
                user_id="user_789",
                items=[
                    OrderItem(product_id="PROD-004", name="Performance Stretch Trousers", quantity=2, price=395.00),
                    OrderItem(product_id="PROD-008", name="Premium Leather Chelsea Boots", quantity=1, price=725.00),
                ],
                total_amount=1515.00,
                status="delivered",
                created_at="2025-11-20T16:45:00",
                updated_at="2025-11-24T11:30:00",
            ),
            "ORD-004": OrderDetails(
                order_id="ORD-004",
                user_id="user_123",
                items=[
                    OrderItem(product_id="PROD-006", name="Swiss Automatic Watch", quantity=1, price=2850.00),
                ],
                total_amount=2850.00,
                status="pending",
                created_at="2025-11-30T13:20:00",
                updated_at="2025-11-30T13:20:00",
            ),
            "ORD-005": OrderDetails(
                order_id="ORD-005",
                user_id="user_456",
                items=[
                    OrderItem(product_id="PROD-005", name="Lightweight Down Vest", quantity=1, price=325.00),
                    OrderItem(product_id="PROD-003", name="Heritage Leather Weekender Bag", quantity=1, price=1250.00),
                ],
                total_amount=1575.00,
                status="pending",
                created_at="2025-12-01T14:45:00",
                updated_at="2025-12-01T14:45:00",
            ),
        }

    def get_order(self, order_id: str) -> Optional[OrderDetails]:
        """
        Retrieve order details by order_id.

        Args:
            order_id: The unique order identifier

        Returns:
            OrderDetails if found, None otherwise
        """
        return self._orders.get(order_id)

    def get_order_status(self, order_id: str) -> Optional[str]:
        """
        Get the status of an order.

        Args:
            order_id: The unique order identifier

        Returns:
            Order status string if found, None otherwise
        """
        order = self._orders.get(order_id)
        return order.status if order else None

    def make_order(self, user_id: str, items: list[OrderItem]) -> dict[str, str | OrderDetails]:
        """
        Create a new order for a user with the specified items. Each OrderItem must include product_id (format: PROD-XXX), name, quantity, and price. Use search_products first to find products and get accurate product details (product_id, name, price) before creating an order.

        Args:
            user_id: The unique user identifier
            items: List of OrderItem objects, each containing product_id (e.g., "PROD-001"), name, quantity, and price

        Returns:
            Dictionary with success status, message, and order details if successful
        """
        if not items:
            return {"success": "false", "message": "Cannot create order with no items"}

        # Convert dicts to OrderItem objects if necessary (when called via OpenAI tool calling)
        order_items: list[OrderItem] = []
        for item in items:
            if isinstance(item, dict):
                order_items.append(OrderItem(**item))
            else:
                order_items.append(item)

        # Generate new order ID
        existing_order_ids = [int(oid.split("-")[1]) for oid in self._orders]
        next_order_num = max(existing_order_ids) + 1 if existing_order_ids else 1
        new_order_id = f"ORD-{next_order_num:03d}"

        # Calculate total amount
        total_amount = sum(item.quantity * item.price for item in order_items)

        # Create timestamp
        now = datetime.now().isoformat()

        # Create the order
        new_order = OrderDetails(
            order_id=new_order_id,
            user_id=user_id,
            items=order_items,
            total_amount=total_amount,
            status="pending",
            created_at=now,
            updated_at=now,
        )

        # Store the order
        self._orders[new_order_id] = new_order

        return {
            "success": "true",
            "message": f"Order {new_order_id} created successfully",
            "order": new_order.model_dump(),
        }

    def update_order(self, order_id: str, items: list[OrderItem]) -> dict[str, str | OrderDetails]:
        """
        Update an existing order with new items. Replaces all items in the order and recalculates the total. Use this to add, remove, or modify items in an order. Only works for orders that are still modifiable (pending or processing status).

        Business Logic:
        - Order must exist
        - Order status must be 'pending' or 'processing' (not shipped/delivered/cancelled)
        - New items list cannot be empty

        Args:
            order_id: The unique order identifier
            items: List of OrderItem objects representing the complete updated order

        Returns:
            Dictionary with success status, message, and updated order details if successful
        """
        order = self._orders.get(order_id)

        if not order:
            return {"success": "false", "message": f"Order {order_id} not found"}

        if order.status not in ["pending", "processing"]:
            return {
                "success": "false",
                "message": f"Cannot modify order with status '{order.status}'. "
                "Only pending or processing orders can be modified.",
            }

        if not items:
            return {"success": "false", "message": "Cannot update order with no items"}

        # Convert dicts to OrderItem objects if necessary (when called via OpenAI tool calling)
        order_items: list[OrderItem] = []
        for item in items:
            if isinstance(item, dict):
                order_items.append(OrderItem(**item))
            else:
                order_items.append(item)

        # Update order items
        order.items = order_items

        # Recalculate total amount
        order.total_amount = sum(item.quantity * item.price for item in order_items)

        # Update timestamp
        order.updated_at = datetime.now().isoformat()

        return {
            "success": "true",
            "message": f"Order {order_id} updated successfully",
            "order": order.model_dump(),
        }

    def swap_item(self, order_id: str, old_product_id: str, new_product_id: str, new_item_name: str) -> dict[str, str]:
        """
        Swap an item in an order with another item.

        Business Logic:
        - Order must exist
        - Order status must be 'pending' or 'processing' (not shipped/delivered/cancelled)
        - Old item must exist in the order

        Args:
            order_id: The unique order identifier
            old_product_id: ID of item to replace
            new_product_id: ID of new item
            new_item_name: Name of new item

        Returns:
            Dictionary with success status and message
        """
        order = self._orders.get(order_id)

        if not order:
            return {"success": "false", "message": f"Order {order_id} not found"}

        if order.status not in ["pending", "processing"]:
            return {
                "success": "false",
                "message": f"Cannot modify order with status '{order.status}'. "
                "Only pending or processing orders can be modified.",
            }

        # Find the item to swap
        item_index = None
        for idx, item in enumerate(order.items):
            if item.product_id == old_product_id:
                item_index = idx
                break

        if item_index is None:
            return {"success": "false", "message": f"Item {old_product_id} not found in order {order_id}"}

        # Keep the same quantity and price for simplicity
        old_item = order.items[item_index]
        order.items[item_index] = OrderItem(
            product_id=new_product_id, name=new_item_name, quantity=old_item.quantity, price=old_item.price
        )

        order.updated_at = datetime.now().isoformat()

        return {
            "success": "true",
            "message": f"Successfully swapped {old_item.name} with {new_item_name} in order {order_id}",
        }

    def cancel_order(self, order_id: str) -> dict[str, str]:
        """
        Cancel an order.

        Business Logic:
        - Order must exist
        - Order status must be 'pending' or 'processing' (not shipped/delivered)

        Args:
            order_id: The unique order identifier

        Returns:
            Dictionary with success status and message
        """
        order = self._orders.get(order_id)

        if not order:
            return {"success": "false", "message": f"Order {order_id} not found"}

        if order.status in ["shipped", "delivered"]:
            return {
                "success": "false",
                "message": f"Cannot cancel order with status '{order.status}'. Please contact support for returns.",
            }

        if order.status == "cancelled":
            return {"success": "false", "message": f"Order {order_id} is already cancelled"}

        order.status = "cancelled"
        order.updated_at = datetime.now().isoformat()

        return {"success": "true", "message": f"Order {order_id} has been cancelled"}


# Global instance
orders_api = OrdersAPI()
