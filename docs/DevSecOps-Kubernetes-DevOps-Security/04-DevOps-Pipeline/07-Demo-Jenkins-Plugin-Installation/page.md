# Demo Jenkins Plugin Installation

Source: https://notes.kodekloud.com/docs/DevSecOps-Kubernetes-DevOps-Security/DevOps-Pipeline/Demo-Jenkins-Plugin-Installation/page

This guide explains how to automate the installation of multiple Jenkins plugins using the Jenkins Remote API.

In this guide, you’ll learn how to install multiple Jenkins plugins automatically by leveraging the Jenkins Remote API. This approach avoids manual UI steps under **Manage Jenkins → Manage Plugins**, speeding up your CI/CD setup.

## 1. Verify Jenkins Is Running

First, confirm that the Jenkins service is active:

```bash theme={null}
sudo systemctl status jenkins
```

Example output:

```text theme={null}
● jenkins.service - LSB: Start Jenkins at boot time
   Loaded: loaded (/etc/init.d/jenkins; generated)
   Active: active (exited) since Tue 2021-06-15 05:07:43 UTC; 1h 39min ago
     Docs: man:systemd-sysv-generator(8)
```

Next, retrieve the initial admin password for API authentication:

```bash theme={null}
sudo cat /var/[AWS_SECRET_ACCESS_KEY]
