from kafka import KafkaConsumer
import json


class ClickstreamConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            "clickstream-events",
            bootstrap_servers="localhost:9092",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

    def consume(self):
        print("Waiting for events...\n")

        for message in self.consumer:
            print(message.value)