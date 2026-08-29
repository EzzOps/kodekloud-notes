# Note: the colon after --host is incorrect here
CMD ["python3", "-m", "flask", "run", "--host:0.0.0.0"]
```

## 2. Building the Docker Image

Open your terminal and execute:

```bash theme={null}
docker build -t flask-docker-demo .
```

You should see output similar to:

```bash theme={null}
[+] Building 2.0s (10/10) FINISHED
 => [internal] load build definition from Dockerfile             0.0s
 => [internal] load .dockerignore                                0.0s
 => [internal] load metadata for docker.io/library/python:3.8-slim-buster 0.0s
 => [1/5] FROM docker.io/library/python:3.8-slim-buster@sha256:…    0.0s
 => [2/5] WORKDIR /app                                            0.0s
 => [3/5] COPY requirements.txt requirements.txt                0.0s
 => [4/5] RUN pip3 install -r requirements.txt                  0.0s
 => [5/5] COPY .                                                 0.0s
 => exporting to image                                           0.0s
 => => writing image sha256:215f34…                              0.0s
 => => naming to docker.io/flask-docker-demo                    0.0s
```

Verify the image exists:

```bash theme={null}
docker images | grep flask-docker-demo
```

## 3. Running the Container

Try starting the container and mapping container port 5000 to host port 5000:

```bash theme={null}
docker run -p 5000:5000 flask-docker-demo
```

### Common Port Binding Error

```bash theme={null}
docker: Error response from daemon: Ports are not available: listen tcp 0.0.0.0:5000: bind: address already in use.
```

If you see this, remap the host port (e.g., to 5001):

```bash theme={null}
docker run -p 5001:5000 flask-docker-demo
```

### Flask Option Parsing Error

```bash theme={null}
Usage: python -m flask run [OPTIONS]
Try 'python -m flask run --help' for help.

Error: No such option: --host:0.0.0.0
```

This happens because Flask expects `--host` in the form `--host=<address>`, not `--host:<address>`.

## 4. Fixing the Dockerfile

Update the `CMD` line to use `=` instead of `:`:

```dockerfile theme={null}
FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY .

# Fixed: use '=' instead of ':'
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
```

Rebuild the image:

```bash theme={null}
docker build -t flask-docker-demo .
```

## 5. Running Successfully

Start the container on host port 5001:

```bash theme={null}
docker run -p 5001:5000 flask-docker-demo
```

You should see:

```bash theme={null}
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

Open your browser at [http://localhost:5001](http://localhost:5001) to confirm your Flask app is live.

<Callout icon="triangle-alert">
  This built-in Flask server is for development only. For production deployments, use a WSGI server like [Gunicorn](https://gunicorn.org/) or [uWSGI](https://uwsgi-docs.readthedocs.io/).
</Callout>

## 6. Command Reference

| Command                                     | Description                                   |
| ------------------------------------------- | --------------------------------------------- |
| `docker build -t flask-docker-demo .`       | Build the Docker image for the Flask app      |
| `docker images`                             | List all local Docker images                  |
| `docker run -p HOST:5000 flask-...`         | Run container, mapping host port to container |
| `docker run -p 5001:5000 flask-docker-demo` | Remap host port if default is unavailable     |

## Next Steps

1. Commit your changes and push to GitHub.
2. Integrate with a CI/CD pipeline for automated builds.
3. Deploy to a cloud platform knowing your container behaves the same as it does locally.

***

## Links and References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/docker/)
* [GitHub Actions: Continuous Integration](https://docs.github.com/en/actions)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-devops-project/module/a334971a-4fa2-4c61-8891-9c189e2aab64/lesson/3d22542d-25a9-43be-9f13-65c0fdcb4e23" />
</CardGroup>


# Sprint 01 review

Source: https://notes.kodekloud.com/docs/GCP-DevOps-Project/Sprint-01/Sprint-01-review/page

This article reviews Sprint 01 goals, achievements, insights, and outlines next steps for a GCP DevOps project.

Welcome to our Sprint 01 Review! In this lesson, we’ll recap the goals we set at the start of the sprint, highlight our achievements, share key insights, and outline next steps for our GCP DevOps project.

<Callout icon="lightbulb">
  A **Sprint Review** is conducted at the end of each sprint (weekly or bi-weekly) to demonstrate completed work, gather feedback, and update the backlog accordingly.
</Callout>

## Sprint 01 Goals and Status

| Goal                                                       | Description                                  | Status      |
| ---------------------------------------------------------- | -------------------------------------------- | ----------- |
| Initialize a GitHub repository                             | Create and configure a new repo on GitHub    | ✅ Completed |
| Clone the repository locally & apply DevOps best practices | Set up branching strategy, CI/CD templates   | ✅ Completed |
| Develop a simple Python Flask application                  | Scaffold a “Hello, World!” Flask web service | ✅ Completed |
| Test the application locally & resolve issues              | Run unit tests, lint code, debug errors      | ✅ Completed |
| Push the completed code back to GitHub                     | Commit changes and push to the `main` branch | ✅ Completed |

## Sharing Insights

During the Sprint Review, teams should also discuss:

* Blockers encountered during development
* Novel challenges or key learnings that can improve our DevOps pipeline
* Suggestions for refining workflows in upcoming sprints

<Callout icon="triangle-alert">
  If a blocker persists past the sprint boundary, raise it immediately in the backlog refinement meeting to avoid delays in future sprints.
</Callout>

## Next Steps

With Sprint 01 wrapped up, our focus shifts to:

1. **Sprint 02 Planning**: Defining scope for containerizing the Flask app with Docker.
2. **CI/CD Integration**: Configuring GCP Cloud Build triggers for automated deployments.
3. **Infrastructure as Code**: Writing Terraform scripts to provision networking and compute resources on GCP.

Stay tuned for the next lesson, where we’ll dive into Dockerizing our Python Flask application and setting up a CI/CD pipeline on Google Cloud Platform.

## References

* [GitHub Documentation](https://docs.github.com/)
* [Flask Web Framework](https://flask.palletsprojects.com/)
* [Google Cloud DevOps Solutions](https://cloud.google.com/solutions/devops)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gcp-devops-project/module/a334971a-4fa2-4c61-8891-9c189e2aab64/lesson/1ee30e56-5f1b-4641-b80e-8eb9fdd92d96" />
</CardGroup>
