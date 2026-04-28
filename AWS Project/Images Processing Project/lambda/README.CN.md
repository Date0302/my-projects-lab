# AWS Image Processing System (Lambda Functions)

#### 🌐 Language / 言語 / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

本项目包含构建在 AWS Serverless 架构上的 图像上传与处理系统，核心逻辑由三个 Lambda Functions 组成。
每个 Lambda 在整个系统中承担不同职责，协同完成：

安全上传图片，异步图像处理，处理结果通知，系统监控

本 README 文件将汇总三个 Lambda 的功能与系统架构说明。

### 系统主要特点：

完全 serverless & autoscaling

异步 SQS 解耦

S3 分离存储（原图 / 处理图）

Cognito 安全上传

CloudWatch 指标监控

生产级可扩展架构

## 包含的 Lambda Functions

系统内共有 3 个 Lambda：

1. generate-upload-url         （生成预签名 URL 给前端）
2. image-processor-lambda      （后台图像处理 → DynamoDB → SNS）
3. s3-metrics-lambda           （S3 监控指标 → CloudWatch）


详细说明如下：

###  1. GenerateUploadURL Lambda

####  功能

给已登录的 Cognito 用户生成 预签名上传 URL（PUT）

确保每个用户上传的图片都会自动放入其专属目录

前端通过此 URL 安全地上传图片，不需要暴露 AWS 秘钥

####  输入（来自 API Gateway）

JWT authorizer 自动传递用户身份（Cognito User ID）

####  输出

{
  "upload_url": "<PresignedURL>",
  "file_path": "user-uploads/<userId>/<uuid>.jpg"
}

####  安全特性

只能经过 Cognito 登录用户调用

S3 预签名 URL 有效期 5 分钟

保证用户隔离，不会覆盖他人文件

###  2. image-processor-lambda

本系统的核心处理 Lambda。

####  功能

从 SQS 队列接收消息

下载原始图片（S3）

使用 Pillow 生成缩略图

上传结果到 processed bucket

写入 DynamoDB（图像元数据）

发送 SNS 通知邮件

####  后端异步处理优势

高并发

去耦

Lambda 自动扩容

每个任务独立，不会互相阻塞

####  输出（写入 DynamoDB 的数据示例）

{
  "imageId": "uuid",
  "originalS3Key": "user-uploads/xxx/xxx.jpg",
  "processedS3Key": "processed/uuid.jpg",
  "status": "DONE"
}

###  3. S3 Metrics Monitoring Lambda

####  功能

定时（1 分钟、5 分钟、1 小时任意）统计：

S3 图像数量

S3 总大小（bytes）

并上报到 CloudWatch：

Namespace: CustomS3
Metrics:

  - BucketSizeBytes
  - NumberOfObjects

####  用途

做报表

做成本监控

让 CloudWatch 可以创建告警（如 S3 快满了）

####  依赖

纯 boto3，无需额外库。