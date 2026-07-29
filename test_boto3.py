import boto3

bucket = "pk-ai-augmented-data-platform-2026"

s3 = boto3.client(
    "s3",
    region_name="eu-north-1"
)

response = s3.put_object(
    Bucket=bucket,
    Key="bronze/clickstream/test.json",
    Body='{"hello":"world"}',
    ContentType="application/json"
)

print(response)
print("SUCCESS")