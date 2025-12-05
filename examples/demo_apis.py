"""Demo script showing how to use the mock APIs."""

from concierge.external_systems import appointments_api, knowledge_api, orders_api, users_api


def demo_orders_api() -> None:
    """Demonstrate Orders API functionality."""
    print("\n=== ORDERS API DEMO ===\n")

    # Query order status
    print("1. Query luxury order status:")
    order = orders_api.get_order("ORD-001")
    if order:
        print(f"   Order {order.order_id}: {order.status}")
        print(f"   Total: ${order.total_amount:,.2f}")
        print(f"   Items: {', '.join(item.name for item in order.items)}")

    # Swap item in order
    print("\n2. Swap item in pending order:")
    result = orders_api.swap_item("ORD-004", "PROD-006", "PROD-001", "Merino Wool Performance Jacket")
    print(f"   {result['message']}")

    # Try to modify shipped order (should fail)
    print("\n3. Try to modify shipped order (should fail):")
    result = orders_api.swap_item("ORD-001", "PROD-002", "PROD-005", "Lightweight Down Vest")
    print(f"   {result['message']}")

    # Cancel order
    print("\n4. Cancel pending order:")
    result = orders_api.cancel_order("ORD-005")
    print(f"   {result['message']}")


def demo_appointments_api() -> None:
    """Demonstrate Appointments API functionality."""
    print("\n=== APPOINTMENTS API DEMO ===\n")

    # Query appointments by email
    print("1. Query styling appointments by email:")
    appointments = appointments_api.get_appointments_by_email("john.doe@example.com")
    print(f"   Found {len(appointments)} appointments for john.doe@example.com:")
    for apt in appointments:
        print(f"   - {apt.appointment_id}: {apt.date} at {apt.time} ({apt.service_type}) - {apt.status}")

    # Query appointments by phone
    print("\n2. Query fitting appointments by phone:")
    appointments = appointments_api.get_appointments_by_phone("+1-555-0102")
    print(f"   Found {len(appointments)} appointments for +1-555-0102:")
    for apt in appointments:
        print(f"   - {apt.appointment_id}: {apt.date} at {apt.time} ({apt.service_type})")

    # Schedule new appointment
    print("\n3. Schedule new VIP styling session:")
    result = appointments_api.schedule_appointment(
        user_id="user_999",
        email="new.client@example.com",
        phone="+1-555-9999",
        date="2025-12-20",
        time="15:00",
        service_type="Personal Styling Session",
    )
    print(f"   {result['message']}")
    if result["success"] == "true":
        print(f"   Appointment ID: {result['appointment_id']}")

    # Reschedule appointment
    print("\n4. Reschedule styling appointment:")
    result = appointments_api.reschedule_appointment("APT-001", "2025-12-07", "13:00")
    print(f"   {result['message']}")

    # Cancel appointment
    print("\n5. Cancel VIP styling appointment:")
    result = appointments_api.cancel_appointment("APT-005")
    print(f"   {result['message']}")


def demo_knowledge_api() -> None:
    """Demonstrate Knowledge/Products API functionality."""
    print("\n=== KNOWLEDGE API DEMO ===\n")

    # Search products
    print("1. Search luxury products for 'merino wool':")
    products = knowledge_api.search_products("merino wool")
    print(f"   Found {len(products)} products:")
    for prod in products[:3]:  # Show top 3
        print(f"   - {prod.name}: ${prod.price:,.2f} ({prod.category})")
        print(f"     In stock: {prod.in_stock}")

    # Get specific product
    print("\n2. Get specific product (Technical Cashmere Sweater):")
    product = knowledge_api.get_product("PROD-002")
    if product is not None:
        print(f"   {product.name}: ${product.price:,.2f}")
        print(f"   Description: {product.description}")
        print(f"   Features: {', '.join(product.features[:3])}")

    # Search policies
    print("\n3. Search policies for 'styling services':")
    policies = knowledge_api.search_policies("styling")
    print(f"   Found {len(policies)} policy documents:")
    for policy in policies[:2]:  # Show top 2
        print(f"   - {policy.title} ({policy.category})")
        print(f"     {policy.content[:100]}...")

    # Get policies by category
    print("\n4. Get service policies:")
    policies = knowledge_api.get_policies_by_category("services")
    for policy in policies:
        print(f"   - {policy.title}")
        print(f"     {policy.content[:150]}...")

    # Get available products
    print("\n5. Get available luxury products:")
    available = knowledge_api.get_available_products()
    print(f"   {len(available)} luxury items in stock:")
    for product in available[:4]:  # Show first 4
        print(f"   - {product.name}: ${product.price:,.2f}")


def demo_users_api() -> None:
    """Demonstrate Users API functionality."""
    print("\n=== USERS API DEMO ===\n")

    # Get user by email
    print("1. Get user by email:")
    user = users_api.get_user_by_email("john.doe@example.com")
    if user:
        print(f"   User ID: {user.user_id}")
        print(f"   Name: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Phone: {user.phone}")

    # Get user by phone
    print("\n2. Get user by phone:")
    user = users_api.get_user_by_phone("+1-555-0102")
    if user:
        print(f"   User ID: {user.user_id}")
        print(f"   Name: {user.name}")
        print(f"   Email: {user.email}")
        print(f"   Phone: {user.phone}")

    # Get user by ID
    print("\n3. Get user by ID:")
    user = users_api.get_user_by_id("user_789")
    if user:
        print(f"   User ID: {user.user_id}")
        print(f"   Name: {user.name}")

    # Try non-existent user
    print("\n4. Try to get non-existent user:")
    user = users_api.get_user_by_email("nonexistent@example.com")
    if user is None:
        print("   User not found (expected)")

    # Show all users
    print("\n5. All users in the system:")
    all_users = users_api.get_all_users()
    print(f"   Total users: {len(all_users)}")
    for user in all_users:
        print(f"   - {user.user_id}: {user.name} ({user.email})")


if __name__ == "__main__":
    demo_orders_api()
    demo_appointments_api()
    demo_knowledge_api()
    demo_users_api()
    print("\n=== DEMO COMPLETE ===\n")
