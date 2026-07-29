from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker("en_IN")

# Number of customers to generate
NUM_CUSTOMERS = 10000

# Membership tiers
TIERS = ["Bronze", "Silver", "Gold", "Platinum"]


def generate_customers(num_customers=NUM_CUSTOMERS):
    """
    Generate synthetic customer master data.
    """

    customers = []

    for i in range(1, num_customers + 1):

        customer = {
            "customer_id": f"CUST{i:06}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "phone": fake.msisdn()[:10],
            "gender": random.choice(["Male", "Female"]),
            "dob": fake.date_of_birth(
                minimum_age=18,
                maximum_age=70
            ),
            "city": fake.city(),
            "state": fake.state(),
            "country": "India",
            "join_date": fake.date_between(
                start_date="-5y",
                end_date="today"
            ),
            "tier": random.choices(
                TIERS,
                weights=[50, 30, 15, 5],
                k=1
            )[0]
        }

        customers.append(customer)

    return pd.DataFrame(customers)


def save_customers(df):

    output_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "master_data"
        / "customers.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"✅ Saved {len(df)} customers")
    print(f"📁 {output_path}")


def main():

    df = generate_customers()

    save_customers(df)


if __name__ == "__main__":
    main()