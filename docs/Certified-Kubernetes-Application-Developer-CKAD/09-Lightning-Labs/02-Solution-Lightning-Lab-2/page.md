# Solution Lightning Lab 2

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Lightning-Labs/Solution-Lightning-Lab-2/page

This article provides solutions for troubleshooting pods, creating CronJobs, deploying pods, setting up Ingress resources, and inspecting logs in Kubernetes.

In this lesson, we walk through the solutions for Lightning Lab Two. This lab consists of several tasks designed to help you troubleshoot pods, update their configurations, create a CronJob, deploy a pod with custom parameters, set up an Ingress resource for virtual hosting routing, and inspect logs for warning messages.

***

## Task 1: Identify and Troubleshoot the Problematic Pod

First, identify which pod is not in a "Ready" state. Several pods are deployed across various namespaces. Run the following command to list all pods:

```bash theme={null}
kubectl get pod --all-namespaces
```

You will see output similar to this:

```bash theme={null}
NAMESPACE      NAME                          READY   STATUS    RESTARTS   AGE
default        dev-pod-dind-878516          3/3     Running   0          4m21s
default        pod-xyz123                    1/1     Running   0          4m20s
default        webapp-color                  1/1     Running   0          4m21s
dev0403        nginx0403                     1/1     Running   0          4m22s
dev0403        pod-dar85                     1/1     Running   0          4m21s
dev1401        nginx1401                     1/1     Running   0          4m21s
dev2406        pod-kab87                     1/1     Running   0          4m21s
dev2406        nginx2406                     1/1     Running   0          4m20s
dev2406        pod-var2016                   1/1     Running   0          4m21s
e-commerce     e-com-1123                   1/1     Running   0          31m
kube-system    coredns-74ff55c5b-c2mdt      1/1     Running   0          31m
kube-system    coredns-74ff55c5b-w774j4     1/1     Running   0          31m
kube-system    etcd-controlplane             1/1     Running   0          31m
kube-system    kube-apiserver-controlplane   1/1     Running   0          31m
kube-system    kube-controller-manager-controlplane   1/1     Running   0          31m
kube-system    kube-proxy-k6kg8              1/1     Running   0          31m
kube-system    kube-proxy-nv9b1              1/1     Running   0          30m
kube-system    kube-scheduler-controlplane    1/1     Running   0          31m
kube-system    weave-net-s64p6               2/2     Running   0          30m
kube-system    weave-net-sbt9v               2/2     Running   1          31m
marketing      redis-bf75d68-fjvw6          1/1     Running   0          4m20s
```

Inspect the problematic pod—identified here as `nginx1401` in the `dev1401` namespace—by running:

```bash theme={null}
kubectl describe pod nginx1401 -n dev1401
```

Examine the events section for clues. In this example, the events indicate that the readiness probe has failed, suggesting a misconfiguration. Next, extract the pod configuration to a YAML file for further inspection:

```bash theme={null}
kubectl get pod nginx1401 -n dev1401 -o yaml > nginx1401.yaml
```

Review the configuration, which includes probe settings. A snippet from the YAML output might look like this:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"creationTimestamp":null,"labels":{"run":"nginx"},"name":"nginx1401","namespace":"dev1401"},"spec":{"containers":[{"image":"kodekloud/nginx","imagePullPolicy":"IfNotPresent","name":"nginx","ports":[{"containerPort":8080}],"readinessProbe":{"httpGet":{"path":"/","port":8080},"initialDelaySeconds":10,"periodSeconds":60},"resources":{}},{"dnsPolicy":"ClusterFirst","restartPolicy":"OnFailure"}],"status":{}}}
  creationTimestamp: '2022-08-08T03:39:07Z'
  labels:
    run: nginx
managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations: {}
        f:kubectl.kubernetes.io/last-applied-configuration: {}
        f:labels: {}
        f:run: {}
      f:spec:
        f:containers:
          k:{"name":"nginx"}:
            f:image: {}
            f:imagePullPolicy: {}
            f:name: {}
            f:ports:
              k:{"containerPort":8080,"protocol":"TCP"}: {}
```

Notice that although the readiness probe is set to check port 8080, other parts of the configuration might be expecting port 9080. To correct the inconsistency, update the configuration as follows:

```yaml theme={null}
