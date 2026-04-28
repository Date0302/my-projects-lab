# README

## 项目概述

本仓库展示了我在 AWS 云计算、无服务器架构、事件驱动系统和云安全管理方面的综合能力。
包含两个主要项目：

1. Images Processing Project：用户上传图像的自动处理、异步任务调度与安全存储
2. Security Incident Automation & Compliance Audit Platform Project：企业级安全管理与事件响应

通过这两个项目，展示我在 AWS 服务集成、云架构设计、无服务器计算和安全防护的实践能力。

## 1.Images Processing Project

### 项目目标

- 用户上传图像 → 自动处理 → 安全存储
- 异步任务调度以提高系统扩展性
- 展示 Lambda、S3、SQS、Cognito 的整合应用

### 核心组件

Lambda Functions：图像上传、异步处理、任务通知

S3：原图和处理图像存储

SQS：异步任务队列

Cognito：用户注册与认证

IAM：最小权限角色管理

## 2.Security Incident Automation & Compliance Audit Platform Project

### 项目目标

模拟企业级 AWS 安全场景

配置 GuardDuty 监控异常访问

使用 IAM 策略和角色管理权限

构建事件驱动安全响应流程

### 核心组件

GuardDuty：实时安全威胁监控

EventBridge：事件路由与规则触发

Lambda：自动化安全事件响应

IAM：用户和角色权限管理

## 3.部署指南

1. 配置 AWS CLI 并设置访问密钥
2. 创建 S3 存储桶（图像项目 & 安全日志）
3. 配置 IAM 角色与策略，确保最小权限
4. 部署 Lambda 函数，配置触发器
5. 配置 SQS 队列（图像项目）或 EventBridge 规则（安全项目）
6. 设置 Cognito 用户池（图像项目）
7. 测试完整流程，确保图像处理与安全事件响应正常

## 4.技术栈

AWS 服务：Lambda, S3, SQS, IAM, Cognito, GuardDuty, EventBridge, CloudWatch, SNS

编程语言：Python 3.11+

工具：draw.io

## 5.项目亮点

展示完整 AWS 全栈能力：无服务器架构 + 异步处理 + 安全管理

实现事件驱动、自动化流程和高可用架构

注重安全与权限控制，遵循最小权限原则