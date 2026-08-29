# Demo Destination Rules

Source: https://notes.kodekloud.com/docs/Istio-Service-Mesh/Traffic-Management/Demo-Destination-Rules/page

This tutorial covers configuring traffic splitting in Istio using Destination Rules and Virtual Services to manage service endpoint routing.

In this tutorial, we will create new subsets using Destination Rules and route traffic to grouped service endpoints. You will learn how to update your Istio configuration with custom labels, modify the Virtual Services, and manage traffic distribution between different versions of the reviews service.

## Overview

Initially, the reviews service has three subsets defined by version labels: V1, V2, and V3. The corresponding Virtual Service configuration routes traffic based on these subsets. However, there may be scenarios when you need to group different deployments under a new rule or label. In our example, we introduce a new label (`test: beta`) to group deployments and update the existing configurations accordingly.

<Callout icon="lightbulb">
  Ensure that any changes to labels also reflect in the corresponding Destination Rule and Virtual Service configurations to avoid routing mismatches.
</Callout>

## Updating the Reviews Service

First, we add the new label to our application. The new label (`test: beta`) allows us to create additional subsets without affecting the initial routing for Version V1. In this example, we copy `reviews.yml` from the samples directory and proceed to update it.

### Step 1: Open the File

Use your terminal to open the `reviews.yml` file:

```bash theme={null}
istio-training@local istio-1.10.3 $ vi reviews.yml
```

### Step 2: Add the New Label

For the reviews service, add the label `test: beta` and ensure Version V1 is skipped for the new grouping:

```yaml theme={null}
