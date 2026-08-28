# Example: change into the extracted node_exporter directory
cd node_exporter-*/    # adjust to your extracted folder name
```

2. Copy the node\_exporter binary to `/usr/local/bin`:

```bash theme={null}
sudo cp node_exporter /usr/local/bin/
sudo chmod 0755 /usr/local/bin/node_exporter
```

3. Create a dedicated user for running node\_exporter:

```bash theme={null}
# Create a system user without a login shell and without creating a home directory
sudo useradd --no-create-home --shell /usr/sbin/nologin --system node_exporter
```

4. Make the node\_exporter binary owned by the node\_exporter user:

```bash theme={null}
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

<Callout icon="lightbulb">
  It's good practice to run exporters as a non-privileged, system user (no shell and no home). This reduces the blast radius if the exporter is compromised.
</Callout>

5. Create the systemd service unit at `/etc/systemd/system/node_exporter.service`. The unit tells systemd to wait for the network to be online before starting the service and ensures it becomes part of the normal multi-user startup:

```ini theme={null}
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

6. Reload systemd to pick up the new unit, start the service, and enable it at boot:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
```

7. Verify the service is running:

```bash theme={null}
sudo systemctl status node_exporter
```

You should see an active (running) state in the status output.

8. Confirm node\_exporter is exposing metrics (default port 9100) by curling the metrics endpoint:

```bash theme={null}
curl http://localhost:9100/metrics
```

You should see plain-text Prometheus metrics returned. Prometheus can now be configured to scrape this target (add `localhost:9100` or the appropriate host:port to your Prometheus scrape targets).

That’s all — node\_exporter is now managed by systemd, runs as a dedicated user, and will start automatically on boot.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/73d167e2-f9bc-4d37-97b6-897fdb184b85" />
</CardGroup>


# Node Exporter

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Node-Exporter/page

Guide to installing and configuring Prometheus Node Exporter to expose Linux system metrics for Prometheus scraping, including examples, security tips, and service setup.

Node Exporter is the standard Prometheus exporter for collecting hardware- and OS-level metrics from Linux hosts. It exposes CPU, memory, disk, network, kernel, and many other system metrics on an HTTP endpoint that Prometheus can scrape.

To install Node Exporter, download the appropriate binary for your OS/architecture from the Prometheus downloads page and run it on the host you want to monitor. Always choose the latest stable release compatible with your environment.

<Frame>
  <img alt="The image shows instructions for installing Node Exporter with a section of downloadable binaries for different operating systems and architectures. It includes a menu option for copying the URL." />
</Frame>

<Callout icon="lightbulb">
  Download the Node Exporter binary that matches your OS/architecture. Optionally verify the SHA256 checksum listed on the release page with `sha256sum` before extracting the archive.
</Callout>

## Quick install (Linux example)

1. Copy the download URL for the Node Exporter release that matches your architecture.
2. Download the tarball with `wget` (or `curl`).
3. Extract and run the binary.

Example commands:

```bash theme={null}
