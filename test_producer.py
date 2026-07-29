import json
import time
from pathlib import Path

import pandas as pd
from kafka import KafkaProducer

from generator.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    DATA_FILES,
    TOPICS
)


class EnterpriseProducer:

    def __init__(self):

        self.producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        self.datasets = {}

        print("=" * 70)
        print("Loading datasets...")
        print("=" * 70)

        for dataset, file_path in DATA_FILES.items():

            path = Path(file_path)

            if not path.exists():
                print(f"❌ Missing: {file_path}")
                continue

            try:
                df = pd.read_csv(path)

                self.datasets[dataset] = {
                    "topic": TOPICS[dataset],
                    "rows": df.to_dict(orient="records"),
                    "index": 0
                }

                print(f"✅ {dataset:<18} {len(df)} rows")

            except Exception as e:
                print(f"❌ Error loading {dataset}: {e}")

        print("\nLoaded datasets:")
        print(list(self.datasets.keys()))
        print("=" * 70)

    def send_event(self, topic, event):

        self.producer.send(topic, event)
        self.producer.flush()

        print(f"✅ [{topic}] {event}")

    def start(self):

        print("\n🚀 Producer Started\n")

        if not self.datasets:
            print("❌ No datasets loaded.")
            return

        while True:

            active = False

            for dataset, data in self.datasets.items():

                if data["index"] >= len(data["rows"]):
                    continue

                active = True

                event = data["rows"][data["index"]]

                self.send_event(
                    data["topic"],
                    event
                )

                data["index"] += 1

            if not active:
                break

            time.sleep(1)

        print("\n🎉 Streaming Finished")


if __name__ == "__main__":

    producer = EnterpriseProducer()
    producer.start()