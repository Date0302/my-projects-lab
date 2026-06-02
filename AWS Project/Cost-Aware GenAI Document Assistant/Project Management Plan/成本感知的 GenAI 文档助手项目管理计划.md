# 成本感知的 GenAI 文档助手 – 项目管理计划

**项目名称**：Cost-Aware GenAI Document Assistant  

**项目经理**：Project Owner  

**项目发起人**：本人  

**文档版本**：1.0  

**创建日期**：2026-06-02  

## 1. 项目章程

| 项目名称     | 成本感知的 GenAI 文档助手                                    |
| ------------ | ------------------------------------------------------------ |
| 项目目标     | 基于 AWS 无服务器架构构建一套智能文档问答系统，通过问题复杂度动态路由到不同成本的 LLM 模型，实现功能、性能与成本的最佳平衡，并提供成本的可视化追踪与分析。 |
| 主要成功标准 | 1. 实现文档上传与向量化存储的自动化流程<br>2. 根据问题复杂度动态选择低成本或高能力模型<br>3. 每次调用的 Token 数与成本可追踪并可视化<br>4. 成本相比始终使用最高能力模型降低 ≥70%<br>5. 用户端响应延迟 <2 秒，答案质量满足常见问答需求 |
| 项目经理     | Project Owner                                                |
| 项目发起人   | 本人                                                         |
| 批准日期     | 2026-05-20                                                   |

## 2. 项目目标与范围

### 2.1 项目目标

- 构建一套完全无服务器、自动扩展的文档问答系统
- 实现基于问题复杂度的动态模型路由（低成本 Titan vs. 高能力 Claude 3）
- 提供完整的成本追踪与可视化仪表板
- 确保数据安全与用户认证
- 作为解决方案架构师的作品集项目，展示架构权衡与决策能力

### 2.2 项目范围

**包含**：
- 文档上传与处理链路（API Gateway → S3 → Step Functions → 文本提取 → 向量化 → OpenSearch）
- 查询与路由链路（Cognito 认证 → API Gateway → Orchestrator Lambda → 语义检索 → 模型路由 → 答案生成）
- 成本追踪链路（每次调用记录模型、Token 数、预估成本到 DynamoDB）
- 成本分析与可视化（DynamoDB 导出 → Athena → QuickSight）
- 监控与告警（CloudWatch 日志、自定义成本指标、SNS 告警）
- 安全设计（IAM 最小权限、S3 加密、API Gateway 限流）

**不包含**：
- 多轮对话上下文记忆（仅单轮问答）
- 实时流式响应（WebSocket 预留但未实现）
- 复杂的自定义模型微调
- 支持非文本文件（如音视频）
- 生产级多区域部署

## 3. 关键干系人

| 角色                | 职责                            | 沟通方式                   |
| ------------------- | ------------------------------- | -------------------------- |
| 项目经理            | 整体架构设计、部署实施、测试    | 日常自检                   |
| 最终用户            | 上传文档、提问                  | 通过 API 测试工具模拟      |
| 成本管理员          | 监控 AWS 成本、优化模型路由阈值 | 每周检查 QuickSight 仪表板 |
| 安全审计            | 审查 IAM 策略、Cognito 配置     | 定期自检                   |
| 潜在雇主/作品集评审 | 评估架构决策与文档完整性        | 项目展示                   |

## 4. 假设与约束

### 4.1 假设

- AWS 账号已开通 Bedrock 模型访问权限（Titan、Claude 3）
- 文档格式限于 PDF、TXT、常见办公文档（通过 PyPDF2/chardet 处理）
- 用户问题以英文为主，复杂度判断规则可基于关键词和长度
- OpenSearch Serverless 向量搜索返回 Top‑K 相关段落即可满足问答需求
- 成本数据基于 Bedrock 按需定价估算，实际费用与预估偏差在 ±20% 内

### 4.2 约束

- 项目为单人实施，无专职数据科学或运维团队
- 所有服务部署在单一 AWS 区域
- Lambda 执行时间受 15 分钟限制，但文档处理预期在几秒内完成
- 向量化使用 Titan Embeddings，不切换到其他嵌入模型
- 不引入第三方 LLM 或外部 API

## 5. 架构设计概述

基于用户提供的文档与架构图，系统分为以下三条核心流水线：

### 5.1 数据注入流水线（文档处理）

- **文档上传**：API Gateway + S3（原始桶），使用预签名 URL 保证安全
- **工作流编排**：S3 事件 → EventBridge → Step Functions（支持重试、可视化调试）
- **文本提取**：Lambda（Python + PyPDF2/chardet）解析文档内容
- **向量化**：调用 Bedrock Titan Embeddings 模型生成向量
- **向量存储**：OpenSearch Serverless（自动扩展，支持语义搜索与元数据过滤）

