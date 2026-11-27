---
name: cloud
description: Cloud fundamentals for AWS and GCP plus Terraform intro: IAM and least privilege, core services (compute, storage, DB, queues), networking basics, and IaC workflow.
display_name: Cloud (AWS/GCP + Terraform)
icon: cloud
---

# Cloud Reference

## IAM — least privilege everywhere

- No root account usage; SSO + short-lived credentials; separate roles per workload.
- Policies: start from zero permissions, add only what's needed; prefer AWS managed policies per job function, then narrow.
- Service accounts (GCP) / roles (AWS) instead of long-lived keys; rotate keys when used.
- Audit: CloudTrail (AWS) / Cloud Audit Logs (GCP) enabled from day one; alert on root usage and policy changes.

## Core services (both clouds)

- **Compute**: EC2 / Cloud Run / GCE / Cloud Functions — containers on Fargate/Cloud Run when possible.
- **Storage**: S3 / Cloud Storage — block public access by default; versioning + lifecycle rules; encryption at rest (KMS).
- **Databases**: RDS / Cloud SQL (managed Postgres/MySQL) or Aurora / Cloud Spanner; private subnets, no public IP.
- **Queues/events**: SQS/SNS, EventBridge / Pub/Sub — for async decoupling.
- **Secrets**: Secrets Manager / Secret Manager — never env files in images.
- **CDN/edge**: CloudFront / Cloud CDN in front of public apps.

## Networking basics

- VPC with public + private subnets; NAT gateway for egress from private; security groups / firewall rules default-deny.
- Private endpoints for S3/DB access from inside the VPC (avoid NAT costs and exposure).

## Terraform / IaC

- State in a remote backend (S3 + DynamoDB lock / GCS) — never local; state contains secrets.
- One repo per environment or workspaces; `terraform plan` in CI, apply only from CI with approval.
- Modules for reusable pieces (vpc, ecs-service, rds); pin provider versions.
- `terraform import` for existing resources; never hand-edit cloud console when IaC owns the resource.

## Cost hygiene

- Budgets + alerts; tag everything (`env`, `owner`, `project`); right-size via metrics; spot/preemptible for batch.

## Official sources

- AWS: docs.aws.amazon.com · Well-Architected: aws.amazon.com/architecture/well-architected · GCP: cloud.google.com/docs · Terraform: developer.hashicorp.com/terraform
