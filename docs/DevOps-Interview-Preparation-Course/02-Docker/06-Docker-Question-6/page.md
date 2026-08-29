# Docker Question 6

Source: https://notes.kodekloud.com/docs/DevOps-Interview-Preparation-Course/Docker/Docker-Question-6/page

This lesson compares two Dockerfiles to determine which results in a smaller Docker image based on the choice of base image.

This lesson explores two Dockerfiles and explains which resulting Docker image will be smaller and why. The only difference between these Dockerfiles is the choice of the base image. Dockerfile 1 uses the lightweight "node:12-alpine" image, while Dockerfile 2 uses the default "node" image, which typically points to the latest version and is based on a more comprehensive Debian distribution.

## Detailed Examination of the Dockerfiles

Below are the final, corrected versions of both Dockerfiles:

```dockerfile theme={null}
