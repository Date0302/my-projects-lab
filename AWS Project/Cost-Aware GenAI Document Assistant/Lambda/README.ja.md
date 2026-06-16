# README

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

このプロジェクトには、ドキュメントの取り込み、ベクトル化、インテリジェントなQAルーティング、およびコストを考慮した意思決定を実現する4つのコアLambda関数が含まれています。以下に、各関数の責務、入出力、モック実装の説明、および本番環境で想定される代替案を示します。

## 関数リスト

|       関数名        |                             責務                             |               トリガー方法                |
| :-----------------: | :----------------------------------------------------------: | :---------------------------------------: |
| Document-processor  |    ドキュメントのテキスト抽出、チャンク分割、クリーニング    | S3イベント → EventBridge → Step Functions |
| Embedding-generator |       テキストチャンクをベクトルに変換（現状はモック）       |       Step Functionsによる呼び出し        |
|    Orchestrator     | ドキュメント処理とembedding生成ワークフローのオーケストレーション |       Step Functionsステートマシン        |
|    Query-router     |        質問の分類、モデルルーティング、コスト見積もり        |      API Gateway → Lambda（同期的）       |

## 1. Document-processor

### 責務
1.S3からアップロードされた生ドキュメント（PDF / TXT）を読み取る

2.テキストコンテンツを抽出する

3.チャンク分割とクリーニング（余分な空白、特殊文字の削除）を実行する

4.後続のベクトル化のために構造化されたテキストチャンクを出力する

### 現在の実装（モック）
1.S3やBedrockには実際に接続していない

2.イベントから `document_name` と `content` フィールドを受け取る

3.単語数をカウントしてログに記録する

### 入力例
```json
{
  "document_name": "sla_definition.pdf",
  "content": "A Service Level Agreement (SLA) is a commitment between a service provider and a customer..."
}
```

### 出力例

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

### 本番環境で想定される代替案
1.boto3を使用してS3のget_objectを呼び出す

2.PyPDF2 / pdfplumberを統合してPDFを解析する

3.固定サイズまたは意味境界でチャンク分割する

4.クリーニング済みテキストチャンクをS3ステージングに保存するか、次のステップに直接渡す

