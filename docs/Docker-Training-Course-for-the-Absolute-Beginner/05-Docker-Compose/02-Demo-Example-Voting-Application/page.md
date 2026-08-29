# Output:
# -bash: docker-compose: command not found
```

You may need to install Docker Compose using `apt-get`:

```bash theme={null}
apt-get install docker-compose
```

If the package is not found via apt-get, use curl as demonstrated earlier.

***

## Deploying the Application Stack

With your Docker Compose file configured, start the application stack by executing:

```bash theme={null}
docker-compose up
```

As Docker Compose creates the containers, you will see output similar to:

```bash theme={null}
root@Docker_Host_2:/root # docker-compose up
Creating root_redis_1 ... done
Creating root_db_1 ... done
Creating root_vote_1 ... done
Creating root_result_1 ...
Creating root_worker_1 ...
```

*Note:* The container names are prefixed with the name of your current directory (e.g., "root").

### Viewing Log Output

The log output will display the initialization process for each service. For instance, during the setup of the PostgreSQL database, you might see:

```text theme={null}
waiting for server start...LOG:  could not bind IPv6 socket: Cannot assign requested address
HINT:  Is another postmaster already running on port 5432? If not, wait a few seconds and retry.
LOG:  database system was shut down at 2017-08-20 21:56:07 UTC
LOG:  MultiXact member wraparound protections are now enabled
LOG:  autovacuum launcher started
Waiting for db
done
server started
ALTER ROLE
...
Connected to db
ERROR:  relation "votes" does not exist at character 38
STATEMENT:  SELECT vote, COUNT(id) AS count FROM votes GROUP BY vote
Error performing query: error: relation "votes" does not exist
Connected to db
Found redis at 172.17.0.2
Connecting to redis
```

These messages confirm that the containers are in the process of booting up. Once you see all containers running, you can access the voting application and results page; cast a vote and view the outcome.

> **triangle-alert** Before deploying a new stack, always ensure that no unnecessary containers are running by stopping them. You can verify this by running:

  ```bash theme={null}
  docker ps
  ```

***

## Conclusion

Thank you for following along with this Docker Compose tutorial. You now have a solid understanding of how to use Docker Compose to deploy a multi-container application stack. For more information on Docker Compose and container orchestration, be sure to explore more resources in the Docker documentation.

![The image shows a webpage titled "Cats vs Dogs!" with options to vote for either "CATS" or "DOGS," and a note about changing the vote.](https://kodekloud.com/kk-media/image/upload/v1752874130/notes-assets/images/Docker-Training-Course-for-the-Absolute-Beginner-Demo-Example-Voting-Application-with-Docker-Compose/frame_320.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/docker-training-course-for-the-absolute-beginner/module/e4f7711c-d82a-4953-ab4c-bce10b901ed9/lesson/40f7795c-fd73-45aa-adf3-ff6356fbea56)


# Demo Example Voting Application

Source: https://notes.kodekloud.com/docs/Docker-Training-Course-for-the-Absolute-Beginner/Docker-Compose/Demo-Example-Voting-Application/page

This article provides a guide on deploying a voting application using Docker, covering its architecture, source code, and multi-container deployment.

Welcome to this detailed guide on the example voting application from the Docker Samples GitHub repository (located under the "example-voting-app" directory). In this article, we will review the application's architecture, explore the source code, and deploy the application using Docker. We will also extend the deployment using Docker Compose and Docker Swarm stacks for a more robust, multi-container environment.

***

## Application Overview and Architecture

The voting application is composed of several distinct components:

* **Voting App:** A Python-based web application built with Flask, where users cast their votes.
* **Redis:** A messaging system that collects the submitted votes.
* **Worker:** A .NET application (with a Java-like code sample preserved) that processes votes and updates a PostgreSQL database.
* **Result App:** A Node.js and Express application that retrieves and displays voting results from the database.

Note that Redis and PostgreSQL are provided as prebuilt images from Docker Hub, while the Python, .NET, and Node.js applications are custom-developed and organized in separate folders within the repository.

Below is the architecture diagram featured in the lesson:

![The image shows a system architecture diagram for a voting app using Python, Node.js, Redis, PostgreSQL, and .NET components.](https://kodekloud.com/kk-media/image/upload/v1752874131/notes-assets/images/Docker-Training-Course-for-the-Absolute-Beginner-Demo-Example-Voting-Application/frame_90.jpg)

***

## The Voting Application

The voting app is a Flask-based Python application found in the `vote` directory. Its main file, `app.py`, defines GET and POST routes. The GET route renders the index page for voting, while the POST route captures the vote, connects to Redis, and stores the vote data.

Below is an enhanced excerpt of the Python code with clear descriptions:

```python theme={null}
import os
import json
import random
from flask import Flask, request, make_response, render_template, g
from redis import Redis

app = Flask(__name__)

def get_redis():
    if not hasattr(g, 'redis'):
        g.redis = Redis(host='redis', db=0, socket_timeout=5)
    return g.redis

@app.route("/", methods=['GET', 'POST'])
def index():
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
        option_a="Cats",
        option_b="Dogs",
        hostname=os.uname()[1],
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
```

When a user submits a vote, the application connects to the Redis container (accessed via the hostname "redis") and pushes the vote data into the `votes` list.

### Dockerfile for the Voting App

The Flask application is containerized using a Dockerfile based on the Python 2.7 Alpine image:

```dockerfile theme={null}
