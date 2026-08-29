# NodeJS Application Overview

Source: https://notes.kodekloud.com/docs/Certified-Jenkins-Engineer/Setting-up-CI-Pipeline/NodeJS-Application-Overview/page

This article provides an overview of Node.js, its features, npm, and a typical project structure for building applications.

In this lesson, we’ll explore [Node.js][Node.js]—an open-source, cross-platform JavaScript runtime—and see how it powers custom [GitHub Actions][GitHub Actions] workflows. You’ll learn about its core features, the built-in package manager, and a typical project layout.

## What Is Node.js?

[Node.js][Node.js] is a JavaScript runtime built on Google’s high-performance [V8 engine][V8]. It lets you run JavaScript outside the browser, so you can build server-side apps, CLI tools, and more—all with the same language you use in the browser. Node.js supports Windows, macOS, and Linux.

<Callout icon="lightbulb">
  For production environments, use the Long-Term Support (LTS) version of Node.js. Manage multiple versions easily with tools like [nvm](https://github.com/nvm-sh/nvm).
</Callout>

## Node Package Manager (npm)

When you install Node.js, you also get [npm][npm]—the package manager that helps you discover, install, and manage JavaScript libraries and dependencies. With npm you can:

* Share code with the community via the npm registry
* Install and update packages with a single command
* Define project scripts for testing, building, and running your app

## Sample Node.js Project Structure

A minimal Node.js project often includes these three files:

| File         | Purpose                                             |
| ------------ | --------------------------------------------------- |
| package.json | Metadata (name, version) and dependency definitions |
| index.js     | Application entry point and core logic              |
| test.js      | Automated tests for your code                       |

To set up your project:

```bash theme={null}
