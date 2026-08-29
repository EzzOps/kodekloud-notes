# Clone the demos repo
git clone http://localhost:5000/kk-org/cgoa-demos
cd cgoa-demos/patterns/release

# Create namespace and apply deployment + service
kubectl create ns rolling-recreate
kubectl -n rolling-recreate apply -f .
```

Verify the resources were created:

```bash theme={null}
kubectl -n rolling-recreate get all
```

Example output:

```bash theme={null}
NAME                          READY   STATUS    RESTARTS   AGE
pod/app-8455fbd799-6xwx4      1/1     Running   0          9s
pod/app-8455fbd799-7qzmr      1/1     Running   0          9s
pod/app-8455fbd799-8vmj8      1/1     Running   0          9s
pod/app-8455fbd799-mjphc      1/1     Running   0          9s
pod/app-8455fbd799-nrc9f      1/1     Running   0          9s

NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/app-service  NodePort   10.106.209.30    <none>        80:32431/TCP   9s

NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app  5/5     5            5           9s
```

The app exposes a simple endpoint (/app) that returns the version string:

<Frame>
  <img alt="A web browser window displaying a centered banner that reads &#x22;Application Version: v1&#x22; in large blue text inside a rounded, blue-outlined box on a light blue gradient background. The address bar shows a localhost URL." />
</Frame>

## 2) Poll the endpoint continuously to observe updates

Use the following shell loop to poll the NodePort and colorize v1 / v2 responses. Replace the NodePort (32431) if yours differs.

```bash theme={null}
while true; do
  echo -n "$(date '+%H:%M:%S') - "
  curl -s --max-time 1 http://localhost:32431/app 2>/dev/null | \
  awk '{
    if (/^Application Version:/) {
      if ($0 ~ /v1/) print "\033[34m" $0 "\033[0m";
      else if ($0 ~ /v2/) print "\033[33m" $0 "\033[0m";
      else print $0;
    } else {
      print "\033[31mERROR: Service unreachable\033[0m"
    }
  }'
  sleep 1
done
```

Leave the loop running in a terminal. This will make the effect of each update immediately visible.

## 3) Rolling update (no downtime)

Because RollingUpdate is the default strategy, updating the Deployment image will perform a rolling upgrade: new pods are created and traffic shifts gradually from old pods to new pods.

Update the image to v2 using kubectl set image:

```bash theme={null}
kubectl -n rolling-recreate set image deployment/app app=siddharth67/app:v2
```

kubectl will respond:

```bash theme={null}
deployment.apps/app image updated
```

Sample polling output (shows continuous responses transitioning from v1 to v2 without downtime):

```bash theme={null}
16:34:14 - Application Version: v1
16:34:15 - Application Version: v1
...
16:34:32 - Application Version: v2
16:34:33 - Application Version: v2
...
```

Explanation: RollingUpdate creates new pods running v2 while terminating old v1 pods in a controlled manner, maintaining service availability during the rollout.

## 4) Recreate strategy (introduce downtime)

To demonstrate downtime, change the Deployment strategy to Recreate. Edit the deployment:

```bash theme={null}
kubectl -n rolling-recreate edit deployment app
```

Add or modify the `strategy` section in the `spec`:

```yaml theme={null}
strategy:
  type: Recreate
```

Save the edit. Confirm the deployment now uses Recreate:

```bash theme={null}
kubectl -n rolling-recreate get deploy app -o yaml
```

You should see:

```yaml theme={null}
spec:
  replicas: 5
  strategy:
    type: Recreate
