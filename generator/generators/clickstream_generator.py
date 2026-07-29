import random
import uuid
from pathlib import Path

import pandas as pd

from .journey_engine import get_random_journey


def load_sessions():
    path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "sessions.csv"
    )
    return pd.read_csv(path)


def load_products():
    path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "products.csv"
    )
    return pd.read_csv(path)


def generate_clickstream(sessions, products):

    product_ids = products["product_id"].tolist()

    clickstream = []

    for _, session in sessions.iterrows():

        journey = get_random_journey()

        current_time = pd.to_datetime(session["start_time"])

        for event_type in journey["events"]:

            clickstream.append(
                {
                    "event_id": str(uuid.uuid4()),
                    "session_id": session["session_id"],
                    "customer_id": session["customer_id"],
                    "product_id": random.choice(product_ids),
                    "event_type": event_type,
                    "device": session["device"],
                    "browser": session["browser"],
                    "timestamp": current_time,
                }
            )

            current_time += pd.Timedelta(
                seconds=random.randint(5, 60)
            )

    return pd.DataFrame(clickstream)


def save_clickstream(df):

    output_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "clickstream.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} clickstream events")


def main():

    sessions = load_sessions()

    products = load_products()

    clickstream = generate_clickstream(
        sessions,
        products
    )

    save_clickstream(clickstream)


if __name__ == "__main__":
    main()