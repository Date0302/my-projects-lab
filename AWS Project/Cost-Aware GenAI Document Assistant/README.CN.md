# README

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

本项目是一个构建在 AWS 无服务器架构上的成本感知型智能文档问答系统。核心创新在于：根据问题复杂度动态路由到不同成本的 AI 模型，并将成本作为一等公民进行追踪、分析与可视化，完美体现了解决方案架构师在功能、性能与成本之间的权衡艺术。

## 核心特性

- 完全无服务器：基于 Lambda、API Gateway、S3、DynamoDB 等托管服务，自动伸缩，零服务器运维
- 成本感知的动态路由：根据问题复杂度智能选择 LLM 模型（Titan Lite vs. Claude 3），在不影响体验的前提下大幅降低推理成本
- RAG 检索增强生成：使用 OpenSearch Serverless 进行语义检索，让 AI 基于企业私有文档回答问题
- 生产级可观测性：完整追踪每次调用的模型、Token 数、成本，通过 QuickSight 可视化 + CloudWatch 告警
- 安全合规：Cognito 身份认证、S3 加密、API Gateway 限流与 CORS 控制
- 可靠性设计：Step Functions 重试与死信队列 (DLQ)、DynamoDB TTL 自动清理

## 制作项目原因

作为解决方案架构师候选人，我不仅要能“搭建”系统，更要能做出有理有据的架构决策。企业落地生成式 AI 最大的痛点之一是不可控的推理成本——无差别地调用最强模型（如 Claude 3）会导致费用爆炸，而一刀切使用低成本模型又可能牺牲复杂问题的回答质量。

本项目通过动态路由解决了这一矛盾：系统自动识别问题类型，简单高频问题走低成本路径，复杂推理问题走高质量路径，并让成本可视化，从而为业务方提供数据驱动的成本优化建议。这正是解决方案架构师的核心价值所在。

## 核心组件详解

### 1. 文档注入管道 (Data Ingestion Pipeline)

| 组件       | 技术选型                          | 设计决策                                                     |
| ---------- | --------------------------------- | ------------------------------------------------------------ |
| 文档上传   | API Gateway + S3 (原始桶)         | 使用预签名 URL 模式，避免前端直写 S3 带来的安全风险          |
| 工作流编排 | AWS Step Functions                | 支持重试、错误处理、可视化调试，比单纯 Lambda 串联更健壮     |
| 文本处理   | Lambda (Python + PyPDF2/chardet)  | 无服务器，按调用计费，自动处理多种文档格式                   |
| 向量化     | Amazon Bedrock - Titan Embeddings | 与 Bedrock 其他模型统一生态，成本低廉（约 $0.0001/1K tokens） |
| 向量存储   | Amazon OpenSearch Serverless      | 无需管理集群，自动扩缩，天然支持向量搜索与元数据过滤         |

**关键设计**：S3 事件无法直接触发 Step Functions，中间通过 EventBridge 或 Lambda 桥接（架构图中已隐含）。

### 2. 智能问答与成本控制管道 (Query & Cost-Aware Pipeline)

这是系统的核心决策层。

|     组件     |                    技术选型                     |                           设计决策                           |
| :----------: | :---------------------------------------------: | :----------------------------------------------------------: |
|   用户认证   |                 Amazon Cognito                  |   托管用户池，与 API Gateway 原生集成，开箱即用的 JWT 验证   |
|   问答入口   |         API Gateway (REST + WebSocket)          |       REST 用于单次请求，WebSocket 为后续流式响应预留        |
|  核心编排器  |              Lambda (Orchestrator)              |    承载所有业务逻辑：检索、复杂度判断、模型路由、成本记录    |
|   语义检索   |         OpenSearch Serverless 向量搜索          |         返回与问题最相关的 Top-K 文档片段作为上下文          |
| 模型路由逻辑 | 基于规则（问题长度/关键词）+ 可扩展为轻量分类器 | 初期规则：问题 < 20 字符或包含“是什么/定义”等关键词 → 低成本路径；包含“为什么/对比/分析”或长问题 → 高能力路径 |
|  低成本模型  |       Amazon Bedrock - Titan Text G1‑Lite       |  推理速度快，成本约 $0.0003/1K 输入 tokens，适合事实性问答   |
|  高能力模型  |     Amazon Bedrock - Claude 3 Haiku/Sonnet      | 推理能力强，支持复杂逻辑，成本约 $0.0025/1K 输入 tokens（约为 Titan 的 8 倍） |
|   成本日志   |                 Amazon DynamoDB                 | 高写入吞吐，TTL 自动清理，记录每次调用的时间、模型、Token 数、估算成本 |

