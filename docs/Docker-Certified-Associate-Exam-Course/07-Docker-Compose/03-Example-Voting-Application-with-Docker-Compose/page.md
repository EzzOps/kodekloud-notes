# Data layer
docker run -d --name redis redis
docker run -d --name db postgres

# Services
docker run -d --name vote   -p 5000:80 voting-app
docker run -d --name result -p 5001:80 result-app
docker run -d --name worker worker
```

However, without networking configuration, containers cannot communicate.

### 4.1 Linking Containers (Deprecated)

The `--link` flag creates `/etc/hosts` entries for cross-container DNS:

```bash theme={null}
docker run -d --name redis redis
docker run -d --name db postgres

docker run -d --name vote -p 5000:80 --link redis:redis voting-app
docker run -d --name result -p 5001:80 --link db:db result-app
docker run -d --name worker --link redis:redis --link db:db worker
```

In your Node.js code, you’d connect via the hostname `db`:

```javascript theme={null}
pg.connect('postgres://postgres@db/postgres', (err, client, done) => {
  if (err) console.error("Waiting for db");
  callback(err, client);
});
```

> **triangle-alert** Container links are **deprecated**. Instead, use user‐defined networks as shown in the next sections.

***

## 5. From `docker run` to `docker-compose.yaml`

Convert your verified `docker run` commands into a Compose file:

```bash theme={null}
# Working commands for reference
docker run -d --name redis redis
docker run -d --name db postgres:9.4
docker run -d --name vote   -p 5000:80 --link redis:redis voting-app
docker run -d --name result -p 5001:80 --link db:db result-app
docker run -d --name worker --link db:db --link redis:redis worker
```

**Compose definition**:

```yaml theme={null}
version: '2'
services:
  redis:
    image: redis

  db:
    image: postgres:9.4

  vote:
    image: voting-app
    ports:
      - "5000:80"
    links:
      - redis

  result:
    image: result-app
    ports:
      - "5001:80"
    links:
      - db

  worker:
    image: worker
    links:
      - redis
      - db
```

Launch with:

```bash theme={null}
docker-compose up
```

***

## 6. Building Local Images in Compose

If your service images are built locally, specify a `build:` context instead of `image:`:

```yaml theme={null}
version: '2'
services:
  vote:
    build: ./vote
    ports:
      - "5000:80"
    links:
      - redis

  result:
    build: ./result
    ports:
      - "5001:80"
    links:
      - db

  worker:
    build: ./worker
    links:
      - redis
      - db

  redis:
    image: redis

  db:
    image: postgres:9.4
```

Compose will build these images from each directory’s Dockerfile before starting the containers.

***

## 7. Compose File Versions Compared

Different Compose versions introduce new features and schemas. Refer to this summary:

| Version | Structure      | Highlights                             |
| ------- | -------------- | -------------------------------------- |
| v1      | No `services:` | Legacy; no networks or `depends_on`    |
| v2      | `services:`    | Built‐in network, `depends_on` support |
| v3      | Same as v2     | Adds Swarm deployment settings         |

### Examples

#### Version 1

```yaml theme={null}
version: '1'
redis:
  image: redis
db:
  image: postgres:9.4
vote:
  image: voting-app
  ports:
    - "5000:80"
  links:
    - redis
```

#### Version 2

```yaml theme={null}
version: '2'
services:
  redis:
    image: redis

  db:
    image: postgres:9.4

  vote:
    image: voting-app
    ports:
      - "5000:80"
    depends_on:
      - redis
```

#### Version 3

```yaml theme={null}
version: '3'
services:
  redis:
    image: redis

  db:
    image: postgres:9.4

  vote:
    image: voting-app
    ports:
      - "5000:80"
```

For full details, see the [Docker Compose file reference](https://docs.docker.com/compose/compose-file/).

***

## 8. Defining Custom Networks

By default, Compose creates a single bridge network. You can isolate traffic with multiple networks:

![The image is a diagram illustrating a Docker Compose setup with components like a voting app, result app, Redis, database, and worker, connected to represent a system architecture.](https://kodekloud.com/kk-media/image/upload/v1752873839/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Compose/docker-compose-setup-diagram.jpg)

```yaml theme={null}
version: '2'
services:
  redis:
    image: redis
    networks:
      - back-end

  db:
    image: postgres:9.4
    networks:
      - back-end

  vote:
    image: voting-app
    networks:
      - front-end
      - back-end

  result:
    image: result-app
    networks:
      - front-end
      - back-end

  worker:
    image: worker
    networks:
      - back-end

networks:
  front-end: {}
  back-end: {}
```

Containers on **front-end** can only communicate with those also on **back-end**.

***

## Next Steps

Now that you’ve mastered service definitions, version schemas, and custom networks, try creating and running your own `docker-compose.yaml` configurations in the exercises below.

***

## Links and References

* [Docker Compose Overview](https://docs.docker.com/compose/)
* [Compose File Reference](https://docs.docker.com/compose/compose-file/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/a2906902-2117-467c-90e3-4cdd032599f8/lesson/40c23529-3b71-41f0-9309-d310e3f31234)


# Example Voting Application with Docker Compose

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Compose/Example-Voting-Application-with-Docker-Compose/page

Learn to orchestrate a multi-service voting application using Docker Compose, including Redis, PostgreSQL, a voting frontend, a worker processor, and a results dashboard.

In this step-by-step tutorial, you’ll learn how to orchestrate a multi-service voting application using Docker Compose. By the end, you’ll have a running stack that includes Redis, PostgreSQL, a voting frontend, a worker processor, and a results dashboard.

## Prerequisites

* Docker Engine installed (version ≥ 19.03)
* Basic familiarity with `docker` CLI
* A terminal/SSH session on Linux, macOS, or Windows WSL

## Step 1: Install Docker Compose

Docker Compose isn’t bundled with Docker Engine by default. Install it on Linux with:

```bash theme={null}
sudo curl -L "https://github.com/docker/compose/releases/download/1.16.1/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

Expected output:

```bash theme={null}
docker-compose version 1.16.1, build 1719ceb
```

> **lightbulb** Replace `1.16.1` with the latest stable release. See the [Compose releases on GitHub](https://github.com/docker/compose/releases) for details.

## Step 2: Clean Up Existing Containers

Before deploying, stop any previous demo containers:

```bash theme={null}
