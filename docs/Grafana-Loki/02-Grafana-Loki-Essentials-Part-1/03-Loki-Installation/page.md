# Loki Installation

Source: https://notes.kodekloud.com/docs/Grafana-Loki/Grafana-Loki-Essentials-Part-1/Loki-Installation/page

This guide explains how to install Loki locally and configure it with Promtail as a logging agent.

In this guide, you'll learn how to install Loki on your local machine and configure it to work with Promtail as your logging agent. For more detailed information, please refer to the [official Loki documentation](https://grafana.com/docs/loki/latest/).

## 1. Overview

Loki provides multiple deployment options including Helm charts for Kubernetes and Docker container installations. This guide focuses on installing Loki locally. Before you begin, visit the Loki documentation page and review the installation instructions.

## 2. Downloading Configuration Files for Loki and Promtail

Start by downloading the configuration files necessary for both Loki and Promtail. Open your terminal and execute the following commands:

```bash theme={null}
wget https://raw.githubusercontent.com/grafana/loki/main/cmd/loki/loki-local-config.yaml
wget https://raw.githubusercontent.com/grafana/loki/main/clients/cmd/promtail/promtail-local
```

These commands download a basic configuration for a local setup. Feel free to modify these files later according to your specific logging requirements.

## 3. Downloading the Loki Binary

Select the appropriate release for your system architecture. Visit the Loki [release page](https://github.com/grafana/loki/releases) for the latest version. For example, to download and prepare the Loki binary, run the following commands:

```bash theme={null}
curl -O "https://github.com/grafana/loki/releases/download/v2.7.2/loki-linux-amd64.zip"
