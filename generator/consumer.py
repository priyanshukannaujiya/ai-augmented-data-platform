import json
from datetime import datetime
from pathlib import Path

import boto3
from kafka import KafkaConsumer
from botocore.exceptions import ClientError

from generator.config import (
    KAFKA_BOOTSTRAP_SERVERS,
    TOPICS,
    S3_BUCKET,
    AWS_REGION
)


class EnterpriseConsumer:
    """
    Enterprise-grade Kafka Consumer that subscribes to all topics
    and uploads the events into the S3 Bronze layer.
    """

    def __init__(self):
        
        # Subscribe to all topics dynamically from the config
        try:
            self.consumer = KafkaConsumer(
                *TOPICS.values(),
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                auto_offset_reset="earliest",
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode("utf-8"))
            )
        except Exception as e:
            print(f"Failed to initialize Kafka Consumer: {e}")
            self.consumer = None

        # Initialize AWS S3 Client
        try:
            self.s3 = boto3.client(
                "s3",
                region_name=AWS_REGION
            )
        except Exception as e:
            print(f"Failed to initialize S3 Client: {e}")
            self.s3 = None

        self.bucket_name = S3_BUCKET
        self.project_root = Path(__file__).resolve().parent.parent

        print("=" * 60)
        print("= Enterprise Consumer Started =")
        print("=" * 60)

    def upload_to_bronze(self, topic, event):
        """
        Uploads the given event to the S3 bronze layer and saves a local copy.
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")

        # Automatically detect folder from topic (e.g., customers-events -> customers)
        folder = topic.replace("-events", "")

        # Define the object key / local path
        object_key = f"bronze/{folder}/{timestamp}.json"
        
        # 1. Save locally using pathlib to maintain local folder structure
        local_path = self.project_root / "generator" / object_key
        try:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_path, "w", encoding="utf-8") as f:
                json.dump(event, f, indent=4)
        except Exception as e:
            print(f"Warning: Failed to save local copy at {local_path}: {e}")

        # 2. Upload to S3 Bronze Layer
        if self.s3:
            try:
                self.s3.put_object(
                    Bucket=self.bucket_name,
                    Key=object_key,
                    Body=json.dumps(event, indent=4),
                    ContentType="application/json"
                )
                print(f"Uploaded to S3 -> {object_key}")
            except ClientError as e:
                print(f"AWS S3 Error uploading {object_key}")
                print(e.response)
            except Exception as e:
                print(f"Error uploading {object_key} to S3: {e}")

    def consume(self):
        """
        Continuously consume messages from all subscribed Kafka topics.
        """
        if not self.consumer:
            print("Consumer not initialized properly. Cannot consume.")
            return

        print("Listening for events...")
        for message in self.consumer:
            topic = message.topic
            event = message.value

            print("\n" + "=" * 60)
            print(f"Topic : {topic}")
            print(json.dumps(event, indent=4))

            # Process and upload the event
            self.upload_to_bronze(topic, event)


if __name__ == "__main__":
    consumer = EnterpriseConsumer()
    consumer.consume()