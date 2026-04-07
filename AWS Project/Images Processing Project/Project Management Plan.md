# Images Processing Project – Project Management Plan

#### 🌐 Language / 言語 / 语言

 US English: [Project Management Plan.md](Project Management Plan.md)                                                JP 日本語: [Project Management Plan.ja.md](Project Management Plan.ja.md)                                         CN 中文: [Project Management Plan.zh-CN.md](Project Management Plan.zh-CN.md)

**Project Name**: Images Processing Project

**Project Manager**: Project Owner

**Project Sponsor**: Self

**Document Version**: 1.0

**Creation Date**: 2026-04-05

## 1. Project Charter

| Project Name         | Cloud-Native Image Processing Architecture                   |
| -------------------- | ------------------------------------------------------------ |
| Project Objectives   | Build an end-to-end automated flow for image upload, processing, storage, and notification using AWS serverless technologies, improving scalability and reducing operational costs. |
| Key Success Criteria | 1. Automatic processing triggered after image upload<br>2. System handles concurrent requests smoothly<br>3. All data access follows least-privilege principle<br>4. Storage cost controlled via lifecycle policies |
| Project Manager      | Project Owner                                                |
| Project Sponsor      | Self                                                         |
| Approval Date        | 2026-04-01                                                   |

## 2. Project Objectives & Scope

### 2.1 Project Objectives

- Automate image upload and processing
- Improve system scalability and stability
- Reduce manual operations and maintenance costs
- Ensure secure data access

### 2.2 Project Scope

**In Scope**:
- Image upload module (API Gateway + Lambda + S3)
- Image processing module (compression, watermarking)
- Message queue and event-driven flow (SQS decoupling)
- Data storage and lifecycle management (S3 + DynamoDB)
- User authentication and access control (Cognito + IAM)
- Processing completion notifications (SNS)

**Out of Scope**:
- Frontend UI (API only)
- AI/ML image recognition
- Video processing
- On-premise or hybrid cloud deployment

## 3. Key Stakeholders

| Role             | Responsibility                                    | Communication Method                       |
| ---------------- | ------------------------------------------------- | ------------------------------------------ |
| Project Manager  | Overall planning, architecture design, deployment | Daily self-check                           |
| End Users        | Use image upload API                              | No direct contact (simulated via API logs) |
| Security Auditor | Review IAM policies, Cognito config               | Periodic self-audit                        |
| Cost Manager     | Monitor AWS billing, optimize resources           | Weekly Budgets check                       |

## 4. Assumptions & Constraints

### 4.1 Assumptions

- User network can access AWS services normally
- Only common image formats (JPEG, PNG) are processed
- AWS free tier or low-cost account, no budget approval needed
- Lambda max execution time of 15 minutes is sufficient for typical images

### 4.2 Constraints

- No EC2 or Kubernetes; serverless services only
- No GPU acceleration
- No support for very large files (>1GB)
- Single-person development, no dedicated testing team

## 5. Architecture Overview

- S3: raw bucket + processed bucket
- API Gateway + Lambda: upload endpoint
- SQS: asynchronous decoupling, peak smoothing
- Lambda (processing): compression, watermarking
- SNS: send completion notifications
- DynamoDB: store image metadata (filename, size, processing time, status)
- Cognito: user authentication + temporary credentials
- IAM + Security Boundary: least-privilege isolation

## 6. Key Deliverables

| ID   | Deliverable                       | Description                             |
| ---- | --------------------------------- | --------------------------------------- |
| D1   | Architecture diagram              | PDF + draw.io file                      |
| D2   | Upload API code                   | Lambda + API Gateway configuration      |
| D3   | Image processing function code    | Compression & processing Lambda         |
| D4   | SQS queue configuration           | Standard queue + DLQ                    |
| D5   | SNS topic configuration           | Email/HTTP endpoint notifications       |
| D6   | DynamoDB table design             | Metadata schema                         |
| D7   | Cognito user pool & identity pool | Authentication flow                     |
| D8   | IAM policy set                    | Service roles and boundaries            |
| D9   | S3 lifecycle rules                | Standard → IA → Glacier                 |
| D10  | Deployment scripts                | CloudFormation or Terraform             |
| D11  | Test report                       | Functional, security, performance tests |
| D12  | Project documentation             | This PMP document                       |