### 5.2 查询与成本感知流水线（核心）

- **用户认证**：Amazon Cognito 用户池，JWT 验证
- **查询入口**：API Gateway
- **核心编排**：Orchestrator Lambda
  - 语义检索：OpenSearch 返回相关文档片段
  - 复杂度判断：基于规则（问题长度、关键词）
  - 模型路由：简单问题 → Titan Text G1‑Lite（低成本）；复杂问题 → Claude 3 Haiku/Sonnet（高能力）
  - 成本记录：写入 DynamoDB（模型、Token 数、预估费用）
- **响应返回**：答案 + 所用模型 + 成本估计 + 延迟

### 5.3 成本分析流水线

- **成本数据湖**：DynamoDB 按时间分区导出至 S3（Parquet 格式）
- **无服务器查询**：Amazon Athena 进行 SQL 分析
- **可视化仪表板**：Amazon QuickSight（总成本趋势、模型占比、简单/复杂问题比例、平均单次成本）
- **预算告警**：CloudWatch 监控日累计成本 → SNS 通知（阈值 $5/天）

## 6. 主要交付物

| 编号 | 交付物                          | 描述                           |
| :--: | :------------------------------ | ------------------------------ |
|  D1  | 架构设计图                      | draw.io / PDF 文件             |
|  D2  | 文档处理 Step Functions 定义    | 状态机 JSON                    |
|  D3  | 文本提取 Lambda 代码            | Python + PyPDF2/chardet        |
|  D4  | 向量化 Lambda 代码              | 调用 Bedrock Titan Embeddings  |
|  D5  | OpenSearch Serverless 索引配置  | 向量映射与元数据字段           |
|  D6  | Orchestrator Lambda 代码        | 检索 + 路由 + 成本记录         |
|  D7  | 模型路由规则配置                | 可配置的阈值与关键词列表       |
|  D8  | DynamoDB 成本日志表             | 表结构 + TTL 策略              |
|  D9  | Athena 视图与 QuickSight 仪表板 | SQL 定义 + 可视化面板          |
| D10  | CloudWatch 成本告警规则         | 自定义指标 + SNS 主题          |
| D11  | IAM 安全策略集                  | 各组件最小权限角色             |
| D12  | IaC 部署脚本                    | AWS CDK 或 Terraform 模板      |
| D13  | 测试报告                        | 功能、路由准确率、成本降低验证 |
| D14  | 运维手册                        | 故障排除、日志查询、成本优化   |
| D15  | 项目文档                        | 本 PMP 文档                    |

## 7. 风险管理

| 风险                                       | 影响 | 应对措施                                                     |
| ------------------------------------------ | ---- | ------------------------------------------------------------ |
| Bedrock 模型调用延迟过高，影响用户体验     | 中   | 设置 API Gateway 超时与重试；监控 p99 延迟；如持续超标可切换至更快的模型 |
| 复杂度判断规则不准确，导致高成本模型被滥用 | 中   | 初始规则基于启发式，预留扩展接口（可替换为轻量级分类器）；定期分析成本日志调整阈值 |
| 向量搜索返回不相关内容，答案质量差         | 中   | 优化分块策略与元数据过滤；增加 Top-K 值或引入重排序（Rerank）作为后续增强 |
| OpenSearch Serverless 成本超预期           | 低   | 使用按需容量模式，监控 OCU 使用量；设置索引保留策略          |
| DynamoDB 成本日志增长过快                  | 低   | TTL 自动清理（如 90 天），可导出到 S3 Glacier 长期归档       |
| 未授权访问导致敏感文档泄露                 | 高   | Cognito 强制认证 + API Gateway 授权器 + S3 存储桶策略禁止公开访问；IAM 最小权限 |

## 8. 成本管理

### 8.1 成本组成

- **计算成本**：Lambda 调用（文档处理、Orchestrator）、Step Functions 状态转换
- **AI 模型成本**：Bedrock（Titan Embeddings、Titan Text、Claude 3）按输入/输出 Token 计费
- **存储成本**：S3（原始文档 + 处理后数据）、OpenSearch Serverless（向量索引）、DynamoDB（日志）
- **查询成本**：Athena 按扫描数据量计费
- **可视化**：QuickSight 标准版按用户数（单用户免费额度内）
- **其他**：API Gateway、CloudWatch、SNS（免费额度内）

### 8.2 优化策略

- 动态路由：约 80% 简单问题走 Titan Lite，成本仅为 Claude 3 的 1/8
- S3 生命周期：原始文档 30 天后转 IA，90 天后转 Glacier
- DynamoDB TTL 自动删除超过 90 天的日志
- OpenSearch 使用按需容量，无请求时不计费
- 设置 AWS Budgets 告警，每月成本控制在 $10 以内（演示用途）

