# Cost-Aware GenAI Document Assistant – Project Management Plan

**Project Name**: Cost-Aware GenAI Document Assistant  

**Project Manager**: Project Owner  

**Project Sponsor**: Self  

**Document Version**: 1.0  

**Creation Date**: 2026-06-02  

## 1. Project Charter

| Project Name         | Cost-Aware GenAI Document Assistant                          |
| -------------------- | ------------------------------------------------------------ |
| Project Objectives   | Build an intelligent document QA system on AWS serverless architecture, dynamically routing queries to LLM models of different costs based on question complexity, achieving optimal balance of functionality, performance, and cost, with visualized cost tracking and analysis. |
| Key Success Criteria | 1. Automated document upload and vectorization pipeline<br>2. Dynamic selection of low-cost or high-capability models based on question complexity<br>3. Token count and cost per invocation traceable and visualized<br>4. Cost reduction ≥70% compared to always using the highest-capability model<br>5. User response latency <2 seconds, answer quality meeting common QA needs |
| Project Manager      | Project Owner                                                |
| Project Sponsor      | Self                                                         |
| Approval Date        | 2026-05-20                                                   |

## 2. Project Objectives & Scope

### 2.1 Project Objectives

- Build a fully serverless, auto-scaling document QA system
- Implement dynamic model routing (low-cost Titan vs. high-capability Claude 3) based on question complexity
- Provide comprehensive cost tracking and visualization dashboard
- Ensure data security and user authentication
- Serve as a Solutions Architect portfolio project demonstrating architectural trade-offs and decision-making

### 2.2 Project Scope

**In Scope**:
- Document upload and processing pipeline (API Gateway → S3 → Step Functions → text extraction → vectorization → OpenSearch)
- Query and routing pipeline (Cognito authentication → API Gateway → Orchestrator Lambda → semantic search → model routing → answer generation)
- Cost tracking pipeline (record model, token count, estimated cost per invocation to DynamoDB)
- Cost analysis and visualization (DynamoDB export → Athena → QuickSight)
- Monitoring and alerting (CloudWatch logs, custom cost metrics, SNS alerts)
- Security design (IAM least privilege, S3 encryption, API Gateway throttling)

**Out of Scope**:
- Multi-turn conversation context memory (single-turn QA only)
- Real-time streaming responses (WebSocket reserved but not implemented)
- Complex custom model fine-tuning
- Support for non-text files (e.g., audio/video)
- Production-grade multi-region deployment

## 3. Key Stakeholders

| Role                                  | Responsibility                                               | Communication Method              |
| ------------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| Project Manager (Self)                | Overall architecture design, deployment, testing             | Daily self-check                  |
| End Users (simulated)                 | Upload documents, ask questions                              | Simulated via API testing tools   |
| Cost Manager (Self)                   | Monitor AWS costs, optimize model routing thresholds         | Weekly QuickSight dashboard check |
| Security Auditor (simulated)          | Review IAM policies, Cognito configuration                   | Periodic self-audit               |
| Potential Employer/Portfolio Reviewer | Evaluate architectural decisions and documentation completeness | Project showcase                  |

## 4. Assumptions & Constraints

### 4.1 Assumptions

- AWS account has Bedrock model access enabled (Titan, Claude 3)
- Document formats limited to PDF, TXT, common office documents (processed via PyPDF2/chardet)
- User questions primarily in English; complexity rules based on keywords and length
- OpenSearch Serverless vector search returning Top‑K relevant chunks is sufficient for QA needs
- Cost estimates based on Bedrock on-demand pricing; actual deviation within ±20%

### 4.2 Constraints

- Single-person implementation, no dedicated data science or operations team
- All services deployed in a single AWS region
- Lambda execution timeout 15 minutes, but document processing expected within seconds
- Vectorization uses Titan Embeddings; no switching to other embedding models
- No third-party LLMs or external APIs

## 5. Architecture Overview

Based on provided documents and diagrams, the system consists of three core pipelines:

### 5.1 Data Ingestion Pipeline (Document Processing)

- **Document Upload**: API Gateway + S3 (raw bucket), pre-signed URLs for security
- **Workflow Orchestration**: S3 event → EventBridge → Step Functions (retry, visual debugging)
- **Text Extraction**: Lambda (Python + PyPDF2/chardet) parses document content
- **Vectorization**: Calls Bedrock Titan Embeddings model to generate vectors
- **Vector Storage**: OpenSearch Serverless (auto-scaling, supports semantic search and metadata filtering)

