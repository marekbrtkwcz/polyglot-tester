# Cloud Diagnostics Reference

Companion to the cloud knowledge: commands that answer "who has access",
"what will this plan change", and "has anything drifted".

## IAM — prove least privilege

- Who am I right now: `aws sts get-caller-identity` / `gcloud auth list`.
- Can this identity do X (before granting it):
  `aws iam simulate-principal-policy --policy-source-arn <arn> --action-names <action> <resource>`.
- Who holds a permission in GCP: `gcloud asset analyze-iam-policy`
  (IAM Policy Analyzer) on the resource in question.
- Root or long-lived key used lately: CloudTrail
  `aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=root`;
  GCP: Cloud Audit Logs filtered to the service account.

## Terraform — before and after apply

- `terraform plan -detailed-exitcode` — exit 0: no changes, 1: error,
  2: there ARE changes. Gate CI on this: a non-interactive `plan` that
  exits 2 means drift or an unapplied change.
- `terraform state list` / `terraform show` — what IaC actually owns right
  now; a resource missing from state but live in the console is a drift bomb.
- `terraform import` — adopt an existing resource; the `plan` afterwards
  must come back clean, or the import is incomplete.
- `terraform force-unlock <id>` — after a crashed apply on a locked state.
- A resource changed by hand shows up as a permanent diff: bring the change
  back into config, never `ignore_changes` it away silently.

## Cost quick checks

- What jumped last week: `aws ce get-cost-and-usage` with a daily
  `--time-period` and `--group-by Tag` (needs Cost Explorer access).
- Untagged spend is invisible spend: `aws resourcegroupstaggingapi get-resources`
  to find untagged resources; budgets + alerts on both clouds.
- Right-size from metrics, not guesses; spot/preemptible for batch only.

## Incident readiness

- The rotation drill: rotate one real secret in Secrets Manager / Secret
  Manager and watch the app — before it has to happen at 2am.
- Know where the kill switches are: who can disable a public bucket, revoke
  a key, or roll back the last apply — and does that need another team?
