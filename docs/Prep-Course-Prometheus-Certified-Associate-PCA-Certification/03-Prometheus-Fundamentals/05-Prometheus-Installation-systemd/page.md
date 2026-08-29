# From inside the extracted prometheus-<version>.linux-amd64 directory:
sudo cp prometheus /usr/local/bin/
sudo cp promtool /usr/local/bin/
sudo chmod 0755 /usr/local/bin/prometheus /usr/local/bin/promtool
```

Step 4 — Install console files and the configuration file
Copy the default `consoles` and `console_libraries` directories and the `prometheus.yml` configuration file into `/etc/prometheus`. Ensure the `prometheus` user owns everything under `/etc/prometheus`:

```bash theme={null}
# Copy consoles and libraries
sudo cp -r consoles /etc/prometheus/
sudo cp -r console_libraries /etc/prometheus/

# Copy the default config (adjust path if your prometheus.yml is elsewhere)
sudo cp prometheus.yml /etc/prometheus/

# Ensure prometheus owns everything under /etc/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus
```

Step 5 — Create the systemd service unit
Create the systemd unit file at `/etc/systemd/system/prometheus.service` with the following contents. This unit runs Prometheus as the `prometheus` user and points Prometheus to the configuration and storage paths we created above:

```ini theme={null}
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus --config.file=/etc/prometheus/prometheus.yml --storage.tsdb.path=/var/lib/prometheus/ --web.console.templates=/etc/prometheus/consoles --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

> **lightbulb** Systemd unit filenames and unit names are case-sensitive. Use the lowercase unit name when running `systemctl` (for example: `prometheus.service` or `prometheus`).

Step 6 — Reload systemd, start, enable, and verify
Reload systemd to pick up the new unit, then start and enable the service so it runs on boot. Check the service status and logs if needed:

```bash theme={null}
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus
sudo systemctl status prometheus --no-pager
```

A healthy service will show `Active: active (running)` in the status output. If you see errors, inspect recent logs:

```bash theme={null}
# View recent logs for the Prometheus service
sudo journalctl -u prometheus --no-pager -n 100
```

Quick reference table

| Action             | Command / File                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------- |
| Create system user | `sudo useradd --no-create-home --system --shell /usr/sbin/nologin --home-dir /nonexistent prometheus` |
| Config directory   | `/etc/prometheus`                                                                                     |
| Data directory     | `/var/lib/prometheus`                                                                                 |
| Install binaries   | `sudo cp prometheus promtool /usr/local/bin/`                                                         |
| Systemd unit file  | `/etc/systemd/system/prometheus.service`                                                              |
| Start & enable     | `sudo systemctl start prometheus && sudo systemctl enable prometheus`                                 |
| Logs               | `sudo journalctl -u prometheus -n 100`                                                                |

Verification
Open your browser and go to: [http://localhost:9090](http://localhost:9090) — this is the default Prometheus web UI. If you are running Prometheus on a remote host, replace `localhost` with the host IP or domain and ensure any firewall rules allow access to port `9090`.

Troubleshooting tips

* Verify paths in the systemd unit match where you copied the binaries and config (`/usr/local/bin/prometheus`, `/etc/prometheus/prometheus.yml`, `/var/lib/prometheus`).
* Ensure directory ownership: `/etc/prometheus` and `/var/lib/prometheus` must be owned by the `prometheus` user.
* Use `sudo journalctl -u prometheus` to inspect logs for startup errors: [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.html)
* If Prometheus fails to bind to port 9090, ensure no other process is using that port and that firewall rules permit access.

> **warning** Always download Prometheus binaries from the official releases page: [https://prometheus.io/download/](https://prometheus.io/download/). Verify checksums for the tarball if available to avoid installing tampered binaries.

Links and references

* Prometheus downloads: [https://prometheus.io/download/](https://prometheus.io/download/)
* systemd overview: [https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)
* systemctl manual: [https://www.freedesktop.org/software/systemd/man/systemctl.html](https://www.freedesktop.org/software/systemd/man/systemctl.html)
* journalctl manual: [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/e03e8702-ef6c-4402-b626-4437fc40b513/lesson/597bc552-f9de-4d23-b908-5a4148626197)


# Prometheus Installation systemd

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Prometheus-Fundamentals/Prometheus-Installation-systemd/page

Guide to install and configure Prometheus as a systemd service including user setup, directories, binaries, unit file, and enabling at boot

Running Prometheus directly from the terminal (for example, `./prometheus`) launches it in the foreground. If you close that terminal, Prometheus stops. It also won't start automatically after a reboot. To run Prometheus like any other long‑running service — in the background and enabled at boot — create a dedicated systemd unit and a system user that owns the Prometheus files.

This guide walks through:

* creating a system user and directories
* installing the Prometheus binaries and configuration
* creating a systemd unit file
* starting and enabling the service

***

## 1. Create a Prometheus user

Create a system user that cannot log in interactively. This user will own and run the Prometheus process.

```bash theme={null}
sudo useradd --no-create-home --shell /bin/false prometheus
```

> **lightbulb** Using `--no-create-home` and `/bin/false` prevents shell login for the prometheus user. This is a security best practice for service accounts.

***

## 2. Create directories and set permissions

Create directories for configuration and time series storage, then assign ownership to the `prometheus` user and group.

```bash theme={null}
sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
