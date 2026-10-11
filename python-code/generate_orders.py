import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()


def generate_nested_orders(num_orders=100):
    orders = []

    # Core apparel product catalog
    products = [
        {"product_id": "P101", "name": "Basic Short", "price": 68.00, "category": "Mens"},
        {"product_id": "P102", "name": "Basic Jogger", "price": 94.00, "category": "Womens"},
        {"product_id": "P103", "name": "Basic Tee", "price": 44.00, "category": "Mens"},
        {"product_id": "P104", "name": "Basic Hoodie", "price": 98.00, "category": "Womens"},
        {"product_id": "P105", "name": "Full Length Leggings", "price": 88.00, "category": "Womens"}
    ]

    for _ in range(num_orders):
        num_items = random.randint(1, 4)
        line_items = []
        order_total = 0.0

        for _ in range(num_items):
            prod = random.choice(products)
            quantity = random.randint(1, 3)
            item_total = prod["price"] * quantity
            order_total += item_total

            line_items.append({
                "product_id": prod["product_id"],
                "product_name": prod["name"],
                "category": prod["category"],
                "price": prod["price"],
                "quantity": quantity,
                "item_total": round(item_total, 2)
            })

        random_days_ago = random.randint(0, 14)
        order_date = (datetime.utcnow() - timedelta(days=random_days_ago)).isoformat() + "Z"

        order_payload = {
            "order_id": f"ORD{random.randint(100000, 999999)}",
            "customer": {
                "customer_id": f"CUST{random.randint(1000, 9999)}",
                "email": fake.email(),
                "shipping_state": fake.state_abbr()
            },
            "order_date": order_date,
            "order_total": round(order_total, 2),
            "payment_status": random.choice(["PAID", "PAID", "PAID", "FAILED"]),
            "line_items": line_items
        }
        orders.append(order_payload)

    return orders


if __name__ == "__main__":
    mock_dataset = generate_nested_orders(100)
    output_dir = "raw-data"
    output_filename = "raw_orders_data.json"
    full_output_path = os.path.join(output_dir, output_filename)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created new directory: '{output_dir}/'")

    with open(full_output_path, "w") as f:
        json.dump(mock_dataset, f, indent=4)

    print(f" Success! Generated 100 nested orders and saved to '{output_filename}'.")
