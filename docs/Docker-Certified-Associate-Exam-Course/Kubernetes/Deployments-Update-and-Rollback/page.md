# app.py
from flask import Flask, g
from redis import Redis

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis
```

And in C# the services connect using the Service DNS names:

```csharp theme={null}
// Program.cs
var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
var redisConn = OpenRedisConnection("redis");
var redis = redisConn.GetDatabase();
```

#### Database Credentials

* **Username:** postgres
* **Password:** postgres

## Service Types

* **ClusterIP**: Internal-only (redis, db)
* **NodePort**: External access (voting-app, result-app) – ports > 30000

## Summary of Resources

| Resource   | Type | Service Type | Port |
| ---------- | ---- | ------------ | ---- |
| voting-app | Pod  | NodePort     | 80   |
| result-app | Pod  | NodePort     | 80   |
| redis      | Pod  | ClusterIP    | 6379 |
| postgres   | Pod  | ClusterIP    | 5432 |
| worker     | Pod  | (none)       | —    |

<Callout icon="lightbulb">
  The **worker** Pod has no Service because it does not receive traffic from other components.
</Callout>

## Docker Images

We’ll use the following container images:

* `kodekloud/example-voting-app_vote:v1`
* `kodekloud/example-voting-app_worker:v1`
* `kodekloud/example-voting-app_result:v1`
* `redis:latest`
* `postgres:latest`

<Frame>
  ![The image is a diagram of a Kubernetes deployment for an example voting app, showing different pods (voting-app, result-app, redis, postgres, worker) and their interactions through services. It includes steps for deploying pods and creating services with ClusterIP and NodePort.](https://kodekloud.com/kk-media/image/upload/v1752873990/notes-assets/images/Docker-Certified-Associate-Exam-Course-Deploy-voting-app-on-Kubernetes/kubernetes-voting-app-deployment-diagram.jpg)
</Frame>

In the next section, we’ll create the Pods and Services and test the end-to-end workflow of the voting application.

## Links and References

* [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/)
* [Kubernetes Pods](https://kubernetes.io/docs/concepts/workloads/pods/)
* [Flask Redis Client](https://pypi.org/project/redis/)
* [Npgsql .NET Driver](https://www.npgsql.org/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/d9358627-4fc7-4acc-ab96-fa25232555c6/lesson/b8b05fda-aefb-40c1-b079-ef5f174ab682" />
</CardGroup>


# Deployments Update and Rollback

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Kubernetes/Deployments-Update-and-Rollback/page

This guide covers Kubernetes Deployments, including updates, rollbacks, strategies, and commands for managing application versions.

In Kubernetes, Deployments automate application updates, versioning, and rollbacks. This guide covers:

* How rollouts create revisions
* Deployment update strategies
* Applying and inspecting updates
* Undoing changes

## Rollouts and Versioning

Whenever you create or modify a Deployment, Kubernetes starts a new rollout, creating a revision:

<Frame>
  ![The image shows a diagram titled "Rollout and Versioning" with two revisions of Nginx versions, 1.7.0 and 1.7.1, represented by icons.](https://kodekloud.com/kk-media/image/upload/v1752873991/notes-assets/images/Docker-Certified-Associate-Exam-Course-Deployments-Update-and-Rollback/rollout-versioning-nginx-revisions.jpg)
</Frame>

To monitor your rollout and review history:

```bash theme={null}
kubectl rollout status deployment/myapp-deployment
