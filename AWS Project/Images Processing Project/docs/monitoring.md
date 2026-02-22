# Monitoring Strategy

#### 🌐 言語 / Language / 语言

 英語: [monitoring.md](monitoring.md)                                               日本語: [monitoring.ja.md](monitoring.ja.md)

## Monitoring Tools

The system uses Amazon CloudWatch for monitoring and observability.

## Key Metrics

### Lambda Metrics

- Duration
- Invocations
- Errors
- Throttles
- Max Memory Used

### SQS Metrics

- ApproximateNumberOfMessagesVisible
- ApproximateAgeOfOldestMessage

## Logging

All Lambda executions generate logs in CloudWatch Logs.

Logs include:

- execution start
- image processing status
- error messages
- duration

Logs help with debugging and root cause analysis.

## Operational Visibility

Using CloudWatch enables:

- real-time monitoring
- failure detection
- performance tracking
- resource utilization analysis

## Recommended Enhancements

For production environments:

- Add CloudWatch alarms
- Enable X-Ray tracing
- Configure Dead Letter Queue (DLQ)
- Implement structured logging

## Reliability Strategy

The system is resilient due to:

- SQS message durability
- Lambda retry mechanism
- CloudWatch observability

This ensures high availability and maintainability.