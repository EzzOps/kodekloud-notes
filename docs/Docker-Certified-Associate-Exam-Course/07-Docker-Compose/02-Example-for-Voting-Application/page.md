# List running containers
docker ps

# Stop containers by ID or prefix
docker stop 69 54 5b 2f 0b

# Verify all relevant containers are stopped
docker ps
```

> **triangle-alert** Stopping containers will terminate running services. Ensure you don’t have unsaved data in those containers.

## Step 3: Define Services in docker-compose.yml

Create a file named `docker-compose.yml` with the following content. It leverages Compose file format version 3.

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
    depends_on:
      - redis

  worker:
    image: worker-app
    depends_on:
      - db
      - redis

  result:
    image: result-app
    ports:
      - "5001:80"
    depends_on:
      - db
```

### Service Overview

| Service | Image          | Ports   | Description                                   |
| ------- | -------------- | ------- | --------------------------------------------- |
| redis   | `redis`        | –       | In-memory queue for incoming votes            |
| db      | `postgres:9.4` | –       | Persistent storage for vote records           |
| vote    | `voting-app`   | 5000→80 | Frontend where users cast their vote          |
| worker  | `worker-app`   | –       | Processes queued votes into the PostgreSQL DB |
| result  | `result-app`   | 5001→80 | Displays aggregated vote results              |

> **lightbulb** The `depends_on` key ensures containers start in the correct order, but it doesn’t wait for health checks. Consider adding healthchecks for production workloads.\
  See the [Compose file reference](https://docs.docker.com/compose/compose-file/compose-versioning/) for advanced options.

## Step 4: Deploy the Stack

From the directory containing `docker-compose.yml`, run:

```bash theme={null}
docker-compose up -d
```

This command will pull images, create a default network, and start all five containers. Container names are prefixed by your folder name (e.g., `root_redis_1`).

Verify everything is up:

```bash theme={null}
docker ps
```

You should see containers for Redis, PostgreSQL, vote, worker, and result.

## Step 5: Access the Application

* Voting interface: [http://localhost:5000](http://localhost:5000)
* Results dashboard: [http://localhost:5001](http://localhost:5001)

Cast a vote on the first page, then switch to the results page to see real-time counts.

![The image shows a webpage titled "Cats vs Dogs!" with two buttons labeled "CATS" and "DOGS," where "DOGS" is selected. It also mentions that you can change your vote and displays a container ID at the bottom.](https://kodekloud.com/kk-media/image/upload/v1752873840/notes-assets/images/Docker-Certified-Associate-Exam-Course-Example-Voting-Application-with-Docker-Compose/cats-vs-dogs-vote-selected.jpg)

## Clean Up

When you’re done testing, stop and remove all services with:

```bash theme={null}
docker-compose down
```

This command stops containers and removes the network. Volumes and images remain unless you add the `--volumes` or `--rmi all` flags.

## References and Further Reading

* [Docker Compose Installation](https://docs.docker.com/compose/install/)
* [Compose File Versioning](https://docs.docker.com/compose/compose-file/compose-versioning/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/ps/)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-certified-associate-exam-course/module/a2906902-2117-467c-90e3-4cdd032599f8/lesson/40c7d096-831d-49f9-8106-fa2517936afd)


# Example for Voting Application

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Compose/Example-for-Voting-Application/page

This sample application demonstrates building and deploying a microservices-based voting system using Docker.

Welcome to this hands-on demo of the Example Voting App. This sample application demonstrates how to build and deploy a simple microservices-based voting system using Docker. The complete source code is available in the Docker samples repository on GitHub under **example-voting-app**:

![The image shows a GitHub repository page for an example Docker Compose app, listing files and directories along with commit details. The repository has 99 commits, 3 branches, and 13 contributors.](https://kodekloud.com/kk-media/image/upload/v1752873841/notes-assets/images/Docker-Certified-Associate-Exam-Course-Example-for-Voting-Application/github-repo-docker-compose-example.jpg)

In this guide, we will:

1. Review the overall architecture.
2. Dive into each component’s source code and Dockerfile.
3. Deploy all services step by step with `docker run`.

***

## Architecture Overview

The voting system consists of five microservices:

| Component | Language/Tech   | Responsibility                             |
| --------- | --------------- | ------------------------------------------ |
| vote      | Python (Flask)  | Web UI for casting votes                   |
| redis     | Redis           | Message queue for vote events              |
| worker    | Java            | Consumes votes from Redis and writes to DB |
| db        | PostgreSQL      | Stores vote records                        |
| result    | Node.js/Express | Displays aggregated voting results         |

![The image is a diagram showing the architecture of a voting application. It includes components like a Python voting app, a Node.js result app, Redis, a PostgreSQL database, and a .NET worker, with arrows indicating data flow between them.](https://kodekloud.com/kk-media/image/upload/v1752873842/notes-assets/images/Docker-Certified-Associate-Exam-Course-Example-for-Voting-Application/voting-application-architecture-diagram.jpg)

***

## 1. vote (Python Flask)

The **vote** service provides a simple web page to cast votes and pushes each vote into Redis.

Navigate to the `vote` directory to explore its code and Dockerfile:

![The image shows a GitHub repository page for "dockersamples/example-voting-app" with a list of files and directories, including "Dockerfile" and "app.py". The page is in the "vote" directory of the master branch.](https://kodekloud.com/kk-media/image/upload/v1752873843/notes-assets/images/Docker-Certified-Associate-Exam-Course-Example-for-Voting-Application/github-repo-dockersamples-voting-app.jpg)

### app.py

```python theme={null}
from flask import Flask, request, make_response, render_template, g
from redis import Redis
import os, random, json, socket

option_a = os.getenv("OPTION_A", "Cats")
option_b = os.getenv("OPTION_B", "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host="redis", db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=["GET", "POST"])
def vote_page():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None
    if request.method == 'POST':
        redis_conn = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis_conn.rpush('votes', data)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
```

> **lightbulb** The Redis host is referenced as `redis`. Ensure the Redis container is linked or networked under this name.

### Dockerfile

```dockerfile theme={null}