**输入/输出示例** (Orchestrator Lambda)：

```json
// 输入（用户提问）
{
  "userId": "user123",
  "question": "请解释一下什么是服务等级协议 (SLA)？"
}

// 输出（系统返回）
{
  "answer": "服务等级协议 (SLA) 是服务提供方与客户之间的正式承诺...",
  "model_used": "amazon.titan-text-lite",
  "cost_estimate_usd": 0.00021,
  "latency_ms": 520
}
```

### 3. 成本分析与可视化管道 (Cost Analytics Pipeline)

|     组件     |           技术选型           |                           设计决策                           |
| :----------: | :--------------------------: | :----------------------------------------------------------: |
|  成本数据湖  | DynamoDB 导出 → S3 (Parquet) | DynamoDB 按时间分区导出，转换为 Parquet 格式以便 Athena 高效查询 |
| 无服务器查询 |        Amazon Athena         |             标准 SQL 分析成本日志，无需预置集群              |
| 可视化仪表盘 |      Amazon QuickSight       |             托管 BI 工具，支持自动刷新和行级安全             |
|   预算告警   |       CloudWatch + SNS       |     监控每日累计成本，超过阈值（如 $5/天）触发邮件/短信      |

**仪表盘关键指标**：
- 近 7 天 / 30 天总成本趋势
- 各模型调用次数与成本占比
- 简单问题 vs 复杂问题的请求比例
- 单位请求平均成本（用于向业务方汇报 ROI）

## 架构权衡与设计决策

作为解决方案架构师项目，这里**显式记录**几个关键权衡：

|    决策点    |         选项 A          |        选项 B         |       最终选择        |                             理由                             |
| :----------: | :---------------------: | :-------------------: | :-------------------: | :----------------------------------------------------------: |
| 模型路由策略 |    始终使用 Claude 3    |     动态规则路由      |       动态路由        |    成本可降低 70-80%，且 80% 的日常问题可由低成本模型胜任    |
|  向量数据库  | Aurora PG with pgvector | OpenSearch Serverless | OpenSearch Serverless |    无需管理集群，与 Bedrock 集成更自然，成本为按请求付费     |
|  实时性要求  |    同步等待 LLM 响应    |       异步轮询        |         同步          |    问答场景对延迟敏感（目标 < 2s），同步可接受且实现简单     |
| 成本追踪粒度 |     仅汇总每日成本      |   每次调用记录明细    |     每次调用明细      | 提供细粒度成本归因，便于后续优化（例如识别最耗钱的用户或问题类型） |

## 使用的 AWS 服务

|    类别    |                             服务                             |
| :--------: | :----------------------------------------------------------: |
| 计算与编排 |                AWS Lambda, AWS Step Functions                |
| API 与安全 |              Amazon API Gateway, Amazon Cognito              |
|    存储    |                  Amazon S3, Amazon DynamoDB                  |
|   AI/ML    | Amazon Bedrock (Titan Embeddings, Titan Text, Claude 3), Amazon OpenSearch Serverless |
|    分析    |               Amazon Athena, Amazon QuickSight               |
| 监控与告警 |                Amazon CloudWatch, Amazon SNS                 |
|  事件集成  |        Amazon EventBridge (桥接 S3 到 Step Functions)        |

## 监控与运维

系统已集成 CloudWatch 进行全方位监控：
- 查看各 Lambda 函数的执行日志、持续时间、错误率、节流次数
- 在 CloudWatch 控制台设置基于自定义成本指标的告警（例如 `TotalDailyCost` 超过 $10）
- Step Functions 工作流可视化追踪每个文档的处理状态
- X-Ray 分布式追踪（可选）用于分析端到端延迟瓶颈

## 如何运行（概要）

1. 使用 AWS CDK 或 Terraform 一键部署所有资源（IaC 模板已提供）
2. 创建 Cognito 测试用户并获取 JWT Token
3. 通过 API Gateway 上传文档（POST /documents）
4. 通过 API Gateway 提问（POST /query），携带 JWT Token
5. 等待 30 秒（向量化完成后），再次提问即可获得基于文档的回答
6. 在 QuickSight 中打开成本仪表盘，观察不同模型路径的成本分布
7. 设置 CloudWatch 预算阈值，验证 SNS 告警

## 项目状态

该项目作为一个解决方案架构师作品集项目已完成。所有代码、IaC 模板、架构图和演示视频均已在代码库中提供。成本数据为基于 Bedrock 按需定价的真实估算值。
