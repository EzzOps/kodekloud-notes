# Policies

Source: https://notes.kodekloud.com/docs/Spacelift-Elevate-Your-Infrastructure-Deployment/Spacelift-Basics/Policies/page

This article explains how to create and manage policies in Spacelift to enforce restrictions during Terraform plans.

In this article, we explain how to work with policies in Spacelift to enforce restrictions during a Terraform plan. For instance, you can create a policy to allow only specific instance types—such as t2.micro—to prevent unwanted resource configurations and avoid unnecessary expenditures.

────────────────────────────

## Creating a New Policy

Start by navigating to the Policies tab in Spacelift and create a new policy. For example, name it "instance size policy." When prompted, select a plan policy since this type enforces rules during the planning phase and can fail a run if a rule is violated.

Below is an example of a base policy written in Go for Spacelift:

```go theme={null}
package spacelift
