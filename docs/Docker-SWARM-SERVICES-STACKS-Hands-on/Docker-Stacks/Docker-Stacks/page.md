# Docker Stacks

Source: https://notes.kodekloud.com/docs/Docker-SWARM-SERVICES-STACKS-Hands-on/Docker-Stacks/Docker-Stacks/page

This article explores advanced Docker concepts for deploying and managing application stacks using Docker Compose and Docker Swarm.

Welcome to this in-depth guide on Docker Stacks. I’m Mumshad Mannambeth, and in this article we’ll explore advanced Docker concepts to help you deploy and manage application stacks more efficiently. Instead of running multiple individual containers with the Docker run command, you can now define your entire application stack in a single Docker Compose file and launch it effortlessly.

## From Single Containers to Application Stacks

Previously, you might have deployed your services with commands like:

```bash theme={null}
docker run mmumshad/simple-webapp
docker run mongodb
docker run redis:alpine
docker run ansible
```

With Docker Stacks, these individual commands can be consolidated into a single Docker Compose file:

```yaml theme={null}
