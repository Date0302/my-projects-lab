# Infrastructure Overview

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

This document describes the infrastructure components, design decisions, and operational aspects of the Cost-Aware GenAI Document Assistant project. The entire platform is built on AWS serverless services to ensure scalability, low maintenance, and cost efficiency.

## Infrastructure Architecture (High Level)

The infrastructure is organized into four logical layers:

1. Ingestion Layer – S3 + Step Functions + Lambda for document processing and vectorization.
2. Query & Routing Layer – API Gateway + Cognito + Lambda (Orchestrator) + Bedrock + OpenSearch Serverless.
3. Asynchronous Messaging Layer – SQS for decoupling heavy processing tasks (optional but included for resilience).
4. Observability & Analytics Layer – CloudWatch, DynamoDB exports, Athena, QuickSight, SNS.

All resources are provisioned with AWS CDK or Terraform (IaC templates provided in the repository).

## Core Infrastructure Components

### AWS Lambda

|    Function Name    |                           Purpose                            |
| :-----------------: | :----------------------------------------------------------: |
| document-processor  | Extracts text from uploaded documents (PDF/TXT), chunks, and cleans. |
| embedding-generator |   Calls Bedrock Titan Embeddings to vectorize text chunks.   |
|    orchestrator     | Core routing logic: semantic search, model selection, cost logging. |
|    query-router     |  (Optional) Lightweight classifier for question complexity.  |

All Lambda functions are configured with:

1.Memory: 512 MB – 1024 MB (depending on workload)

2.Timeout: 3 minutes (document processor) / 30 seconds (orchestrator)

3.Reserved concurrency: 10 (to control cost and prevent runaway scaling)

4.Dead Letter Queue (DLQ) via SQS for failed async invocations

### Amazon S3

|       Bucket Name       |                           Purpose                            |
| :---------------------: | :----------------------------------------------------------: |
| raw-documents-<account> | Stores uploaded original documents (versioning enabled, SSE-S3 encryption). |
|   cost-logs-<account>   | Receives DynamoDB exports in Parquet format for Athena queries. |

Event Notifications: raw-documents bucket sends s3:ObjectCreated:events to an EventBridge rule, which then triggers the Step Functions workflow.

### Amazon SQS

Used for asynchronous decoupling between workflow stages, especially for non‑critical or retry‑heavy tasks.

|      Queue Name      |                           Purpose                            |
| :------------------: | :----------------------------------------------------------: |
| doc-processing-queue | Holds messages from document ingestion pipeline; consumed by `document-processor` Lambda. |
|   embedding-queue    | (Optional) Decouples text chunking from embedding generation. |

**Configuration**:

1.Visibility timeout: 5 minutes

2.Redrive policy: DLQ after 3 receive attempts

3.FIFO queues not required (idempotent processing)

### AWS Step Functions

Orchestrates the document ingestion workflow:
1. Text extraction
2. Chunking
3. Embedding generation
4. Indexing into OpenSearch Serverless

State machine includes retry on Bedrock throttling errors and a Catch block for failures (logs to CloudWatch and SNS).

### Amazon DynamoDB

| Table Name        | Purpose                                                      |
| ----------------- | ------------------------------------------------------------ |
| cost-logs         | Stores per‑invocation cost data: userId, modelId, inputTokens, outputTokens, estimatedCostUsd, timestamp. |
| document-metadata | (Optional) Tracks document processing status (uploaded → vectorized). |

Features:

1.On‑demand capacity (or provisioned with auto‑scaling)

2.TTL (Time To Live) on cost-logs – 90 days

3.DynamoDB Streams → S3 export for long‑term analytics

### Amazon OpenSearch Serverless

1.Collection name: rag-vector-store

2.Index mapping: knn_vector (dimension = 1536 for Titan Embeddings)

3.Metadata fields: `documentId`, `chunkIndex`, `sourceBucket`, `uploadTime`

4.Encryption: AWS KMS (customer‑managed key)

### Amazon Bedrock

Models enabled in the account:
|           Model            |             Use Case             |
| :------------------------: | :------------------------------: |
| amazon.titan-embed-text-v1 | Text to vector (1536 dimensions) |
|   amazon.titan-text-lite   |       Low‑cost factual QA        |
| anthropic.claude-3-sonnet  |    High‑reasoning complex QA     |

