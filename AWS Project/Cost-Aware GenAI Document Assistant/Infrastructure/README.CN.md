# Infrastructure Overview

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

本文档描述了成本感知的生成式 AI 文档助手项目的基础设施组件、设计决策和运维方面。整个平台构建在 AWS 无服务器服务之上，以确保可扩展性、低维护和成本效率。

## 基础设施架构（高层）

基础设施分为四个逻辑层：

1. 注入层 – S3 + Step Functions + Lambda，用于文档处理和向量化。
2. 查询与路由层 – API Gateway + Cognito + Lambda（编排器）+ Bedrock + OpenSearch Serverless。
3. 异步消息层 – SQS，用于解耦重型处理任务（可选，但为弹性而包含）。
4. 可观测性与分析层 – CloudWatch、DynamoDB 导出、Athena、QuickSight、SNS。

所有资源均使用 AWS CDK 或 Terraform 配置（IaC 模板在代码库中提供）。

## 核心基础设施组件

### AWS Lambda

|       函数名        |                      用途                       |
| :-----------------: | :---------------------------------------------: |
| document-processor  | 从上传的文档（PDF/TXT）中提取文本、分块和清洗。 |
| embedding-generator | 调用 Bedrock Titan Embeddings 将文本块向量化。  |
|    orchestrator     |  核心路由逻辑：语义搜索、模型选择、成本记录。   |
|    query-router     |     （可选）用于问题复杂度的轻量级分类器。      |

所有 Lambda 函数配置如下：

1. 内存：512 MB – 1024 MB（取决于工作负载）
2. 超时：3 分钟（文档处理器）/ 30 秒（编排器）
3. 预留并发：10（以控制成本并防止失控扩展）
4. 通过 SQS 的死信队列（DLQ）处理失败的异步调用

### Amazon S3

|         桶名称          |                          用途                           |
| :---------------------: | :-----------------------------------------------------: |
| raw-documents-<account> |    存储上传的原始文档（启用版本控制，SSE-S3 加密）。    |
|   cost-logs-<account>   | 接收 DynamoDB 导出的 Parquet 格式数据，供 Athena 查询。 |

事件通知：raw-documents 桶将 s3:ObjectCreated:* 事件发送到 EventBridge 规则，然后触发 Step Functions 工作流。

### Amazon SQS

用于工作流阶段之间的异步解耦，特别是非关键或重试密集型任务。

|       队列名称       |                             用途                             |
| :------------------: | :----------------------------------------------------------: |
| doc-processing-queue | 保存来自文档注入管道的消息；由 `document-processor` Lambda 消费。 |
|   embedding-queue    |              （可选）将文本分块与嵌入生成解耦。              |

**配置**：

1. 可见性超时：5 分钟
2. 重新驱动策略：3 次接收尝试后进入 DLQ
3. 不需要 FIFO 队列（幂等处理）

### AWS Step Functions

编排文档注入工作流：
1. 文本提取
2. 分块
3. 嵌入生成
4. 索引到 OpenSearch Serverless

状态机包括对 Bedrock 节流错误的重试，以及用于故障的 Catch 块（记录到 CloudWatch 和 SNS）。

### Amazon DynamoDB

| 表名              | 用途                                                         |
| ----------------- | ------------------------------------------------------------ |
| cost-logs         | 存储每次调用的成本数据：userId、modelId、inputTokens、outputTokens、estimatedCostUsd、timestamp。 |
| document-metadata | （可选）跟踪文档处理状态（已上传 → 已向量化）。              |

特性：

1. 按需容量（或使用自动扩展的预置容量）
2. cost-logs 表的 TTL（生存时间）– 90 天
3. DynamoDB Streams → S3 导出，用于长期分析

### Amazon OpenSearch Serverless

1. 集合名称：rag-vector-store
2. 索引映射：knn_vector（维度 = 1536，用于 Titan Embeddings）
3. 元数据字段：`documentId`、`chunkIndex`、`sourceBucket`、`uploadTime`
4. 加密：AWS KMS（客户托管密钥）

### Amazon Bedrock

账户中启用的模型：
|            模型            |         用途          |
| :------------------------: | :-------------------: |
| amazon.titan-embed-text-v1 | 文本到向量（1536 维） |
|   amazon.titan-text-lite   |   低成本事实性问答    |
| anthropic.claude-3-sonnet  |  高推理能力复杂问答   |

### API Gateway 与 Cognito

- **API Gateway**（REST）：
  - 端点：POST /upload（生成预签名 URL）、POST /query
  - 限流：每秒 1000 个请求，突发 2000
  - 启用 CORS
