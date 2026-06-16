# Infrastructure Overview

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

このドキュメントでは、Cost-Aware GenAI Document Assistant プロジェクトのインフラストラクチャコンポーネント、設計判断、運用面について説明します。プラットフォーム全体は AWS サーバーレスサービス上に構築されており、スケーラビリティ、低メンテナンス、コスト効率を確保しています。

## インフラストラクチャアーキテクチャ（高レベル）

インフラストラクチャは 4 つの論理レイヤーで構成されています。

1. 取り込みレイヤー – S3 + Step Functions + Lambda（ドキュメント処理とベクトル化用）
2. クエリとルーティングレイヤー – API Gateway + Cognito + Lambda（Orchestrator）+ Bedrock + OpenSearch Serverless
3. 非同期メッセージングレイヤー – SQS（負荷の高い処理タスクを分離するため、オプションだが耐障害性のために含む）
4. 可観測性と分析レイヤー – CloudWatch、DynamoDBエクスポート、Athena、QuickSight、SNS

すべてのリソースは AWS CDK または Terraform でプロビジョニングされます（IaCテンプレートはリポジトリにあります）。

## コアインフラストラクチャコンポーネント

### AWS Lambda

|       関数名        |                             用途                             |
| :-----------------: | :----------------------------------------------------------: |
| document-processor  | アップロードされたドキュメント（PDF/TXT）からテキストを抽出、チャンク分割、クリーニングします。 |
| embedding-generator | Bedrock Titan Embeddings を呼び出してテキストチャンクをベクトル化します。 |
|    orchestrator     | コアルーティングロジック：セマンティック検索、モデル選択、コスト記録。 |
|    query-router     |       （オプション）質問の複雑さを判断する軽量分類器。       |

すべての Lambda 関数は次のように構成されています。

1. メモリ: 512 MB – 1024 MB（ワークロードに依存）
2. タイムアウト: 3分（ドキュメントプロセッサ）/ 30秒（オーケストレーター）
3. 予約同時実行数: 10（コストを制御し、暴走的なスケーリングを防ぐ）
4. 失敗した非同期呼び出し用の SQS によるデッドレターキュー（DLQ）

### Amazon S3

|       バケット名        |                             用途                             |
| :---------------------: | :----------------------------------------------------------: |
| raw-documents-<account> | アップロードされた元のドキュメントを保存（バージョニング有効、SSE-S3暗号化）。 |
|   cost-logs-<account>   | DynamoDBエクスポートをParquet形式で受け取り、Athenaクエリに使用します。 |

イベント通知: raw-documents バケットは s3:ObjectCreated:* イベントを EventBridge ルールに送信し、それが Step Functions ワークフローをトリガーします。

### Amazon SQS

ワークフローステージ間の非同期分離に使用されます。特に非クリティカルまたは再試行が多いタスクに適しています。

|       キュー名       |                             用途                             |
| :------------------: | :----------------------------------------------------------: |
| doc-processing-queue | ドキュメント取り込みパイプラインからのメッセージを保持し、`document-processor` Lambda が消費します。 |
|   embedding-queue    | （オプション）テキストチャンク分割と埋め込み生成を分離します。 |

**設定**：

1. 可視性タイムアウト: 5分
2. 再送信ポリシー: 3回の受信試行後に DLQ へ
3. FIFOキューは不要（冪等処理）

### AWS Step Functions

ドキュメント取り込みワークフローをオーケストレーションします。
1. テキスト抽出
2. チャンク分割
3. 埋め込み生成
4. OpenSearch Serverless へのインデックス作成

ステートマシンには、Bedrock のスロットリングエラーに対する再試行と、障害時の Catch ブロック（CloudWatch と SNS にログ記録）が含まれています。

### Amazon DynamoDB

| テーブル名        | 用途                                                         |
| ----------------- | ------------------------------------------------------------ |
| cost-logs         | 呼び出しごとのコストデータ（userId、modelId、inputTokens、outputTokens、estimatedCostUsd、timestamp）を保存します。 |
| document-metadata | （オプション）ドキュメント処理ステータス（アップロード済み → ベクトル化済み）を追跡します。 |

機能：

1. オンデマンド容量（または自動スケーリング付きプロビジョニング容量）
2. cost-logs の TTL（Time To Live）– 90日
3. DynamoDB Streams → S3エクスポート（長期分析用）

### Amazon OpenSearch Serverless

1. コレクション名: rag-vector-store
2. インデックスマッピング: knn_vector（次元 = 1536、Titan Embeddings用）
3. メタデータフィールド: `documentId`、`chunkIndex`、`sourceBucket`、`uploadTime`
4. 暗号化: AWS KMS（カスタマーマネージドキー）

### Amazon Bedrock

アカウントで有効になっているモデル：
|           モデル           |           ユースケース           |
| :------------------------: | :------------------------------: |
| amazon.titan-embed-text-v1 | テキストをベクトル化（1536次元） |
|   amazon.titan-text-lite   |      低コストの事実ベースQA      |
| anthropic.claude-3-sonnet  |       高推論能力の複雑なQA       |

### API Gateway と Cognito

