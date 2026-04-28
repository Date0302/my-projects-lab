# AWS Serverless Image Upload & Processing System

#### 🌐 Language / 言語 / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

This project is a high-performance, scalable image upload and processing system built on the AWS Serverless architecture. The core logic consists of three collaboratively working Lambda functions, implementing end-to-end functionality from secure upload and asynchronous processing to result notification and monitoring.

## System Architecture Overview

**Core Features**

- **Fully Serverless Architecture:** Based on managed services like Lambda, S3, and SQS; auto-scaling with no servers to manage.
- **Asynchronous Decoupled Design:** Separates upload and processing workflows using SQS Standard Queue, enhancing system reliability and resilience under load.
- **Secure Storage Separation:** Original and processed images are stored separately, with upload security ensured via Cognito authentication.
- **Production-Grade Observability:** Fully integrated with CloudWatch monitoring and SNS notifications for easy tracking and alerting.
- **Metadata Management:** Uses DynamoDB to store all image metadata for easy tracking and querying.

### Lambda Functions Detailed Explanation

The system includes the following three core Lambda functions:

#### 1. Generate-Upload-URL Lambda

**Functionality**

- Generates a secure S3 pre-signed upload URL (PUT method) for authenticated Cognito users.
- Automatically categorizes each user's uploaded images into their dedicated directory.

**Input/Output**

- **Input:** User identity (Cognito User ID) automatically passed via API Gateway's JWT authorizer.

- 

  **Output:**

  ```
  {
    "upload_url": "<PresignedURL>",
    "file_path": "user-uploads/<userId>/<uuid>.jpg"
  }
  ```

**Security Features**

- Can only be invoked by logged-in Cognito users.
- Pre-signed URL defaults to a 5-minute validity period to prevent misuse.
- Ensures user data security through directory isolation, preventing overwriting of others' files.

#### 2. Image Processor Lambda

This is the core processing unit of the system.

**Functionality**

- Receives image upload event messages from the SQS Standard Queue.
- Downloads the original image from the source S3 bucket.
- Performs image processing (e.g., generating thumbnails, format conversion) using the Pillow library.
- Uploads the processed results to the designated target S3 bucket.
- Writes processing status and metadata (e.g., image ID, S3 paths, status) to a DynamoDB table.
- Sends processing result notifications (success/failure) to an SNS topic.

**Advantages of Backend Asynchronous Processing**

- **High Concurrency Processing:** Leverages Lambda's auto-scaling capability to handle traffic fluctuations.
- **Decoupling & Reliability:** SQS acts as a buffer layer, ensuring tasks are not lost if the processing component fails.
- **Task Independence:** Each processing task is isolated; failure of a single task does not affect the overall system.

**Output Example (Written to DynamoDB)**

```
{
  "imageId": "uuid",
  "originalS3Key": "user-uploads/xxx/xxx.jpg",
  "processedS3Key": "processed/uuid.jpg",
  "status": "DONE",
  "lastModified": "2023-10-01T12:00:00Z"
}
```

#### 3. S3 Metrics Monitoring Lambda

**Functionality**

- Periodically (configurable, e.g., 1 minute, 5 minutes, 1 hour) statistics the size and object count of a specified S3 bucket.
- Reports custom metrics (e.g., `BucketSizeBytes`, `NumberOfObjects`) to CloudWatch.

**Purpose**

- **Cost Monitoring & Reporting:** Monitors storage growth trends to support cost optimization.
- **Proactive Alerting:** Set CloudWatch alarms based on metrics (e.g., storage capacity thresholds).

**Dependencies**

- Uses only the `boto3`SDK, with no additional third-party library dependencies.

## Monitoring & Operations

The system is fully integrated with CloudWatch for comprehensive monitoring:

- View execution logs, duration, and error rates for each Lambda function.
- Set alarms in the CloudWatch console based on custom metrics (metrics under the `CustomS3`namespace).
- Receive processing success or failure messages via SNS notifications.
