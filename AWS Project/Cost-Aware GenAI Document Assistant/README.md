# README

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

This project is a cost-aware intelligent document QA system built on AWS serverless architecture. The core innovation is dynamically routing queries to AI models of different costs based on question complexity, while tracking, analyzing, and visualizing cost as a first-class citizen – perfectly demonstrating the architect's art of trade-offs between functionality, performance, and cost.

## Core Features

- Fully Serverless: Built on managed services like Lambda, API Gateway, S3, DynamoDB – auto-scaling, zero server management
- Cost-Aware Dynamic Routing: Intelligently selects LLM models (Titan Lite vs. Claude 3) based on question complexity, significantly reducing inference cost without compromising user experience
- RAG (Retrieval-Augmented Generation): Uses OpenSearch Serverless for semantic search, enabling AI to answer questions based on enterprise private documents
- Production-Grade Observability: Complete tracking of model, token count, and cost per invocation, visualized via QuickSight + alerts via CloudWatch
- Security & Compliance: Cognito authentication, S3 encryption, API Gateway throttling and CORS control
- Reliability Design: Step Functions retries and DLQ (Dead Letter Queue), DynamoDB TTL auto-cleanup

## Why This Project?

As a Solutions Architect candidate, I need to not only "build" systems but also make well-reasoned architectural decisions. One of the biggest pain points for enterprises adopting Generative AI is uncontrolled inference cost – blindly calling the most powerful model (e.g., Claude 3) for every request leads to cost explosion, while using low-cost models for everything may sacrifice answer quality for complex questions.

This project solves this contradiction through dynamic routing: the system automatically identifies question types, routes simple high-frequency questions to a low-cost path and complex reasoning questions to a high-quality path, while making cost visible – providing data-driven cost optimization recommendations to business stakeholders. This is exactly the core value of a Solutions Architect.

## Detailed Component Breakdown

### 1. Data Ingestion Pipeline

| Component              | Technology Choice                 | Design Decision                                              |
| ---------------------- | --------------------------------- | ------------------------------------------------------------ |
| Document Upload        | API Gateway + S3 (raw bucket)     | Uses pre-signed URL pattern to avoid security risks of frontend directly writing to S3 |
| Workflow Orchestration | AWS Step Functions                | Supports retries, error handling, visual debugging – more robust than plain Lambda chaining |
| Text Processing        | Lambda (Python + PyPDF2/chardet)  | Serverless, pay-per-invocation, automatically handles multiple document formats |
| Vectorization          | Amazon Bedrock - Titan Embeddings | Unified ecosystem with other Bedrock models, low cost (~$0.0001/1K tokens) |
| Vector Storage         | Amazon OpenSearch Serverless      | No cluster management, auto-scaling, native support for vector search and metadata filtering |

**Key Design**: S3 events cannot directly trigger Step Functions; an EventBridge or Lambda bridge is used in between (implied in the architecture diagram).

### 2. Query & Cost-Aware Pipeline

This is the core decision layer of the system.

| Component             | Technology Choice                                            | Design Decision                                              |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| User Authentication   | Amazon Cognito                                               | Managed user pool, natively integrates with API Gateway, out-of-the-box JWT validation |
| Query Entry           | API Gateway (REST + WebSocket)                               | REST for single requests, WebSocket reserved for future streaming responses |
| Core Orchestrator     | Lambda (Orchestrator)                                        | Hosts all business logic: retrieval, complexity judgment, model routing, cost logging |
| Semantic Search       | OpenSearch Serverless vector search                          | Returns Top-K most relevant document chunks as context       |
| Model Routing Logic   | Rule-based (question length / keywords) + extensible to lightweight classifier | Initial rules: question < 20 chars or contains "what is/definition" etc. → low-cost path; contains "why/compare/analyze" or long questions → high-capability path |
| Low-Cost Model        | Amazon Bedrock - Titan Text G1‑Lite                          | Fast inference, cost ~$0.0003/1K input tokens, suitable for factual QA |
| High-Capability Model | Amazon Bedrock - Claude 3 Haiku/Sonnet                       | Strong reasoning, supports complex logic, cost ~$0.0025/1K input tokens (~8x Titan) |
| Cost Logging          | Amazon DynamoDB                                              | High write throughput, TTL auto-cleanup, records timestamp, model, token count, estimated cost per invocation |