- **API Gateway**（REST）：
  - エンドポイント: POST /upload（プリサインドURL生成）、POST /query
  - スロットリング: 毎秒1000リクエスト、バースト2000
  - CORS有効
- **Cognito ユーザープール**：
  - すべてのエンドポイントに JWT オーソライザーをアタッチ
  - アクセストークンの有効期間: 1時間

### AWS IAM

すべての関数とサービスは最小権限の原則に従います。

1. Lambda実行ロール: 特定の生バケットに対する s3:GetObject、特定のモデルARNに対する bedrock:InvokeModel、コストテーブルに対する dynamodb:PutItem のみを許可。
2. S3バケットポリシー: 暗号化されていないアップロードを拒否、パブリックアクセスを制限。
3. Step Functionsロール: Lambda呼び出し、DynamoDB更新、SNS公開の最小限のアクション。

## デプロイワークフロー（IaC）

インフラストラクチャは完全にコードとして定義されています。デプロイ手順：

1. 前提条件：
   - 管理者権限で設定された AWS CLI（初回デプロイ用）
   - Node.js 18+（CDK）または Terraform 1.3+
   - ターゲットリージョン（us-east-1 または us-west-2）で Bedrock モデルが有効になっていること

2. 手順：
   ```bash
   # AWS CDK を使用
   cdk bootstrap
   cdk deploy --all
   
   # Terraform を使用
   terraform init
   terraform apply -auto-approve

3. デプロイ後：
   - Cognito テストユーザーを作成（AWSコンソールまたはCLI経由）
   - スタック出力から API Gateway エンドポイント URL をメモ

デプロイにより、上記のすべてのリソース（S3バケット、Lambda関数、Step Functionsステートマシン、SQSキュー、OpenSearchコレクション、CloudWatchダッシュボード）が作成されます。

## セキュリティ設計

| 項目             | 実装                                                         |
| ---------------- | ------------------------------------------------------------ |
| 保存時の暗号化   | S3（SSE‑S3）、DynamoDB（デフォルト暗号化）、OpenSearch（KMS） |
| 転送中の暗号化   | すべてのAPIコール、Bedrockエンドポイント、サービス間通信で TLS 1.2+ を使用 |
| 認証             | Cognito JWT（すべてのユーザー向けAPIで必須）                 |
| 認可             | リソースベースのポリシーを持つ IAM ロール（例：Lambdaは自身のS3プレフィックスにのみアクセス可能） |
| シークレット管理 | APIキーは AWS Secrets Manager に保存（ある場合）、Lambda環境変数から参照 |
| サービス分離     | 各Lambdaは独自のVPCで実行？不要（サーバーレス）。ただし、OpenSearch をプライベートサブネットにデプロイする場合は VPC エンドポイントを追加。 |

## 監視とロギング（CloudWatch）

別途 [CloudWatch Monitoring](./CloudWatch%20Monitoring.md) ドキュメントも参照してください。

自動的に作成されるロググループ：

1. すべての Lambda 関数（`/aws/lambda/<function-name>`）
2. Step Functions 実行履歴
3. API Gateway アクセスログ

Lambda が発行するカスタムメトリクス：

1. CostPerInvocation（USD）– ディメンション: ModelId
2. RoutingDecision（1 = 低コストパス、2 = 高コストパス）

アラーム：

1. HighDailyCost – `TotalDailyCost > 5` で SNS メールを送信
2. LambdaThrottling – 5分間のスロットル数 > 10 で SNS を送信
3. StepFunctionFailure – ステートマシンの実行が失敗したら SNS を送信

ダッシュボード：

1. GenAI-Operations: Lambda 呼び出し、エラー、実行時間、スロットルを表示
2. GenAI-Cost: モデル別のコスト傾向とリクエスト分布を表示

## 高可用性と障害復旧

1. すべてのサービスはリージョナル（デフォルト us-east-1）で、AZ間の自動フェイルオーバーを備えています。
2. S3 と DynamoDB に永続化されたデータは 3 つの AZ 間で複製されます。
3. クロスリージョン DR（このデモでは実装されていません）を行う場合は、次のようにします。
   （1）生ドキュメントに対して S3 クロスリージョンレプリケーション（CRR）を有効にする。
   （2）コストログに DynamoDB グローバルテーブルを使用する。
   （3）スナップショット/リストアで OpenSearch インデックスを複製する。

## コスト最適化に関する注意事項

1. Lambda の同時実行制限により、負荷スパイク時のコスト暴走を防ぎます。
2. SQS キューがバッファとして機能するため、アップロードごとに直接 Bedrock を呼び出すことはありません。
3. DynamoDB の TTL により古いコストログを自動削除し、Athena クエリは必要なパーティションのみをスキャンします。
4. OpenSearch Serverless の容量は `capacity.autoscaling = true` に設定され、最小 2 OCU です。

**関連ドキュメント**：

- [Deployment Overview](./Deployment-overview.md)
- [S3 Architecture](./S3%20Architecture.md)
- [SQS Architecture](./SQS%20Architecture.md)
- [CloudWatch Monitoring](./CloudWatch%20Monitoring.md)
- [Main README](./README.md)