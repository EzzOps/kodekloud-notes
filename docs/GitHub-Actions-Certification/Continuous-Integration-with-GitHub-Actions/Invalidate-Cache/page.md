# Invalidate Cache

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Continuous-Integration-with-GitHub-Actions/Invalidate-Cache/page

This guide explains how to use GitHub Actions to invalidate and refresh the NPM cache based on changes in `package-lock.json`.

In this guide, you’ll learn how GitHub Actions uses a hash of `package-lock.json` to invalidate and refresh the NPM cache whenever dependencies change. By incorporating `hashFiles('package-lock.json')` into your cache key, you ensure that outdated artifacts aren’t reused and that a fresh cache is stored after updates.

## Initial Cache Setup

Assume your repository includes a workflow that caches `node_modules` based on the lockfile’s hash. Here’s the original `package.json`:

```json theme={null}
{
  "name": "Solar_System",
  "version": "6.6.7",
  "author": "Siddharth Barahalikar <barahalikar.siddharth@gmail.com>",
  "homepage": "https://www.linkedin.com/in/barahalikar-siddharth/",
  "license": "MIT",
  "scripts": {
    "start": "node app.js",
    "test": "mocha app-test.js --timeout 10000 --reporter mocha-junit-reporter --exit",
    "coverage": "nyc --reporter cobertura --reporter lcov --reporter text --reporter json-summary mocha app-test.js --timeout 10000"
  },
  "nyc": {
    "check-coverage": true,
    "lines": 90
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.18.2",
    "mocha-junit-reporter": "2.2.1",
    "mongoose": "5.13.20",
    "nyc": "^15.1.0"
  },
  "devDependencies": {
    "chai": "*",
    "chai-http": "*",
    "mocha": "*"
  }
}
```

These dependencies are restored from cache on each workflow run and only invalidated when `package-lock.json` changes.

## Adding a New Dependency

When you introduce a new package, the lockfile hash changes, triggering a cache miss:

```bash theme={null}
