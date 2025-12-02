# Mock APIs Documentation

This document describes the three mock API systems implemented for the Concierge Service.

## Overview

The service includes three mock external systems:
1. **Orders API** - Manage order queries and modifications
2. **Appointments API** - Schedule, reschedule, and query appointments
3. **Knowledge API** - Search products and policy documents

All APIs are pre-populated with mock data and can be accessed through their global instances.

## 1. Orders API

**File**: `src/concierge/external_systems/orders.py`

### Features

- Query order details and status by `order_id`
- Swap items in pending/processing orders
- Cancel orders (business logic enforced)
- Update order status

### Business Logic

- Only `pending` or `processing` orders can be modified
- `shipped`, `delivered`, or `cancelled` orders cannot be changed
- Item swaps maintain quantity and price

### Methods

```python
from concierge.external_systems import orders_api

# Get order details
order = orders_api.get_order("ORD-001")

# Get order status
status = orders_api.get_order_status("ORD-001")

# Swap an item
result = orders_api.swap_item(
    order_id="ORD-004",
    old_item_id="ITEM-006",
    new_item_id="ITEM-007",
    new_item_name="New Monitor"
)

# Cancel order
result = orders_api.cancel_order("ORD-004")

# Update order status
result = orders_api.update_order_status("ORD-001", "delivered")
```

### Mock Data

Pre-loaded with 4 orders:
- `ORD-001`: Shipped order (2 items)
- `ORD-002`: Processing order
- `ORD-003`: Delivered order
- `ORD-004`: Pending order (can be modified)

## 2. Appointments API

**File**: `src/concierge/external_systems/appointments.py`

### Features

- Query appointments by email or phone
- Schedule new appointments
- Reschedule existing appointments
- Cancel appointments
- Confirm appointments

### Business Logic

- No duplicate appointments at same date/time for same user
- Cannot reschedule `cancelled` or `completed` appointments
- Cannot cancel `completed` appointments
- Appointments indexed by both email and phone for quick lookup

### Methods

```python
from concierge.external_systems import appointments_api

# Query by email
appointments = appointments_api.get_appointments_by_email("john.doe@example.com")

# Query by phone
appointments = appointments_api.get_appointments_by_phone("+1-555-0101")

# Schedule new appointment
result = appointments_api.schedule_appointment(
    email="user@example.com",
    phone="+1-555-1234",
    date="2025-12-15",
    time="14:00",
    service_type="Consultation"
)

# Reschedule appointment
result = appointments_api.reschedule_appointment(
    appointment_id="APT-001",
    new_date="2025-12-16",
    new_time="10:00"
)

# Cancel appointment
result = appointments_api.cancel_appointment("APT-005")

# Confirm appointment
result = appointments_api.confirm_appointment("APT-001")
```

### Mock Data

Pre-loaded with 5 appointments:
- Multiple appointments for `john.doe@example.com`
- Various service types: Consultation, Technical Support, Follow-up, Product Demo
- Different statuses: scheduled, confirmed, completed

## 3. Knowledge API

**File**: `src/concierge/external_systems/inventory.py`

### Features

- Search products by keyword (with relevance scoring)
- Search policy documents by keyword
- Get products by category or ID
- Get policies by category or ID
- Filter available (in-stock) products

### Search Strategy

The API uses keyword-based search with relevance scoring:
- **Products**: Searches name, description, category, and features
- **Policies**: Searches title, content, keywords, and category
- Results are ranked by relevance score (higher = more relevant)

### Methods

```python
from concierge.external_systems import knowledge_api

# Search products
products = knowledge_api.search_products("wireless")

# Get specific product
product = knowledge_api.get_product("PROD-001")

# Get products by category
accessories = knowledge_api.get_products_by_category("Accessories")

# Get available products
available = knowledge_api.get_available_products()

# Search policies
policies = knowledge_api.search_policies("shipping")

# Get specific policy
policy = knowledge_api.get_policy("POL-001")

# Get policies by category
return_policies = knowledge_api.get_policies_by_category("returns")
```

### Mock Data

**Products** (6 items):
- Wireless Headphones Pro ($199.99)
- Ergonomic Keyboard ($149.99)
- 4K Webcam ($129.99) - Out of stock
- Standing Desk Converter ($249.99)
- USB-C Hub ($49.99)
- Wireless Mouse ($39.99)

**Policies** (6 documents):
- Shipping Policy
- Return Policy
- Warranty Information
- Payment Methods
- Product Support
- Privacy Policy

## Running Examples

### Run the Demo Script

```bash
make demo
```

This runs `examples/demo_apis.py` which demonstrates all API functionality.

### Run Tests

```bash
make test
```

Tests are located in `tests/test_mock_apis.py`.

## Response Format

All modification operations (swap, cancel, reschedule, etc.) return a dictionary:

```python
{
    "success": "true" | "false",
    "message": "Description of result",
    # Additional fields may be present (e.g., appointment_id for new appointments)
}
```

## Integration with Agent

These mock APIs can be integrated with the agent system to:
1. Handle user queries about orders, appointments, and products
2. Execute actions like rescheduling appointments or modifying orders
3. Provide information retrieval for product and policy questions

The APIs are designed to be easily replaceable with real external system integrations while maintaining the same interface.
