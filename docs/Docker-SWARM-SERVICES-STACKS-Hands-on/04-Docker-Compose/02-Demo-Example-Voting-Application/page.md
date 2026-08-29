# Output:
# docker-compose version 1.16.1, build 1719ceb
```

Before we proceed, ensure that any previously running containers are stopped. Confirm no containers are active using:

```bash theme={null}
docker ps
```

## Creating the Docker Compose File

Next, create a `docker-compose.yml` file that defines the required services for the voting application architecture. The stack includes:

* **Redis** – Key-value store used by various services.
* **DB** – PostgreSQL database (image version `9.4`).
* **Vote** – The voting web application.
* **Worker** – Processes voting logic and communicates with both Redis and DB.
* **Result** – Displays the voting results.

Start by using the `cat` command to create the file:

```bash theme={null}
root@Docker_Host_2:/root# cat > docker-compose.yml
```

Then, add the following service definitions with the necessary images, port mappings, and service linkages:

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
    links:
      - redis

  worker:
    image: worker-app
    links:
      - redis
      - db

  result:
    image: result-app
    ports:
      - "5001:80"
    links:
      - db
```

In this configuration:

* The **vote** service maps container port 80 to host port 5000.
* The **result** service maps container port 80 to host port 5001.
* The `links` attribute creates communication channels among the containers (e.g., vote connects to Redis, and worker connects to both Redis and DB).

Save the file once the configuration is complete.

## Starting the Application

Launch the application stack by running:

```bash theme={null}
root@Docker_Host_2:/root# docker-compose up
```

The output should confirm that the containers are being created, similar to:

```bash theme={null}
Creating root_redis_1 ... done
Creating root_db_1 ... done
Creating root_vote_1 ...
Creating root_result_1 ...
Creating root_worker_1 ...
```

Note that the container names are prefixed with the current directory name (in this case, "root")—a standard behavior of Docker Compose.

As the containers initialize, you will see logs indicating the startup process. Here is an example snippet of the logs:

```text theme={null}
waiting for server to start...
LOG:  could not bind IPv6 socket: Cannot assign requested address
HINT:  Is another postmaster already running on port 5432? If not, wait a few seconds and retry.
LOG:  database system was shut down at 2017-08-20 21:56:07 UTC
LOG:  MultiXact member wraparound protections are now enabled
LOG:  autovacuum launcher started
Waiting for db
done
server started
ALTER ROLE

/usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*

LOG:  received fast shutdown request
LOG:  aborting any active transactions
LOG:  autovacuum launcher shutting down
LOG:  shutting down
waiting for server to shut down...
LOG:  database system is shut down
Waiting for db
done
server stopped
PostgreSQL init process complete; ready for start up.

LOG:  database system was shut down at 2017-08-20 21:56:09 UTC
LOG:  MultiXact member wraparound protections are now enabled
LOG:  database system is ready to accept connections
Connected to db
ERROR:  relation "votes" does not exist at character 38
STATEMENT:  SELECT vote, count(id) FROM votes GROUP BY vote
Error performing query: error: relation "votes" does not exist
Connected to db
Found redis at 172.17.0.2
Connecting to redis
```

Once all containers are running, you can access the voting application to cast votes and view the results.

![A webpage titled "Cats vs Dogs!" with voting options for "CATS" and "DOGS," showing "DOGS" selected. It includes a container ID and a tip about changing votes.](https://kodekloud.com/kk-media/image/upload/v1752874065/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Example-Voting-App-using-Docker-Compose/frame_320.jpg)

Thank you for following along in this guide. We hope this tutorial has enhanced your understanding of deploying multi-container applications with Docker Compose. Happy deploying!

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-swarm-services-stacks-hands-on/module/43e8db99-9bc6-4277-88b0-a6f699d2fd76/lesson/397ded1a-f9bc-4dea-acbb-ba192d128044)


# Demo Example Voting Application

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Docker-Compose/Demo-Example-Voting-Application/page

This guide covers deploying a multi-container voting application using Docker, including its architecture, components, and deployment steps.

Welcome to this guide on deploying the example voting application from the Docker samples repository. This demo showcases a multi-container application architecture using Docker, featuring several components. In this article, we review the application's design, examine source code segments, and deploy the application using Docker commands. Later, we will expand this demo to incorporate Docker Compose, Docker Stacks, and Swarm services.

***

## Overview

The voting application is composed of the following components:

* A Python-based voting application (using Flask) that presents a web page for casting votes.
* A Redis messaging service that temporarily stores votes.
* A Java-based worker application that processes votes from Redis and updates a PostgreSQL database.
* A Node.js-powered results application that queries PostgreSQL and displays real-time voting results.

Redis and PostgreSQL utilize official Docker Hub images, while the voting app, worker, and results components are custom-developed.

Below is the architecture diagram that illustrates the interaction between these components:

![The image is a diagram of a voting app architecture using Python, Node.js, Redis, PostgreSQL, and .NET, showing the interaction between components.](https://kodekloud.com/kk-media/image/upload/v1752874066/notes-assets/images/Docker-SWARM-SERVICES-STACKS-Hands-on-Demo-Example-Voting-Application/frame_100.jpg)

***

## The Voting Application

The repository organizes the custom applications into distinct folders. Let’s begin by exploring the voting application. Within the **vote** directory, the Flask application is defined in the file `app.py`. The application handles both GET and POST requests. In a GET request, it renders the main page (`index.html`), while the POST handler processes the vote by pushing vote data to Redis.

Below is an example of the Python code for the voting application:

```python theme={null}
@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)

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
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
```

In the **vote** directory, you will also find the `Dockerfile`, which builds the voting application image. This Dockerfile uses the Python 2.7 Alpine image, installs dependencies from `requirements.txt`, copies the source code, exposes port 80, and runs the application using Gunicorn.

```dockerfile theme={null}
