# Copy the provided config file into place
sudo cp alertmanager.yml /etc/alertmanager/alertmanager.yml

# Ensure the directories and files are owned by the alertmanager user
sudo chown -R alertmanager:alertmanager /etc/alertmanager
sudo chown -R alertmanager:alertmanager /var/lib/alertmanager
```

<Callout icon="warning">
  Be careful with `chown -R` — do NOT run `sudo chown -R alertmanager:alertmanager /etc/` or similarly broad commands. Target only `/etc/alertmanager` (and other specific directories) to avoid damaging system ownerships.
</Callout>

## 4. Install the binaries

Copy the `alertmanager` binary and the `amtool` helper to a directory on PATH, set execute permissions, and set ownership:

```bash theme={null}
sudo cp alertmanager /usr/local/bin/alertmanager
sudo cp amtool /usr/local/bin/amtool

sudo chmod 0755 /usr/local/bin/alertmanager /usr/local/bin/amtool
sudo chown root:root /usr/local/bin/alertmanager /usr/local/bin/amtool
```

Notes:

* Keeping the binaries owned by `root` and world-executable is common and safe; the process will run as the `alertmanager` user when started by systemd.
* If you prefer, you can set ownership to `alertmanager:alertmanager`, but `root:root` is typical.

## 5. Create the systemd service unit

Create `/etc/systemd/system/alertmanager.service` with the following content:

```ini theme={null}
[Unit]
Description=Alertmanager Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=alertmanager
Group=alertmanager
ExecStart=/usr/local/bin/alertmanager \
    --config.file=/etc/alertmanager/alertmanager.yml \
    --storage.path=/var/lib/alertmanager
Restart=always

[Install]
WantedBy=multi-user.target
```

Key points:

* `--config.file` points to your Alertmanager config (`/etc/alertmanager/alertmanager.yml`).
* `--storage.path` sets the data directory (`/var/lib/alertmanager`).
* The unit runs the process as `alertmanager:alertmanager`.

After creating the unit file, reload systemd so it recognizes the new service:

```bash theme={null}
sudo systemctl daemon-reload
```

## 6. Start, enable, and verify the service

Start and enable the service so it runs on boot:

```bash theme={null}
sudo systemctl start alertmanager
sudo systemctl enable alertmanager
```

Check status and follow logs:

```bash theme={null}
sudo systemctl status alertmanager
sudo journalctl -u alertmanager -f
```

Troubleshooting checklist:

* Validate that `/etc/alertmanager/alertmanager.yml` is valid YAML (use a linter or `amtool check-config` if available).
* Confirm ownership and permissions: the `alertmanager` user must be able to read the config and write to `/var/lib/alertmanager`.
* Inspect `journalctl` output for startup errors and missing flags or permission issues.

## Reference: Example final systemd unit

For convenience, here is the final unit again:

```ini theme={null}
[Unit]
Description=Alertmanager Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=alertmanager
Group=alertmanager
ExecStart=/usr/local/bin/alertmanager \
    --config.file=/etc/alertmanager/alertmanager.yml \
    --storage.path=/var/lib/alertmanager
Restart=always

[Install]
WantedBy=multi-user.target
```

Congratulations — Alertmanager should now be installed and managed by systemd.

Links and references:

* Alertmanager releases: [https://github.com/prometheus/alertmanager/releases](https://github.com/prometheus/alertmanager/releases)
* Alertmanager documentation: [https://prometheus.io/docs/alerting/latest/alertmanager/](https://prometheus.io/docs/alerting/latest/alertmanager/)
* systemd documentation: [https://www.freedesktop.org/wiki/Software/systemd/](https://www.freedesktop.org/wiki/Software/systemd/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/eb7ae2f0-0d55-4789-af61-fdf337265d10" />

  <Card title="Practice Lab" icon="flask-conical" href="https://learn.kodekloud.com/user/courses/prometheus-certified-associate-pca/module/499d9ac5-c2e0-43fe-b000-f08f33fbf2dc/lesson/fbd1026a-cd0c-4ebf-89bb-4182630754ba" />
</CardGroup>


# Alertmanager Installation

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Alerting/Alertmanager-Installation/page

Guide to download, install, run, and configure Alertmanager and integrate it with Prometheus for alert delivery and basic troubleshooting.

This guide walks through installing Alertmanager, starting the service, and configuring Prometheus to send alerts to it. The steps assume a Linux host with wget and tar available.

## Download Alertmanager

1. Open the Prometheus downloads page and locate the Alertmanager section to copy the direct URL for the binary you need:
   * Prometheus downloads: [https://prometheus.io/download/](https://prometheus.io/download/)

2. On the Alertmanager server, download and extract the archive:

```bash theme={null}
