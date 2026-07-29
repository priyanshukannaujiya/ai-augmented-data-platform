import json
from datetime import datetime

import boto3
from kafka import KafkaConsumer


class ClickstreamConsumer:

    def __init__(self):

        # Kafka Consumer
        self.consumer = KafkaConsumer(
            "clickstream-events",
            bootstrap_servers="localhost:9092",
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )

        # AWS S3 Client
        self.s3 = boto3.client(
            "s3",
            region_name="eu-north-1"
        )

        # S3 Bucket Name
        self.bucket_name = "pk-ai-augmented-data-platform-2026"

    def upload_to_s3(self, event):

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        object_key = f"bronze/clickstream/{timestamp}.json"

        try:
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=json.dumps(event, indent=4),
                ContentType="application/json"
            )

            print(f"✅ Uploaded successfully: s3://{self.bucket_name}/{object_key}")

        except Exception as e:
            print(f"❌ Failed to upload to S3")
            print(e)

    def consume(self):

        print("🚀 Consumer Started...\n")

        for message in self.consumer:

            event = message.value

            print("Received Event:")
            print(json.dumps(event, indent=4))

            self.upload_to_s3(event)


if __name__ == "__main__":

    consumer = ClickstreamConsumer()

    consumer.consume()