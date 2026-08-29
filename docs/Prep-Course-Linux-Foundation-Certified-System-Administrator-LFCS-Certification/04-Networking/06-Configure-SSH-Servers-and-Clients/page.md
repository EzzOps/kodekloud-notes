# Configure SSH Servers and Clients

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Networking/Configure-SSH-Servers-and-Clients/page

This article covers the configuration and management of SSH servers and clients for secure remote access to Linux systems.

Managing remote Linux servers securely requires both an SSH client on your local machine and an SSH daemon (server) running on the remote system. The SSH daemon listens for and accepts connection requests from the SSH client. Most Linux distributions come with the OpenSSH daemon pre-installed, so let's review its configuration and best practices.

## SSH Server Configuration

The primary configuration file for the SSH daemon is located at `/etc/ssh/sshd_config` (note the "d" indicating the daemon). To modify its settings, use your preferred text editor. For example:

```bash theme={null}
sudo vim /etc/ssh/sshd_config
```

In contrast, the SSH client configuration file is found at `/etc/ssh/ssh_config` (without the "d"). Be sure not to confuse these two files when adjusting settings:

```bash theme={null}
sudo vim /etc/ssh/ssh_config
```

Since Linux installations typically include both the SSH client and daemon, understanding the distinct configuration files is essential.

### Key Settings in /etc/ssh/sshd\_config

When you open `/etc/ssh/sshd_config`, you might see content similar to the following:

```bash theme={null}
