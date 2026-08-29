# Verify:
ls -ld /etc/prometheus /var/lib/prometheus
```

Table: directory purposes

| Path                  | Purpose                                                                                   |
| --------------------- | ----------------------------------------------------------------------------------------- |
| `/etc/prometheus`     | Prometheus configuration and consoles (`prometheus.yml`, `consoles`, `console_libraries`) |
| `/var/lib/prometheus` | TSDB (time series database) storage                                                       |

After you copy files (next steps), make sure the directories and files are owned by the prometheus user:

```bash theme={null}
sudo chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
```

***

## 3. Download and extract Prometheus

Download the Prometheus release and extract it.

```bash theme={null}
wget https://github.com/prometheus/prometheus/releases/download/v2.37.0/prometheus-2.37.0.linux-amd64.tar.gz
tar xzf prometheus-2.37.0.linux-amd64.tar.gz
cd prometheus-2.37.0.linux-amd64
```

***

## 4. Install binaries and copy supporting files

Copy the `prometheus` binary and the `promtool` CLI to `/usr/local/bin`, and copy consoles and config files into `/etc/prometheus`.

```bash theme={null}
# Move binaries
sudo cp prometheus /usr/local/bin/
sudo cp promtool /usr/local/bin/
sudo chmod 0755 /usr/local/bin/prometheus /usr/local/bin/promtool
sudo chown prometheus:prometheus /usr/local/bin/prometheus /usr/local/bin/promtool

# Copy consoles and console libraries for the web UI
sudo cp -r consoles /etc/prometheus
sudo cp -r console_libraries /etc/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus/consoles /etc/prometheus/console_libraries

# Copy the example config (rename to prometheus.yml)
sudo cp prometheus.yml /etc/prometheus/prometheus.yml
sudo chown prometheus:prometheus /etc/prometheus/prometheus.yml
sudo chmod 0644 /etc/prometheus/prometheus.yml
```

> **lightbulb** `consoles` and `console_libraries` provide optional local web UI templates. If you are not using these right away, copying them still ensures the web UI works later without additional steps.

***

## 5. Test running Prometheus as the prometheus user

You can test the exact command the systemd unit will run:

```bash theme={null}
sudo -u prometheus /usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/ \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries
```

This runs Prometheus in the foreground (for testing). When satisfied, stop it with Ctrl+C and proceed to create the systemd service.

***

## 6. Create the systemd service unit

Create `/etc/systemd/system/prometheus.service` with the contents below. This unit ensures Prometheus starts after the network is available and runs under the `prometheus` user.

```ini theme={null}
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/ \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

Explanation highlights:

* `Wants=network-online.target` and `After=network-online.target` ensure the network is up before Prometheus starts.
* `User` / `Group` set the service account; `Type=simple` is sufficient for Prometheus.
* `ExecStart` is the full command to run Prometheus with the correct paths.

You can create the file with:

```bash theme={null}
sudo vi /etc/systemd/system/prometheus.service
# (paste the unit file contents, save and exit)
```

<Frame>
  <img alt="The image shows a dark-themed command line interface titled &#x22;Prometheus Installation systemd,&#x22; with no visible content or commands displayed." />
</Frame>

***

## 7. Reload systemd, start and enable Prometheus

After adding or changing unit files, reload systemd and start the service:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl start prometheus
```

Check the status:

```bash theme={null}
sudo systemctl status prometheus
```

To ensure Prometheus starts automatically on boot:

```bash theme={null}
sudo systemctl enable prometheus
sudo systemctl is-enabled prometheus   # should print "enabled"
```

> **warning** If `systemctl status prometheus` reports failures, inspect the journal for details: `sudo journalctl -u prometheus -b`. Common issues include incorrect file paths, file ownership, or an invalid `prometheus.yml`.

***

## 8. Troubleshooting tips

* Confirm `prometheus` binary location: `which prometheus` or `ls -l /usr/local/bin/prometheus`.
* Confirm config file syntax: `promtool check config /etc/prometheus/prometheus.yml`.
* Check logs: `sudo journalctl -u prometheus -f` to tail live logs.

***

## References

* Prometheus releases: [https://github.com/prometheus/prometheus/releases](https://github.com/prometheus/prometheus/releases)
* systemd documentation: [https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/9f512f96-05d4-420d-b643-4ab94a9b5c20)


# Prometheus Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Installation/page

Guide to installing and starting Prometheus on a Linux bare-metal or VM using precompiled binaries, configuring, and verifying with the web UI and a basic PromQL query.

This guide walks through installing a Prometheus server on a Bare-Metal/VM system using the precompiled Linux binary. It covers downloading the release, extracting the archive, inspecting the directory layout, starting the server, and verifying the installation with the web UI and a simple PromQL query.

<Frame>
  <img alt="The image shows an installation instruction for Bare-Metal/VM with a download link for Prometheus and a download icon." />
</Frame>

## Overview — high level

* Download the Prometheus tarball for your OS/architecture from the official downloads page.
* Extract the tarball to get the `prometheus` binary, `promtool`, and `prometheus.yml`.
* Start the server with `./prometheus`.
* Visit the web UI at `http://<PROMETHEUS_HOST>:9090` and run a basic `up` query to confirm the server is scraping itself.

> **lightbulb** Always download the latest stable Prometheus release from the official site: [https://prometheus.io/download/](https://prometheus.io/download/). New releases include bug fixes and new features; examples in this guide use older version filenames for illustration only.

## 1) Download the Prometheus binary

Visit the Prometheus download page, select the Linux AMD64 (or the correct OS/arch), and copy the link to the tarball. You can fetch it directly on the target machine with `wget` (paste the copied URL).

Example (replace with the URL you copied):

```bash theme={null}
