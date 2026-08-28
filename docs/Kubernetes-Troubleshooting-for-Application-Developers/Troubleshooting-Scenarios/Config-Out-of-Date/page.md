# Config Out of Date

Source: https://notes.kodekloud.com/docs/Kubernetes-Troubleshooting-for-Application-Developers/Troubleshooting-Scenarios/Config-Out-of-Date/page

This lesson explores configuration changes in Kubernetes and how to troubleshoot issues with environment variable updates in running pods.

In this lesson, we explore a common scenario encountered in Kubernetes where configuration changes (such as updates to ConfigMaps or Secrets) are not immediately reflected in running pods. This guide walks you through inspecting deployments, testing environment configurations, and troubleshooting issues related to environment variable updates.

## Viewing Deployments in the Production Namespace

Begin by listing all deployments in the "production" namespace:

```bash theme={null}
k get deployments.apps -n production
NAME          READY  UP-TO-DATE  AVAILABLE  AGE
mysql         1/1    1           1          3m3s
two-tier-app  0/1    1           0          3m3s
web-app       1/1    1           1          3m3s
```

## Inspecting the Web Application Deployment

Start with the web application deployment by examining its YAML definition:

```yaml theme={null}
selector:
  matchLabels:
    app: node-env-app
strategy:
  rollingUpdate:
    maxSurge: 25%
    maxUnavailable: 25%
  type: RollingUpdate
template:
  metadata:
    creationTimestamp: null
    labels:
      app: node-env-app
  spec:
    containers:
      - envFrom:
          - configMapRef:
              name: web-message
        image: rakshithraka/node-env-app
        imagePullPolicy: Always
        name: web-app
        ports:
          - containerPort: 3000
            protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
    dnsPolicy: ClusterFirst
    restartPolicy: Always
    schedulerName: default-scheduler
    securityContext: {}
    terminationGracePeriodSeconds: 30
status:
  availableReplicas: 1
  conditions:
    lastTransitionTime: "2024-06-08T21:25:36Z"
```

Focus on the environment configuration where the web application receives its environment variables from a ConfigMap named **web-message**. To inspect this ConfigMap, retrieve its details by running:

```bash theme={null}
k get cm -n production web-message -o yaml
```

The YAML output reveals a single key-value pair:

```yaml theme={null}
apiVersion: v1
data:
  MESSAGE: Hello, World
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"MESSAGE":"Hello, World"},"kind":"ConfigMap","metadata":{"annotations":{},"name":"web-message","namespace":"production"}}
  creationTimestamp: "2024-06-08T21:24:54Z"
  name: web-message
  namespace: production
  resourceVersion: "7974"
  uid: 5aee4439-24b7-462c-b35c-ad7725c109c2
```

## Testing the Web Application

To test the web application, set up port forwarding for the web service in a separate terminal:

```bash theme={null}
k port-forward -n production svc/web-svc 3000:3000
```

With port forwarding active, verify the app's response by sending a request:

```bash theme={null}
curl localhost:3000
```

The HTML response displays "Hello, World" – the message sourced from the **web-message** ConfigMap.

## Updating the ConfigMap

Suppose you want to update the message from "Hello, World" to "Hello, KodeKloud." Edit the ConfigMap with:

```bash theme={null}
k edit cm -n production web-message
```

After saving the changes, you might expect that curling the web service returns the updated message. However, if you run:

```bash theme={null}
curl localhost:3000
```

the response still shows "Hello, World." To further verify, execute the following command to inspect the pod’s environment variables:

```bash theme={null}
k exec -n production -it web-app-5c4d9cb496-sjxr5 -- /bin/sh
