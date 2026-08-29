# Creating a CodePipeline with Source and Build stage

Source: https://notes.kodekloud.com/docs/Hands-On-AWS-Project-Deploy-Your-First-Crypto-App/CodePipeline-automated-deployment/Creating-a-CodePipeline-with-Source-and-Build-stage/page

Guide to creating an AWS CodePipeline with CodeCommit source and CodeBuild build stages, validating builds, pushing fixes to trigger pipeline, and manually updating ECS service

Welcome — in this lesson we'll create a basic AWS CodePipeline with Source and Build stages, verify a build run, and push a code fix so the pipeline automatically picks it up. This walkthrough assumes you have an existing CodeCommit repository (for example `aws-microservice-project`) and a CodeBuild project (for example `AWS MicroserviceProject`). We'll also show a short Git workflow to push fixes from Cloud9.

## Background: why we needed to fix the app

Earlier we introduced a change that produced a broken task definition (task definition 6) because a few lines were commented out in the application. Below is the problematic version that was reverted from the repository for debugging:

```python theme={null}
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)