### 5.2 Query & Cost-Aware Pipeline (Core)

- **User Authentication**: Amazon Cognito User Pool, JWT validation
- **Query Entry**: API Gateway (REST)
- **Core Orchestration**: Orchestrator Lambda
  - Semantic search: OpenSearch returns relevant document chunks
  - Complexity judgment: rule-based (question length, keywords)
  - Model routing: simple questions → Titan Text G1‑Lite (low cost); complex questions → Claude 3 Haiku/Sonnet (high capability)
  - Cost logging: writes to DynamoDB (model, token count, estimated cost)
- **Response**: answer + model used + cost estimate + latency

### 5.3 Cost Analytics Pipeline

- **Cost Data Lake**: DynamoDB time-partitioned export to S3 (Parquet format)
- **Serverless Query**: Amazon Athena for SQL analysis
- **Visualization Dashboard**: Amazon QuickSight (total cost trend, model share, simple/complex question ratio, average cost per request)
- **Budget Alert**: CloudWatch monitors daily cumulative cost → SNS notification (threshold $5/day)

## 6. Key Deliverables

|  ID  | Deliverable                                   | Description                                             |
| :--: | --------------------------------------------- | ------------------------------------------------------- |
|  D1  | Architecture diagram                          | draw.io / PDF file                                      |
|  D2  | Document processing Step Functions definition | State machine JSON                                      |
|  D3  | Text extraction Lambda code                   | Python + PyPDF2/chardet                                 |
|  D4  | Vectorization Lambda code                     | Calls Bedrock Titan Embeddings                          |
|  D5  | OpenSearch Serverless index configuration     | Vector mapping and metadata fields                      |
|  D6  | Orchestrator Lambda code                      | Retrieval + routing + cost logging                      |
|  D7  | Model routing rule configuration              | Configurable thresholds and keyword lists               |
|  D8  | DynamoDB cost log table                       | Table schema + TTL policy                               |
|  D9  | Athena views and QuickSight dashboard         | SQL definitions + visual panels                         |
| D10  | CloudWatch cost alert rules                   | Custom metrics + SNS topic                              |
| D11  | IAM security policy set                       | Least-privilege roles per component                     |
| D12  | IaC deployment scripts                        | AWS CDK or Terraform templates                          |
| D13  | Test report                                   | Functional, routing accuracy, cost reduction validation |
| D14  | Operations manual                             | Troubleshooting, log queries, cost optimization         |
| D15  | Project documentation                         | This PMP document                                       |

## 7. Risk Management

| Risk                                                         | Impact | Mitigation                                                   |
| ------------------------------------------------------------ | ------ | ------------------------------------------------------------ |
| High Bedrock model latency affecting user experience         | Medium | Set API Gateway timeouts and retries; monitor p99 latency; switch to faster model if persistent |
| Inaccurate complexity rules causing overuse of high-cost model | Medium | Initial heuristic rules with extension path (replaceable with lightweight classifier); regularly analyze cost logs to adjust thresholds |
| Irrelevant vector search results, poor answer quality        | Medium | Optimize chunking strategy and metadata filtering; increase Top-K or add reranking as future enhancement |
| OpenSearch Serverless cost overrun                           | Low    | Use on-demand capacity mode; monitor OCU usage; set index retention policies |
| Rapid growth of DynamoDB cost logs                           | Low    | TTL auto-cleanup (e.g., 90 days); export to S3 Glacier for long-term archive |
| Unauthorized access leading to sensitive document leakage    | High   | Cognito mandatory authentication + API Gateway authorizer + S3 bucket policy blocking public access; IAM least privilege |

## 8. Cost Management

### 8.1 Cost Components

- **Compute costs**: Lambda invocations (document processing, Orchestrator), Step Functions state transitions
- **AI model costs**: Bedrock (Titan Embeddings, Titan Text, Claude 3) – pay per input/output token
- **Storage costs**: S3 (raw documents + processed data), OpenSearch Serverless (vector index), DynamoDB (logs)
- **Query costs**: Athena – pay per data scanned
- **Visualization**: QuickSight Standard edition – per user (single user within free tier)
- **Other**: API Gateway, CloudWatch, SNS (within free tier limits)

### 8.2 Optimization Strategies

- Dynamic routing: ~80% of simple questions go to Titan Lite, cost ~1/8 of Claude 3
- S3 lifecycle: raw documents transition to IA after 30 days, to Glacier after 90 days
- DynamoDB TTL auto-deletes logs older than 90 days
- OpenSearch on-demand capacity – no charge when idle
- Set AWS Budgets alert; control monthly cost within $10 (for demonstration)

