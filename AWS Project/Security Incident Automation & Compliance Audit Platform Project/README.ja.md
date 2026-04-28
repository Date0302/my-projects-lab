# AWS Security Log Analytics Project

#### 🌐 言語 / Language / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

## 概要
このプロジェクトは、ネイティブAWSサービスを使用したセキュリティログ分析・可視化プラットフォームを実装します。
監査および脅威検出を目的として、AWSセキュリティ関連ログの収集、分析、可視化に焦点を当てています。

このプロジェクトは、AWSセキュリティアーキテクチャ、ログ分析、可視化スキルを紹介するための学習・デモンストレーションプロジェクトとして設計されています。

## アーキテクチャ
アーキテクチャは、集中ロギングおよび分析アプローチに基づいています。

主なフロー：

AWS CloudTrailが管理イベントログを生成

ログは暗号化されたAmazon S3バケットに保存

Amazon Athenaを使用してS3から直接ログをクエリ

Amazon QuickSightを使用してセキュリティダッシュボードを構築

AWS Lambdaを使用してセキュリティイベントのテストとシミュレーション

Amazon EventBridgeを使用してLambda関数をトリガー

（アーキテクチャ図はリポジトリ内に提供されています）

## 使用するAWSサービス
AWS CloudTrail

Amazon S3

AWS Lambda

Amazon EventBridge

Amazon Athena

Amazon QuickSight

AWS IAM

AWS KMS

## 主な機能
CloudTrailログのS3への集中保存

Athenaを使用したサーバーレスログ分析

セキュリティ関連のAPIアクティビティ分析

QuickSightを使用したAWSアカウントアクティビティの可視化

AWS KMSを使用した暗号化ログ保存

最小権限のIAMロール設計

## セキュリティ設計
CloudTrailログはAWS KMSを使用して暗号化

S3バケットはデフォルトのサーバーサイド暗号化を強制

IAMロールは最小権限の原則に従う

分析は読み取り専用であり、本番リソースを変更しない

## プロジェクトステータス
このプロジェクトは、実践的なセキュリティ分析ラボとして完了しています。
一部のクエリとダッシュボードはデモンストレーション目的で簡略化されています。