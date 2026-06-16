# README

#### 🌐 Language / 言語 / 语言

🇺🇸English: [README.md](README.md) | 🇯🇵日本語: [README.ja.md](README.ja.md) | 🇨🇳中文: [README.CN.md](README.CN.md)

This project contains 4 core Lambda functions that work together to achieve document ingestion, vectorization, intelligent Q&A routing, and cost-aware decision making. The following describes each function's responsibilities, input/output, mock implementation notes, and expected production-grade alternatives.

## Function List

|    Function Name    |                        Responsibility                        |             Trigger Method              |
| :-----------------: | :----------------------------------------------------------: | :-------------------------------------: |
| Document-processor  |         Document text extraction, chunking, cleaning         | S3 event → EventBridge → Step Functions |
| Embedding-generator |       Convert text chunks to vectors (currently mock)        |        Step Functions invocation        |
|    Orchestrator     | Orchestrate document processing and embedding generation workflow |      Step Functions state machine       |
|    Query-router     |   Question classification, model routing, cost estimation    |   API Gateway → Lambda (synchronous)    |

---

## 1. Document-processor

### Responsibility
1.Read uploaded raw documents (PDF / TXT) from S3

2.Extract text content

3.Perform chunking and cleaning (remove extra whitespace, special characters)

4.Output structured text chunks for subsequent vectorization

### Current Implementation (Mock)
1.Not actually connected to S3 or Bedrock

2.Receives `document_name` and `content` fields from the event

3.Counts words and logs the result

### Input Example
```json
{
  "document_name": "sla_definition.pdf",
  "content": "A Service Level Agreement (SLA) is a commitment between a service provider and a customer..."
}
```

### Output Example

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

### Expected Production-Grade Alternative
1.Use boto3 to call S3 get_object

2.Integrate PyPDF2 / pdfplumber to parse PDF

3.Chunk by fixed size or semantic boundaries

4.Save cleaned text chunks to S3 staging or pass directly to next step

### IAM Permissions (Minimal Example)
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::raw-documents-*/*"
}
```

## 2. Embedding-generator

### Responsibility
1. Receive text chunks, call Amazon Bedrock Titan Embeddings model

2. Generate 1536-dimensional vectors

3. Write vectors and metadata to OpenSearch Serverless

### Current Implementation (Mock)
1. Use MD5 hash to simulate embedding vectors (only for demonstrating workflow integrity)

2. Does not produce real vectors, no connection to Bedrock or OpenSearch

### Input Example
```json
{
  "text": "A Service Level Agreement (SLA) is a commitment..."
}
```

### Output Example
```json
{
  "statusCode": 200,
  "body": {
    "text": "A Service Level Agreement (SLA) is a commitment...",
    "embedding": "a1b2c3d4e5f6...",  // MD5 hash string
    "message": "Embedding generated successfully"
  }
}
```

### Expected Production-Grade Alternative
1. Call bedrock-runtime.invoke_model using amazon.titan-embed-text-v1

2. Write the returned vector (list of floats) to OpenSearch Serverless (using opensearch-py or requests-aws4auth)

3. Add timeout retries and error handling

### IAM Permissions
```json
{
  "Effect": "Allow",
  "Action": ["bedrock:InvokeModel"],
  "Resource": "arn:aws:bedrock:*::foundation-model/amazon.titan-embed-text-v1"
}
```

## 3. Orchestrator

### Responsibility
1. Act as the core task of the Step Functions state machine

2. Coordinate document processing and embedding generation steps

3. Pass intermediate data (document name, text chunks) and aggregate the final state

### Current Implementation (Mock)
1. Does not actually call other Lambdas or services

2. Simulates the two steps "document processing" and "embedding generation" within the same function

3. Returns the aggregated state object

### Input Example
```json
{
  "document_name": "sla_definition.pdf",
  "text": "Full extracted text ..."
}
```

### Output Example
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

### Expected Production-Grade Alternative
1. Use Step Functions' Lambda Invoke tasks to call Document-processor and Embedding-generator respectively

2. Pass the output of the previous stage as input to the next stage

3. Add error capture and retry strategies (configured in the Step Functions definition)

### IAM Permissions
No additional permissions required (acts only as orchestrator; actual invocations are done directly by Step Functions; if in-function invocation is needed, lambda:Invoke is required)

## 4. Query-router

### Responsibility
1. Receive user's natural language question

2. Determine question complexity (simple / complex)

3. Select appropriate Bedrock model (low-cost vs. high-quality)

4. Estimate inference cost and return routing decision

### Current Implementation (Real logic, demonstrable)
1. Lightweight classifier based on keyword rules + length

2. Returns model name and estimated cost (hardcoded prices, consistent with Bedrock pricing)

3. Does not actually call Bedrock, only outputs routing decision

### Classification Rules
| Condition                                           | Judgment | Model                       | Estimated Cost |
| --------------------------------------------------- | -------- | --------------------------- | -------------- |
| Contains compare/analyze/why/architecture/trade-off | complex  | `anthropic.claude-3-haiku`  | $0.0025        |
| Contains what/define/who/when                       | simple   | `amazon.titan-text-lite-v1` | $0.0002        |
| Question length > 15 words                          | complex  | `anthropic.claude-3-haiku`  | $0.0025        |
| Otherwise                                           | simple   | `amazon.titan-text-lite-v1` | $0.0002        |

### Input Example
```json
{
  "question": "What is the difference between a standard SLA and a premium SLA?"
}
```

### Output Example
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

### Expected Production-Grade Alternative
1. Add a **lightweight classification model** (e.g., distilled Hugging Face model) to improve accuracy

2. Actually call the corresponding Bedrock model and return the answer

3. Write real token counts and cost to DynamoDB

### IAM Permissions
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

---

## Deployment and Testing (Local Mock)

All functions can be tested locally using sam local or python-lambda-local.

### Example: Test Query-router
```bash
# Create event.json
echo '{"question": "What is an SLA?"}' > event.json

# Use sam local
sam local invoke Query-router --event event.json
```

### Integration Testing Recommendations
1. Use Step Functions local simulation to run the Orchestrator workflow
2. Chain the mock outputs of Document-processor and Embedding-generator
3. Call Query-router via API Gateway to verify routing logic

## Key Differences from Mock to Production

| Aspect                 | Current Implementation (Portfolio) | Production-Grade Implementation            |
| ---------------------- | ---------------------------------- | ------------------------------------------ |
| Document Parsing       | Directly receives content field    | S3 read + PDF/TXT parsing libraries        |
| Vectorization          | MD5 hash                           | Bedrock Titan Embeddings + OpenSearch      |
| Workflow Orchestration | Single function mock               | Step Functions cross-function coordination |
| Model Invocation       | Routing decision only              | Real `invoke_model` + streaming response   |
| Cost Logging           | Hardcoded                          | Real token‑based calculation + DynamoDB    |
| Observability          | CloudWatch logs                    | X-Ray tracing + custom metrics             |