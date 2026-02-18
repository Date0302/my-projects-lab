# Deployment

## 0. Prerequisites

AWS Account (Organizations enabled)

Region: ap-northeast-1 (Tokyo)

Basic experience with IAM / Lambda / S3 / Athena operations

## 1. Enable Security Services (Data Source Preparation)

### 1.1 Enable GuardDuty

Open Amazon GuardDuty

Select region `ap-northeast-1`

Click Enable GuardDuty

GuardDuty generates security events such as UnauthorizedAccess and CryptoMining.

### 1.2 Enable Inspector v2

Open Amazon Inspector

Enable Inspector v2

Select EC2 / ECR / Lambda scanning

Inspector Critical Findings will serve as security event inputs.

### 1.3 Enable Macie

Open Amazon Macie

Enable Macie

Macie Findings are used to detect sensitive data or public access risks in S3.

## 2. CloudTrail and S3 Log Storage

### 2.1 Enable CloudTrail

Open AWS CloudTrail

Create a Trail (Management events enabled by default)

Store logs in a specified S3 Bucket

### 2.2 Verify S3 Logs

Navigate to the S3 Bucket

Confirm that CloudTrail `.json.gz` files exist

These logs will serve as the data source for Athena queries.

## 3. Athena Log Query (Audit Layer)

### 3.1 Create Athena Table

Open Amazon Athena

Select a database (or create a new one)

Execute `create_table_cloudtrail.sql`

This step maps CloudTrail logs into a queryable structure.

### 3.2 Execute Security Audit Queries

Run sample SQL queries (e.g., IAM / API call queries)

Confirm the Query status is "Query successful"

Even if zero rows are returned, it indicates the query is configured correctly.

## 4. SNS Notification Channel

### 4.1 Create SNS Topic

Open Amazon SNS

Create a Topic: `security-incident-topic`

Type: Standard

Note the Topic ARN for Lambda notifications.

## 5. Lambda Security Event Handler Function

### 5.1 Create IAM Execution Role

Create a Lambda execution role with the following minimum permissions:

CloudWatch Logs

SNS:Publish

S3:GetObject / PutObject

states:StartExecution

Follow the principle of Least Privilege.

### 5.2 Create Lambda Function

Runtime: Python 3.11

Upload `lambda_function.py`

Attach the execution role

Lambda is responsible for:

Parsing GuardDuty / Inspector / CloudTrail / Macie events

Sending SNS notifications

Triggering Step Functions

### 5.3 Test Lambda

Test using sample GuardDuty / CloudTrail events

Confirm log output in CloudWatch Logs

Some API permission errors may exist during the project phase and will be documented.

## 6. Step Functions

### 6.1 Create State Machine

Create a Standard Workflow

Example State Machine names:

```
SFN-UnauthorizedAccess
SFN-CryptoMining
```

### 6.2 Record State Machine ARN

Populate the actual ARN in the Lambda configuration.

## 7. EventBridge Rules

### 7.1 Create GuardDuty Rule

Source: `aws.guardduty`

Detail-type: `GuardDuty Finding`

Target: Lambda function

### 7.2 Other Event Sources

Inspector2 Finding

AWS API Call via CloudTrail

Macie Finding

## 8. Architecture Validation

GuardDuty / Inspector generate events

EventBridge triggers Lambda

Lambda outputs logs + SNS notifications

Athena can query historical logs

# Deployment

## 0. 前置条件

AWS Account（已开启 Organizations）

区域：ap-northeast-1 (Tokyo)

已具备基础 IAM / Lambda / S3 / Athena 操作经验

## 1. 启用安全服务（数据源准备）

### 1.1 启用 GuardDuty

打开 Amazon GuardDuty

选择区域 `ap-northeast-1`

点击 Enable GuardDuty

GuardDuty 用于生成 UnauthorizedAccess、CryptoMining 等安全事件。

### 1.2 启用 Inspector v

打开 Amazon Inspector

启用 Inspector v2

选择 EC2 / ECR / Lambda 扫描

Inspector Critical Finding 将作为安全事件输入。

### 1.3 启用 Macie

打开 Amazon Macie

启用 Macie

Macie Finding 用于检测 S3 中的敏感数据或 Public Access 风险。

## 2. CloudTrail 与 S3 日志存储

### 2.1 启用 CloudTrail

打开 AWS CloudTrail

创建 Trail（Management events 默认开启）

日志存储到指定 S3 Bucket

### 2.2 确认 S3 日志

进入 S3 Bucket

确认 CloudTrail `.json.gz` 文件存在

该日志将作为 Athena 查询的数据源。

## 3. Athena 日志查询（审计层）

### 3.1 创建 Athena 表

打开 Amazon Athena

选择数据库（或新建）

执行 `create_table_cloudtrail.sql`

此步骤用于将 CloudTrail 日志映射为可查询结构。

### 3.2 执行安全审计查询

执行示例 SQL（如 IAM / API 调用查询）

确认 Query 状态为 Query successful

即使返回行数为 0，也表示查询配置正确。

## 4. SNS 通知通道

### 4.1 创建 SNS Topic

打开 Amazon SNS

创建 Topic：`security-incident-topic`

类型：Standard

记录 Topic ARN，用于 Lambda 通知。

## 5. Lambda 安全事件处理函数

### 5.1 创建 IAM 执行角色

创建 Lambda 执行角色，包含以下最小权限：

CloudWatch Logs

SNS:Publish

S3:GetObject / PutObject

states:StartExecution

遵循 Least Privilege 原则。

### 5.2 创建 Lambda 函数

Runtime：Python 3.11

上传 `lambda_function.py`

绑定执行角色

Lambda 负责：

解析 GuardDuty / Inspector / CloudTrail / Macie 事件

发送 SNS 通知

触发 Step Functions

### 5.3 测试 Lambda

使用 GuardDuty / CloudTrail 示例事件进行 Test

在 CloudWatch Logs 中确认日志输出

部分 API 权限错误在项目阶段允许存在，并在文档中记录。

## 6. Step Functions

### 6.1 创建 State Machine

创建 Standard Workflow

State Machine 名称示例：

`SFN-UnauthorizedAccess`

`SFN-CryptoMining`

### 6.2 记录 State Machine ARN

将实际 ARN 填入 Lambda 配置中：

## 7. EventBridge 规则

### 7.1 创建 GuardDuty 规则

Source：`aws.guardduty`

Detail-type：`GuardDuty Finding`

Target：Lambda 函数

### 7.2 其他事件源

Inspector2 Finding

AWS API Call via CloudTrail

Macie Finding

## 8. 架构验证

GuardDuty / Inspector 产生事件

EventBridge 触发 Lambda

Lambda 输出日志 + SNS 通知

Athena 可查询历史日志