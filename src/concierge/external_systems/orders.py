"""Mock Orders API for managing order queries and modifications."""

import json
from datetime import datetime
from typing import Optional

from concierge.datatypes.general_types import OrderDetails, OrderItem
from concierge.paths import ORDERS_DATA_PATH


class OrdersAPI:
    """Mock API for order management operations."""

    def __init__(self) -> None:
        """Initialize the Orders API with mock data."""
        self._orders: dict[str, OrderDetails] = self._initialize_mock_orders()

    @staticmethod
    def _initialize_mock_orders() -> dict[str, OrderDetails]:
        """Load mock order data from JSON file."""
        data_path = ORDERS_DATA_PATH
        with data_path.open() as f:
            orders_data = json.load(f)

        orders = {}
        for order_id, order_dict in orders_data.items():
            # Convert items to OrderItem objects
            items = [OrderItem(**item) for item in order_dict["items"]]
            order_dict["items"] = items
            orders[order_id] = OrderDetails(**order_dict)

        return orders

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