### IAM権限（最小例）
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::raw-documents-*/*"
}
```

## 2. Embedding-generator

### 責務
1. テキストチャンクを受け取り、Amazon Bedrock Titan Embeddingsモデルを呼び出す

2. 1536次元のベクトルを生成する

3. ベクトルとメタデータをOpenSearch Serverlessに書き込む

### 現在の実装（モック）
1. MD5ハッシュを使用して埋め込みベクトルをシミュレート（ワークフローの完全性を示すためのみ）

2. 実際のベクトルは生成せず、BedrockやOpenSearchにも接続しない

### 入力例
```json
{
  "text": "A Service Level Agreement (SLA) is a commitment..."
}
```

### 出力例
```json
{
  "statusCode": 200,
  "body": {
    "text": "A Service Level Agreement (SLA) is a commitment...",
    "embedding": "a1b2c3d4e5f6...",  // MD5ハッシュ文字列
    "message": "Embedding generated successfully"
  }
}
```

### 本番環境で想定される代替案
1. bedrock-runtime.invoke_model を amazon.titan-embed-text-v1 を使用して呼び出す

2. 返されたベクトル（浮動小数点数のリスト）をOpenSearch Serverlessに書き込む（opensearch-py または requests-aws4auth を使用）

3. タイムアウト時の再試行とエラーハンドリングを追加する

### IAM権限
```json
{
  "Effect": "Allow",
  "Action": ["bedrock:InvokeModel"],
  "Resource": "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v1"
}
```

## 3. Orchestrator

### 責務
1. Step Functionsステートマシンの中核タスクとして機能する

2. ドキュメント処理とembedding生成のステップを調整する

3. 中間データ（ドキュメント名、テキストチャンク）を渡し、最終状態を集約する

### 現在の実装（モック）
1. 実際には他のLambdaやサービスを呼び出さない

2. 同じ関数内で「ドキュメント処理」と「embedding生成」の2つのステップをシミュレートする

3. 集約された状態オブジェクトを返す

### 入力例
```json
{
  "document_name": "sla_definition.pdf",
  "text": "Full extracted text ..."
}
```

### 出力例
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

### 本番環境で想定される代替案
1. Step FunctionsのLambda Invokeタスクを使用して、それぞれDocument-processorとEmbedding-generatorを呼び出す

2. 前のステージの出力を次のステージの入力として渡す

3. エラーキャプチャと再試行戦略を追加する（Step Functions定義内で設定）

### IAM権限
追加の権限は不要（オーケストレーターとしてのみ機能し、実際の呼び出しはStep Functionsが直接行う；関数内からの呼び出しが必要な場合はlambda:Invokeが必要）

## 4. Query-router

### 責務
1. ユーザーの自然言語による質問を受け取る

2. 質問の複雑さを判断する（単純 / 複雑）

3. 適切なBedrockモデルを選択する（低コスト vs. 高品質）

4. 推論コストを見積もり、ルーティングの決定を返す

### 現在の実装（実際のロジック、デモ可能）
1. キーワードルール + 長さに基づく軽量な分類器

2. モデル名と見積もりコストを返す（ハードコードされた価格、Bedrockの価格設定に準拠）

3. Bedrockは実際には呼び出さず、ルーティング決定のみを出力する

### 分類ルール
| 条件                                              | 判定    | モデル                      | 見積もりコスト |
| ------------------------------------------------- | ------- | --------------------------- | -------------- |
| compare/analyze/why/architecture/trade-off を含む | complex | `anthropic.claude-3-haiku`  | $0.0025        |
| what/define/who/when を含む                       | simple  | `amazon.titan-text-lite-v1` | $0.0002        |
| 質問の長さ > 15 単語                              | complex | `anthropic.claude-3-haiku`  | $0.0025        |
| その他                                            | simple  | `amazon.titan-text-lite-v1` | $0.0002        |

### 入力例
```json
{
  "question": "What is the difference between a standard SLA and a premium SLA?"
}
```

### 出力例
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

### 本番環境で想定される代替案
1. **軽量な分類モデル**（例：Hugging Faceの蒸留モデル）を追加して精度を向上させる

2. 対応するBedrockモデルを実際に呼び出し、回答を返す

3. 実際のトークン数とコストをDynamoDBに書き込む

### IAM権限
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

## デプロイとテスト（ローカルモック）

すべての関数は、sam local または python-lambda-local を使用してローカルでテストできます。

### 例：Query-routerのテスト
```bash
# event.jsonを作成
echo '{"question": "What is an SLA?"}' > event.json

# sam localを使用
sam local invoke Query-router --event event.json
```

### 統合テストの推奨事項
1. Step Functionsローカルシミュレーションを使用してOrchestratorワークフローを実行する
2. Document-processorとEmbedding-generatorのモック出力を連鎖させる
3. API Gatewayを介してQuery-routerを呼び出し、ルーティングロジックを検証する

## モックから本番への主な違い

| 側面                             | 現在の実装（ポートフォリオ）    | 本番環境実装                               |
| -------------------------------- | ------------------------------- | ------------------------------------------ |
| ドキュメント解析                 | contentフィールドを直接受け取る | S3読み取り + PDF/TXT解析ライブラリ         |
| ベクトル化                       | MD5ハッシュ                     | Bedrock Titan Embeddings + OpenSearch      |
| ワークフローオーケストレーション | 単一関数でのモック              | Step Functionsによる関数間調整             |
| モデル呼び出し                   | ルーティング決定のみ            | 実際の `invoke_model` + ストリーミング応答 |
| コスト記録                       | ハードコード                    | 実際のトークンベース計算 + DynamoDB        |
| 可観測性                         | CloudWatchログ                  | X-Rayトレーシング + カスタムメトリクス     |