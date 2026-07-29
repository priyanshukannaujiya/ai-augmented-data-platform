KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

AWS_REGION = "eu-north-1"

S3_BUCKET = "pk-ai-augmented-data-platform-2026"

TOPICS = {
    "customers": "customers-events",
    "products": "products-events",
    "orders": "orders-events",
    "sessions": "sessions-events",
    "clickstream": "clickstream-events",
}

DATA_FILES = {
    "customers": "generator/data/customers.csv",
    "products": "generator/data/products.csv",
    "orders": "generator/data/orders.csv",
    "sessions": "generator/data/sessions.csv",
    "clickstream": "generator/data/clickstream.csv",
}