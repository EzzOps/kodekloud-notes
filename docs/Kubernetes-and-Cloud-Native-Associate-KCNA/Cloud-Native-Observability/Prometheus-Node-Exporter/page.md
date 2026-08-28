# Prometheus Node Exporter

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Associate-KCNA/Cloud-Native-Observability/Prometheus-Node-Exporter/page

This guide explains how to install the Prometheus Node Exporter on a Linux host for system-level metrics collection.

This guide details how to set up the Prometheus Node Exporter on a Linux host. The Node Exporter collects system-level metrics and provides them in a format that Prometheus can scrape for monitoring.

## Step 1: Downloading the Node Exporter

Begin by visiting the official [Prometheus downloads page](https://prometheus.io/download) and selecting the Node Exporter. Choose the desired version and either download the binary directly or copy the URL for use with wget.

<Frame>
  ![The image shows instructions for downloading Node Exporter binaries, including file names, OS, architecture, size, and SHA256 checksums.](https://kodekloud.com/kk-media/image/upload/v1752880553/notes-assets/images/Kubernetes-and-Cloud-Native-Associate-KCNA-Prometheus-Node-Exporter/frame_40.jpg)
</Frame>

Once you have the URL, download the tarred file using wget. For example:

```bash theme={null}
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
```

The output should resemble:

```bash theme={null}
$ wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
HTTP request sent, awaiting response... 200 OK
Length: 9033415 (8.6M) [application/octet-stream]
Saving to: ‘node_exporter-1.3.1.linux-amd64.tar.gz’

node_exporter-1.3.1.linux-amd64.tar.gz   100%[==============================================================>]   8.61M  12.4MB/s    in 0.7s

2022-09-02 15:04:10 (12.4 MB/s) - ‘node_exporter-1.3.1.linux-amd64.tar.gz’ saved [9033415/9033415]
```

<Callout icon="lightbulb">
  Verify the file's integrity by comparing its SHA256 checksum with the one provided on the download page.
</Callout>

## Step 2: Extracting the Archive

Extract the downloaded tar file using the tar command:

```bash theme={null}
tar -xvf node_exporter-1.3.1.linux-amd64.tar.gz
```

This command creates a directory named `node_exporter-1.3.1.linux-amd64` containing the executable and additional files (LICENSE and NOTICE). Change to the directory with:

```bash theme={null}
cd node_exporter-1.3.1.linux-amd64
```

## Step 3: Running the Node Exporter

Inside the directory, start the Node Exporter by running its executable:

```bash theme={null}
./node_exporter
```

You should see output indicating that the exporter is listening on the default port 9100:

```bash theme={null}
ts=2022-09-05T16:51:59.947Z caller=node_exporter.go:115 level=info collector=vmstat
ts=2022-09-05T16:51:59.947Z caller=node_exporter.go:199 level=info msg="listening on" address=:9100
ts=2022-09-05T16:51:59.947Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
```

<Callout icon="lightbulb">
  Make sure that port 9100 is open in your firewall settings to allow Prometheus to scrape the metrics.
</Callout>

## Step 4: Verifying the Installation

To confirm that the Node Exporter is running correctly, use curl to request the metrics endpoint:

```bash theme={null}
curl localhost:9100/metrics
```

A typical response includes Prometheus-formatted metrics such as:

```plaintext theme={null}