```

Now update the image again (flip it back to v1 to see downtime):

```bash theme={null}
kubectl -n rolling-recreate set image deployment/app app=siddharth67/app:v1
```

kubectl will report:

```bash theme={null}
deployment.apps/app image updated
```

Behavior: With Recreate, Kubernetes terminates all existing pods immediately and only then creates the new pods. During the gap between pod termination and the new pods becoming Ready, the Service has no ready endpoints and will return timeouts or errors.

Example polling output showing downtime:

```bash theme={null}
16:35:30 - Application Version: v2
16:35:31 - Application Version: v2
16:35:32 - ERROR: Service unreachable
16:35:33 - ERROR: Service unreachable
16:35:34 - Application Version: v1
16:35:35 - Application Version: v1
```

<Callout icon="warning">
  Using the Recreate strategy will cause downtime because all old pods are terminated before new pods are created. Use Recreate only when you must avoid running multiple versions concurrently and can tolerate interruptions.
</Callout>

## Comparison: RollingUpdate vs Recreate

| Strategy      | Behavior during update                                    | Use case                                  |
| ------------- | --------------------------------------------------------- | ----------------------------------------- |
| RollingUpdate | Gradually replaces pods; maintains availability           | Zero-downtime updates; safe in production |
| Recreate      | Terminates all old pods, then creates new ones (downtime) | When concurrent versions must not coexist |

## References

* [Kubernetes Deployments](https://kubernetes.[SECRET_REDACTED]/)
* [RollingUpdate vs Recreate](https://kubernetes.[SECRET_REDACTED]/#strategy)
* [kubectl set image](https://kubernetes.io/[AWS_SECRET_ACCESS_KEY]-commands#set)

Summary

* RollingUpdate (default): incrementally updates pods and preserves availability.
* Recreate: shuts down all existing pods first, then starts new ones — which causes downtime.

This concludes the demo showing the practical differences between RollingUpdate and Recreate strategies for Kubernetes Deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/7d82a500-7aec-46b8-9e96-dfae70468001" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/eccc6e22-3cbe-442b-be33-2c6839a2d8f6" />
</CardGroup>


# Deployment and Release pattern

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Argo-Project-Associate-CAPA/Argo-Rollouts/Deployment-and-Release-pattern/page

Kubernetes deployment and release patterns including RollingUpdate Recreate Blue Green and Canary to minimize downtime control traffic and enable safe incremental rollouts using GitOps and observability

In this lesson we cover common deployment and release patterns in Kubernetes: Rolling Updates, Recreate, Blue-Green, and Canary releases. These patterns help you deploy new application versions safely, minimize downtime, and control traffic during rollouts. We start with the two core strategies supported by Kubernetes Deployments: RollingUpdate and Recreate.

## Why deployment strategy matters

For a popular web application with thousands of users, deploying a new version must avoid downtime and prevent cluster overload. Kubernetes deployment strategies determine how pods are replaced, how traffic is shifted, and how much control you have over rollout speed and failure recovery.

* RollingUpdate: Gradual replacement of pods; new pods are created and validated before old ones are removed.
* Recreate: Terminates all old pods first, then starts new pods—simpler but causes downtime.
* Blue-Green and Canary: Provide explicit traffic control for staged exposure of new versions.

***

## Rolling Update (recommended for most stateless apps)

Rolling updates allow Kubernetes to replace pods incrementally. This ensures continuous availability while gradually shifting to the new version. You can control the pace using `maxSurge`, `maxUnavailable`, and readiness probes/minReadySeconds.

Key benefits:

* Minimal disruption—application remains available during rollout.
* Controlled, incremental changes to limit risk.
* Ability to pause or rollback if problems are detected.

Typical GitOps workflow:

1. Developer updates the Deployment manifest in Git (e.g., image tag v1.0 → v2.0).
2. GitOps operator (Argo CD, Flux, etc.) detects the change and applies it to the cluster.
3. Kubernetes applies the rolling update according to the Deployment strategy settings.

Example Deployment configured for a rolling update:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # at most 1 extra pod above desired replicas
      maxUnavailable: 0  # do not allow any unavailable pods during update
  minReadySeconds: 10   # pod must be ready for this many seconds before considered available
  selector:
    matchLabels:
      app: example-app
  template:
    metadata:
      labels:
        app: example-app
    spec:
      containers:
        - name: web
          image: myrepo/example-app:2.0
          ports:
            - containerPort: 80
```

