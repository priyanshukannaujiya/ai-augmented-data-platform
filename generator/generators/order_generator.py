import random
import uuid
from pathlib import Path

import pandas as pd

PAYMENT_METHODS = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Wallet",
    "Cash on Delivery"
]

ORDER_STATUS = [
    "paid",
    "cancelled",
    "refunded"
]


def load_clickstream():

    path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "clickstream.csv"
    )

    return pd.read_csv(path)


def load_products():

    path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "products.csv"
    )

    return pd.read_csv(path)


def generate_orders(clickstream, products):

    checkout_events = clickstream[
        clickstream["event_type"] == "checkout_start"
    ]

    product_lookup = (
        products
        .set_index("product_id")["price"]
        .to_dict()
    )

    orders = []

    for _, row in checkout_events.iterrows():

        quantity = random.randint(1, 3)

        price = product_lookup.get(
            row["product_id"],
            1000
        )

        orders.append({

            "order_id": f"ORD-{uuid.uuid4().hex[:10].upper()}",

            "customer_id": row["customer_id"],

            "session_id": row["session_id"],

            "product_id": row["product_id"],

            "quantity": quantity,

            "unit_price": price,

            "amount": quantity * price,

            "payment_method": random.choices(
                PAYMENT_METHODS,
                weights=[45,20,15,10,10],
                k=1
            )[0],

            "status": random.choices(
                ORDER_STATUS,
                weights=[90,5,5],
                k=1
            )[0],

            "order_timestamp": row["timestamp"]

        })

    return pd.DataFrame(orders)


def save_orders(df):

    output_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "data"
        / "orders.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Generated {len(df)} orders")
    print(output_path)


def main():

    clickstream = load_clickstream()

    products = load_products()

    orders = generate_orders(
        clickstream,
        products
    )

    save_orders(orders)


if __name__ == "__main__":
    main()