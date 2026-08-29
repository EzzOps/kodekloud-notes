# Demo 1 Getting Access to Open Source Projects

Source: https://notes.kodekloud.com/docs/Open-Source-for-Beginners/Open-Source/Demo-1-Getting-Access-to-Open-Source-Projects/page

This demo guides you in finding and downloading the source code of Docker Compose from GitHub.

Welcome to the first demo of this course! In this walkthrough, we’ll explore how to find and download the source code of a popular open source project—Docker Compose. By the end, you’ll have the project’s files on your local machine and understand the basic layout of a GitHub repository.

## What Is Docker Compose?

Docker Compose is an open source tool for defining and running multi-container Docker applications. You describe your services in a `docker-compose.yml` file and start everything with a single command. It simplifies development workflows by coordinating multiple containers with minimal configuration.

<Callout icon="lightbulb">
  If you’re new to Docker or Compose, no worries—this demo focuses on accessing the project’s codebase rather than using it.
</Callout>

## 1. Explore Docker’s Open Source Page

First, visit Docker’s official open source portal to see all the projects they maintain.

<Frame>
  ![The image shows an octopus holding blue cubes next to a document icon labeled "YAML," with a plus sign between them.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882532/notes-assets/images/Open-Source-for-Beginners-Demo-1-Getting-Access-to-Open-Source-Projects/octopus-blue-cubes-yaml-icon.jpg)
</Frame>

Head to the [Docker Open Source page][docker-oss] and scroll down until you see **Docker Compose**.

<Frame>
  ![The image is a screenshot of the Docker website's "Open Source" page, highlighting Docker's collaboration with the open source ecosystem and its projects. It includes navigation links and a "Get Started" button.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882533/notes-assets/images/Open-Source-for-Beginners-Demo-1-Getting-Access-to-Open-Source-Projects/docker-open-source-page-screenshot.jpg)
</Frame>

## 2. Navigate to the GitHub Repository

Click the Docker Compose link to jump to its GitHub repository. If you don’t have a GitHub account, sign up at [github.com][github].

<Frame>
  ![The image shows a GitHub repository page for "docker/compose," displaying the file structure, recent commits, and repository statistics like stars and forks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882534/notes-assets/images/Open-Source-for-Beginners-Demo-1-Getting-Access-to-Open-Source-Projects/github-repo-docker-compose-structure.jpg)
</Frame>

### About the Repository

| Statistic | Description                             |
| --------- | --------------------------------------- |
| Stars     | How many users have starred the repo    |
| Forks     | How many times the repo has been forked |
| License   | The open source license (Apache 2.0)    |

Below the **About** section you’ll find:

* **Tags**: Keywords that describe the project
* **Releases**: Version history and changelogs
* **Contributors**: Who has committed to the codebase
* **README Preview**: A quick overview of the project’s goals and usage

<Frame>
  ![The image shows a GitHub repository page for "Docker Compose v2," featuring a cartoon octopus with Docker containers and information about the repository, including contributors and language usage statistics.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882536/notes-assets/images/Open-Source-for-Beginners-Demo-1-Getting-Access-to-Open-Source-Projects/github-repo-docker-compose-octopus.jpg)
</Frame>

<Callout icon="triangle-alert">
  Always check the LICENSE file before using or modifying open source code to ensure compliance with its terms.
</Callout>

## 3. Download the Source Code

To grab the entire codebase:

1. Click the green **Code** button in the top-right of the repo.
2. Select **Download ZIP**.
3. Unzip the downloaded file to your desired directory.

<Frame>
  ![The image shows a GitHub repository page for "docker/compose," displaying the file structure, clone options, and repository details like stars and forks.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882537/notes-assets/images/Open-Source-for-Beginners-Demo-1-Getting-Access-to-Open-Source-Projects/github-repo-docker-compose-structure-2.jpg)
</Frame>

Congratulations—you now have the Docker Compose source code on your local machine!

## Next Steps

Repeat this process to explore other open source projects. In the next demo, we’ll look at how to read and run the project’s examples.

***

## Links and References

* [Docker Open Source][docker-oss]
* [Docker Compose GitHub Repository](https://github.com/docker/compose)
* [GitHub Signup](https://github.com)

[docker-oss]: https://www.docker.com/open-source

[github]: https://github.com

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/open-source-for-beginners/module/649f4ff1-452a-46e6-9822-6cb8808ccc6f/lesson/1cfa4b39-1b99-4969-96d3-53f94f7edcea" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/open-source-for-beginners/module/649f4ff1-452a-46e6-9822-6cb8808ccc6f/lesson/be446a0c-784c-4546-bd18-f6e32afa525e" />
</CardGroup>
