# README

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

本项目包含 4 个核心 Lambda 函数，协同实现文档注入、向量化、智能问答路由与成本感知决策。以下说明每个函数的职责、输入/输出、模拟实现说明以及预期的生产级替代方案。

## 函数列表

|       函数名        |                职责                 |                触发方式                |
| :-----------------: | :---------------------------------: | :------------------------------------: |
| Document-processor  |      文档文本提取、分块、清洗       | S3 事件 → EventBridge → Step Functions |
| Embedding-generator |  将文本块转换为向量（当前为模拟）   |          Step Functions 调用           |
|    Orchestrator     | 编排文档处理与 embedding 生成工作流 |         Step Functions 状态机          |
|    Query-router     |    问题分类、模型路由、成本估算     |      API Gateway → Lambda（同步）      |

---

## 1. Document-processor

### 职责
- 从 S3 读取上传的原始文档（PDF / TXT）
- 提取文本内容
- 进行分块（chunking）与清洗（去除多余空白、特殊字符）
- 输出结构化文本块供后续向量化

### 当前实现（模拟）
- 未实际连接 S3 与 Bedrock
- 接收 event 中的 document_name 和 content 字段
- 计算单词数量并记录日志

### 输入示例
```json
{
  "document_name": "sla_definition.pdf",
  "content": "A Service Level Agreement (SLA) is a commitment between a service provider and a customer..."
}
```

### 输出示例

```json
{
  "statusCode": 200,
  "body": {
    "document_name": "sla_definition.pdf",
    "word_count": 15,
    "message": "Document processed successfully"
  }
}
```

### 预期生产级替代
- 使用 boto3 调用 S3 get_object
- 集成 PyPDF2 / pdfplumber 解析 PDF
- 按固定大小或语义边界分块
- 将清洗后的文本块存入 S3 暂存或直接传递给下一步

### IAM 权限（最小示例）
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::raw-documents-*/*"
}
```

---

## 2. Embedding-generator

### 职责
1.接收文本块，调用 Amazon Bedrock Titan Embeddings 模型

2.生成 1536 维向量

3.将向量与元数据写入 OpenSearch Serverless

### 当前实现（模拟）
1.使用 MD5 哈希模拟嵌入向量（仅用于演示工作流完整性）

2.不产生真实向量，不连接 Bedrock 或 OpenSearch

### 输入示例
```json
{
  "text": "A Service Level Agreement (SLA) is a commitment..."
}
```

### 输出示例
```json
{
  "statusCode": 200,
  "body": {
    "text": "A Service Level Agreement (SLA) is a commitment...",
    "embedding": "a1b2c3d4e5f6...",  // MD5 哈希字符串
    "message": "Embedding generated successfully"
  }
}
```

### 预期生产级替代
1.调用 bedrock-runtime.invoke_model 使用 amazon.titan-embed-text-v1

2.将返回的向量（list of floats）写入 OpenSearch Serverless（使用 opensearch-py 或 requests-aws4auth）

3.增加超时重试与错误处理

### IAM 权限
```json
{
  "Effect": "Allow",
  "Action": ["bedrock:InvokeModel"],
  "Resource": "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v1"
}
```

## 3. Orchestrator

### 职责
1.作为 Step Functions 状态机的核心任务

2.协调文档处理与 embedding 生成步骤

3.传递中间数据（文档名、文本块）并聚合最终状态

### 当前实现（模拟）
1.不实际调用其他 Lambda 或服务

2.在同一函数内模拟“文档处理”和“embedding 生成”两个步骤

3.返回聚合后的状态对象

### 输入示例
```json
{
  "document_name": "sla_definition.pdf",
  "text": "Full extracted text ..."
}
```

### 输出示例
```json
{
  "statusCode": 200,
  "body": {
    "document_processing": {
      "document_name": "sla_definition.pdf",
      "word_count": 234
    },
    "embedding_generation": {
      "embedding_status": "generated",
      "embedding_length": 5234
    },
    "workflow_status": "completed"
  }
}
```

### 预期生产级替代
1.使用 Step Functions 的 Lambda Invoke 任务类型分别调用 Document-processor 和 Embedding-generator

2.负责将上一阶段的输出作为下一阶段的输入

3.增加错误捕获与重试策略（在 Step Functions 定义中配置）

### IAM 权限
不需要额外权限（仅作为编排器，实际调用由 Step Functions 直接完成；若需函数内调用则需 lambda:Invoke）

## 4. Query-router

### 职责
1.接收用户的自然语言问题

2.判断问题复杂度（简单 / 复杂）

3.选择合适的 Bedrock 模型（低成本 vs. 高质量）

4.估算推理成本并返回路由决策

### 当前实现（真实逻辑，可演示）
1.基于关键词规则 + 长度的轻量级分类器

2.返回模型名称和估算成本（硬编码价格，符合 Bedrock 定价）

3.不实际调用 Bedrock，仅输出路由决策

### 分类规则
| 条件                                            | 判定    | 模型                        | 估算成本 |
| ----------------------------------------------- | ------- | --------------------------- | -------- |
| 包含 compare/analyze/why/architecture/trade-off | complex | `anthropic.claude-3-haiku`  | $0.0025  |
| 包含 what/define/who/when                       | simple  | `amazon.titan-text-lite-v1` | $0.0002  |
| 问题长度 > 15 个单词                            | complex | `anthropic.claude-3-haiku`  | $0.0025  |
| 其他                                            | simple  | `amazon.titan-text-lite-v1` | $0.0002  |

### 输入示例
```json
{
  "question": "What is the difference between a standard SLA and a premium SLA?"
}
```

### 输出示例
```json
{
  "statusCode": 200,
  "body": {
    "question": "What is the difference between a standard SLA and a premium SLA?",
    "question_type": "complex",
    "selected_model": "anthropic.claude-3-haiku",
    "estimated_cost_usd": 0.0025
  }
}
```

### 预期生产级替代
1.增加**轻量级分类模型**（如 Hugging Face 蒸馏模型）提高准确率

2.实际调用 Bedrock 对应的模型并返回答案

3.将真实 token 数和成本写入 DynamoDB

### IAM 权限
```json
{
  "Effect": "Allow",
  "Action": ["bedrock:InvokeModel"],
  "Resource": [
    "arn:aws:bedrock:*::foundation-model/amazon.titan-text-lite-v1",
    "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku*"
  ]
}
```

---

## 部署与测试（本地模拟）

所有函数均可使用 sam local 或 python-lambda-local 进行本地测试。

### 示例：测试 Query-router
```bash
# 构造 event.json
echo '{"question": "What is an SLA?"}' > event.json

# 使用 sam local
sam local invoke Query-router --event event.json
```

### 集成测试建议
1. 使用 Step Functions 本地模拟运行 Orchestrator 工作流
2. 将 Document-processor 和 Embedding-generator 的模拟输出串联
3. 通过 API Gateway 调用 `Query-router` 验证路由逻辑

## 从模拟到生产的关键差异

| 方面       | 当前实现（作品集展示） | 生产级实现                            |
| ---------- | ---------------------- | ------------------------------------- |
| 文档解析   | 直接接收 content 字段  | S3 读取 + PDF/TXT 解析库              |
| 向量化     | MD5 哈希               | Bedrock Titan Embeddings + OpenSearch |
| 工作流编排 | 单函数模拟             | Step Functions 跨函数协调             |
| 模型调用   | 仅路由决策             | 真实 `invoke_model` + 流式响应        |
| 成本记录   | 硬编码                 | 基于真实 token 量计算 + DynamoDB      |
| 可观测性   | CloudWatch 日志        | X-Ray 追踪 + 自定义指标               |
