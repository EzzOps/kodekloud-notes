# Create voting frontend
kubectl create -f voting-app-pod.yaml
kubectl create -f voting-app-service.yaml

# Create Redis and its Service
kubectl create -f redis-pod.yaml
kubectl create -f redis-service.yaml

# Create Postgres and its Service
kubectl create -f postgres-pod.yaml
kubectl create -f postgres-service.yaml

# Create worker (no service)
kubectl create -f worker-app-pod.yaml

# Create result frontend and its Service
kubectl create -f result-app-pod.yaml
kubectl create -f result-app-service.yaml
```

Check status of Pods and Services

```bash theme={null}
kubectl get pods,svc
```

Sample expected output (condensed)

```text theme={null}
NAME                       READY   STATUS    RESTARTS   AGE
pod/postgres-pod           1/1     Running   0          2m20s
pod/redis-pod              1/1     Running   0          2m52s
pod/result-app-pod         1/1     Running   0          32s
pod/voting-app-pod         1/1     Running   0          6m44s
pod/worker-app-pod         1/1     Running   0          60s

NAME                       TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/db                 ClusterIP   10.105.81.36    <none>        5432/TCP         2m12s
service/kubernetes         ClusterIP   10.96.0.1       <none>        443/TCP          2d4h
service/redis              ClusterIP   10.110.47.42    <none>        6379/TCP         2m48s
service/result-service     NodePort    10.101.220.79   <none>        80:30005/TCP     25s
service/voting-service     NodePort    10.109.194.132  <none>        80:30004/TCP     4m31s
```

## Access the frontends (Minikube)

If using Minikube, get accessible URLs:

```bash theme={null}
minikube service voting-service --url
minikube service result-service --url
```

Example:

```text theme={null}
http://192.168.99.101:30004
http://192.168.99.101:30005
```

Open the voting service URL in a browser and cast votes.

Flow summary:

* Voting frontend records votes in Redis.
* Worker reads votes from Redis and writes aggregates into Postgres.
* Result frontend reads aggregated totals from Postgres and displays them.

If vote counts do not update:

* Verify Postgres env variables (POSTGRES\_USER, POSTGRES\_PASSWORD) match what worker/result expect.
* Ensure Service selectors match Pod labels exactly.

## Conclusion

You have successfully deployed the multi-tier voting application to Kubernetes:

* Created Pods for voting, result, redis, postgres, and worker.
* Provided ClusterIP services for internal components (redis, db).
* Exposed frontends via NodePort services (voting and result).
* Verified end-to-end behavior by casting votes and viewing results.

Further reading and references:

* [Kubernetes Concepts — Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [dockersamples/example-voting-app](https://github.com/dockersamples/example-voting-app)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/8681edc1-fcb6-475f-b034-087b2f8d8577)


# Demo Deployments Updates and Rollback

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Demo-Deployments-Updates-and-Rollback/page

This tutorial teaches managing rolling updates and rollbacks for Kubernetes Deployments.

In this tutorial, you will learn how to manage rolling updates and rollbacks for Kubernetes Deployments. We’ll cover:

1. Creating a Deployment
2. Downgrading an image using `kubectl edit`
3. Updating the image with `kubectl set image`
4. Rolling back to a previous revision
5. Simulating and recovering from a failed rollout

***

## 1. Create the Deployment

First, ensure there are no existing Pods in the `default` namespace:

```bash theme={null}
kubectl get pods
