from kafka import KafkaProducer
import json


class ClickstreamProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda value: json.dumps(value).encode("utf-8")
        )

    def send_event(self, event):
        self.producer.send("clickstream-events", value=event)
        self.producer.flush()
        print(f"Event sent: {event}")