# AWS Image Processing System (Lambda Functions)

#### 🌐 Language / 言語 / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

This project contains an image upload and processing system built on the AWS Serverless architecture. The core logic consists of three Lambda Functions.

Each Lambda plays a different role within the system, working together to complete:

Secure image upload, Asynchronous image processing, Processing result notification, System monitoring

This README file summarizes the functionality of the three Lambdas and the system architecture description.

### Main System Features:

- Fully serverless & autoscaling
- Asynchronous SQS decoupling
- S3 separated storage (original / processed images)
- Cognito secure upload
- CloudWatch metrics monitoring
- Production-grade scalable architecture

## Included Lambda Functions

The system contains 3 Lambdas:

1. `generate-upload-url`(Generates pre-signed URL for frontend)
2. `image-processor-lambda`(Background image processing → DynamoDB → SNS)
3. `s3-metrics-lambda`(S3 monitoring metrics → CloudWatch)

Detailed explanations follow:

###  1. Generate-Upload-URL Lambda

####  Functionality

Generates a pre-signed upload URL (PUT) for logged-in Cognito users.

Ensures each user's uploaded images are automatically placed into their dedicated directory.

The frontend uses this URL to upload images securely without exposing AWS keys.

####  Input (from API Gateway)

User identity (Cognito User ID) automatically passed by JWT authorizer.

####  Output

```
{
  "upload_url": "<PresignedURL>",
  "file_path": "user-uploads/<userId>/<uuid>.jpg"
}
```

####  Security Features

Can only be invoked by authenticated Cognito users.

S3 pre-signed URL validity is 5 minutes.

Ensures user isolation, preventing overwriting of others' files.

###  2. image-processor-lambda

The core processing Lambda of this system.

####  Functionality

- Receives messages from the SQS queue.
- Downloads the original image (S3).
- Uses Pillow to generate thumbnails.
- Uploads results to the processed bucket.
- Writes to DynamoDB (image metadata).
- Sends SNS notification emails.

####  Advantages of Backend Asynchronous Processing

- High concurrency
- Decoupling
- Lambda auto-scaling
- Each task is independent and does not block others.

####  Output (Example data written to DynamoDB)

```
{
  "imageId": "uuid",
  "originalS3Key": "user-uploads/xxx/xxx.jpg",
  "processedS3Key": "processed/uuid.jpg",
  "status": "DONE"
}
```

###  3. S3 Metrics Monitoring Lambda

####  Functionality

Periodically (configurable: 1 min, 5 min, 1 hour, etc.) statistics:

- S3 image count
- S3 total size (bytes)

And reports to CloudWatch:

- Namespace: `CustomS3`
- Metrics: `BucketSizeBytes` `NumberOfObjects`

####  Purpose

- Reporting
- Cost monitoring
- Enables CloudWatch alarm creation (e.g., S3 bucket is almost full).

####  Dependencies

Pure `boto3`, no additional libraries required.
