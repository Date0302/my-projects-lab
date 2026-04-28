# AWS Image Processing System (Lambda Functions)

#### 🌐 言語 / Language / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

このプロジェクトは、AWSサーバーレスアーキテクチャ上に構築された画像アップロード・処理システムを含みます。中核ロジックは3つのLambda関数で構成されています。

各Lambdaはシステム内で異なる役割を担い、連携して以下を実現します：

安全な画像アップロード、非同期画像処理、処理結果通知、システム監視

このREADMEファイルは、3つのLambdaの機能とシステムアーキテクチャの説明をまとめています。

### システムの主な特徴：

- 完全サーバーレス＆自動スケーリング
- 非同期SQSによる疎結合
- S3分離ストレージ（原画 / 処理済み画像）
- Cognitoによる安全なアップロード
- CloudWatchメトリクス監視
- プロダクショングレードの拡張可能なアーキテクチャ

## 含まれるLambda関数

システムには3つのLambdaが含まれています：

1. `generate-upload-url`（フロントエンドにプリサインドURLを生成）
2. `image-processor-lambda`（バックグラウンド画像処理 → DynamoDB → SNS）
3. `s3-metrics-lambda`（S3監視メトリクス → CloudWatch）

以下に詳細を説明します。

### 1. Generate-Upload-URL Lambda

#### 機能

ログイン済みのCognitoユーザーに対して、プリサインドアップロードURL（PUT）を生成します。

各ユーザーがアップロードした画像が自動的に専用ディレクトリに配置されることを保証します。

フロントエンドはこのURLを使用して、AWSキーを公開せずに画像を安全にアップロードできます。

#### 入力（API Gatewayから）

JWTオーソライザーによってユーザーID（Cognito User ID）が自動的に渡されます。

#### 出力

{
  "upload_url": "<PresignedURL>",
  "file_path": "user-uploads/<userId>/<uuid>.jpg"
}

#### セキュリティ機能

認証されたCognitoユーザーのみが呼び出し可能です。

S3プリサインドURLの有効期間は5分です。

ユーザーの分離を保証し、他人のファイルを上書きしないようにします。

### 2. image-processor-lambda

このシステムの中核となる処理Lambdaです。

#### 機能

- SQSキューからメッセージを受信します。
- 元の画像をダウンロードします（S3）。
- Pillowを使用してサムネイルを生成します。
- 処理結果をprocessedバケットにアップロードします。
- DynamoDBに書き込みます（画像メタデータ）。
- SNS通知メールを送信します。

#### バックエンド非同期処理の利点

- 高並行処理
- 疎結合
- Lambdaの自動スケーリング
- 各タスクは独立しており、他のタスクをブロックしません。

#### 出力（DynamoDBに書き込まれるデータ例）

{
  "imageId": "uuid",
  "originalS3Key": "user-uploads/xxx/xxx.jpg",
  "processedS3Key": "processed/uuid.jpg",
  "status": "DONE"
}

### 3. S3 Metrics Monitoring Lambda

#### 機能

定期的（設定可能：1分、5分、1時間など）に統計を取ります：

- S3画像数
- S3合計サイズ（バイト）

そしてCloudWatchに報告します：

- Namespace: `CustomS3`
- Metrics: `BucketSizeBytes` `NumberOfObjects`

#### 目的

- レポーティング
- コスト監視
- CloudWatchアラームの作成を可能にします（例：S3バケットがほぼ満杯になったとき）

#### 依存関係

純粋な `boto3` のみで、追加のライブラリは不要です。

