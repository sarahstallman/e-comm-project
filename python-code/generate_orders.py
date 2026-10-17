import os
import json
import random
from datetime import datetime, timedelta, timezone
from faker import Faker

# Generate realistic data
fake = Faker()


def generate_nested_orders(num_orders=100):
    """Build a list of mock e-commerce orders, each with a nested customer
    object and a nested list of line items (mimics a raw JSON API/export)."""
    orders = []

    # Core apparel product catalog - each order's line items are sampled from this
    products = [
        {"product_id": "P101", "name": "Basic Short", "price": 68.00, "category": "Mens"},
        {"product_id": "P102", "name": "Basic Jogger", "price": 94.00, "category": "Womens"},
        {"product_id": "P103", "name": "Basic Tee", "price": 44.00, "category": "Mens"},
        {"product_id": "P104", "name": "Basic Hoodie", "price": 98.00, "category": "Womens"},
        {"product_id": "P105", "name": "Full Length Leggings", "price": 88.00, "category": "Womens"}
    ]

    for order_num in range(num_orders):
        # Each order has between 1 and 4 line items
        num_items = random.randint(1, 4)
        line_items = []
        order_total = 0.0

        for _ in range(num_items):
            # Pick a random product (the same product can appear on multiple
            # lines within one order since choices are independent)
            prod = random.choice(products)
            quantity = random.randint(1, 3)
            item_total = prod["price"] * quantity
            order_total += item_total

            # Denormalized line item: product details are copied in as they
            # would be in a raw source payload
            line_items.append({
                "product_id": prod["product_id"],
                "product_name": prod["name"],
                "category": prod["category"],
                "price": prod["price"],
                "quantity": quantity,
                "item_total": round(item_total, 2)
            })

        # Spread order dates across the last 14 days
        random_days_ago = random.randint(0, 14)
        order_date = (
            (datetime.now(timezone.utc) - timedelta(days=random_days_ago))
            .isoformat()
            .replace("+00:00", "Z")
        )

        order_payload = {
            # Sequential IDs guarantee uniqueness within a run
            "order_id": f"ORD{100000 + order_num}",
            # Nested object: will flatten in a dbt staging model
            "customer": {
                "customer_id": f"CUST{random.randint(1000, 9999)}",
                "email": fake.email(),
                "shipping_state": fake.state_abbr()
            },
            "order_date": order_date,
            "order_total": round(order_total, 2),
            # Weighted 3:1 so roughly 25% of orders are FAILED
            "payment_status": random.choice(["PAID", "PAID", "PAID", "FAILED"]),
            # Nested array: flatten/explode downstream
            "line_items": line_items
        }
        orders.append(order_payload)

    return orders


if __name__ == "__main__":
    mock_dataset = generate_nested_orders(100)

    # Resolve paths relative to this script so it works from any working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Output goes to a raw-data folder one level above this script's folder
    output_dir = os.path.join(project_root, "raw-data")
    full_output_path = os.path.join(output_dir, "raw_orders_data.json")

    # Create the output folder on first run
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created new sibling directory: '{output_dir}/'")

    # Write the orders as JSON (indent=4 for readability)
    with open(full_output_path, "w") as f:
        json.dump(mock_dataset, f, indent=4)

    print(f"Success! Generated 100 nested orders and saved to '{full_output_path}'.")