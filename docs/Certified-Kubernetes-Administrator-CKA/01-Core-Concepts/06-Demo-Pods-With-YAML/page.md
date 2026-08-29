# Demo Pods with YAML

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Core-Concepts/Demo-Pods-With-YAML/page

This article demonstrates how to create a Kubernetes Pod using a YAML definition file for better control over pod specifications.

In this lesson, we will create a Kubernetes Pod using a YAML definition file instead of the "kubectl run" command. This method offers more control by allowing you to define pod specifications explicitly in a file. You can choose any text editor for this task; for instance, Windows users may prefer Notepad++ over Notepad, while Linux users might opt for vim. In future sections, we will explore additional IDEs and tools to streamline YAML editing, but we will stick with the basics for now.

## Step 1: Creating the YAML File

Open your terminal and use vim to create a file named pod.yaml:

```bash theme={null}
vim pod.yaml
```

Inside the file, define the following key elements:

* **apiVersion:** Should be set to `v1` for a Pod.
* **kind:** Must be `Pod` (case-sensitive).
* **metadata:** A dictionary that includes the pod's name and any labels used for grouping.
* **spec:** Contains the pod specifications, including a list of containers.

<Callout icon="lightbulb">
  Be sure to follow proper indentation rules. Use two spaces per level (avoid
  tabs), as misalignment can lead to errors.
</Callout>

Below is a complete example configuration for a single-container Pod using the `nginx` image:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    app: nginx
    tier: frontend
spec:
  containers:
    - name: nginx
      image: nginx
```

<Callout icon="lightbulb">
  To add additional containers, insert another block within the containers list
  with the appropriate name and image.
</Callout>

## Step 2: Saving and Verifying the YAML File

After editing the file, exit vim and save your changes by typing:

```bash theme={null}
:wq
```

Verify the contents of your YAML file with:

```bash theme={null}
cat pod.yaml
```

The output should match the YAML configuration shown above.

## Step 3: Creating the Pod in the Cluster

Create the Pod on your Kubernetes cluster using your YAML file. You can use either the `kubectl create` or `kubectl apply` command. Here’s an example with `kubectl apply`:

```bash theme={null}
kubectl apply -f pod.yaml
