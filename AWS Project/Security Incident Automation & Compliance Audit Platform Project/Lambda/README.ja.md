# Security Orchestration Lambda Function

#### 🌐 言語 / Language / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

## 概要

このLambda関数は、AWSセキュリティ自動化プロジェクトにおける中央セキュリティオーケストレーション層として機能します。複数のAWSサービスからセキュリティ関連イベントを受信し、集中ロギング、アラート送信、およびAWS Step Functionsを使用した自動応答ワークフローのトリガーを実行します。

## サポートされるイベントソース

このLambdaはAmazon EventBridgeによってトリガーされ、以下のセキュリティイベントタイプをサポートします。

| ソースサービス   | イベントタイプ                  | 説明                                    |
| ---------------- | ------------------------------- | --------------------------------------- |
| Amazon GuardDuty | GuardDutyセキュリティFinding    | 不正アクセス、暗号通貨マイニング活動    |
| Amazon Inspector | Inspector2セキュリティFinding   | クリティカルな脆弱性の発見              |
| AWS CloudTrail   | CloudTrailによるAWS API呼び出し | リスクの高いIAMポリシー変更             |
| Amazon Macie     | MacieセキュリティFinding        | 機密データの露出 / パブリックS3アクセス |

## 主な責務

### 1. 集中イベント処理

- イベントソースとタイプを識別
- セキュリティインシデントを分類

### 2. セキュリティイベントのロギング

- 構造化されたJSONログをAmazon S3に保存
- AthenaおよびQuickSightによる下流分析をサポート

### 3. セキュリティアラート通知

- 処理された各イベントに対してリアルタイムアラートを送信
- アラートにはイベントソース、タイプ、処理結果を含む

------

### 4. 自動応答オーケストレーション

イベントタイプに基づいて、Lambdaは専用のAWS Step Functionsステートマシンをトリガーし、さらなる自動修復を実行します。

| インシデントタイプ           | Step Functionsステートマシン |
| ---------------------------- | ---------------------------- |
| 不正アクセス                 | SFN-UnauthorizedAccess       |
| 暗号通貨マイニング           | SFN-CryptoMining             |
| InspectorクリティカルFinding | SFN-InspectorCritical        |
| IAMポリシー変更              | SFN-IAMPolicyChange          |
| Macie機密データ              | SFN-MacieSensitiveData       |

⚠ Step Functions内の修復アクションは、**本番環境リソースを変更する代わりにアーキテクチャ設計を示すためのプレースホルダーとして意図的に実装されています**。

## IAM権限

Lambda実行ロールには以下の権限が必要です。

- Amazon S3: `PutObject`
- Amazon SNS: `Publish`
- AWS Step Functions: `StartExecution`
- Amazon CloudWatch Logs: 基本的なログ記録権限

## 設計ノート

- このLambdaは単一エントリのセキュリティ制御ポイントとして設計されています
- 可観測性、監査可能性、拡張性を重視しています
- 検出、オーケストレーション、修復のロジックを分離しています
- SOCスタイルのセキュリティ監視および分析ユースケースに適しています