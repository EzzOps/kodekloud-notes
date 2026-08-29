# ● jenkins.service - Jenkins Continuous Integration Server
#    Active: active (running)
```

If Node.js is available on the controller, freestyle jobs can execute `node` and `npm` directly. Agents without Node.js will fail unless you provide a managed installation.

## 2. Test Node.js in a Freestyle Project

1. In Jenkins, click **New Item**, enter `npm-version-test`, choose **Freestyle project**, then **OK**.
2. Under **Build** → **Execute shell**, add:

   ```bash theme={null}
   node -v
   npm -v
   ```

![The image shows a Jenkins interface where a user is creating a new item, with options to select different project types like Freestyle project, Pipeline, and others. The item name entered is "npm-version-test."](https://kodekloud.com/kk-media/image/upload/v1752871059/notes-assets/images/Certified-Jenkins-Engineer-Demo-InstallSetup-NodeJS-Build-Tool/jenkins-new-item-npm-version-test.jpg)

3. Save and run the job. You should see:

   ```bash theme={null}
   Started by user example
   Building in workspace /var/lib/jenkins/workspace/npm-version-test
   [npm-version-test] $ /bin/sh -xe /tmp/jenkins.sh
   + node -v
   v20.16.0
   + npm -v
   10.8.1
   Finished: SUCCESS
   ```

![The image shows a Jenkins dashboard for a project named "npm-version-test," displaying build status and history with options for configuration and project management.](https://kodekloud.com/kk-media/image/upload/v1752871060/notes-assets/images/Certified-Jenkins-Engineer-Demo-InstallSetup-NodeJS-Build-Tool/jenkins-dashboard-npm-version-test.jpg)

> **triangle-alert** If your builds run on agents without Node.js, this job will fail. To ensure consistency, use Jenkins-managed tools.

## 3. Install the NodeJS Plugin

Add Node.js as a managed tool in Jenkins:

1. Go to **Manage Jenkins** → **Manage Plugins** → **Available**.
2. Search for **NodeJS**, select **NodeJS plugin (v1.6.2)**, then **Install without restart**.

![The image shows a Jenkins interface with a search for "NodeJS" in the available plugins section, displaying the NodeJS plugin version 1.6.2.](https://kodekloud.com/kk-media/image/upload/v1752871062/notes-assets/images/Certified-Jenkins-Engineer-Demo-InstallSetup-NodeJS-Build-Tool/jenkins-nodejs-plugin-search-1-6-2.jpg)

Wait for the installation to complete:

![The image shows a Jenkins dashboard displaying the download progress of plugins, with all tasks marked as successful. The interface includes options for managing plugins and settings.](https://kodekloud.com/kk-media/image/upload/v1752871063/notes-assets/images/Certified-Jenkins-Engineer-Demo-InstallSetup-NodeJS-Build-Tool/jenkins-dashboard-plugin-download-progress.jpg)

## 4. Configure Node.js as a Global Tool

1. Navigate to **Manage Jenkins** → **Global Tool Configuration**.

2. Under **NodeJS installations**, click **Add NodeJS**, then fill in:

   * **Name**: `Node.js 22.6.0`
   * **Install automatically**: checked
   * **Version**: `22.6.0`

3. Click **Save**.

![The image shows a Jenkins configuration screen for adding NodeJS, with options to install a specific version and configure global npm packages.](https://kodekloud.com/kk-media/image/upload/v1752871064/notes-assets/images/Certified-Jenkins-Engineer-Demo-InstallSetup-NodeJS-Build-Tool/jenkins-nodejs-configuration-screen.jpg)

## 5. Use the Managed Node.js in a Freestyle Job

1. Open the **npm-version-test** job and click **Configure**.
2. In **Build Environment**, enable **Provide Node & npm bin/ folder to PATH**, then select **Node.js 22.6.0**.

![The image shows a configuration screen for a build environment, likely in a CI/CD tool, with options for Node.js installation and npm settings. The interface includes checkboxes and dropdown menus for various settings, such as providing Node & npm bin folder to PATH and executing shell commands.](https://kodekloud.com/kk-media/image/upload/v1752871065/notes-assets/images/Certified-Jenkins-Engineer-Demo-InstallSetup-NodeJS-Build-Tool/ci-cd-build-environment-node-npm.jpg)

3. Save and trigger the build. The first run installs Node.js on the controller:

   ```bash theme={null}
   Started by user example
   Building in workspace /var/lib/jenkins/workspace/npm-version-test
   Unpacking https://nodejs.org/dist/v22.6.0/node-v22.6.0-linux-x64.tar.gz to /var/lib/jenkins/tools/.../nodejs-22-6-0
   [npm-version-test] $ /bin/sh -xe /tmp/jenkins.sh
   + node -v
   v22.6.0
   + npm -v
   10.8.2
   Finished: SUCCESS
   ```

Subsequent builds reuse the cached installation, ensuring consistent Node.js versions across all agents.

## Summary

| Step                      | Description                                                 |
| ------------------------- | ----------------------------------------------------------- |
| Verify Host Installation  | Check `node -v` and `npm -v` on the Jenkins controller.     |
| Freestyle Project Test    | Run a basic freestyle job using host-installed Node.js.     |
| Install NodeJS Plugin     | Add NodeJS plugin via **Manage Plugins**.                   |
| Global Tool Configuration | Define Node.js under **Global Tool Configuration**.         |
| Use Managed Node.js       | Enable Node.js in **Build Environment** of a freestyle job. |

## Links and References

* [Jenkins Documentation](https://www.jenkins.io/doc/)
* [NodeJS Plugin](https://plugins.jenkins.io/nodejs/)
* [Node.js Official Site](https://nodejs.org/)

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-jenkins-engineer/module/73d0066f-a01f-4d13-a00c-c9baf9aae603/lesson/adb86404-e404-46e0-9a10-42601b3a5a33)


# Demo Run and Test NodeJS App on Local Machine

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Setting-up-CI-Pipeline/Demo-Run-and-Test-NodeJS-App-on-Local-Machine/page

This guide covers running and testing a Solar System Node.js application locally, including setup, testing, and containerization.

In this guide, we’ll walk through running and testing a **Solar System** Node.js application on your local (or virtual) machine. We’ll cover:

* Cloning the repository
* Inspecting `package.json`
* Reviewing application code (`app.js`, controllers, client)
* Executing unit tests and enforcing coverage
* Containerizing with Docker
* Exploring OpenAPI specs
* Running the app and demoing endpoints
* Automating everything with Jenkins pipelines

## Prerequisites

Ensure you have these versions installed:

```bash theme={null}
node --version    # v8.11.3+
npm --version     # v6.1.0+
```

Install project dependencies:

```bash theme={null}
npm install
```

Run a quick test:

```bash theme={null}
npm test
npm run coverage
```

## Repository Overview

The **Solar System** app uses:

* **Express** for the REST API
* **Mongoose** for MongoDB integration
* **Mocha** & **Chai** for testing
* **nyc** for code coverage
* **serverless-http** for AWS Lambda support

![The image shows a GitHub repository page for a project titled "Solar System NodeJS Application," featuring a list of files and their commit history. The repository primarily uses JavaScript, HTML, and Dockerfile.](https://kodekloud.com/kk-media/image/upload/v1752871066/notes-assets/images/Certified-Jenkins-Engineer-Demo-Run-and-Test-NodeJS-App-on-Local-Machine/solar-system-nodejs-repo-files.jpg)

### Project Structure

| File/Folder         | Purpose                              |
| ------------------- | ------------------------------------ |
| `package.json`      | Metadata, scripts, dependencies      |
| `app.js`            | Express setup & MongoDB connection   |
| `app.controller.js` | Route definitions & Mongoose schemas |
| `client.js`         | Frontend logic for `/os` endpoint    |
| `app-test.js`       | Mocha/Chai test suite                |
| `Dockerfile`        | Containerization instructions        |
| `openapi.yaml`      | OpenAPI 3.0 definitions              |
| `index.html`        | Static frontend                      |

## 1. Clone the Repository

```bash theme={null}
git clone https://github.com/sidd-harth/solar-system-gitea.git
cd solar-system-gitea/
```

## 2. Inspect `package.json`

Open `package.json` to review scripts and dependencies:

```json theme={null}
{
  "name": "Solar System",
  "version": "6.7.6",
  "scripts": {
    "start": "node app.js",
    "test": "mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit",
    "coverage": "nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test"
  },
  "nyc": {
    "check-coverage": true,
    "lines": 90
  },
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^5.13.20",
    "cors": "^2.8.5",
    "serverless-http": "^1.15.0"
  },
  "devDependencies": {
    "mocha": "*",
    "chai": "*",
    "chai-http": "*"
  }
}
```

Key points:

* `test` runs Mocha with JUnit output.
* `coverage` enforces ≥ 90% line coverage via **nyc**.
* **serverless-http** enables AWS Lambda compatibility.

## 3. Application Entry Point (`app.js`)

This file initializes Express, connects to MongoDB, and exports the app for tests and serverless:

```javascript theme={null}
// app.js
const path = require('path');
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');
const serverless = require('serverless-http');

