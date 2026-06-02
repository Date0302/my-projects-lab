# Deployment Overview

## Deployment Architecture

The platform is designed using a modular serverless architecture on AWS.

## Deployment Workflow

1. Upload documents to Amazon S3
2. Trigger Lambda workflow
3. Process documents
4. Generate embeddings
5. Route user queries
6. Store logs in CloudWatch

## Infrastructure Components

### AWS Lambda

1.orchestrator

2.document-processor

3.embedding-generator

4.query-router

### Amazon S3

Used for document storage and upload management.

### Amazon SQS

Used for asynchronous workflow processing.

### Amazon CloudWatch

Used for centralized logging and monitoring.

### AWS IAM

Used for least-privilege access control.

## Security Design

1.Least privilege IAM policies

2.Service isolation

3.Centralized logging

4. Serverless architecture