- **Cognito 用户池**：
  - 所有端点都附加了 JWT 授权器
  - 访问令牌有效期：1 小时

### AWS IAM

所有函数和服务遵循最小权限策略：

1. Lambda 执行角色：仅允许对特定原始桶执行 s3:GetObject，对特定模型 ARN 执行 bedrock:InvokeModel，对成本表执行 dynamodb:PutItem。
2. S3 桶策略：拒绝未加密上传，限制公共访问。
3. Step Functions 角色：最小的 Lambda 调用、DynamoDB 更新和 SNS 发布操作。

## 部署工作流（IaC）

基础设施完全定义为代码。部署步骤：

1. 前提条件：
   - 配置了管理员权限的 AWS CLI（用于首次部署）
   - Node.js 18+（CDK）或 Terraform 1.3+
   - 在目标区域（us-east-1 或 us-west-2）启用 Bedrock 模型

2. 步骤：
   ```bash
   # 使用 AWS CDK
   cdk bootstrap
   cdk deploy --all
   
   # 使用 Terraform
   terraform init
   terraform apply -auto-approve

3. 部署后：
   - 创建 Cognito 测试用户（通过 AWS 控制台或 CLI）
   - 从堆栈输出中记录 API Gateway 端点 URL

部署将创建上述所有资源，包括 S3 桶、Lambda 函数、Step Functions 状态机、SQS 队列、OpenSearch 集合和 CloudWatch 仪表板。

## 安全设计

| 区域       | 实现方式                                                     |
| ---------- | ------------------------------------------------------------ |
| 静态加密   | S3（SSE‑S3）、DynamoDB（默认加密）、OpenSearch（KMS）        |
| 传输中加密 | 所有 API 调用、Bedrock 端点以及服务间通信均使用 TLS 1.2+     |
| 身份验证   | Cognito JWT（所有面向用户的 API 都需要）                     |
| 授权       | 基于资源的 IAM 角色策略（例如，Lambda 只能访问其自己的 S3 前缀） |
| 密钥管理   | API 密钥存储在 AWS Secrets Manager 中（如有），通过 Lambda 环境变量引用 |
| 服务隔离   | 每个 Lambda 是否运行在自己的 VPC 中？不需要（无服务器），但如果 OpenSearch 部署在私有子网中，则添加 VPC 端点。 |

## 监控与日志（CloudWatch）

另见单独的 [CloudWatch Monitoring](./CloudWatch%20Monitoring.md) 文档。

自动创建的日志组：

1. 所有 Lambda 函数（`/aws/lambda/<function-name>`）
2. Step Functions 执行历史
3. API Gateway 访问日志

Lambda 发布的自定义指标：

1. CostPerInvocation（美元）– 维度：ModelId
2. RoutingDecision（1 表示低成本路径，2 表示高成本路径）

告警：

1. HighDailyCost – 当 `TotalDailyCost > 5` 时发送 SNS 邮件
2. LambdaThrottling – 当 5 分钟内节流计数 > 10 时发送 SNS
3. StepFunctionFailure – 当状态机执行失败时发送 SNS

仪表板：

1. GenAI-Operations：显示 Lambda 调用、错误、持续时间、节流
2. GenAI-Cost：显示每个模型的成本趋势和请求分布

## 高可用性与灾难恢复

1. 所有服务均为区域级（默认 us-east-1），在可用区之间自动故障转移。
2. 持久化在 S3 和 DynamoDB 中的数据在 3 个可用区之间复制。
3. 对于跨区域 DR（本演示未实现），您可以：
   （1）为原始文档启用 S3 跨区域复制（CRR）。
   （2）使用 DynamoDB 全局表存储成本日志。
   （3）通过快照/恢复复制 OpenSearch 索引。

## 成本优化说明

1. Lambda 并发限制可防止负载高峰期间成本失控。
2. SQS 队列充当缓冲区，因此不会每次上传都直接调用 Bedrock。
3. DynamoDB 的 TTL 自动删除旧成本日志；Athena 查询仅扫描必要的分区。
4. OpenSearch Serverless 容量设置为 `capacity.autoscaling = true`，最小 2 个 OCU。

**相关文档**：

- [Deployment Overview](./Deployment-overview.md)
- [S3 Architecture](./S3%20Architecture.md)
- [SQS Architecture](./SQS%20Architecture.md)
- [CloudWatch Monitoring](./CloudWatch%20Monitoring.md)
- [Main README](./README.md)