const app = express();
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname)));
app.use(cors());

mongoose.connect(process.env.MONGO_URI, {
  user: process.env.MONGO_USERNAME,
  pass: process.env.MONGO_PASSWORD,
  useNewUrlParser: true,
  useUnifiedTopology: true
}, err => {
  if (err) console.error('MongoDB connection error:', err);
});

// Export for tests & AWS Lambda
module.exports = app;
```

## 4. Controller & Routes (`app.controller.js`)

Define the Mongoose schema and API endpoints:

```javascript theme={null}
// app.controller.js
const os = require('os');
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const dataSchema = new Schema({
  id: Number,
  name: String,
  description: String,
  image: String,
  velocity: String,
  distance: String
});
const Planet = mongoose.model('planets', dataSchema);

app.post('/planet', (req, res) => {
  Planet.findOne({ id: req.body.id }, (err, planet) => {
    if (err) return res.status(500).send(err);
    res.json(planet);
  });
});

app.get('/os', (req, res) => {
  res.json({ os: os.hostname() });
});

app.get('/live', (req, res) => {
  res.json({ status: 'live' });
});

app.get('/ready', (req, res) => {
  res.json({ status: 'ready' });
});
```

## 5. Frontend Logic (`client.js`)

Fetch and display the hostname from `/os`:

```javascript theme={null}
// client.js
window.onload = () => {
  fetch('/os')
    .then(res => res.ok ? res.json() : Promise.reject('Request failed'))
    .then(data => {
      document.getElementById('hostname').innerText = `Pod - ${data.os}`;
    })
    .catch(console.error);
};

const btn = document.getElementById('submit');
if (btn) {
  btn.addEventListener('click', () => {
    // handle planet search...
  });
}
```

## 6. Unit Tests (`app-test.js`)

Validate endpoints with Mocha, Chai, and `chai-http`:

```javascript theme={null}
// app-test.js
const chai = require('chai');
const chaiHttp = require('chai-http');
const app = require('./app');

chai.use(chaiHttp);
chai.should();

describe('Solar System API', () => {
  describe('POST /planet', () => {
    it('returns Mercury for id=1', done => {
      chai.request(app)
        .post('/planet')
        .send({ id: 1 })
        .end((err, res) => {
          res.should.have.status(200);
          res.body.should.include({ id: 1, name: 'Mercury' });
          done();
        });
    });
  });

  it('GET /os returns host information', done => {
    chai.request(app)
      .get('/os')
      .end((err, res) => {
        res.should.have.status(200);
        res.body.should.have.property('os');
        done();
      });
  });
});
```

## 7. Dockerfile

Build an Alpine-based Node.js container:

```dockerfile theme={null}