### API Gateway & Cognito

- **API Gateway** (REST):
  - Endpoints: POST /upload (signed URL generation), POST /query
  - Throttling: 1000 requests per second, burst 2000
  - CORS enabled
- **Cognito User Pool**:
  - JWT authorizer attached to all endpoints
  - Access token validity: 1 hour

### AWS IAM

All functions and services follow least‑privilege policies:

1.Lambda execution roles: only allow s3:GetObject on the specific raw bucket, bedrock:InvokeModel on specific model ARNs, dynamodb:PutItem on cost table.

2.S3 bucket policies: deny unencrypted uploads, restrict public access.

3.Step Functions role: minimal actions for Lambda invocation, DynamoDB updates, and SNS publish.

## Deployment Workflow (IaC)

The infrastructure is fully defined as code. To deploy:

1. Prerequisites:
   - AWS CLI configured with administrator permissions (for first deployment)
   - Node.js 18+ (CDK) or Terraform 1.3+
   - Bedrock models enabled in the target region (us-east-1 or us-west-2)

2. Steps:
   ```bash
   # Using AWS CDK
   cdk bootstrap
   cdk deploy --all
   
   # Using Terraform
   terraform init
   terraform apply -auto-approve

3. Post‑deployment:
   - Create a Cognito test user (via AWS Console or CLI)
   - Note the API Gateway endpoint URL from stack outputs

The deployment creates all resources listed above, including S3 buckets, Lambda functions, Step Functions state machine, SQS queues, OpenSearch collection, and CloudWatch dashboards.

## Security Design

| Area                  | Implementation                                               |
| --------------------- | ------------------------------------------------------------ |
| Encryption at rest    | S3 (SSE‑S3), DynamoDB (default encryption), OpenSearch (KMS) |
| Encryption in transit | TLS 1.2+ for all API calls, Bedrock endpoints, and inter‑service communication |
| Authentication        | Cognito JWT (required for all user‑facing APIs)              |
| Authorization         | IAM roles with resource‑based policies (e.g., Lambda can only access its own S3 prefix) |
| Secrets management    | API keys stored in AWS Secrets Manager (if any), referenced via Lambda environment variables |
| Service isolation     | Each Lambda runs in its own VPC? Not required (serverless), but VPC endpoints added for OpenSearch if deployed in private subnet. |

## Monitoring & Logging (CloudWatch)

See also the separate [CloudWatch Monitoring](./CloudWatch%20Monitoring.md) document.

Log groups automatically created for:

1.All Lambda functions (`/aws/lambda/<function-name>`)

2.Step Functions execution history

3.API Gateway access logs

Custom metrics published by Lambda:

1.CostPerInvocation (in USD) – dimension: ModelId

2.RoutingDecision(1 for low‑cost path, 2 for high‑cost path)

Alarms:

1.HighDailyCost→ SNS email when `TotalDailyCost > 5`

2.LambdaThrottling → SNS when throttle count > 10 in 5 minutes

3.StepFunctionFailure → SNS when state machine execution fails

Dashboards:

1.GenAI-Operations: shows Lambda invocations, errors, duration, throttles

2.GenAI-Cost: displays per‑model cost trend and request distribution

## High Availability & Disaster Recovery

1.All services are regional (us-east-1 by default) with automatic failover within AZs.

2.Data persisted in S3 and DynamoDB is replicated across 3 AZs.

3.For cross‑region DR (not implemented in this demo), you would:

（1）Enable S3 Cross‑Region Replication (CRR) for raw documents.

（2）Use DynamoDB global tables for cost logs.

（3）Replicate OpenSearch indices via snapshot/restore.

## Cost Optimization Notes

1.Lambda concurrency limits prevent runaway costs during load spikes.

2.SQS queues act as buffers so no direct invocation of Bedrock on every upload.

3.TTL on DynamoDB automatically removes old cost logs; Athena queries only scan necessary partitions.

4.OpenSearch Serverless capacity is set to `capacity.autoscaling = true` with a minimum of 2 OCUs.

**Related Documents**:

- [Deployment Overview](./Deployment-overview.md)
- [S3 Architecture](./S3%20Architecture.md)
- [SQS Architecture](./SQS%20Architecture.md)
- [CloudWatch Monitoring](./CloudWatch%20Monitoring.md)
- [Main README](./README.md)