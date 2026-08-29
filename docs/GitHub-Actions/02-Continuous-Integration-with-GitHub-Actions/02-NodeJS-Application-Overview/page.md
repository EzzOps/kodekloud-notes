# NodeJS Application Overview

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Continuous-Integration-with-GitHub-Actions/NodeJS-Application-Overview/page

This guide covers Node.js setup, testing, and running a simple application, along with integrating it into a GitHub Actions workflow.

In this guide, you’ll learn what Node.js is and how to set up, test, and run a simple “Hello World” application. We’ll also show you how to integrate this Node.js project into a custom [GitHub Actions](https://docs.github.com/en/actions) workflow for continuous integration.

## What Is Node.js?

Node.js is an open-source, cross-platform JavaScript runtime built on Chrome’s [V8 engine](https://v8.dev). It enables you to run JavaScript on the server side, unifying your front-end and back-end development in a single language. Installing Node.js also provides npm (Node Package Manager) for managing your dependencies.

> **lightbulb** * High performance with non-blocking I/O
  * Vast ecosystem via `npm`
  * Single language for client and server

## Prerequisites

Before you begin, ensure you have Node.js and npm installed on your machine.

```bash theme={null}
node -v    # e.g., v18.16.0
npm -v     # e.g., 9.8.1
```

> **triangle-alert** Always verify that your CI/CD environment (like GitHub Actions) uses the same Node.js version as your local setup to avoid inconsistencies.

## Sample Project Structure

Below is a minimal Node.js project that returns “Hello World” from a `/hello` endpoint.

| File         | Purpose                                                        |
| ------------ | -------------------------------------------------------------- |
| package.json | Metadata (name, version), dependencies, and script definitions |
| index.js     | Main application file (defines server and routes)              |
| test.js      | Simple test suite to verify the logic in `index.js`            |

## Installing Dependencies

Install all required packages listed in `package.json`:

```bash theme={null}
npm install
```

On success, npm generates a `node_modules` directory containing your project’s dependencies.

## Running Your Tests

Run the test suite defined in `test.js`:

```bash theme={null}
npm test
```

Expected output:

```bash theme={null}
> my-app@1.0.0 test
> node test.js

Testing is successful
```

## Starting the Application

Launch the server:

```bash theme={null}
npm start
```

You’ll see:

```bash theme={null}
> my-app@1.0.0 start
> node index.js

App listening on port 3000
```

In another terminal or your browser, request the `/hello` endpoint:

```bash theme={null}
curl http://localhost:3000/hello
