# Solution ReplicaSets optional

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Core-Concepts/Solution-ReplicaSets-optional/page

This guide reviews the ReplicaSets lab exercise, detailing commands, expected outputs, and steps for diagnosing issues and scaling efficiently.

In this guide, we review the ReplicaSets lab exercise by detailing each command, expected output, and the rationale behind every step. Follow along to understand how to diagnose issues, update configurations, and scale your ReplicaSet efficiently.

***

## Checking the Initial State

Before proceeding, verify there are no existing Pods or ReplicaSets in your cluster.

1. List all Pods:

   ```bash theme={null}
   kubectl get pods
   ```

   Expected output:

   ```text theme={null}
   No resources found in default namespace.
   ```

   This confirms that there are currently zero Pods running.

2. List any existing ReplicaSets:

   ```bash theme={null}
   kubectl get replicaset
   ```

   The command similarly shows no ReplicaSets at this point.

***

## Verifying the New ReplicaSet

After applying some changes, a new ReplicaSet is created. Confirm its presence using:

```bash theme={null}
kubectl get replicaset
```

The output should display something similar to:

```text theme={null}
NAME             DESIRED   CURRENT   READY   AGE
new-replica-set  4         4         0       9s
```

This indicates that the new ReplicaSet is configured to have 4 Pods. Running the command a second time reaffirms the same output.

***

## Determining the Image Used by the ReplicaSet

To inspect the details of the ReplicaSet and determine which image is assigned to its Pods, execute:

```bash theme={null}
kubectl describe replicaset new-replica-set
```

Within the Pod Template section under Containers, look for the image field:

```text theme={null}
Image: busybox777
```

Also, the command section appears as:

```text theme={null}
Command:
  sh
  -c
  echo Hello Kubernetes! && sleep 3600
```

This verifies that the ReplicaSet is initially using the image "busybox777".

***

## Examining the Pod Readiness Issue

If the Pods are not transitioning to the Ready state, further investigation is required:

1. Check the replica status:

   ```bash theme={null}
   kubectl describe replicaset new-replica-set
   ```

   You should see an excerpt like:

   ```text theme={null}
   Replicas: 4 current / 4 desired
   Pods Status: 0 Running / 4 Waiting / 0 Succeeded / 0 Failed
   ```

2. Inspect one of the Pods to identify the issue:

   ```bash theme={null}
   kubectl describe pod new-replica-set-7r2qw
   ```

   Notice the container is in a Waiting state with the reason:

   ```text theme={null}
   Reason: ImagePullBackOff
   ```

   And an associated event message:

   ```text theme={null}
   Failed to pull image "busybox777": ... pull access denied, repository does not exist or may require authorization
   ```

<Callout icon="triangle-alert">
  The error indicates that there is no image named "busybox777" available in the repository. Use the standard BusyBox image instead.
</Callout>

***

## Deleting a Pod Managed by the ReplicaSet

ReplicaSets are designed to maintain the desired number of Pods automatically. Even if you delete a Pod, the ReplicaSet immediately replicates a new one.

1. List the Pods:

   ```bash theme={null}
   kubectl get pods
   ```

   Example output:

   ```text theme={null}
   NAME                     READY   STATUS            RESTARTS   AGE
   new-replica-set-wkzjh    0/1     ImagePullBackOff   0          2m59s
   new-replica-set-vpkh8    0/1     ImagePullBackOff   0          2m59s
   new-replica-set-hr2zqw   0/1     ImagePullBackOff   0          2m59s
   new-replica-set-tn2mp    0/1     ImagePullBackOff   0          2m59s
   ```

2. Delete one of the Pods:

   ```bash theme={null}
   kubectl delete pod new-replica-set-wkzjh
   ```

   Confirmation output:

   ```text theme={null}
   pod "new-replica-set-wkzjh" deleted
   ```

3. List the Pods again to note that the ReplicaSet has recreated the missing Pod.

***

## Creating ReplicaSets Using YAML Definition Files

Two YAML definition files are located in the `/root` directory:

* replicaset-definition-1.yaml
* replicaset-definition-2.yaml

### Fixing the First Definition File

The initial content of replicaset-definition-1.yaml is:

```yaml theme={null}
apiVersion: v1
kind: ReplicaSet
metadata:
  name: replicaset-1
spec:
  replicas: 2
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx
```

