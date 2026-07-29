import random
from pathlib import Path

import pandas as pd
from faker import Faker

fake = Faker("en_IN")

NUM_SESSIONS = 50000

DEVICES = ["Mobile", "Desktop", "Tablet"]

BROWSERS = [
    "Chrome",
    "Safari",
    "Firefox",
    "Edge"
]


def load_customers():

    path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "master_data"
        / "customers.csv"
    )

    return pd.read_csv(path)


def generate_sessions(customers, num_sessions=NUM_SESSIONS):

    sessions = []

    customer_ids = customers["customer_id"].tolist()

    for i in range(1, num_sessions + 1):

        customer = random.choice(customer_ids)

        start_time = fake.date_time_between(
            start_date="-30d",
            end_date="now"
        )

        duration = random.randint(30, 1800)

        end_time = start_time + pd.Timedelta(seconds=duration)

        session = {

            "session_id": f"SES{i:06}",

            "customer_id": customer,

            "device": random.choices(
                DEVICES,
                weights=[70, 20, 10],
                k=1
            )[0],

            "browser": random.choice(BROWSERS),

            "start_time": start_time,

            "end_time": end_time,

            "duration_seconds": duration

        }

        sessions.append(session)

    return pd.DataFrame(sessions)


def save_sessions(df):

    output_path = (
        Path(__file__)
        .resolve()
        .parent.parent
        / "output"
        / "sessions"
        / "sessions.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"✅ Saved {len(df)} sessions")
    print(output_path)


def main():

    customers = load_customers()

    sessions = generate_sessions(customers)

    save_sessions(sessions)


if __name__ == "__main__":
    main()