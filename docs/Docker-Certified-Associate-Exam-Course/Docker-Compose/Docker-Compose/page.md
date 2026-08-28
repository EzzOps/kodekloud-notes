# Docker Compose

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Compose/Docker-Compose/page

Docker Compose simplifies the management and deployment of multi-container applications using a single YAML configuration file.

Docker Compose lets you define and run multi‐container applications from a single YAML file. Instead of managing each `docker run` command manually, you declare services, networks, and volumes in `docker-compose.yaml` and launch the entire stack with one command:

```bash theme={null}
docker-compose up
```

***

## 1. Recap: Running Multiple Containers with `docker run`

To illustrate the complexity of manual container orchestration, imagine starting four services individually:

```bash theme={null}
docker run -d --name web mmumshad/simple-webapp
docker run -d --name database mongo
docker run -d --name messaging redis:alpine
docker run -d --name orchestration ansible
```

Each container runs, but wiring them together (networking, links, ports) quickly becomes tedious.

***

## 2. Defining Services in Compose

In `docker-compose.yaml`, all services and their options live under the `services:` key:

```yaml theme={null}
version: '3'
services:
  web:
    image: mmumshad/simple-webapp

  database:
    image: mongo

  messaging:
    image: redis:alpine

  orchestration:
    image: ansible
```

Then bring the entire stack up:

```bash theme={null}
docker-compose up
```

<Callout icon="lightbulb">
  Every configuration change is version‐controlled in your Compose file—no more hunting down individual CLI commands.
</Callout>

***

## 3. Sample Voting Application Architecture

We’ll demonstrate Compose using Docker’s sample voting app, composed of:

* **Voting app** (Python web UI): records “cats” or “dogs” votes in Redis.
* **Worker** (.NET): reads votes from Redis and updates PostgreSQL.
* **PostgreSQL**: stores persistent vote counts.
* **Result app** (Node.js web UI): displays tallied results from PostgreSQL.

<Frame>
  ![The image is a diagram of a sample voting application architecture, showing components like a voting app in Python, an in-memory database using Redis, a worker in .NET, and a result app connected to a PostgreSQL database. It also includes a simple voting result table for cats and dogs.](https://kodekloud.com/kk-media/image/upload/v1752873837/notes-assets/images/Docker-Certified-Associate-Exam-Course-Docker-Compose/voting-app-architecture-diagram.jpg)
</Frame>

***

## 4. Manual Stack Deployment with `docker run`

If images already exist on Docker Hub, you might start containers like this:

```bash theme={null}
