# Run and Test NodeJS App on Local Machine

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/Run-and-Test-NodeJS-App-on-Local-Machine/page

Learn to run and test the Solar System Node.js application locally before integrating it into a GitLab CI/CD pipeline.

Learn how to run and test the Solar System Node.js application locally before integrating it into a GitLab CI/CD pipeline. The source code is hosted on GitLab.

![The image shows a GitLab repository page for a project named "Solar-System," displaying the project files and their last commit details. The interface includes options for managing, planning, and deploying the project.](https://kodekloud.com/kk-media/image/upload/v1752877290/notes-assets/images/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines-Run-and-Test-NodeJS-App-on-Local-Machine/gitlab-solar-system-repo-page.jpg)

## Prerequisites

* Node.js and npm
* A running MongoDB instance or Atlas cluster
* Git installed on your machine

To verify Node.js and npm:

```bash theme={null}
node --version   # e.g., v18.x.x
npm --version    # e.g., 9.x.x
```

## Clone the Repository

```bash theme={null}
git clone https://gitlab.com/sidd-harth/solar-system.git
cd solar-system
```

## Project Structure and Key Files

This repository includes:

* **package.json**: Defines metadata, scripts, dependencies, and coverage thresholds
* **app.js**: Backend Express.js server
* **client.js**: Frontend script to fetch planet data
* **Dockerfile**: Build instructions for a Docker image
* **deployment.yaml** & **service.yaml**: Kubernetes manifests

### package.json

```json theme={null}
{
  "name": "Solar System",
  "version": "6.7.6",
  "author": "Siddharth Barahalikar",
  "license": "MIT",
  "scripts": {
    "start": "node app.js",
    "test": "mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit",
    "coverage": "nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test.js"
  },
  "nyc": {
    "check-coverage": true,
    "lines": 90
  },
  ...
}
```

| Script   | Description                                 | Command            |
| -------- | ------------------------------------------- | ------------------ |
| start    | Launch the Express server                   | `npm start`        |
| test     | Run tests with Mocha and JUnit reporter     | `npm test`         |
| coverage | Generate coverage reports (cobertura, lcov) | `npm run coverage` |

### Application Backend (app.js)

```javascript theme={null}
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mongoose = require('mongoose');

const app = express();
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, '/')));
app.use(cors());

mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
}, (err) => {
  if (err) {
    console.error("Connection error:", err);
  } else {
    console.log("Connected to MongoDB");
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

> **lightbulb** Ensure you add your REST API route handlers in `app.js` (for example, a GET `/os` endpoint) before testing.

### Frontend Controller (client.js)

```javascript theme={null}
console.log('Client script loaded');

window.onload = () => {
  console.log("Requesting all planets");
  fetch("/os", { method: "GET" })
    .then(res => res.ok ? res.json() : Promise.reject("Fetch error"))
    .then(data => console.log(data))
    .catch(error => console.error(error));
};
```

### Dockerfile

```dockerfile theme={null}
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

### Kubernetes Manifests

```yaml theme={null}