When running:

```bash theme={null}
kubectl create -f /root/replicaset-definition-1.yaml
```

you encounter the error:

```text theme={null}
error: unable to recognize "/root/replicaset-definition-1.yaml": no matches for kind "ReplicaSet" in version "v1"
```

Inspecting the available API versions with:

```bash theme={null}
kubectl explain replicaset
```

reveals that the correct API version is `apps/v1`. Update the file accordingly. After the change, creation should succeed.

### Fixing the Second Definition File

The content of replicaset-definition-2.yaml is:

```yaml theme={null}
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-2
spec:
  replicas: 2
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: nginx
    spec:
      containers:
        - name: nginx
          image: nginx
```

Creating it results in the error:

```text theme={null}
The ReplicaSet "replicaset-2" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"tier":"nginx"}: selector does not match template labels
```

This occurs because the selector (`tier: frontend`) does not match the Pod template labels (`tier: nginx`). Correct the Pod template labels to use `tier: frontend` so they match the selector. After this fix, create the ReplicaSet again using:

```bash theme={null}
kubectl create -f /root/replicaset-definition-2.yaml
```

The ReplicaSet "replicaset-2" should now be successfully created.

***

## Deleting Newly Created ReplicaSets

After verification, remove replicaset-1 and replicaset-2 from your cluster.

1. List the current ReplicaSets to check their status:

   ```bash theme={null}
   kubectl get rs
   ```

   Example output:

   ```text theme={null}
   NAME                DESIRED   CURRENT   READY   AGE
   new-replica-set     4         4         0       10m
   replicaset-1        2         2         2       3m4s
   replicaset-2        2         2         2       22s
   ```

2. Delete the ReplicaSets:

   ```bash theme={null}
   kubectl delete rs replicaset-1
   kubectl delete rs replicaset-2
   ```

Confirmation messages will indicate that both ReplicaSets have been removed.

***

## Updating the Original ReplicaSet's Image

Since the original ReplicaSet ("new-replica-set") uses an incorrect image ("busybox777"), update it to use the proper BusyBox image.

1. Edit the ReplicaSet:

   ```bash theme={null}
   kubectl edit rs new-replica-set
   ```

   Locate the container section and update the image field:

   ```yaml theme={null}
   containers:
     - name: busybox-container
       image: busybox
   ```

2. Save the changes and verify by describing the ReplicaSet:

   ```bash theme={null}
   kubectl describe rs new-replica-set
   ```

Despite the update, existing Pods may still reflect the previous error because updating the ReplicaSet does not restart the existing Pods. To resolve this issue, manually delete the problematic Pods so that the ReplicaSet creates new ones with the corrected image:

```bash theme={null}
kubectl delete pod new-replica-set-vpkh8 new-replica-set-tn2mp new-replica-set-7r2qw
```

After a short wait, list the Pods again:

```bash theme={null}
kubectl get pods
```

New Pods should appear and transition to the Running state.

***

## Scaling the ReplicaSet

### Scaling Up

To increase the ReplicaSet to five replicas, run:

```bash theme={null}
kubectl scale rs new-replica-set --replicas=5
```

Then verify the updated Pod count:

```bash theme={null}
kubectl get pods
```

Expected output:

```text theme={null}
NAME                       READY   STATUS    RESTARTS   AGE
new-replica-set-f5gth      1/1     Running   0          55s
new-replica-set-nsbgx      1/1     Running   0          55s
new-replica-set-8z7z5      1/1     Running   0          55s
new-replica-set-whhll      1/1     Running   0          55s
new-replica-set-mwpnz      1/1     Running   0          4s
```

### Scaling Down

To scale the ReplicaSet down, you can edit the resource directly:

1. Open the ReplicaSet for editing:

   ```bash theme={null}
   kubectl edit rs new-replica-set
   ```

2. Modify the replicas value from 5 to 2 in the YAML:

   ```yaml theme={null}
   spec:
     replicas: 2
   ```

3. Save your changes. Verify the update with:

   ```bash theme={null}
   kubectl get rs new-replica-set
   ```

The ReplicaSet will now adjust to maintain only two Pods.

***

## Final Commands Recap

Below is a summary of the commands used throughout this lab exercise:

```bash theme={null}
