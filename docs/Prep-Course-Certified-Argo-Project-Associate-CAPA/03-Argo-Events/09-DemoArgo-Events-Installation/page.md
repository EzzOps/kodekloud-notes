# In another terminal:
curl -d '{"message":"hello"}' -H "Content-Type: application/json" -X POST http://localhost:13000/push
# Expected response:
# success
```

2. Create a MinIO credentials secret in the `argo-events` namespace:

```bash theme={null}
kubectl -n argo-events create secret generic minio-creds \
  --from-literal=accesskey=admin \
  --from-literal=secretkey=password
# Output:
# secret/minio-creds created
```

3. Trigger the external HTTP endpoint used by the HTTP trigger (example using httpdump):

```bash theme={null}
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"username":"Marcel","password":"supersecret","this is a":"test"}' \
  https://httpdump.app/dumps/6758c612-9d34-486f-b82a-63c0a7dc4054
```

Sensor logs and troubleshooting

When triggers run or fail, inspect sensor logs to diagnose behavior:

* Successful HTTP trigger logs (example):

```text theme={null}
namespace=argo-events, sensorName=multi-dependency-sensor-2, triggerName=http-trigger, level=info, time=2025-10-25T11:41:03Z, msg=Making a http request...
namespace=argo-events, sensorName=multi-dependency-sensor-2, level=info, time=2025-10-25T11:45:16Z, msg=Successfully processed trigger 'http-trigger'
```

* RBAC/permission error for Workflow trigger (example):

```text theme={null}
time="2025-10-25T11:43:28.979Z" level=error msg="Create request failed" error="workflows.argoproj.io is forbidden: User \"system:serviceaccount:argo-events:default\" cannot create resource \"workflows\" in API group \"argoproj.io\" in the namespace \"argo\""
Error: Failed to submit workflow: rpc error: code = PermissionDenied desc = "workflows.argoproj.io is forbidden: User \"system:serviceaccount:argo-events:default\" cannot create resource \"workflows\" in API group \"argoproj.io\" in the namespace \"argo\""
```

Fixes:

* Ensure the trigger template includes `serviceAccountName` (as shown in the sensor YAML).
* Grant that service account the necessary RBAC roles to create Workflows in the target namespace.

Event flow and UI

A visual graph helps map how event sources, sensors, dependencies, conditions, and triggers relate. The UI shows nodes for event sources, sensors, each dependency, and the triggers that fire when conditions are met.

<Frame>
  <img alt="A screenshot of the Argo Events &#x22;Event Flow&#x22; web UI showing a visual node graph of event sources, sensors, conditions, and workflow triggers. Visible nodes include labels like &#x22;example&#x22;, &#x22;my-webhook&#x22;, &#x22;minio&#x22;, &#x22;webhook-sensor&#x22;, &#x22;multi-dependency-sensor-2&#x22;, &#x22;test-dep&#x22;, and &#x22;hello-workflow-trigger&#x22;." />
</Frame>

When everything is configured and RBAC is correct, triggers will execute and generate expected outputs — for example, HTTP dumps and Argo Workflows. After updating the sensor to include the proper service account, a new workflow should appear in the Argo Workflows list.

<Frame>
  <img alt="A screenshot of the Argo Workflows web UI showing a list of workflow entries with names, namespaces, start/finish times, durations and progress. A left sidebar shows filters and a workflow summary, and the top has buttons to submit new or view completed workflows." />
</Frame>

Summary

* Use dependency names inside `conditions` expressions to control trigger execution.
* Use && and || to combine dependency conditions; parentheses support grouping.
* If `conditions` is omitted, all sensor dependencies must be satisfied (implicit AND).
* For Argo Workflow triggers, set `serviceAccountName` and ensure the service account has RBAC permissions to create Workflows in the target namespace.

<Callout icon="lightbulb">
  Tip: When testing triggers, inspect sensor logs (kubectl -n \<ns> logs \<sensor-pod>) to see why a trigger did or didn't execute. Permission errors and missing dependency events are common causes for trigger failures.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/9aa7ef66-4228-49f6-88b5-ea0620c511ac" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/1d67f5a4-74b5-4121-892b-f68b5d87c82f/lesson/f2ab6559-02a0-4c5e-8ad9-fd950b0c4c89" />
</CardGroup>


# DemoArgo Events Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Events/DemoArgo-Events-Installation/page

Guide to install and verify Argo Events on Kubernetes, optionally integrate Argo Workflows, inspect resources, view UI integration, and troubleshoot common startup issues.

This guide shows how to install Argo Events into a Kubernetes cluster, verify the controller is running, and optionally integrate Argo Workflows so you can trigger workflows from events. Follow the steps below to deploy the controller, inspect installed resources, and troubleshoot common startup issues.

## Overview

* Install the argo-events namespace and Argo Events manifests.
* (Optional) Install Argo Workflows if you plan to trigger workflows from events.
* Verify CRDs, RBAC, config maps, and the controller deployment.
* Inspect pods and logs to ensure the controller becomes Ready.
* Use the Argo Workflows UI to view EventSources and Sensors when integrated.

## Prerequisites

* A Kubernetes cluster with kubectl configured to target the cluster.
* (Optional) If you plan to use the Argo Workflows UI, install Argo Workflows into the cluster.

## Installation

Create the argo-events namespace and apply the official Argo Events install manifest:

```bash theme={null}
kubectl create namespace argo-events
kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-events/stable/manifests/install.yaml
