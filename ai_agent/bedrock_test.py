"""
Test script to verify Amazon Bedrock connectivity and Claude Haiku 4.5 inference.
"""
import boto3
import botocore.exceptions
from ai_agent.config import AWS_REGION, BEDROCK_MODEL_ID

def test_bedrock_inference():
    print(f"Initializing Bedrock Runtime client in region: {AWS_REGION}...")
    
    try:
        # Create Bedrock client using default AWS credential provider chain
        # (This will automatically pick up AWS credentials from the environment or ~/.aws/credentials)
        session = boto3.Session(region_name=AWS_REGION)
        client = session.client("bedrock-runtime")
        
        print(f"Testing inference with model/profile ID: {BEDROCK_MODEL_ID}")
        
        # Test prompt
        system_prompt = [{"text": "You are an AWS Data Engineering assistant."}]
        messages = [
            {
                "role": "user",
                "content": [{"text": "Explain in two sentences what a Bronze-to-Silver AWS Glue ETL job does."}]
            }
        ]
        
        print("\nSending request to Amazon Bedrock...")
        
        # Using the Bedrock Converse API (Recommended for Claude models)
        response = client.converse(
            modelId=BEDROCK_MODEL_ID,
            messages=messages,
            system=system_prompt,
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.5,
            }
        )
        
        # Extract and print response
        output_message = response['output']['message']
        content = output_message['content']
        
        print("\n" + "="*50)
        print("BEDROCK RESPONSE:")
        print("="*50)
        for block in content:
            if 'text' in block:
                print(block['text'])
        print("="*50)
        print("\nSuccess! Bedrock inference test completed.")

    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print("\n" + "!"*50)
        print(f"AWS API ERROR: {error_code}")
        print(f"Message: {error_message}")
        print("!"*50)
        
        if error_code == "AccessDeniedException":
            print("\nTroubleshooting: Ensure your IAM user has 'bedrock:InvokeModel' permission.")
        elif error_code == "ValidationException":
            print("\nTroubleshooting: Verify the BEDROCK_MODEL_ID in config.py is correct and available in your region.")
        elif error_code == "ResourceNotFoundException":
            print("\nTroubleshooting: The specified Model ID or Inference Profile was not found.")
            print("Try changing BEDROCK_MODEL_ID in config.py to 'anthropic.claude-3-5-haiku-20241022-v1:0'")
            
    except botocore.exceptions.NoCredentialsError:
        print("\nERROR: AWS credentials not found.")
        print("Please configure your AWS credentials using 'aws configure' or environment variables.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    test_bedrock_inference()
