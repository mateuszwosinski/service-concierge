"""Demo script showing how to use the mock APIs."""

from concierge.external_systems import appointments_api, knowledge_api, orders_api


def demo_orders_api() -> None:
    """Demonstrate Orders API functionality."""
    print("\n=== ORDERS API DEMO ===\n")

    # Query order status
    print("1. Query order status:")
    order = orders_api.get_order("ORD-001")
    if order:
        print(f"   Order {order.order_id}: {order.status}")
        print(f"   Total: ${order.total_amount}")
        print(f"   Items: {', '.join(item.name for item in order.items)}")

    # Swap item in order
    print("\n2. Swap item in order:")
    result = orders_api.swap_item("ORD-004", "ITEM-006", "ITEM-NEW", "Updated Monitor")
    print(f"   {result['message']}")

    # Try to modify shipped order (should fail)
    print("\n3. Try to modify shipped order:")
    result = orders_api.swap_item("ORD-001", "ITEM-001", "ITEM-NEW", "Different Item")
    print(f"   {result['message']}")

    # Cancel order
    print("\n4. Cancel order:")
    result = orders_api.cancel_order("ORD-002")
    print(f"   {result['message']}")


def demo_appointments_api() -> None:
    """Demonstrate Appointments API functionality."""
    print("\n=== APPOINTMENTS API DEMO ===\n")

    # Query appointments by email
    print("1. Query appointments by email:")
    appointments = appointments_api.get_appointments_by_email("john.doe@example.com")
    print(f"   Found {len(appointments)} appointments for john.doe@example.com:")
    for apt in appointments:
        print(f"   - {apt.appointment_id}: {apt.date} at {apt.time} ({apt.service_type}) - {apt.status}")

    # Query appointments by phone
    print("\n2. Query appointments by phone:")
    appointments = appointments_api.get_appointments_by_phone("+1-555-0102")
    print(f"   Found {len(appointments)} appointments for +1-555-0102:")
    for apt in appointments:
        print(f"   - {apt.appointment_id}: {apt.date} at {apt.time} ({apt.service_type})")

    # Schedule new appointment
    print("\n3. Schedule new appointment:")
    result = appointments_api.schedule_appointment(
        email="new.user@example.com",
        phone="+1-555-9999",
        date="2025-12-20",
        time="15:00",
        service_type="Product Demo",
    )
    print(f"   {result['message']}")
    if result["success"] == "true":
        print(f"   Appointment ID: {result['appointment_id']}")

    # Reschedule appointment
    print("\n4. Reschedule appointment:")
    result = appointments_api.reschedule_appointment("APT-001", "2025-12-07", "13:00")
    print(f"   {result['message']}")

    # Cancel appointment
    print("\n5. Cancel appointment:")
    result = appointments_api.cancel_appointment("APT-005")
    print(f"   {result['message']}")


def demo_knowledge_api() -> None:
    """Demonstrate Knowledge/Products API functionality."""
    print("\n=== KNOWLEDGE API DEMO ===\n")

    # Search products
    print("1. Search products for 'wireless':")
    products = knowledge_api.search_products("wireless")
    print(f"   Found {len(products)} products:")
    for prod in products[:3]:  # Show top 3
        print(f"   - {prod.name}: ${prod.price} ({prod.category})")
        print(f"     In stock: {prod.in_stock}")

    # Get specific product
    print("\n2. Get specific product:")
    product = knowledge_api.get_product("PROD-002")
    if product is not None:
        print(f"   {product.name}: ${product.price}")
        print(f"   Description: {product.description}")
        print(f"   Features: {', '.join(product.features[:3])}")

    # Search policies
    print("\n3. Search policies for 'return':")
    policies = knowledge_api.search_policies("return")
    print(f"   Found {len(policies)} policy documents:")
    for policy in policies[:2]:  # Show top 2
        print(f"   - {policy.title} ({policy.category})")
        print(f"     {policy.content[:100]}...")

    # Get policies by category
    print("\n4. Get shipping policies:")
    policies = knowledge_api.get_policies_by_category("shipping")
    for policy in policies:
        print(f"   - {policy.title}")
        print(f"     {policy.content[:150]}...")

    # Get available products
    print("\n5. Get available products:")
    available = knowledge_api.get_available_products()
    print(f"   {len(available)} products in stock:")
    for product in available[:4]:  # Show first 4
        print(f"   - {product.name}: ${product.price}")


if __name__ == "__main__":
    demo_orders_api()
    demo_appointments_api()
    demo_knowledge_api()
    print("\n=== DEMO COMPLETE ===\n")
