"""
Configuration for the AI Agent layer.
"""

# AWS Region for Amazon Bedrock
AWS_REGION = "eu-north-1"

# Bedrock Model ID or Inference Profile ID
# Note: For Claude 3.5 Haiku (often referred to as Haiku 4.5 depending on naming) in eu-north-1,
# you might need to use a cross-region inference profile if standard invocation is not supported.
# Standard model ID: 'anthropic.claude-3-5-haiku-20241022-v1:0'
# Cross-region ID: 'eu.anthropic.claude-3-5-haiku-20241022-v1:0'
# 
# If you receive a ResourceNotFoundException or ValidationException, please run the AWS CLI command
# to list inference profiles and update this ID accordingly.
BEDROCK_MODEL_ID = "eu.anthropic.claude-haiku-4-5-20251001-v1:0"

# AWS Glue Configuration
GLUE_REGION = "eu-north-1"
GLUE_JOB_BRONZE_TO_SILVER = "silvertranform"
GLUE_JOB_SILVER_TO_GOLD = "silver to gold "

# Analytics Configuration
GOLD_DATABASE = "ai_augmented_gold_db"
ATHENA_OUTPUT_LOCATION = "s3://pk-ai-augmented-data-platform-2026/athena-results/"
