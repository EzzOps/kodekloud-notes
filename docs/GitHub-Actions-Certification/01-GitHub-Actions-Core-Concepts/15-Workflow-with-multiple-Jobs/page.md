# Workflow with multiple Jobs

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-Core-Concepts/Workflow-with-multiple-Jobs/page

This guide explains how to create a multi-job CI/CD pipeline in GitHub Actions, covering job sequencing and artifact sharing.

In this guide, we’ll transform a simple, single-job GitHub Actions workflow into a robust multi-job CI/CD pipeline. You’ll learn how to split **build**, **test**, and **deploy** stages into separate jobs, ensure proper sequencing, and share artifacts between steps.

***

## Table of Contents

1. [Recap: Single-Job Workflow](#recap-single-job-workflow)
2. [Multi-Job Workflow Setup](#multi-job-workflow-setup)
3. [Default Parallel Execution & Failures](#default-parallel-execution--failures)
4. [Common Errors](#common-errors)
5. [Issues to Address Next](#issues-to-address-next)
6. [References](#references)

***

## Recap: Single-Job Workflow

Our original workflow ran every step in one job:

```yaml theme={null}
