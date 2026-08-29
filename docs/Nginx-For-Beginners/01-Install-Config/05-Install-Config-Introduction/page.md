# Allow SSH and HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 443/tcp

# Enable UFW
sudo ufw enable

# Reload rules (when necessary)
sudo ufw reload

# View rules with numbers (useful for deleting)
sudo ufw status numbered

# Delete a rule by its number (after checking the numbered list)
sudo ufw delete <rule-number>
sudo ufw reload
```

Notes:

* Use `sudo ufw status numbered` to see rule indices and remove rules safely.
* UFW is deliberately simple — it’s suitable for host-level firewalling and quick rule management.

Managing Firewalld (Red Hat / Fedora / CentOS)

If Firewalld is not installed, use your package manager to install and then start and enable it for boot persistence. Use `firewall-cmd` with `--permanent` for persistent rules, then `--reload` to apply them immediately.

Common Firewalld commands:

```bash theme={null}
# Install (example using yum) and ensure running
sudo yum update && sudo yum install -y firewalld
sudo systemctl enable --now firewalld

# Add HTTPS (port 443) permanently and reload
sudo firewall-cmd --permanent --add-port=443/tcp
sudo firewall-cmd --reload

# Remove HTTPS and reload
sudo firewall-cmd --permanent --remove-port=443/tcp
sudo firewall-cmd --reload

# View current configuration (runtime)
sudo firewall-cmd --list-all
```

Notes:

* `--permanent` changes the persistent configuration; `--reload` applies changes to the running runtime.
* You can enable and start Firewalld in one command with `sudo systemctl enable --now firewalld`.

Quick comparison: UFW vs Firewalld

| Feature         | UFW (Debian/Ubuntu)  | Firewalld (RHEL/Fedora/CentOS)                |
| --------------- | -------------------- | --------------------------------------------- |
| Typical command | `ufw allow 443/tcp`  | `firewall-cmd --permanent --add-port=443/tcp` |
| View rules      | `ufw status`         | `firewall-cmd --list-all`                     |
| Ease of use     | Simple, host-focused | Flexible zones and rich rules                 |

Inspecting listening ports with netstat / ss

Tools like `netstat` (from net-tools) or `ss` (from iproute2) show which services are actually listening on ports — they do not show firewall rules.

Install `net-tools` if needed:

```bash theme={null}
# Debian/Ubuntu
sudo apt update && sudo apt install -y net-tools

# Red Hat/Fedora/CentOS
sudo yum install -y net-tools
```

List listening sockets:

```bash theme={null}
# Using netstat
sudo netstat -nltup

# Equivalent using ss (preferred on modern systems)
sudo ss -nltup
```

Explanation of options:

* `-n` show numeric addresses/ports
* `-l` show listening sockets
* `-t` show TCP
* `-u` show UDP
* `-p` show PID/program name

Important distinctions:

* `netstat` / `ss` show which services are bound to ports (i.e., listening). If no service is listening on a port, opening that port in the firewall does not make the service available.
* Firewall tools (UFW / Firewalld) control whether packet flows can reach those services. Both pieces must be configured correctly for a service to be reachable from the network.

Useful links and references

* UFW documentation: [https://help.ubuntu.com/community/UFW](https://help.ubuntu.com/community/UFW)
* Firewalld documentation: [https://firewalld.org/documentation/](https://firewalld.org/documentation/)
* netstat / ss references: `man netstat`, `man ss`
* General Linux firewall concepts: [https://www.kernel.org/doc/html/latest/networking/index.html](https://www.kernel.org/doc/html/latest/networking/index.html)

You can run the commands shown above to confirm which ports your services are listening on and which ports are allowed by your firewall.

- [Watch Video](https://learn.kodekloud.com/user/courses/nginx-for-beginners/module/0de43784-b08d-4ce0-8470-a7541b78fe58/lesson/4ff8592e-fd7b-4f7f-9a35-39994c529479)


# Install Config Introduction

Source: https://notes.kodekloud.com/docs/Nginx-For-Beginners/Install-Config/Install-Config-Introduction/page

Guide to installing, configuring, and managing Nginx across platforms, covering package managers, service commands, nginx.conf structure, hosting static sites, and basic firewall rules.

This lesson covers the essentials for installing, configuring, and managing Nginx. You'll learn:

* How package managers work and which to use on common platforms.
* How to install Nginx on Ubuntu (primary), plus CentOS, macOS, and Windows.
* How to manage Nginx as a service (status, start, stop, restart, reload).
* How the `nginx.conf` file is structured and how configuration is inherited.
* How to host a simple static website with Nginx and allow traffic via UFW.

<Frame>
  <img alt="A presentation slide titled &#x22;Objectives&#x22; listing three goals: understand package managers, install Nginx on Ubuntu/CentOS/macOS/Windows, and manage Nginx services (status, start, stop, reload, restart)." />
</Frame>

***

## Package managers: overview and quick comparison

Package managers automate installing, upgrading, configuring, and removing software. Below are common examples and typical use cases:

| Package manager                                                        |          Platform(s) | Typical commands                                     |
| ---------------------------------------------------------------------- | -------------------: | ---------------------------------------------------- |
| [`apt`](https://wiki.debian.org/Apt)                                   |       Debian, Ubuntu | `sudo apt update` / `sudo apt install nginx`         |
| [`yum`](https://en.wikipedia.org/wiki/YUM_\(package_manager\)) / `dnf` | CentOS, RHEL, Fedora | `sudo yum install nginx` or `sudo dnf install nginx` |
| [Homebrew](https://brew.sh)                                            |                macOS | `brew install nginx`                                 |
| Chocolatey / WSL                                                       |              Windows | `choco install nginx` (or run Nginx inside WSL)      |

Use the package manager native to your OS for the smoothest installation and updates.

> **lightbulb** When choosing where to run Nginx on Windows, prefer WSL (Windows Subsystem for Linux) for a Linux-like experience and easier parity with production Linux servers.

***

## Install Nginx — quick commands by platform

Below are concise, platform-specific instructions. These are the most common, production-friendly approaches.

Ubuntu (Debian-family)

```bash theme={null}
sudo apt update
sudo apt install -y nginx
