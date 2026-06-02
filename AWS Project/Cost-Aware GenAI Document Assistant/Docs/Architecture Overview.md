# Architecture Overview

## Project Overview

This project is a serverless AI workflow platform built on AWS.

The platform uses modular AWS Lambda functions to process documents, generate embeddings, and route queries within a scalable cloud-native architecture.

## Core Components

| Component                  | Purpose                        |
| -------------------------- | ------------------------------ |
| Orchestrator Lambda        | Coordinates workflow execution |
| Document Processor Lambda  | Processes uploaded documents   |
| Embedding Generator Lambda | Generates simulated embeddings |
| Query Router Lambda        | Routes user queries            |

## AWS Services

- AWS Lambda
- Amazon S3
- Amazon SQS
- Amazon CloudWatch
- AWS IAM

## Architecture Goals

- Serverless scalability
- Modular workflow design
- Event-driven processing
- Centralized monitoring
- Secure IAM-based access control