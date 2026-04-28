# README

## Project Overview

This repository showcases my comprehensive skills in AWS cloud computing, serverless architecture, event-driven systems, and cloud security management. It contains two main projects:

1. Images Processing Project: Automated processing, asynchronous task scheduling, and secure storage for user-uploaded images.
2. Security Incident Automation & Compliance Audit Platform Project: An enterprise-grade security management and incident response platform.

Through these two projects, I demonstrate my practical abilities in AWS service integration, cloud architecture design, serverless computing, and security protection.

## 1. Images Processing Project

### Project Goals

User uploads image → Automatic processing → Secure storage

Asynchronous task scheduling to improve system scalability

Demonstrates integration of Lambda, S3, SQS, and Cognito.

### Core Components

Lambda Functions: Image upload, asynchronous processing, task notification.

S3: Original and processed image storage.

SQS: Asynchronous task queue.

Cognito: User registration and authentication.

IAM: Least-privilege role management.

## 2. Security Incident Automation & Compliance Audit Platform Project

### Project Goals

Simulate enterprise-grade AWS security scenarios.

Configure GuardDuty to monitor anomalous access.

Manage permissions using IAM policies and roles.

Build event-driven security response workflows.

### Core Components

GuardDuty: Real-time security threat monitoring.

EventBridge: Event routing and rule triggering.

Lambda: Automated security incident response.

IAM: User and role permission management.

## 3.Deployment Guide 

1. Configure AWS CLI and set access keys.
2. Create S3 buckets (for images project & security logs).
3. Configure IAM roles and policies, ensuring least privilege.
4. Deploy Lambda functions and configure triggers.
5. Configure SQS queues (images project) or EventBridge rules (security project).
6. Set up Cognito User Pool (images project).
7. Test the complete workflow to ensure normal image processing and security incident response.

## 4.Tech Stack

AWS Services: Lambda, S3, SQS, IAM, Cognito, GuardDuty, EventBridge, CloudWatch, SNS

Programming Language: Python 3.11+

Tools: draw.io

## 5.Project Highlights

Demonstrates full-stack AWS capabilities: serverless architecture + asynchronous processing + security management.

Implements event-driven, automated workflows and high-availability architecture.

Emphasizes security and access control, adhering to the principle of least privilege.
