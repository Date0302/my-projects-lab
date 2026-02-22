# Project Structure

#### 🌐 言語 / Language / 语言

 英語: [project-structure.md](project-structure.md)                                               日本語: [project-structure.ja.md](project-structure.ja.md)

Images Processing Project/
│
├── Lambda/
│   ├── image-processor/
│   │   ├── lambda_function.py
│   │   ├── image_service.py
│   │   ├── storage_service.py
│   │   ├── metadata_service.py
│   │   ├── notification_service.py
│   │   ├── requirements.txt
│   │   └── Tests

│   │
│   ├── Generate-Upload-URL/
│   │   ├── lambda_function.py
│   │   └── requirements.txt
│   │
│   └── s3-storage-monitor/
│       ├── lambda_function.py
│       └── requirements.txt
│
├── Deployment/
│   ├── s3-setup.md/
│   ├── sqs lambda flow.md/
│   ├── cognito setup.md/
│   └── Deployment.md
│
├── IAM/
│   ├── lambda-role.json
│   ├── s3-policy.json
│   ├── sqs-policy.json
│   ├── dynamodb-access-policy.json
│   ├── sns-publish-policy.json
│   └── cognito-identity-policy.json
│
├── docs/
│   ├── architecture.md
│   ├── performance.md
│   ├── monitoring.md
│   └── project-structure.md
│
├── architecture.drawio
├── architecture.pdf
│
├── .gitignore
└── README.md

## 説明

lambda/
AWS Lambda関数を格納しています。画像処理やシステムイベントの処理を担当します。

docs/
アーキテクチャ、モニタリング、パフォーマンスに関するドキュメントが含まれています。

requirements.txt
プロジェクトの依存関係を定義しています。

README.md
プロジェクトの概要と使用方法を提供します。