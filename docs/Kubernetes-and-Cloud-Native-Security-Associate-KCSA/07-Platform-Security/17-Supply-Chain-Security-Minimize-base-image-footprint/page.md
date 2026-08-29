# Supply Chain Security Minimize base image footprint

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Platform-Security/Supply-Chain-Security-Minimize-base-image-footprint/page

This lesson focuses on reducing Docker image attack surfaces and disk usage by constructing minimal, secure containers.

Welcome to this lesson on reducing the attack surface and disk usage of Docker images. In this guide, we’ll explore the differences between base and parent images, and share best practices for constructing minimal, secure containers.

## Understanding Parent vs Base Images

Every Docker build begins with a `FROM` instruction. The image you specify is your **parent image**, and its ancestors are known as **base images**. Tracing the lineage helps you understand what gets into your final artifact.

```dockerfile theme={null}
