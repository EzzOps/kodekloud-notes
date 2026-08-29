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

In this configuration:

* The `ExecStart` directive tells systemd which command to execute to start the SSH daemon.
* `ExecReload` specifies how to reload the daemon's configuration.

To edit this service file completely, use:

```bash theme={null}
$ sudo systemctl edit --full sshd.service
```

If you need to revert your changes and return to the default settings, run:

```bash theme={null}
$ sudo systemctl revert sshd.service
```

To check the service status, including its PID, enabled state, and recent log messages, execute:

```bash theme={null}
$ sudo systemctl status sshd.service
```

A typical status output might look like:

```plaintext theme={null}
$ sudo systemctl status sshd.service
sshd.service - OpenSSH server daemon
   Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; vendor preset)
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
Dec 08 16:48:53 LFCS-CentOS sshd[1031]: Server listening on :: port 22.
Dec 08 16:48:53 LFCS-CentOS systemd[1]: Started OpenSSH server daemon.
```

<Callout icon="lightbulb">
  An enabled service will start automatically during system boot. Always check recent log messages to diagnose startup issues.
</Callout>

## Controlling Service States

Managing service states with systemd involves starting, stopping, restarting, and reloading services. The following table summarizes common commands and their use cases:

| Command | Description                               | Example                             |
| ------- | ----------------------------------------- | ----------------------------------- |
| status  | Check the current status and logs         | sudo systemctl status sshd.service  |
| start   | Start a service (if not running)          | sudo systemctl start sshd.service   |
| stop    | Stop a running service                    | sudo systemctl stop sshd.service    |
| restart | Restart the service (stop then start)     | sudo systemctl restart sshd.service |
| reload  | Reload configuration without full restart | sudo systemctl reload sshd.service  |

### Restart vs. Reload

* **Restart:** Stops and then starts the service, which may interrupt current connections.
* **Reload:** Applies configuration changes without disrupting active connections (if supported).

After any action, you should verify the status:

```bash theme={null}
$ sudo systemctl status sshd.service
```

If the configuration reload is successful, the logs may show entries such as:

```text theme={null}
Dec 08 17:26:20 LFCS-CentOS sshd[3952]: Received SIGHUP; restarting.
Dec 08 17:26:20 LFCS-CentOS systemd[1]: Reloaded OpenSSH server daemon.
```

<Callout icon="triangle-alert">
  Not all applications support a graceful reload. If a reload is not possible, systemd may perform a full restart.
</Callout>

## Enabling and Disabling Services

To control whether a service starts automatically at boot, use the following commands:

* **Disable a Service:** Prevents a service from launching on boot.

  ```bash theme={null}
  $ sudo systemctl disable sshd.service
  ```

* **Check Service Status:** Verify if the service is enabled.

  ```bash theme={null}
  $ sudo systemctl status sshd.service
  $ sudo systemctl is-enabled sshd.service
  ```

* **Enable a Service:** Ensures the service starts during boot.

  ```bash theme={null}
  $ sudo systemctl enable sshd.service
  ```

When installing a new server application, you often want to enable and start it simultaneously:

```bash theme={null}
$ sudo systemctl enable sshd.service
$ sudo systemctl start sshd.service
```

Or combine them into one step:

```bash theme={null}
$ sudo systemctl enable --now sshd.service
```

To disable plus stop a service at the same time:

```bash theme={null}
$ sudo systemctl disable --now sshd.service
```

<Callout icon="triangle-alert">
  Be cautious when disabling critical services such as the SSH daemon; doing so can lock you out of your system.
</Callout>

## Masking Services

Even after disabling a service, other components may inadvertently start it. Masking a service creates a symbolic link to /dev/null, ensuring the service can neither be started nor enabled.

To mask a service like atd (which schedules tasks), execute:

```bash theme={null}
$ sudo systemctl mask atd.service
```

Any attempt to start or enable the masked service will result in an error, as shown below:

```bash theme={null}
$ sudo systemctl enable atd.service
Failed to enable unit: Unit file /etc/systemd/system/atd.service is masked.
$ sudo systemctl start atd.service
Failed to start atd.service: Unit atd.service is masked.
```

To restore normal operations, simply unmask the service:

```bash theme={null}
$ sudo systemctl unmask atd.service
```

## Listing All Service Units

Service unit names can sometimes be confusing. For example, the Apache web server might be listed as "httpd.service" instead of "apache.service." To list all service units, regardless of their state, run:

```bash theme={null}
$ sudo systemctl list-units --type service --all
```

This command provides details like:

```text theme={null}
UNIT                                    LOAD      ACTIVE   SUB    DESCRIPTION
accounts-daemon.service                 loaded    active   running Accounts Service
alsa-restore.service                    loaded    inactive dead   Save/Restore Sound Card Settings
alsa-state.service                      loaded    active   running Manage Sound Card State
● apparmor.service                      not-found inactive dead   apparmor.service
atd.service                             loaded    active   running Job spooling tools
auditd.service                          loaded    active   running Security Auditing Service
auth-rpcgss-module.service              loaded    inactive dead   Kernel Module Supporting GSSAPI
...
```

## Conclusion

In this article, we covered how Linux manages startup processes and services using systemd. We explored service units and learned how to inspect, start, stop, reload, enable, disable, and mask services. With these tools and commands, you can manage critical applications effectively, ensuring your system remains stable.

Now it's time to put these concepts into practice in a lab environment to solidify your understanding.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/6122c847-8679-4bad-a5ba-e468f4532bdb" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/736506db-a70d-463d-a061-74c768d309b0/lesson/061c4741-156a-4dc1-ab0e-e2f6c26620dc" />
</CardGroup>


# Schedule tasks to run at a set date and time

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Deploy-Configure-and-Maintain-Systems/Schedule-tasks-to-run-at-a-set-date-and-time/page

This guide explains how to automatically schedule tasks on Linux systems using Cron, Anacron, and At for reliable process automation.

In this guide, we explain how to automatically schedule tasks on Linux systems, ensuring processes like database backups run reliably without manual intervention. You can achieve task automation using three main utilities: Cron, Anacron, and At. Each method is designed for different scheduling scenarios, and in this article, we break down their usage step by step.

***

## Cron

Cron is ideal for repetitive tasks that need to run at specific intervals—whether every few minutes, hours, or on selected days. It enables administrators to define the exact times for running automated commands.

The syntax for a cron job might appear challenging at first, but the system-wide crontab file provides excellent guidance. Located at `/etc/crontab`, this file includes comments that explain the format. Remember, instead of modifying the system-wide crontab, each user should use their personal crontab.

An excerpt from `/etc/crontab` shows the scheduling syntax:

```bash theme={null}
$ cat /etc/crontab
SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
MAILTO=root
