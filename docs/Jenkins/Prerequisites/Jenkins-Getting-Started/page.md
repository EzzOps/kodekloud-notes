# Jenkins Getting Started

Source: https://notes.kodekloud.com/docs/Jenkins/Prerequisites/Jenkins-Getting-Started/page

This article explores Jenkins, an open-source automation server for CI/CD workflows, highlighting its features, documentation, plugins, and community support.

In this article, we dive deep into Jenkins—an open-source automation server that simplifies continuous integration and continuous delivery (CI/CD) workflows by automating manual tasks. Discover Jenkins' extensive features, documentation, plugins, and active community support to enhance your development lifecycle.

Start by visiting the [Jenkins homepage](https://www.jenkins.io) to see the iconic butler mascot. This character embodies how Jenkins operates by taking care of routine tasks so you can focus on innovation.

The homepage is organized into key sections, including a blog, detailed documentation, available plugins, community resources, and subprojects. Let’s examine each of these areas.

## Blog and Documentation

The Jenkins blog offers insights ranging from security alerts to practical guides—such as leveraging containers as build agents. Meanwhile, the comprehensive documentation is an excellent resource for both beginners and experts. It provides step-by-step installation instructions, including Docker-based setups.

Below is an example snippet from the documentation for deploying Jenkins with Docker:

```bash theme={null}
docker run \
  --name jenkins-blueocean \
  --rm \
  --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:1.1
```

<Callout icon="lightbulb">
  This Docker command is a clear example of the easy-to-follow instructions available in Jenkins documentation. It simplifies the setup process, allowing you to get started quickly.
</Callout>

Visual guides in the documentation further enhance your understanding. For instance:

<Frame>
  ![The image shows the Jenkins Community Blog webpage with a dropdown menu under "Documentation" and articles about deprecating non-Java plugins and an Apache Log4j vulnerability.](https://kodekloud.com/kk-media/image/upload/v1752880095/notes-assets/images/Jenkins-Jenkins-Getting-Started/frame_80.jpg)
</Frame>

When exploring Docker installations, the documentation details prerequisites, OS-specific steps, and essential commands:

<Frame>
  ![The image shows a Jenkins documentation page detailing Docker installation prerequisites, including hardware requirements and configuration recommendations for running Jenkins.](https://kodekloud.com/kk-media/image/upload/v1752880096/notes-assets/images/Jenkins-Jenkins-Getting-Started/frame_90.jpg)
</Frame>

## Plugins

Jenkins plugins extend the server's capabilities by integrating with external systems. For example, searching for "Azure" in the plugins section reveals a variety of options that support Azure CLI, Azure App Services, Key Vault, and more—ensuring seamless automation within the Azure ecosystem.

<Frame>
  ![The image shows the Jenkins Plugins Index webpage, featuring a search bar, plugin categories, new and updated plugins, and trending topics.](https://kodekloud.com/kk-media/image/upload/v1752880097/notes-assets/images/Jenkins-Jenkins-Getting-Started/frame_110.jpg)
</Frame>

Specific results for Azure-related plugins include:

<Frame>
  ![The image shows a Jenkins plugin search page with results for "Azure," displaying various Azure-related plugins, their install counts, and release dates.](https://kodekloud.com/kk-media/image/upload/v1752880098/notes-assets/images/Jenkins-Jenkins-Getting-Started/frame_120.jpg)
</Frame>

These integrations are key to optimizing your cloud-based automation processes.

## Community and Subprojects

Jenkins thrives on a vibrant community of users, developers, and contributors. The ecosystem includes regular meetups, collaborative code contributions, thorough testing, and extensive documentation that facilitates knowledge sharing.

The website also highlights several subprojects:

* Jenkins Configuration as Code
* Jenkins Area Meetups

These initiatives offer additional resources and foster community engagement, providing ample opportunities to connect and contribute.

Additionally, the website navigation features dedicated sections for security updates, press releases, and a roadmap outlining future enhancements. This comprehensive resource hub ensures you find all the information needed to fully leverage Jenkins.

## Conclusion

Whether you’re aiming to boost your CI/CD pipeline or exploring automation tools, Jenkins offers an exceptional platform for innovation. Visit jenkins.io for detailed documentation, a wide array of plugins, and active community discussion to further advance your skills.

<Frame>
  ![The image shows the Jenkins website homepage, featuring its logo and options to access documentation and download the software. Jenkins is an open-source automation server.](https://kodekloud.com/kk-media/image/upload/v1752880100/notes-assets/images/Jenkins-Jenkins-Getting-Started/frame_220.jpg)
</Frame>

Happy automating, and see you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.[AWS_SECRET_ACCESS_KEY]-016d-4b60-9731-1cdaaddb3e3c/lesson/7f063a61-a24f-48d4-ac44-7163c42ea752" />
</CardGroup>