## 9. 质量管理

### 9.1 测试策略

| 测试类型       | 范围                                      | 工具/方法                |
| -------------- | ----------------------------------------- | ------------------------ |
| 单元测试       | 文本提取、路由判断逻辑                    | Python unittest / pytest |
| 集成测试       | 文档上传 → 向量化 → 查询 → 成本记录       | 模拟事件 + AWS CLI       |
| 路由准确率测试 | 针对 50 个预定义问题验证模型选择          | 手动标注 + 自动化脚本    |
| 性能测试       | 模拟 10 并发查询，测量延迟与成本          | Artillery / Locust       |
| 成本验证       | 对比预估成本与 AWS Cost Explorer 实际账单 | 分析报告                 |
| 安全测试       | IAM 权限越权尝试、Cognito 未授权访问      | IAM Policy Simulator     |

### 9.2 验收标准

- 文档上传后 30 秒内完成向量化并可检索
- 查询响应时间中位数 < 1.5 秒，p99 < 3 秒
- 简单问题路由到 Titan Lite 的比例 ≥ 90%，复杂问题路由到 Claude 3 的比例 ≥ 95%
- 总成本相比始终使用 Claude 3 降低 ≥ 70%
- 所有 API 请求必须携带有效 JWT 才能访问
- 成本仪表板可正确展示每日/模型维度的费用趋势

## 10. 监控与运维

### 10.1 监控指标

- Lambda：调用次数、错误率、持续时间、限流次数
- Step Functions：执行失败率、各步骤耗时
- OpenSearch：查询延迟、OCU 使用量
- Bedrock：模型调用次数、Token 数、节流错误
- DynamoDB：写入吞吐量、存储大小
- 自定义成本指标：`TotalDailyCost`、`CostPerModel` 上报到 CloudWatch

### 10.2 日志与追踪

- 所有 Lambda 日志输出到 CloudWatch Logs
- Step Functions 启用 X-Ray 追踪（可选）
- 定期导出 CloudTrail 日志到 S3 用于审计

### 10.3 告警规则

| 指标                       | 阈值            | 动作            |
| -------------------------- | --------------- | --------------- |
| Orchestrator Lambda 错误率 | >5% 持续 2 分钟 | SNS 邮件告警    |
| 日累计成本                 | >$5             | SNS 邮件+短信   |
| OpenSearch 查询延迟 p99    | >2 秒           | CloudWatch 告警 |
| SQS 死信队列（如有）非空   | >0              | SNS 告警        |

### 10.4 灾难恢复

- 所有 IaC 模板托管在 Git 仓库
- DynamoDB 按需备份（每周）
- OpenSearch 索引可重建：重新处理原始文档 S3 桶
- 关键配置（IAM、API Gateway）通过版本控制

## 11. 安全策略

- **身份认证**：Amazon Cognito 用户池 + API Gateway JWT 授权器
- **数据加密**：S3 默认 SSE-S3 加密，OpenSearch 节点间加密，DynamoDB 默认加密
- **传输安全**：API Gateway 强制 HTTPS，所有服务间调用使用 TLS
- **IAM 最小权限**：
  
  1.Orchestrator Lambda 角色：读取 OpenSearch、调用 Bedrock、写入 DynamoDB、发布 SNS
  
  2.文档处理 Lambda 角色：读取 S3 原始桶、调用 Bedrock Embeddings、写入 OpenSearch
  
  3.成本导出角色：读取 DynamoDB、写入 S3、调用 Athena
- **网络隔离**：OpenSearch Serverless 使用 VPC 端点（可选，按需配置）
- **输入验证**：API Gateway 请求大小限制，Lambda 内校验文件类型与大小

## 12. 项目成果

- 成功构建了一套成本感知的 GenAI 文档问答系统，完全基于无服务器架构
- 实现了动态模型路由，在实际测试中成本降低约 75%，同时保持答案质量
- 提供了端到端的成本可视化与告警能力，使成本成为一等公民
- 所有交付物完成，可作为解决方案架构师作品集的核心项目
- 展示了架构权衡决策（如路由策略、向量数据库选型、实时性设计）的系统化文档

## 13. 未来扩展建议

- 将规则路由升级为轻量级分类器（如 SageMaker 托管的小型 BERT），提高准确率
- 支持多轮对话与上下文记忆（引入 DynamoDB 会话存储）
- 增加 RAG 的 reranking 阶段，提升答案相关性
- 接入企业 SSO（如 SAML 或 OIDC）替代 Cognito 用户池
- 支持多语言文档与跨语言检索（使用多语言嵌入模型）
- 使用 Amazon Bedrock Agent 进一步简化复杂任务编排

