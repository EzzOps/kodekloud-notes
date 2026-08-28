# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: solar-system
  labels:
    app: solar-system
spec:
  replicas: 2
  selector:
    matchLabels:
      app: solar-system
  template:
    metadata:
      labels:
        app: solar-system
    spec:
      containers:
        - name: solar-system
          image: your-repo/solar-system:latest
          ports:
            - containerPort: 3000
---
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: solar-system
  labels:
    app: solar-system
spec:
  type: NodePort
  selector:
    app: solar-system
  ports:
    - port: 3000
      targetPort: 3000
      protocol: TCP
```

| Resource Type | Purpose                          | Example                      |
| ------------- | -------------------------------- | ---------------------------- |
| Deployment    | Manages pods and rolling updates | Defined in `deployment.yaml` |
| Service       | Exposes pods on the network      | Defined in `service.yaml`    |

## Install Dependencies

```bash theme={null}
npm install
```

You may see notices:

```plaintext theme={null}
44 packages are looking for funding
Run `npm fund` for details

1 high severity vulnerability
To address all issues, run:
  npm audit fix
```

## Running the Server Locally

After dependencies are installed:

```bash theme={null}
npm start
```

Open [http://localhost:3000](http://localhost:3000) in your browser:

<Frame>
  ![The image shows a digital illustration of the solar system with planets orbiting the sun, accompanied by a user interface for searching planets. The background is a starry space theme with text describing the solar system.](https://kodekloud.com/kk-media/image/upload/v1752877291/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Run-and-Test-NodeJS-App-on-Local-Machine/solar-system-planets-ui-illustration.jpg)
</Frame>

You can search by ID (e.g., 3 for Earth, 6 for Saturn). Data is fetched from your MongoDB.

<Frame>
  ![The image shows a webpage about the solar system, specifically focusing on Saturn, with a stylized illustration of the planet and its rings on a starry background. There is a description of Saturn and a search feature for exploring planets.](https://kodekloud.com/kk-media/image/upload/v1752877292/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Run-and-Test-NodeJS-App-on-Local-Machine/saturn-solar-system-webpage-illustration.jpg)
</Frame>

## Testing the Application

Run the test suite:

```bash theme={null}
npm test
```

If environment variables are missing, you will see:

```plaintext theme={null}
MongooseError: The `uri` parameter to `openUri()` must be a string, got `undefined`.
```

<Callout icon="triangle-alert">
  Tests will fail without `MONGO_URI`, `MONGO_USERNAME`, and `MONGO_PASSWORD`. Set these before running `npm test`.
</Callout>

### Temporary Local Credentials

For a quick local demo, hard-code your MongoDB URI in `app.js`:

```javascript theme={null}
mongoose.connect('mongodb+srv://supercluster.d83jj.mongodb.net/superData', {
  user: 'superuser',
  pass: 'SuperPassword',
  useNewUrlParser: true,
  useUnifiedTopology: true
}, (err) => {
  if (err) console.error("Connection error:", err);
});
```

Re-run tests:

```bash theme={null}
npm test
echo $?   # 0 means success
```

A `test_results.xml` file is generated for CI/CD:

```xml theme={null}
<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Mocha Tests" time="3.953" tests="11" failures="0">
  <testsuite name="Planets API Suite" tests="8" time="3.953">
    <testcase name="Fetching Planet Details - Mercury" time="2.350" />
    <testcase name="Fetching Planet Details - Venus" time="0.224" />
    <!-- more testcases -->
  </testsuite>
</testsuites>
```

## Coverage Report

Generate coverage:

```bash theme={null}
npm run coverage
```

```plaintext theme={null}
11 passing (4s)
ERROR: Coverage for lines (88.88%) does not meet global threshold (90%)
```

A non-zero exit code will signal coverage failures in CI pipelines.

## Links and References

* [Node.js](https://nodejs.org/)
* [npm](https://www.npmjs.com/)
* [Express Documentation](https://expressjs.com/)
* [Mongoose Documentation](https://mongoosejs.com/)
* [Mocha](https://mochajs.org/)
* [nyc (Istanbul)](https://github.com/istanbuljs/nyc)
* [Docker Hub](https://hub.docker.com/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/f6de778b-f061-4043-92ad-dc97d2eee6c7" />
</CardGroup>


# Understanding XYZ Team DevOps Pipeline

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Understanding-XYZ-Team-DevOps-Pipeline/page

This guide explains the GitLab CI/CD workflow for building, testing, and deploying the XYZ team’s Node.js application.

In this guide, we’ll walk through the **GitLab CI/CD** workflow for building, testing, and deploying the XYZ team’s [Node.js] application. Every commit in the GitLab repository triggers a sequence of automated stages—running tests, measuring code coverage, building Docker images, and deploying to Kubernetes clusters—culminating in manual approval and production rollout.

***

## Pipeline Overview

| Stage                                  | Description                                                         | Failure Behavior               |
| -------------------------------------- | ------------------------------------------------------------------- | ------------------------------ |
| 1. Unit Testing                        | Install dependencies and run unit tests                             | Stops on failure               |
| 2. Code Coverage                       | Parallel jobs: test-report & coverage-analysis                      | Coverage errors ignored        |
| 3. Containerization                    | Build, smoke-test, and push Docker image                            | Stops on failure               |
| 4. Deploy to Development               | Apply Kubernetes manifests to the dev cluster and fetch ingress URL | Stops on failure               |
| 5. Integration Testing                 | Verify service health via the dev endpoint                          | Stops on failure               |
| 6. Manual Approval                     | Human gate before production deployment                             | Pauses pipeline until approved |
| 7. Deploy to Production                | Apply manifests to the prod cluster and fetch ingress URL           | Stops on failure               |
| 8. Post-Deployment Integration Testing | Validate production health via the live endpoint                    | Stops on failure               |

***

## 1. Unit Testing

Install dependencies with npm and execute all unit tests. Any failure aborts the pipeline immediately.

```bash theme={null}