<Callout icon="lightbulb">
  RollingUpdate is the default Deployment strategy. Use `maxSurge` and `maxUnavailable` to control how many pods are added/removed at each step. Combine readiness probes and `minReadySeconds` to ensure pods serve traffic only after they are healthy.
</Callout>

You can pause a rollout with `kubectl rollout pause deployment/<name>` to investigate failures, and resume or roll back with `kubectl rollout resume` or `kubectl rollout undo` respectively.

***

## Recreate (when multiple versions cannot coexist)

The Recreate strategy terminates all existing pods for a Deployment before creating any new pods. This is appropriate when your application cannot safely run multiple versions simultaneously or requires exclusive access to shared resources during startup.

When to choose Recreate:

* The application cannot safely run multiple versions concurrently.
* Short, acceptable downtime is preferable to complex coordination.
* Legacy or stateful services that require exclusive initialization.

How it works with GitOps:

1. The manifest is updated and pushed to Git.
2. The GitOps operator applies the change.
3. Kubernetes deletes all existing pods for that Deployment, then creates the new pods.

Example Deployment using Recreate:

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-app-recreate
spec:
  replicas: 3
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: example-app-recreate
  template:
    metadata:
      labels:
        app: example-app-recreate
    spec:
      containers:
        - name: web
          image: myrepo/example-app:2.0
          ports:
            - containerPort: 80
```

<Callout icon="warning">
  Recreate causes downtime while old pods are terminated and new pods are created. Use it only when coexisting versions are unsafe or when brief downtime is acceptable.
</Callout>

***

## Blue-Green Deployments and Canary Releases (advanced traffic control)

In addition to RollingUpdate and Recreate, blue-green and canary patterns offer more granular control over traffic and exposure:

* Blue-Green: Maintain two separate environments (blue = current, green = new). Switch traffic to green once verified. This enables near-instant rollback by switching back to blue.
* Canary: Gradually shift a small percentage of user traffic to the new version, monitor behavior, then increase traffic in steps until fully rolled out.

Both patterns are often implemented with service routing, Ingress rules, or service meshes (e.g., Istio, Linkerd), and integrate well with GitOps pipelines for automated promotion.

***

## Quick comparison

| Strategy      | Downtime                | Rollout control                       | Use case                                            |
| ------------- | ----------------------- | ------------------------------------- | --------------------------------------------------- |
| RollingUpdate | Minimal/none            | Incremental (maxSurge/maxUnavailable) | Stateless services, production web apps             |
| Recreate      | Yes (brief)             | Simple (all at once)                  | Legacy/stateful apps that can't run concurrently    |
| Blue-Green    | Minimal (switch moment) | Full environment swap                 | Safe testing in a production-like environment       |
| Canary        | Minimal                 | Fine-grained traffic shift            | Gradual exposure, A/B testing, risk-limited deploys |

***

## Recommended practices

* Use RollingUpdate for most stateless workloads.
* Configure readiness/liveness probes and `minReadySeconds` to avoid routing traffic to unhealthy pods.
* Use GitOps (Argo CD, Flux) to keep manifests declarative and reproducible.
* Employ blue-green or canary patterns for high-risk or business-critical changes; use service meshes for advanced traffic control.
* Automate monitoring and observability (metrics, tracing, logs) to detect regressions early during rollouts.

## Links and references

* [Kubernetes Deployments](https://kubernetes.[SECRET_REDACTED]/)
* [Kubernetes Rolling Update docs](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)
* [Argo CD (GitOps)](https://argo-cd.readthedocs.io/)
* [Flux (GitOps)](https://fluxcd.io/)
* [Blue/Green and Canary patterns overview (article)](https://martinfowler.com/articles/continuousDelivery.html)

This lesson introduced rollout patterns and their trade-offs. Choose the strategy that balances availability, risk, and operational complexity for your application, and integrate it with GitOps pipelines and observability for safe, repeatable deployments.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-argo-project-associate-capa/module/959dfde0-9415-4fc2-bcad-fe9e4bf84cc7/lesson/49e161a0-4014-454e-a5cd-eec72171e086" />
</CardGroup>
