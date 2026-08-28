# Leaked S3 Bucket

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Questions-and-Answers-Scenario-Based-Prep/Security/Leaked-S3-Bucket/page

Practical incident response guide for a leaked S3 bucket covering immediate containment, log collection and forensics, remediation, legal notification, and preventive AWS configuration guardrails.

You're three days into a new role and a security audit lands on your desk: an S3 bucket containing customer data (names, emails, support tickets) has been public for six months. Your manager asks for two deliverables: a fast containment action and a credible incident response plan.

Flipping the bucket to private is a correct immediate step — it stops further exposure — but it is only the start. The critical questions remain: who accessed the data, what was taken, and which customers need to be notified? Below is a practical, interview-friendly walkthrough covering containment, evidence collection, remediation, and follow-up.

## 1) Immediate containment — stop the bleeding

Run this immediately to prevent additional downloads.

```bash theme={null}