**Input/Output Example** (Orchestrator Lambda):

```json
// Input (user question)
{
  "userId": "user123",
  "question": "Please explain what a Service Level Agreement (SLA) is?"
}

// Output (system response)
{
  "answer": "A Service Level Agreement (SLA) is a formal commitment between a service provider and a customer...",
  "model_used": "amazon.titan-text-lite",
  "cost_estimate_usd": 0.00021,
  "latency_ms": 520
}
```

### 3. Cost Analytics Pipeline

| Component               | Technology Choice              | Design Decision                                              |
| ----------------------- | ------------------------------ | ------------------------------------------------------------ |
| Cost Data Lake          | DynamoDB export → S3 (Parquet) | DynamoDB exports by time partition, converted to Parquet for efficient Athena queries |
| Serverless Query        | Amazon Athena                  | Standard SQL analysis of cost logs, no cluster to provision  |
| Visualization Dashboard | Amazon QuickSight              | Managed BI tool, supports auto-refresh and row-level security |
| Budget Alert            | CloudWatch + SNS               | Monitors daily cumulative cost, triggers email/SMS when threshold exceeded (e.g., $5/day) |

**Dashboard Key Metrics**:
- Last 7 / 30 day total cost trend
- Invocation count and cost share by model
- Ratio of simple vs. complex questions
- Average cost per request (for ROI reporting to business)

## Architectural Trade-offs and Design Decisions

As a Solutions Architect portfolio project, the following key trade-offs are **explicitly documented**:

| Decision Point            | Option A                          | Option B                        | Final Choice                    | Justification                                                |
| ------------------------- | --------------------------------- | ------------------------------- | ------------------------------- | ------------------------------------------------------------ |
| Model Routing Strategy    | Always use Claude 3               | Dynamic rule-based routing      | Dynamic routing                 | Reduces cost by 70-80%, and 80% of daily questions can be handled by low-cost model |
| Vector Database           | Aurora PG with pgvector           | OpenSearch Serverless           | OpenSearch Serverless           | No cluster management, more natural integration with Bedrock, pay-per-request pricing |
| Real-time Requirement     | Synchronous wait for LLM response | Asynchronous polling            | Synchronous                     | QA scenarios are latency-sensitive (target <2s), synchronous is acceptable and simpler to implement |
| Cost Tracking Granularity | Aggregate daily cost only         | Per-invocation detailed logging | Per-invocation detailed logging | Provides fine-grained cost attribution for subsequent optimization (e.g., identifying most expensive users or question types) |

## AWS Services Used

| Category                | Services                                                     |
| ----------------------- | ------------------------------------------------------------ |
| Compute & Orchestration | AWS Lambda, AWS Step Functions                               |
| API & Security          | Amazon API Gateway, Amazon Cognito                           |
| Storage                 | Amazon S3, Amazon DynamoDB                                   |
| AI/ML                   | Amazon Bedrock (Titan Embeddings, Titan Text, Claude 3), Amazon OpenSearch Serverless |
| Analytics               | Amazon Athena, Amazon QuickSight                             |
| Monitoring & Alerting   | Amazon CloudWatch, Amazon SNS                                |
| Event Integration       | Amazon EventBridge (bridges S3 to Step Functions)            |

## Monitoring & Operations

The system has integrated CloudWatch for comprehensive monitoring:
- View execution logs, duration, error rates, throttling counts for each Lambda function
- Set alerts based on custom cost metrics (e.g., `TotalDailyCost` exceeding $10) in CloudWatch console
- Step Functions workflow visual tracing for document processing status
- X-Ray distributed tracing (optional) for analyzing end-to-end latency bottlenecks

## How to Run (Overview)

1. Deploy all resources with one click using AWS CDK or Terraform (IaC template provided)
2. Create a test user in Cognito and obtain a JWT Token
3. Upload a document via API Gateway (POST /documents)
4. Ask a question via API Gateway (POST /query) with the JWT Token
5. Wait 30 seconds (for vectorization to complete), then ask again to get an answer based on the document
6. Open the cost dashboard in QuickSight to observe cost distribution across different model paths
7. Set a CloudWatch budget threshold and verify SNS alerting

## Project Status

This project has been completed as a Solutions Architect portfolio project. All code, IaC templates, architecture diagrams, and demo videos are available in the repository. Cost data is based on real estimates using Bedrock on-demand pricing.