"""Tests for mock APIs to demonstrate functionality."""

from concierge.external_systems.appointments import appointments_api
from concierge.external_systems.inventory import knowledge_api
from concierge.external_systems.orders import orders_api


def test_orders_api() -> None:
    """Test Orders API functionality."""
    # Get order status
    order = orders_api.get_order("ORD-001")
    assert order is not None
    assert order.order_id == "ORD-001"
    assert order.status == "shipped"

    # Swap item in pending order
    result = orders_api.swap_item("ORD-004", "ITEM-006", "ITEM-007", "New Monitor")
    assert result["success"] == "true"

    # Try to swap item in shipped order (should fail)
    result = orders_api.swap_item("ORD-001", "ITEM-001", "ITEM-008", "Other Headphones")
    assert result["success"] == "false"

    # Cancel order
    result = orders_api.cancel_order("ORD-004")
    assert result["success"] == "true"


def test_appointments_api() -> None:
    """Test Appointments API functionality."""
    # Get appointments by email
    appointments = appointments_api.get_appointments_by_email("john.doe@example.com")
    assert len(appointments) == 2
    assert all(apt.user_email == "john.doe@example.com" for apt in appointments)

    # Schedule new appointment
    result = appointments_api.schedule_appointment(
        email="test@example.com", phone="+1-555-9999", date="2025-12-15", time="14:00", service_type="Consultation"
    )
    assert result["success"] == "true"
    assert "appointment_id" in result

    # Reschedule appointment
    result = appointments_api.reschedule_appointment("APT-001", "2025-12-06", "11:00")
    assert result["success"] == "true"

    # Cancel appointment
    result = appointments_api.cancel_appointment("APT-005")
    assert result["success"] == "true"


def test_knowledge_api() -> None:
    """Test Knowledge/Products API functionality."""
    # Search products
    products = knowledge_api.search_products("wireless")
    assert len(products) > 0
    assert any("wireless" in p.name.lower() or "wireless" in p.description.lower() for p in products)

    # Get product by ID
    product = knowledge_api.get_product("PROD-001")
    assert product is not None
    assert product.name == "Wireless Headphones Pro"

    # Search policies
    policies = knowledge_api.search_policies("shipping")
    assert len(policies) > 0
    assert any("shipping" in p.title.lower() or "shipping" in p.category.lower() for p in policies)

    # Get available products
    available = knowledge_api.get_available_products()
    assert all(p.in_stock for p in available)

    # Get policies by category
    return_policies = knowledge_api.get_policies_by_category("returns")
    assert len(return_policies) > 0
    assert all(p.category == "returns" for p in return_policies)
