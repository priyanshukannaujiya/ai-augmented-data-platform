import random
from pathlib import Path

import pandas as pd

# Categories, subcategories, and brands
PRODUCT_CATALOG = {
    "Electronics": {
        "Mobiles": ["Apple", "Samsung", "OnePlus", "Xiaomi"],
        "Laptops": ["Dell", "HP", "Lenovo", "Apple"],
        "Headphones": ["Sony", "Boat", "JBL", "Apple"],
    },
    "Fashion": {
        "Men": ["Nike", "Adidas", "Puma", "Levis"],
        "Women": ["Zara", "H&M", "Biba", "Forever21"],
    },
    "Home": {
        "Kitchen": ["Prestige", "Pigeon", "Philips"],
        "Furniture": ["IKEA", "Godrej", "Durian"],
    },
    "Books": {
        "Fiction": ["Penguin", "HarperCollins"],
        "Education": ["Pearson", "McGraw Hill"],
    },
    "Sports": {
        "Fitness": ["Cult", "Decathlon", "Nike"],
    }
}

NUM_PRODUCTS = 2000


def generate_products(num_products=NUM_PRODUCTS):

    products = []

    for i in range(1, num_products + 1):

        category = random.choice(list(PRODUCT_CATALOG.keys()))

        sub_category = random.choice(
            list(PRODUCT_CATALOG[category].keys())
        )

        brand = random.choice(
            PRODUCT_CATALOG[category][sub_category]
        )

        product = {
            "product_id": f"PROD{i:06}",
            "product_name": f"{brand} {sub_category} {i}",
            "category": category,
            "sub_category": sub_category,
            "brand": brand,
            "price": random.randint(200, 100000),
            "stock": random.randint(0, 500),
        }

        products.append(product)

    return pd.DataFrame(products)


def save_products(df):

    output_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "master_data"
        / "products.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"✅ Saved {len(df)} products")
    print(f"📁 {output_path}")


def main():

    df = generate_products()

    save_products(df)


if __name__ == "__main__":
    main()