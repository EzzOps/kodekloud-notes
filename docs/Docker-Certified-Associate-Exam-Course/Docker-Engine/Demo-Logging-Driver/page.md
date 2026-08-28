# Demo Logging Driver

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Engine/Demo-Logging-Driver/page

This tutorial covers managing Dockers logging drivers, including checking defaults, changing settings, and applying options for individual containers.

In this tutorial, you’ll learn how to manage Docker’s logging drivers—check the default, switch the daemon-wide setting, apply advanced options, and override the driver for individual containers.

## 1. Check the Default Logging Driver

Docker uses the `json-file` driver by default, storing container logs as JSON on the host.

```bash theme={null}
