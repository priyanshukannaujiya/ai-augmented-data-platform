import json
import os
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from kafka import KafkaConsumer
from kafka.errors import KafkaError


# ============================================================
# CONFIGURATION
# ============================================================

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

TOPICS = [
    "customers",
    "products",
    "orders",
    "sessions",
    "clickstream",
    "customer_updates"
]

# IMPORTANT: Replace this with your actual S3 bucket name
S3_BUCKET_NAME = "pk-ai-augmented-data-platform-2026"

S3_BRONZE_PREFIX = "bronze"

# Local Bronze folder
LOCAL_BRONZE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "bronze"
)


# ============================================================
# ENTERPRISE KAFKA CONSUMER
# ============================================================

class EnterpriseKafkaConsumer:

    def __init__(self):

        print("=" * 70)
        print("STARTING ENTERPRISE KAFKA CONSUMER")
        print("=" * 70)

        # ----------------------------------------------------
        # Kafka Consumer
        # ----------------------------------------------------

        try:
            self.consumer = KafkaConsumer(
                *TOPICS,
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

                # Start from earliest message if there is
                # no previously committed offset
                auto_offset_reset="earliest",

                # Kafka automatically stores offsets
                enable_auto_commit=True,

                # Consumer group
                group_id="aws-bronze-consumer",

                # Convert Kafka bytes -> Python dictionary
                value_deserializer=lambda x: json.loads(
                    x.decode("utf-8")
                )
            )

            print("[OK] Connected to Kafka")

        except KafkaError as error:
            print(f"[ERROR] Kafka connection failed: {error}")
            raise

        # ----------------------------------------------------
        # AWS S3 Client
        # ----------------------------------------------------

        try:
            self.s3 = boto3.client("s3")

            print("[OK] AWS S3 client initialized")

        except Exception as error:
            print(f"[ERROR] AWS initialization failed: {error}")
            raise

        print("\nSubscribed Topics:")

        for topic in TOPICS:
            print(f"   - {topic}")

        print("=" * 70)


    # ========================================================
    # CREATE PARTITION INFORMATION
    # ========================================================

    def create_partition(self):

        now = datetime.now(timezone.utc)

        partition = {
            "year": str(now.year),
            "month": f"{now.month:02d}",
            "day": f"{now.day:02d}",
            "hour": f"{now.hour:02d}"
        }

        return partition


    # ========================================================
    # CREATE S3 OBJECT KEY
    # ========================================================

    def create_s3_key(self, topic):

        partition = self.create_partition()

        file_id = uuid.uuid4()

        key = (
            f"{S3_BRONZE_PREFIX}/{topic}/"
            f"year={partition['year']}/"
            f"month={partition['month']}/"
            f"day={partition['day']}/"
            f"hour={partition['hour']}/"
            f"{file_id}.json"
        )

        return key


    # ========================================================
    # CREATE LOCAL FILE PATH
    # ========================================================

    def create_local_path(self, topic):

        partition = self.create_partition()

        directory = os.path.join(
            LOCAL_BRONZE_PATH,
            topic,
            f"year={partition['year']}",
            f"month={partition['month']}",
            f"day={partition['day']}",
            f"hour={partition['hour']}"
        )

        # Automatically create directories
        os.makedirs(directory, exist_ok=True)

        filename = f"{uuid.uuid4()}.json"

        return os.path.join(directory, filename)


    # ========================================================
    # SAVE EVENT LOCALLY
    # ========================================================

    def save_local(self, topic, event):

        try:

            filepath = self.create_local_path(topic)

            with open(
                filepath,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    event,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(f"[LOCAL] {filepath}")

        except Exception as error:

            print(
                f"[ERROR] Local write failed "
                f"for topic {topic}: {error}"
            )


    # ========================================================
    # UPLOAD EVENT TO AMAZON S3
    # ========================================================

    def upload_to_s3(self, topic, event):

        try:

            object_key = self.create_s3_key(topic)

            self.s3.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=object_key,
                Body=json.dumps(
                    event,
                    ensure_ascii=False
                ).encode("utf-8"),
                ContentType="application/json"
            )

            print(
                f"[S3] s3://{S3_BUCKET_NAME}/{object_key}"
            )

        except (ClientError, BotoCoreError) as error:

            print(
                f"[AWS ERROR] Upload failed "
                f"for topic {topic}: {error}"
            )

        except Exception as error:

            print(
                f"[ERROR] Unexpected S3 error "
                f"for topic {topic}: {error}"
            )


    # ========================================================
    # PROCESS KAFKA MESSAGE
    # ========================================================

    def process_message(self, message):

        topic = message.topic

        event = message.value

        print("\n" + "-" * 70)

        print(f"TOPIC     : {topic}")
        print(f"PARTITION : {message.partition}")
        print(f"OFFSET    : {message.offset}")

        print("-" * 70)

        # ----------------------------------------------------
        # Local Bronze
        # ----------------------------------------------------

        self.save_local(
            topic,
            event
        )

        # ----------------------------------------------------
        # AWS S3 Bronze
        # ----------------------------------------------------

        self.upload_to_s3(
            topic,
            event
        )


    # ========================================================
    # START CONSUMER
    # ========================================================

    def consume(self):

        print("\nWaiting for Kafka events...")
        print("Press CTRL+C to stop.\n")

        try:

            for message in self.consumer:

                self.process_message(message)

        except KeyboardInterrupt:

            print("\nStopping consumer...")

        except KafkaError as error:

            print(
                f"\n[ERROR] Kafka consumer error: {error}"
            )

        except Exception as error:

            print(
                f"\n[ERROR] Unexpected consumer error: {error}"
            )

        finally:

            self.consumer.close()

            print("[OK] Kafka consumer closed")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    consumer = EnterpriseKafkaConsumer()

    consumer.consume()