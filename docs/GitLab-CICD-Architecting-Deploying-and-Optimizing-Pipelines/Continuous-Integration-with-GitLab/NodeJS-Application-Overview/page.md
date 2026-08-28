# NodeJS Application Overview

Source: https://notes.kodekloud.com/docs/GitLab-CICD-Architecting-Deploying-and-Optimizing-Pipelines/Continuous-Integration-with-GitLab/NodeJS-Application-Overview/page

This guide covers setting up a Node.js project, managing dependencies, running tests, and launching a web server.

In this guide, you’ll learn how to set up a basic Node.js project, install dependencies, run tests, and launch a simple web server. By the end, you’ll be ready to incorporate these steps into a custom [GitHub Action](https://docs.github.com/actions) workflow.

## What Is Node.js?

Node.js is an open-source, event-driven JavaScript runtime built on Chrome’s V8 engine. It enables full-stack development in a single language by allowing JavaScript to run outside of the browser on Windows, macOS, and Linux environments. Installing Node.js also provides npm (Node Package Manager), which helps you discover, install, and manage JavaScript packages.

<Callout icon="lightbulb">
  For production applications, it’s recommended to use the latest LTS version of Node.js. Check [Node.js Releases](https://nodejs.org/en/about/releases/) for details.
</Callout>

## Checking Installed Versions

Before you begin, verify that both Node.js and npm are available:

```bash theme={null}
node -v    # e.g., v18.16.0
npm -v     # e.g., 9.8.1
```

If these commands fail, download and install Node.js from the [official website](https://nodejs.org/).

## Sample Node.js Project Structure

A minimal Node.js application typically includes these items:

| File/Directory | Purpose                                                |
| -------------- | ------------------------------------------------------ |
| package.json   | Project metadata: name, version, dependencies, scripts |
| node\_modules/ | Installed packages after running `npm install`         |
| index.js       | Main application entry point                           |
| test.js        | Contains unit or integration test cases                |

## Installing Dependencies

All required libraries are defined under `dependencies` and `devDependencies` in **package.json**. To install them:

```bash theme={null}
npm install
```

You should see output similar to:

```plain theme={null}
added 58 packages and audited 59 packages in 5s
```

## Running Tests

Most Node.js projects include a `test` script in **package.json**. To execute your test suite:

```bash theme={null}
npm test
```

Example output:

```plain theme={null}
> my-app@1.0.0 test
> node test.js

Testing is successful
```

<Callout icon="triangle-alert">
  Ensure your tests cover edge cases and error paths. Incomplete test coverage can lead to undetected bugs in production.
</Callout>

## Starting the Application

Launch your application using the predefined `start` script:

```bash theme={null}
npm start
```

You’ll see:

```plain theme={null}
> my-app@1.0.0 start
> node index.js

App listening on port 3000
```

## Accessing Your Application

Open your browser and navigate to:

```text theme={null}
http://localhost:3000
```

You should see the response defined in **index.js**, for example, “Hello, World!”.

***

## Next Steps

Now that you can install, test, and run a Node.js app locally, you’re ready to:

* Automate these steps in a **GitHub Actions** workflow
* Containerize your application with **Docker**
* Deploy to a cloud provider using **Terraform** or **Kubernetes**

## References

* [Node.js Official Site](https://nodejs.org/)
* [npm Documentation](https://docs.npmjs.com/)
* [GitHub Actions](https://docs.github.com/actions)
* [JavaScript Guide](https://developer.mozilla.org/docs/Web/JavaScript/Guide)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/gitlab-ci-cd-architecting-deploying-and-optimizing-pipelines/module/3a1c2306-8091-4dfe-b40f-e2ca53918553/lesson/5f3cd913-24bc-40b9-a64e-c8f19f3e25e0" />
</CardGroup>
