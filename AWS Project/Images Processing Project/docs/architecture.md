# Architecture Design

#### 🌐 Language / 言語 / 语言

 US English: [architecture.md](architecture.md)                                                JP 日本語: [architecture.ja.md](architecture.ja.md)

## Overview

This project implements an event-driven image processing system using AWS managed services.

When a user uploads an image:

1. The image is stored in Amazon S3
2. An event is sent to Amazon SQS
3. AWS Lambda consumes the message
4. The image is processed (thumbnail generation)
5. Metadata is stored in DynamoDB
6. A notification is sent via SNS

This architecture is fully serverless and horizontally scalable.

## Why Event-Driven Architecture?

The system is designed using event-driven principles to:

- decouple upload and processing
- improve fault tolerance
- allow asynchronous scaling
- avoid blocking user requests

Using SQS ensures that image processing failures do not affect uploads.

## Service Selection Rationale

### Amazon S3

Used for object storage due to:

- high durability (11 9’s)
- scalable storage
- native event integration

### Amazon SQS

Chosen to:

- decouple S3 from Lambda
- provide retry capability
- prevent data loss during failures

### AWS Lambda

Selected because:

- no server management required
- automatic scaling
- cost-effective for event-based workloads

### Amazon DynamoDB

Used for metadata storage because:

- low latency
- fully managed
- scalable without infrastructure management

### Amazon SNS

Used for notifications to:

- inform downstream systems
- enable future integrations

## Scalability Design

- Lambda automatically scales based on SQS queue size
- S3 supports virtually unlimited storage
- DynamoDB scales horizontally
- No manual infrastructure scaling required

The system supports burst traffic without architectural changes.

## Failure Handling

- SQS ensures message durability
- Lambda retry mechanism handles transient errors
- CloudWatch logs enable debugging

This design improves reliability and operational visibility.

## Production Considerations

In production environments:

- Dependencies should be packaged using Lambda Layers
- CI/CD should handle deployment automation
- Alarms should be configured in CloudWatch
- Dead Letter Queues (DLQ) can be added for advanced failure handling