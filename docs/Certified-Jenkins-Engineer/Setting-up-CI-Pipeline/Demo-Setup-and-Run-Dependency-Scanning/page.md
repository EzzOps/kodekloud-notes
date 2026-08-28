# Dockerfile
FROM node:18-alpine3.17
WORKDIR /usr/app
COPY package*.json ./
RUN npm install
COPY . .
ENV MONGO_URI=uriPlaceholder
ENV MONGO_USERNAME=usernamePlaceholder
ENV MONGO_PASSWORD=passwordPlaceholder
EXPOSE 3000
CMD ["npm", "start"]
```

## 8. OpenAPI Spec (`openapi.yaml`)

Define three endpoints for probes and host info:

```yaml theme={null}
openapi: 3.0.0
info:
  title: Solar System API
  version: 1.0
paths:
  /os:
    get:
      responses:
        '200':
          description: Hostname info
  /live:
    get:
      responses:
        '200':
          description: Liveness probe
  /ready:
    get:
      responses:
        '200':
          description: Readiness probe
```

## 9. Run Locally

1. Install dependencies:
   ```bash theme={null}
   npm install
   ```
2. Export MongoDB credentials or hard-code for quick tests:

<Callout icon="lightbulb">
  If `MONGO_URI` isn’t set, `npm test` will fail. Use:

  ```bash theme={null}
  export MONGO_URI="your-mongo-uri"
  export MONGO_USERNAME="user"
  export MONGO_PASSWORD="pass"
  ```
</Callout>

3. Run tests and coverage:
   ```bash theme={null}
   npm test
   npm run coverage
   ```
4. Add a listener in `app.js` to start the server:

   ```javascript theme={null}
   app.listen(3000, () => console.log('Server running on port 3000'));
   ```
5. Start the application:
   ```bash theme={null}
   npm start
   ```

## 10. Explore in Browser

Navigate to `http://<VM-IP>:3000` to view and search planets:

<Frame>
  ![The image shows a stylized representation of the solar system with planets orbiting the sun, accompanied by a search interface for exploring the planets.](https://kodekloud.com/kk-media/image/upload/v1752871067/notes-assets/images/Certified-Jenkins-Engineer-Demo-Run-and-Test-NodeJS-App-on-Local-Machine/solar-system-planets-orbiting.jpg)
</Frame>

Search for ID “3” (Earth):

<Frame>
  ![The image shows a stylized depiction of Earth with a description about the planet, set against a space-themed background. It includes a "Solar System" header and a search feature for planets.](https://kodekloud.com/kk-media/image/upload/v1752871068/notes-assets/images/Certified-Jenkins-Engineer-Demo-Run-and-Test-NodeJS-App-on-Local-Machine/earth-space-themed-diagram.jpg)
</Frame>

Test the JSON endpoints:

```bash theme={null}
curl http://<VM-IP>:3000/os   # {"os":"jenkins-controller-1"}
curl http://<VM-IP>:3000/live # {"status":"live"}
curl http://<VM-IP>:3000/ready# {"status":"ready"}
```

***

In the next lesson, we’ll automate cloning, building, testing, coverage enforcement, and deployment with **Jenkins pipelines**.

## Links and References

* [Node.js](https://nodejs.org/)
* [Express Guide](https://expressjs.com/)
* [Mongoose Docs](https://mongoosejs.com/)
* [Mocha](https://mochajs.org/)
* [Chai Assertion Library](https://www.chaijs.com/)
* [nyc (Istanbul CLI)](https://github.com/istanbuljs/nyc)
* [OpenAPI Specification](https://swagger.io/specification/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/73d0066f-a01f-4d13-a00c-c9baf9aae603/lesson/33c64c15-9f9d-4742-9abb-28cc3f253de8" />
</CardGroup>


# Demo Setup and Run Dependency Scanning

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Setting-up-CI-Pipeline/Demo-Setup-and-Run-Dependency-Scanning/page

This tutorial explains how to configure Jenkins for scanning project dependencies using NPM Audit and OWASP Dependency-Check to identify vulnerabilities.

In this tutorial, you’ll configure Jenkins to scan project dependencies using two methods:

1. **NPM Audit** (critical-level checks)
2. **OWASP Dependency-Check** (via Jenkins plugin)

These scans help you catch vulnerabilities early and enforce quality gates in your CI pipeline.

## Table of Contents

* [1. NPM Dependency Audit](#1-npm-dependency-audit)
* [2. OWASP Dependency-Check Plugin](#2-owasp-dependency-check-plugin)
  * [2.1 Install the Plugin](#21-install-the-plugin)
  * [2.2 Global Tool Configuration](#22-global-tool-configuration)
  * [2.3 Generate Pipeline Snippet](#23-generate-pipeline-snippet)
* [3. Running the Pipeline](#3-running-the-pipeline)
* [4. Enforcing Quality Gates](#4-enforcing-quality-gates)
* [Conclusion](#conclusion)

***

## 1. NPM Dependency Audit

Add an NPM audit stage to your `Jenkinsfile`:

```groovy theme={null}
pipeline {
  tools {
    nodejs 'nodejs-22-6-0'
  }
  stages {
    stage('Install Dependencies') {
      steps {
        sh 'npm install --no-audit'
      }
    }
    stage('NPM Dependency Audit') {
      steps {
        sh '''
          npm audit --audit-level=critical
          echo $?
        '''
      }
    }
  }
}
```

What happens:

* `npm install --no-audit` installs dependencies without auditing.
* `npm audit --audit-level=critical` checks for critical vulnerabilities and exits `1` if found.

### Sample package.json

```json theme={null}
{
  "scripts": {
    "start": "node app.js",
    "test": "mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit",
    "coverage": "nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test.js"
  },
  "nyc": {
    "check-coverage": true,
    "lines": 90
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.18.2",
    "mocha-junit-reporter": "^2.2.1",
    "mongoose": "^5.13.20",
    "nyc": "^15.1.0",
    "serverless-http": "^3.2.0"
  },
  "devDependencies": {
    "chai": "*",
    "chai-http": "*"
  }
}
```

### CLI Output Example

```bash theme={null}
