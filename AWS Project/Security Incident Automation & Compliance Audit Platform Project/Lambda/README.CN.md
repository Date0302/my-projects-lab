# 安全编排Lambda函数

#### 🌐 言語 / Language / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

## 概要

该Lambda函数作为中央安全编排层，在AWS安全自动化项目中发挥核心作用。它接收来自多个AWS服务的安全相关事件，进行集中日志记录、发送警报，并使用AWS Step Functions触发自动化响应工作流。

## 支持的事件源

此Lambda由Amazon EventBridge触发，支持以下安全事件类型：

| 源服务           | 事件类型                    | 描述                             |
| ---------------- | --------------------------- | -------------------------------- |
| Amazon GuardDuty | GuardDuty安全发现           | 未经授权的访问、加密货币挖矿活动 |
| Amazon Inspector | Inspector2安全发现          | 严重漏洞发现                     |
| AWS CloudTrail   | 通过CloudTrail的AWS API调用 | 有风险的IAM策略变更              |
| Amazon Macie     | Macie安全发现               | 敏感数据暴露/公开S3访问          |

##  核心职责

### 1. 集中式事件处理

- 识别事件源和类型
- 对安全事件进行分类

### 2.安全事件日志记录

- 在Amazon S3中存储结构化的JSON日志
- 支持通过Athena和QuickSight进行下游分析

### 3.安全警报通知

- 为每个处理的事件发送实时警报
- 警报包含事件源、类型和处理结果

------

### 4.自动化响应编排

根据事件类型，Lambda会触发专用的AWS Step Functions状态机以进行进一步的自动化修复。

| 事件类型          | Step Functions状态机   |
| ----------------- | ---------------------- |
| 未经授权的访问    | SFN-UnauthorizedAccess |
| 加密货币挖矿      | SFN-CryptoMining       |
| Inspector严重发现 | SFN-InspectorCritical  |
| IAM策略变更       | SFN-IAMPolicyChange    |
| Macie敏感数据     | SFN-MacieSensitiveData |

⚠Step Functions内部的修复操作**有意实现为占位符**，旨在演示架构设计，而非修改生产环境资源。



##  IAM权限

Lambda执行角色需要以下权限：

Amazon S3: `PutObject`

Amazon SNS: `Publish`

AWS Step Functions: `StartExecution`

Amazon CloudWatch Logs: 基本日志记录权限

## 设计说明

此Lambda设计为单一入口安全控制点

强调可观测性、可审计性和可扩展性

分离检测、编排和修复逻辑

适用于SOC风格的安全监控和分析用例