## 7. Risk Management

| Risk                                           | Impact | Mitigation                                               |
| ---------------------------------------------- | ------ | -------------------------------------------------------- |
| High concurrency causes system pressure        | High   | SQS smoothing, Lambda concurrency reservations           |
| Misconfigured permissions leading to data leak | High   | IAM least privilege + Security Boundary + regular audits |
| Message processing failure or loss             | Medium | SQS DLQ + retry mechanism + failure alarms               |
| Excessive storage cost                         | Medium | S3 lifecycle policies (Standard → IA → Glacier)          |
| Lambda execution timeout                       | Low    | Limit image size or split into multiple steps            |

## 8. Cost Management

- Compute: Lambda only (pay per invocation and duration), no cost when idle
- Storage: S3 tiering + DynamoDB on-demand
- Notifications: SNS (first 1M requests/month free)
- Queue: SQS (first 1M requests/month free)
- Monitoring: CloudWatch free tier sufficient
- Optimization: Set AWS Budgets alerts to prevent overspending

## 9. Quality Management

### 9.1 Testing Strategy

| Test Type         | Scope                                          | Tools/Methods            |
| ----------------- | ---------------------------------------------- | ------------------------ |
| Unit tests        | Lambda functions                               | Python unittest          |
| Integration tests | API → S3 → SQS → Lambda → SNS                  | AWS CLI                  |
| Security tests    | IAM permissions, Cognito temporary credentials | AWS IAM Policy Simulator |
| Performance tests | Simulate 100 concurrent uploads                | Artillery / Locust       |
| Observability     | Logs, errors, latency                          | CloudWatch Logs + X-Ray  |

### 9.2 Acceptance Criteria

- 99% of images processed within 30 seconds after upload
- No IAM privilege escalation warnings
- SQS DLQ correctly receives messages after 3 failures
- All API requests require Cognito authentication

## 10. Monitoring & Operations

### 10.1 Monitoring Metrics

- Lambda invocations, error rate, duration
- SQS queue length (visible + invisible messages)
- S3 bucket size and request count
- DynamoDB read/write capacity usage
- CloudWatch alarm thresholds:
  - Lambda error rate > 5%
  - SQS backlog > 100 messages for 5 minutes

### 10.2 Logging & Tracing

- All Lambda logs output to CloudWatch Logs
- Enable X-Ray for critical request tracing
- Periodically export logs to S3 for long-term audit

### 10.3 Disaster Recovery

- S3 cross-region replication (optional, cost-dependent)
- DynamoDB on-demand backup (weekly)
- Metadata rebuildable: rescan S3 buckets to regenerate DynamoDB records

## 11. Security Policy

- User authentication: Cognito user pool + identity pool
- Temporary credentials: via Cognito, restricted to specific S3 prefixes
- IAM roles:
  - API call role: only write to raw S3 bucket + send to SQS
  - Processing function role: only read raw bucket, write processed bucket, write DynamoDB, publish SNS
  - Security boundary: explicit resource ARNs, no wildcard `*`
- Encryption: S3 server-side encryption (SSE-S3), DynamoDB default encryption

## 12. Project Outcomes

- Built a highly scalable image processing architecture
- Achieved automated upload, processing, and notification flow
- Improved system stability under high concurrency
- Controlled costs while maintaining performance
- All deliverables completed, meeting personal learning and demonstration goals

## 13. Future Enhancements

- Support asynchronous image format conversion (WebP, AVIF)
- Integrate Amazon Rekognition for content moderation
- Add API rate limiting (AWS WAF + API Gateway Usage Plan)
- Provide frontend SDK examples (React / Vue)
- Use Step Functions to orchestrate complex processing workflows