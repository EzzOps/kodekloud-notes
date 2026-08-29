# /usr/lib/systemd/system/sshd.service
[Unit]
Description=OpenSSH server daemon
Documentation=man:sshd(8) man:sshd_config(5)
After=network.target sshd-keygen.target
Wants=sshd-keygen.target

[Service]
Type=notify
EnvironmentFile=/etc/crypto-policies/back-ends/opensshserver.config
EnvironmentFile=-/etc/sysconfig/sshd
ExecStart=/usr/sbin/sshd -D $OPTIONS $CRYPTO_POLICY
ExecReload=/bin/kill -HUP $MAINPID
KillMode=process
Restart=on-failure
RestartSec=42s

[Install]
WantedBy=multi-user.target
```

***

## Editing and Reverting a Unit

To fully edit the `sshd.service` file:

```bash theme={null}
$ sudo systemctl edit --full sshd.service
```

To discard changes and restore the vendor-provided unit:

```bash theme={null}
$ sudo systemctl revert sshd.service
```

***

## Monitoring Service Status

Check detailed status and recent logs:

```bash theme={null}
$ sudo systemctl status sshd.service
```

Sample output:

```text theme={null}
● sshd.service - OpenSSH server daemon
   Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2021-12-08 16:48:53 CST; 15min ago
     Docs: man:sshd(8)
           man:sshd_config(5)
 Main PID: 1031 (sshd)
    Tasks: 1 (limit: 23555)
   Memory: 2.1M
  CGroup: /system.slice/sshd.service
          └─1031 /usr/sbin/sshd -D -oCiphers=aes256-gcm@openssh.com,chacha20-poly1305

Dec 08 16:48:53 LFCS-CentOS systemd[1]: Starting OpenSSH server daemon...
Dec 08 16:48:53 LFCS-CentOS sshd[1031]: Server listening on 0.0.0.0 port 22.
Dec 08 16:48:53 LFCS-CentOS systemd[1]: Started OpenSSH server daemon.
```

Press `Q` to exit.

***

## Managing Service Lifecycle

Use `systemctl` for day-to-day operations:

| Operation         | Command                                         | Description                               |
| ----------------- | ----------------------------------------------- | ----------------------------------------- |
| Start             | `sudo systemctl start sshd.service`             | Launch the service immediately            |
| Stop              | `sudo systemctl stop sshd.service`              | Stop the service                          |
| Restart           | `sudo systemctl restart sshd.service`           | Stop and then start the service           |
| Reload            | `sudo systemctl reload sshd.service`            | Reload configuration without full restart |
| Reload or Restart | `sudo systemctl reload-or-restart sshd.service` | Try reload, else restart                  |

***

## Enabling and Disabling at Boot

Control automatic startup:

```bash theme={null}
# Enable at boot
$ sudo systemctl enable sshd.service

# Disable at boot
$ sudo systemctl disable sshd.service

# Check status
$ sudo systemctl is-enabled sshd.service
```

Combine with `--now` to apply immediately:

```bash theme={null}
# Enable and start now
$ sudo systemctl enable --now sshd.service

# Disable and stop now
$ sudo systemctl disable --now sshd.service
```

<Callout icon="triangle-alert">
  Disabling and stopping `sshd.service` will prevent all SSH logins.
</Callout>

***

## Masking and Unmasking Services

Prevent any activation—manual or dependency-driven—by masking:

```bash theme={null}
$ sudo systemctl mask atd.service
```

Reverse masking:

```bash theme={null}
$ sudo systemctl unmask atd.service
```

Attempting to start a masked service results in:

```text theme={null}
Failed to enable unit: Unit file /etc/systemd/system/atd.service is masked.
Failed to start atd.service: Unit atd.service is masked.
```

***

## Listing All Service Units

View every service, regardless of state:

```bash theme={null}
$ systemctl list-units --type=service --all
```

***

## Further Reading

* [systemd.service Manual](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/b1bf2343-f406-4f20-b97f-1c5bdc245a12" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/ca5e9d7c-9dac-4ecc-9e21-dafef5ef2641/lesson/056b53be-ae53-416a-9c5f-5b9c77d5c7e6" />
</CardGroup>


# Schedule tasks to run at a set date and time

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Operation-of-Running-Systems/Schedule-tasks-to-run-at-a-set-date-and-time/page

Learn to automate routine maintenance on Linux by scheduling tasks with cron, anacron, and at utilities.

Automating routine maintenance—like database backups or log rotations—ensures a reliable Linux server. In this guide, you’ll learn how to schedule both recurring and one-off tasks using three core utilities: **cron**, **anacron**, and **at**.

<Frame>
  ![The image features an icon of an alarm clock and the text "Schedule Tasks To Run At a Set Time" on a dark background.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881491/notes-assets/images/Linux-System-Administration-for-Beginners-Schedule-tasks-to-run-at-a-set-date-and-time/alarm-clock-schedule-tasks-icon.jpg)
</Frame>

## Scheduling Utilities Overview

| Utility | Use Case                               | Configuration File or Command |
| ------- | -------------------------------------- | ----------------------------- |
| cron    | Repetitive jobs (minutes, hours, days) | `/etc/crontab` & `crontab -e` |
| anacron | Periodic jobs when system may be off   | `/etc/anacrontab`             |
| at      | One-time, non-recurring tasks          | `at <time>` / `atq` / `atrm`  |

## 1. cron

`cron` runs tasks on a fixed schedule. The system-wide crontab at `/etc/crontab` also serves as a syntax reference:

```cron theme={null}
