# Trivy Basics

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevSecOps-Pipeline/Trivy-Basics/page

This guide explains how to use Trivy, a vulnerability scanner for container images and artifacts, covering installation, scanning, and output formats.

In this guide, you’ll discover how to use Trivy—a fast, easy-to-use vulnerability scanner for container images and other artifacts. Trivy inspects both operating system packages (Alpine, RHEL, CentOS, Debian, Distroless) and application dependencies (NPM, Cargo, NuGet, Go modules, Maven). We’ll demonstrate scanning a Maven-based Java application, but the commands apply to any supported language or OS.

## Installation

You can install Trivy as a standalone binary or run it via Docker.

### Standalone Binary

Download the latest release from the [Trivy GitHub Releases page](https://github.com/aquasecurity/trivy/releases), then:

```bash theme={null}