## 9. Quality Management

### 9.1 Testing Strategy

| Test Type             | Scope                                                        | Tools/Methods                       |
| --------------------- | ------------------------------------------------------------ | ----------------------------------- |
| Unit tests            | Text extraction, routing logic                               | Python unittest / pytest            |
| Integration tests     | Document upload → vectorization → query → cost logging       | Simulated events + AWS CLI          |
| Routing accuracy test | Validate model selection for 50 predefined questions         | Manual labeling + automation script |
| Performance test      | Simulate 10 concurrent queries, measure latency and cost     | Artillery / Locust                  |
| Cost validation       | Compare estimated costs with actual AWS Cost Explorer        | Analysis report                     |
| Security tests        | IAM privilege escalation attempts, unauthenticated Cognito access | IAM Policy Simulator                |

### 9.2 Acceptance Criteria

- Document vectorized and searchable within 30 seconds of upload
- Median query response time <1.5 sec, p99 <3 sec
- Simple questions routed to Titan Lite ≥90%; complex questions routed to Claude 3 ≥95%
- Total cost reduction ≥70% compared to always using Claude 3
- All API requests require valid JWT
- Cost dashboard correctly displays daily and per-model cost trends

## 10. Monitoring & Operations

### 10.1 Monitoring Metrics

- Lambda: invocations, error rate, duration, throttles
- Step Functions: execution failure rate, step durations
- OpenSearch: query latency, OCU usage
- Bedrock: model invocation count, token count, throttling errors
- DynamoDB: write throughput, storage size
- Custom cost metrics: `TotalDailyCost`, `CostPerModel` published to CloudWatch

### 10.2 Logging & Tracing

- All Lambda logs output to CloudWatch Logs
- Step Functions optionally enable X-Ray tracing
- Periodically export CloudTrail logs to S3 for auditing

### 10.3 Alert Rules

| Metric                         | Threshold         | Action           |
| ------------------------------ | ----------------- | ---------------- |
| Orchestrator Lambda error rate | >5% for 2 minutes | SNS email alert  |
| Daily cumulative cost          | >$5               | SNS email+SMS    |
| OpenSearch query latency p99   | >2 seconds        | CloudWatch alarm |
| SQS DLQ (if any) non-empty     | >0                | SNS alert        |

### 10.4 Disaster Recovery

- All IaC templates version-controlled in Git
- DynamoDB on-demand backup (weekly)
- OpenSearch index rebuildable by reprocessing raw document S3 bucket
- Critical configurations (IAM, API Gateway) under version control

## 11. Security Policy

- **Authentication**: Amazon Cognito User Pool + API Gateway JWT authorizer
- **Data Encryption**: S3 default SSE-S3, OpenSearch node-to-node encryption, DynamoDB default encryption
- **Transport Security**: API Gateway enforces HTTPS; all service calls use TLS
- **IAM Least Privilege**:
  
  1.Orchestrator Lambda role: read OpenSearch, invoke Bedrock, write DynamoDB, publish SNS
  
  2.Document processing Lambda role: read raw S3 bucket, invoke Bedrock Embeddings, write OpenSearch
  
  3.Cost export role: read DynamoDB, write S3, invoke Athena
- **Network Isolation**: OpenSearch Serverless VPC endpoint (optional, as needed)
- **Input Validation**: API Gateway request size limits; Lambda validates file type and size

## 12. Project Outcomes

- Successfully built a cost-aware GenAI document QA system on fully serverless architecture
- Implemented dynamic model routing, achieving ~75% cost reduction in tests while maintaining answer quality
- Provided end-to-end cost visualization and alerting, making cost a first-class citizen
- All deliverables completed; can serve as a core portfolio project for a Solutions Architect
- Demonstrated systematic documentation of architectural trade-offs (routing strategy, vector database selection, real-time design)

## 13. Future Enhancements

- Upgrade rule-based routing to a lightweight classifier (e.g., SageMaker-hosted small BERT) for higher accuracy
- Support multi-turn conversations with context memory (introduce DynamoDB session storage)
- Add reranking stage to RAG for better answer relevance
- Integrate enterprise SSO (e.g., SAML or OIDC) instead of Cognito User Pool
- Support multilingual documents and cross-lingual retrieval (use multilingual embedding models)
- Use Amazon Bedrock Agent to further simplify complex task orchestration