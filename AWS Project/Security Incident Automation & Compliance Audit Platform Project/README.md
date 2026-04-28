# AWS Security Log Analytics Project

#### 🌐 Language / 言語 / 语言

 🇺🇸English: [README.md](README.md)                                                🇯🇵日本語: [README.ja.md](README.ja.md)                                         🇨🇳中文: [README.CN.md](README.CN.md)

## Overview
This project implements a security log analytics and visualization platform
using native AWS services.  
It focuses on collecting, analyzing, and visualizing AWS security-related logs
for audit and threat detection purposes.

The project is designed as a learning and demonstration project
to showcase AWS security architecture, log analytics, and visualization skills.

## Architecture
The architecture is based on a centralized logging and analytics approach.

Main flow:

AWS CloudTrail generates management event logs

Logs are stored in an encrypted Amazon S3 bucket

Amazon Athena is used to query logs directly from S3

Amazon QuickSight is used to build security dashboards

AWS Lambda is used for testing and simulating security events

Amazon EventBridge is used to trigger Lambda functions

(Architecture diagram provided in the repository)

## AWS Services Used
AWS CloudTrail

Amazon S3

AWS Lambda

Amazon EventBridge

Amazon Athena

Amazon QuickSight

AWS IAM

AWS KMS

## Key Features
Centralized storage of CloudTrail logs in S3

Serverless log analytics using Athena

Security-related API activity analysis

Visualization of AWS account activity using QuickSight

Encrypted log storage using AWS KMS

Least-privilege IAM role design

## Security Design
CloudTrail logs are encrypted using AWS KMS

S3 bucket enforces default server-side encryption

IAM roles follow least-privilege principles

Analytics is read-only and does not modify production resources

## Project Status
This project is completed as a hands-on security analytics lab.
Some queries and dashboards are simplified for demonstration purposes.
