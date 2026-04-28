# Security Orchestration Lambda Function

#### 🌐 言語 / Language / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

## 概要

This Lambda function serves as the central security orchestration layer in the AWS Security Automation Project. It receives security-related events from multiple AWS services, performs centralized logging, sends alerts, and triggers automated response workflows using AWS Step Functions.

## Supported Event Sources

This Lambda is triggered by Amazon EventBridge and supports the following security event types:

| Source Service   | Event Type                  | Description                                         |
| ---------------- | --------------------------- | --------------------------------------------------- |
| Amazon GuardDuty | GuardDuty Security Finding  | Unauthorized access, cryptocurrency mining activity |
| Amazon Inspector | Inspector2 Security Finding | Critical vulnerability discoveries                  |
| AWS CloudTrail   | AWS API Call via CloudTrail | Risky IAM policy changes                            |
| Amazon Macie     | Macie Security Finding      | Sensitive data exposure/public S3 access            |

## Core Responsibilities

### 1. Centralized Event Processing

- Identifies event sources and types
- Classifies security incidents

### 2. Security Event Logging

- Stores structured JSON logs in Amazon S3
- Supports downstream analysis via Athena and QuickSight

### 3. Security Alert Notification

- Sends real-time alerts for each processed event
- Alerts include event source, type, and processing results

------

### 4. Automated Response Orchestration

Based on the event type, the Lambda triggers dedicated AWS Step Functions state machines for further automated remediation.

| Incident Type              | Step Functions State Machine |
| -------------------------- | ---------------------------- |
| Unauthorized Access        | SFN-UnauthorizedAccess       |
| Cryptocurrency Mining      | SFN-CryptoMining             |
| Inspector Critical Finding | SFN-InspectorCritical        |
| IAM Policy Change          | SFN-IAMPolicyChange          |
| Macie Sensitive Data       | SFN-MacieSensitiveData       |

⚠ Remediation actions within Step Functions are **intentionally implemented as placeholders** to demonstrate architectural design rather than modify production environment resources.

## IAM Permissions

The Lambda execution role requires the following permissions:

- Amazon S3: `PutObject`
- Amazon SNS: `Publish`
- AWS Step Functions: `StartExecution`
- Amazon CloudWatch Logs: Basic logging permissions

## Design Notes

- This Lambda is designed as a single-entry security control point
- Emphasizes observability, auditability, and extensibility
- Separates detection, orchestration, and remediation logic
- Suitable for SOC-style security monitoring and analysis use cases
