# Project Structure

#### 🌐 言語 / Language

 🇺🇸英語: [project-structure.md](project-structure.md)                                               🇯🇵日本語: [project-structure.ja.md](project-structure.ja.md)

Images Processing Project/
# Full Project Structure

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

## Description

lambda/
Contains AWS Lambda functions responsible for processing images and handling system events.

docs/
Contains architecture, monitoring, and performance documentation.

requirements.txt
Defines project dependencies.

README.md
Provides project overview and usage instructions.
