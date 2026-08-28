# ECS Demo Part 1

Source: https://notes.kodekloud.com/docs/AWS-Certified-Developer-Associate/Containers-on-AWS/ECS-Demo-Part-1/page

This guide details the process of setting up, deploying, updating, and cleaning up an ECS-based application.

Before working with Amazon ECS in the AWS Console, visit [Docker Hub](https://hub.docker.com) and review the two images that form the basis of our demo projects. These public repositories—available at [kodekloud.com/ecs-project1](https://kodekloud.com/ecs-project1) and [kodekloud.com/ecs-project2](https://kodekloud.com/ecs-project2)—contain the project images we will use.

<Frame>
  ![The image shows a webpage displaying a list of repositories under a community organization, with options to search and create a new repository. Each repository entry includes details like the name, last push time, and visibility status.](https://kodekloud.com/kk-media/image/upload/v1752858511/notes-assets/images/AWS-Certified-Developer-Associate-ECS-Demo-Part-1/community-organization-repositories-list.jpg)
</Frame>

## Project One Overview

Project One uses a simple Node.js application powered by an Express server. When a GET request is sent to the root path, the server responds with a basic HTML file. Below is the HTML file delivered by the application:

```html theme={null}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="css/style.css" />
  <title>Document</title>
</head>
<body>
  <h1>ECS Project 1</h1>
</body>
</html>
```

An indicative terminal prompt might appear as follows:

```bash theme={null}
user1 on user1 in ecs-project1 is v1.0.0
```

The core application is built with Express, as demonstrated below:

```javascript theme={null}
const express = require("express");
const path = require("path");

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.render("index");
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
```

A sample Docker CLI prompt may look like:

```bash theme={null}
user1 on 🐳 user1 in ecs-project1 is 🐳 v1.0.0 via 🐳
```

<Callout icon="lightbulb">
  Note that the Express server listens on port 3000.
</Callout>

The Dockerfile for this project is straightforward and exposes port 3000:

```dockerfile theme={null}
FROM node:16
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm install
RUN npm ci --only=production
COPY .
EXPOSE 3000
CMD [ "node", "index.js" ]
```

## Setting Up ECS Using the AWS Console

### Quick Start with ECS

1. Log in to the AWS Console, search for **"ECS"**, and select **Elastic Container Service**.
2. If you're new to ECS, a quick start wizard will guide you. Although sample applications are available, select the custom option to configure your container manually.
3. In the container configuration:
   * **Container Name:** For example, "ECS-Project1".
   * **Image:** Use "KodeKloud/ECS-Project1". If your image resides in a private repository, provide your credentials; otherwise, leave it as is.
   * **Port Mapping:** Set to 3000/TCP to match the Express application.

Below is a recap of the Dockerfile content referenced earlier:

```dockerfile theme={null}
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install
RUN npm ci --only=production
COPY .
EXPOSE 3000
CMD [ "node", "index.js" ]
```

For traditional Docker deployments, an external port can be mapped to an internal port like this:

```bash theme={null}
