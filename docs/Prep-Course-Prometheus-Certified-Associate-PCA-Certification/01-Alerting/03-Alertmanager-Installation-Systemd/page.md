# Alertmanager Installation Systemd

Source: https://notes.kodekloud.com/docs/Prep-Course-Prometheus-Certified-Associate-PCA-Certification/Alerting/Alertmanager-Installation-Systemd/page

Guide to installing and configuring Prometheus Alertmanager as a systemd service, covering download, user and directory setup, binary installation, service unit creation, and startup verification.

This guide shows how to install Prometheus Alertmanager and configure it to be managed by systemd so you can start, stop, and enable it with `systemctl`.

High-level workflow:

* Download and extract Alertmanager.
* Create a dedicated `alertmanager` system user.
* Create configuration and storage directories and place the config.
* Install binaries and set correct permissions.
* Create a systemd unit file, reload systemd, and enable/start the service.

<Callout icon="lightbulb">
  This lesson uses Alertmanager v0.24.0 as an example. Replace the version in the commands if you need a newer/older release. For releases see the Alertmanager GitHub releases: [https://github.com/prometheus/alertmanager/releases](https://github.com/prometheus/alertmanager/releases)
</Callout>

Summary of important paths and settings:

|          Resource | Purpose                          | Example                                                |
| ----------------: | -------------------------------- | ------------------------------------------------------ |
|       System user | Service account for Alertmanager | `alertmanager`                                         |
|  Config directory | Alertmanager configuration       | `/etc/alertmanager/alertmanager.yml`                   |
| Storage directory | Runtime and WAL storage          | `/var/lib/alertmanager`                                |
|          Binaries | Executables on PATH              | `/usr/local/bin/alertmanager`, `/usr/local/bin/amtool` |
|      Systemd unit | Service definition               | `/etc/systemd/system/alertmanager.service`             |

## 1. Download and extract Alertmanager

Example (v0.24.0):

```bash theme={null}
wget https://github.[SECRET_REDACTED].24.0/alertmanager-0.24.0.linux-amd64.tar.gz
tar xzf alertmanager-0.24.0.linux-amd64.tar.gz
cd alertmanager-0.24.0.linux-amd64
```

You should see the extracted files, for example:

```bash theme={null}
$ ls -la
total 55752
drwxr-xr-x  2 user user    4096 Mar 25  2022 .
-rwxr--r--  1 user user     356 Mar 25  2022 alertmanager.yml
-rwxr--r--  1 user user 25067944 Mar 25  2022 amtool
-rwxr--r--  1 user user 20542176 Mar 25  2022 alertmanager
-rw-r--r--  1 user user     457 Mar 25  2022 LICENSE
-rw-r--r--  1 user user     166 Mar 25  2022 NOTICE
```

## 2. Create a dedicated system user

Create a non-login system user to run Alertmanager:

```bash theme={null}
sudo useradd --no-create-home --system --shell /bin/false alertmanager
```

Using `--system` is recommended for service accounts; it keeps user IDs in the system range.

## 3. Create configuration and storage directories

Create the config and storage directories, copy the shipped config into place, and set ownership to the `alertmanager` user:

```bash theme={null}
sudo mkdir -p /etc/alertmanager
sudo mkdir -p /var/lib/alertmanager
