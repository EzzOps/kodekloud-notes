# This is the sshd server system-wide configuration file. See
# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented. Uncommented options override the
Include /etc/ssh/sshd_config.d/*.conf

#Port 123
AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::

#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
#HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers and keying
#RekeyLimit default none

# Logging
#SyslogFacility AUTH
```

The first critical parameter is the port number. By default, the port is commented out (with a default value of 22). To change this value, simply uncomment the line and specify your desired port. The `AddressFamily any` option allows both IPv4 and IPv6 connections. If you wish to restrict connections, you can set `AddressFamily inet` (IPv4) or `AddressFamily inet6` (IPv6).

For example, if your server has two IP addresses—203.0.113.1 (public) and 10.11.12.9 (internal)—and you want SSH access only through the internal network, configure it like below:

```bash theme={null}
# This is the sshd server system-wide configuration file.  See
# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented. Uncommented options override the
# default value.
Include /etc/ssh/sshd_config.d/*.conf

#Port 22
AddressFamily inet
ListenAddress 10.11.12.9
#ListenAddress ::
  
#HostKey /etc/ssh/ssh_host_rsa_key
#HostKey /etc/ssh/ssh_host_ecdsa_key
#HostKey /etc/ssh/ssh_host_ed25519_key

# Ciphers and keying
#RekeyLimit default none
# Logging
#SyslogFacility AUTH
```

Another commonly modified setting is `PermitRootLogin`. By default, this is often set to `prohibit-password`, meaning root login is allowed only via key-based authentication. To entirely disable root login, change the value to `no`. See this example configuration block that disables root login and defines authentication protocols:

```bash theme={null}
# Ciphers and keying
#RekeyLimit default none

# Logging
#SyslogFacility AUTH
#LogLevel INFO

# Authentication:
#LoginGraceTime 2m
PermitRootLogin no
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

#PubkeyAuthentication yes
# Expect .ssh/authorized_keys2 to be disregarded by default in future.
#AuthorizedKeysFile .ssh/authorized_keys .ssh/authorized_keys2

#AuthorizedPrincipalsFile none
#AuthorizedKeysCommand none
#AuthorizedKeysCommandUser nobody

# For this to work you will also need host keys in /etc/ssh/ssh_known_hosts
#HostbasedAuthentication no
```

SSH supports various authentication methods. The two most common methods are password authentication and SSH key-based authentication. Disabling both `PasswordAuthentication` and `KbdInteractiveAuthentication` ensures that only key-based authentication is allowed for heightened security. Consider this snippet:

```bash theme={null}
#HostbasedAuthentication no
# Change to yes if you don't trust ~/.ssh/known_hosts for
# HostbasedAuthentication
#IgnoreUserKnownHosts no
# Don't read the user's ~/.rhosts and ~/.shosts files
#IgnoreRhosts yes

# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication no
#PermitEmptyPasswords no

# Change to yes to enable challenge-response passwords (beware issues with
# some PAM modules and threads)
KbdInteractiveAuthentication no

# Kerberos options
#KerberosAuthentication no
#KerberosOrLocalPasswd yes
#KerberosTicketCleanup yes
#KerberosGetAFSToken no
```

Disabling these authentication methods forces users to adopt the more secure SSH key-based authentication. Additional options include X11 forwarding and other global settings:

```bash theme={null}
UsePAM yes

#AllowAgentForwarding yes
#AllowTcpForwarding yes
#GatewayPorts no
X11Forwarding yes
#X11DisplayOffset 10
#X11UseLocalhost yes
#PermitTTY yes
PrintMotd no
#PrintLastLog yes
#TCPKeepAlive yes
#PermitUserEnvironment no
#Compression delayed
ClientAliveInterval 0
ClientAliveCountMax 3
#UseDNS no
#PidFile /run/sshd.pid
```

### Per-User Overrides

Global settings apply to all users, but you can create exceptions for specific users. For instance, if password authentication is globally disabled and you want to allow it for a specific user such as "anoncvs" (or even a user like "aaron"), add a per-user configuration block at the end of the file:

```bash theme={null}
# Example of overriding settings on a per-user basis
Match User anoncvs
    PasswordAuthentication yes
    #
    # X11Forwarding no
    # AllowTcpForwarding no
    # PermitTTY no
    # ForceCommand cvs server
```

<Callout icon="lightbulb">
  After modifying the configuration file, reload the SSH daemon for changes to take effect:

  sudo systemctl reload ssh.service
</Callout>

Also, be aware that additional configuration files in the `/etc/ssh/sshd_config.d/` directory can override settings from the main file. For example, a file like `/etc/ssh/sshd_config.d/50-cloud-init.conf` may contain `PasswordAuthentication yes`, which re-enables password authentication even if disabled in the main configuration file. List and inspect these files with:

```bash theme={null}
ls /etc/ssh/sshd_config.d
sudo cat /etc/ssh/sshd_config.d/50-cloud-init.conf
```

## SSH Client Configuration

The SSH client is used to connect to remote servers and is available on Windows 10, macOS, and Linux. When you execute the `ssh` command, it opens a text-based application to establish a connection.

User-specific SSH client files are stored in the `.ssh` directory in each user's home folder. For example, for user "jeremy" on a Unix-like system:

```bash theme={null}
ls -la ~/.ssh
```

On Windows, the equivalent directory is:

C:\Users\Jeremy.ssh

Although no default local SSH client configuration file exists, you can create one manually. The global client configuration file is `/etc/ssh/ssh_config`, where default values are commented out. Here’s an example snippet from that file:

```bash theme={null}
Host *
    ForwardAgent no
    ForwardX11 no
    ForwardX11Trusted yes
    PasswordAuthentication yes
    HostbasedAuthentication no
    GSSAPIAuthentication no
    GSSAPIDelegateCredentials no
    GSSAPIKeyExchange no
    GSSAPITestDNS no
    BatchMode no
    CheckHostIP no
    AddressFamily any
    ConnectTimeout 0
    StrictHostKeyChecking ask
    IdentityFile ~/.ssh/id_rsa
    IdentityFile ~/.ssh/id_dsa
    IdentityFile ~/.ssh/id_ecdsa
    IdentityFile ~/.ssh/id_ed25519
    Port 22
    Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc
    MACs hmac-md5,hmac-sha1,umac-64@openssh.com
    EscapeChar ~
    Tunnel no
    TunnelDevice any:any
    PermitLocalCommand no
    VisualHostKey no
```

If your internal network uses a non-standard port (such as 229), update the configuration accordingly. Since global file modifications might be overwritten during updates, a better practice is to add a custom file in `/etc/ssh/ssh_config.d/`. For example, to set the default port globally, create or edit the file with:

```bash theme={null}
Host *
    Port 229
    Ciphers aes128-ctr,aes192-ctr,aes256-ctr,aes128-cbc,3des-cbc
    MACs hmac-md5,hmac-sha1,umac-64@openssh.com
    EscapeChar ~
    Tunnel no
    TunnelDevice any:any
    PermitLocalCommand no
    VisualHostKey no
```

Users can also configure host-specific settings by creating a file named `config` in the `~/.ssh` directory. This file allows you to define host aliases and custom connection parameters. For example:

1. Create and edit the user-specific configuration file:

   ```bash theme={null}
   vim ~/.ssh/config
   ```

2. Add an entry similar to the one below (replace the IP address and username as needed):

   ```text theme={null}
   Host ubuntu-vm
       HostName 10.0.0.186
       User jeremy
   ```

3. Secure the file by setting its permissions:

   ```bash theme={null}
   chmod 600 ~/.ssh/config
   ```

You can now use the alias to connect to your server:

```bash theme={null}
ssh ubuntu-vm
```

On your first connection, you will be prompted to verify the server’s fingerprint.

## Using SSH Keys Instead of Passwords

SSH keys provide stronger security compared to password-based authentication. To generate an SSH key pair on your local machine, run:

```bash theme={null}
ssh-keygen
```

Accept all defaults by pressing Enter at each prompt. (For enhanced security, you may set a passphrase; however, in this example, no passphrase is provided.)

This process creates a private key (e.g., `id_ed25519`) and a public key (`id_ed25519.pub`). To use SSH key-based authentication, copy the public key to your server using the `ssh-copy-id` command:

```bash theme={null}
ssh-copy-id jeremy@10.0.0.173
```

The output will be similar to the following:

```bash theme={null}
jeremy@kodekloud:~$ ssh-copy-id jeremy@10.0.0.173
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/jeremy/.ssh/id_ed25519.pub"
The authenticity of host '10.0.0.173 (10.0.0.173)' can't be established.
ED25519 key fingerprint is SHA256:4jhBsfInTkw9PyPlBIfnWg+n+L19sWQM4TS6IX5YmA.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
jeremy@10.0.0.173's password:
Number of key(s) added: 1
Now try logging into the machine, with:  "ssh 'jeremy@10.0.0.173'"
and check to make sure that only the key(s) you wanted were added.
```

After copying the key, test the connection:

```bash theme={null}
ssh jeremy@10.0.0.173
```

If `ssh-copy-id` is unavailable, you can manually append the contents of `id_ed25519.pub` to the server's `~/.ssh/authorized_keys` file and secure it:

```bash theme={null}
chmod 600 ~/.ssh/authorized_keys
```

## Managing Known Hosts

The first time you connect to a new server, SSH prompts you to confirm the server's fingerprint and stores this information in `~/.ssh/known_hosts`. On subsequent connections, SSH verifies the fingerprint to ensure that you are connecting to the trusted server. If the server’s fingerprint changes—perhaps because of a server reinstall—you may encounter a warning message.

To remove a specific fingerprint (e.g., for IP 10.0.0.251), use:

```bash theme={null}
ssh-keygen -R 10.0.0.251
```

If necessary, you can also delete the entire `known_hosts` file to clear all stored fingerprints.

***

## Diagrams and Further Details

The following diagrams provide a visual representation of SSH configuration and authentication settings:

<Frame>
  ![The image shows a section of a manual page for SSHD configuration, detailing authentication methods and settings like "password," "publickey," and "AuthorizedKeysCommand."](https://kodekloud.com/kk-media/image/upload/v1752881308/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Configure-SSH-Servers-and-Clients/sshd-configuration-authentication-methods.jpg)
</Frame>

<Frame>
  ![The image shows a section of a manual page for SSHD configuration, detailing settings for password authentication, empty passwords, and TCP port forwarding permissions.](https://kodekloud.com/kk-media/image/upload/v1752881309/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Configure-SSH-Servers-and-Clients/sshd-configuration-manual-settings.jpg)
</Frame>

***

This concludes the article on configuring SSH servers and clients. By understanding and applying these settings, you can securely manage and maintain remote systems using either password or, preferably, SSH key-based authentication.

For more comprehensive guides on SSH and Linux server management, consider visiting [Kubernetes Documentation](https://kubernetes.io/docs/) or browsing [Docker Hub](https://hub.docker.com/).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/2ba92913-296b-481d-af2d-6710bf3f7cdd/lesson/9031622f-a6e7-45a5-bd5a-3bfe5486774c" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/2ba92913-296b-481d-af2d-6710bf3f7cdd/lesson/aa45ff2b-80fc-4f74-8048-a8076be7c85d" />
</CardGroup>


# Implement Reverse Proxies and Load Balancers

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Networking/Implement-Reverse-Proxies-and-Load-Balancers/page

This article explains how to set up reverse proxies and load balancers using Nginx for efficient web server management.

In this lesson, we explore how to set up reverse proxies and load balancers for your web servers. When you visit popular websites such as [KodeKloud.com](https://kodekloud.com) or [YouTube.com](https://www.youtube.com), the displayed content is served by a robust infrastructure rather than a single web server. By using a reverse proxy, you can seamlessly route user requests to the appropriate backend server, while load balancing evenly distributes the traffic to prevent any one server from becoming overloaded.

## What Is a Reverse Proxy?

A reverse proxy acts as an intermediary between client requests and the backend web server. Rather than the client directly communicating with the web server, the reverse proxy intercepts the request and forwards it. The typical flow is as follows:

1. The user sends a request to the reverse proxy.
2. The reverse proxy forwards the request to the designated web server.
3. The web server processes the request and sends the response back to the reverse proxy.
4. Finally, the reverse proxy relays the response to the user.

<Frame>
  ![The image illustrates the concept of a reverse proxy, showing the interaction between a user (web browser), a reverse proxy, and a web server. The user requests a web page, which is relayed by the reverse proxy to the web server.](https://kodekloud.com/kk-media/image/upload/v1752881309/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Implement-Reverse-Proxies-and-Load-Balancers/reverse-proxy-user-web-server.jpg)
</Frame>

This setup provides several advantages. For instance, if you deploy a new web server with enhanced resources like increased RAM and CPU power, you can quickly transition traffic by simply updating your reverse proxy configuration. This method avoids the delays associated with DNS propagation in a direct update scenario.

<Frame>
  ![The image illustrates the concept of a reverse proxy, showing the interaction between a user (web browser), a reverse proxy, and a web server, with arrows indicating the flow of web page requests and responses.](https://kodekloud.com/kk-media/image/upload/v1752881310/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Implement-Reverse-Proxies-and-Load-Balancers/reverse-proxy-user-interaction-diagram.jpg)
</Frame>

Another visual example:

<Frame>
  ![The image is a diagram explaining how a reverse proxy works, showing the interaction between a user, a reverse proxy, and two web servers (old and new).](https://kodekloud.com/kk-media/image/upload/v1752881312/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Implement-Reverse-Proxies-and-Load-Balancers/reverse-proxy-diagram-user-servers.jpg)
</Frame>

Reverse proxies not only offer rapid traffic redirection; they can also filter web traffic, cache pages for faster delivery, and perform additional optimizations. These capabilities lay the groundwork for efficient load balancing.

## Load Balancing Basics

Load balancing distributes incoming web requests across multiple servers, ensuring that no single server becomes overwhelmed. For example, by directing requests to the least busy server, load balancing maintains an even distribution of processing tasks. This method is crucial for high-traffic sites like [YouTube.com](https://www.youtube.com) where a single server cannot handle millions of requests simultaneously.

Multiple images in this lesson further emphasize these key concepts:

<Frame>
  ![The image explains what a reverse proxy is, highlighting its advantages such as filtering web traffic and caching pages.](https://kodekloud.com/kk-media/image/upload/v1752881313/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Implement-Reverse-Proxies-and-Load-Balancers/reverse-proxy-advantages-filtering-caching.jpg)
</Frame>

<Frame>
  ![The image illustrates how a load balancer distributes web page requests from a user to multiple web servers, ensuring efficient handling of traffic.](https://kodekloud.com/kk-media/image/upload/v1752881314/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Implement-Reverse-Proxies-and-Load-Balancers/load-balancer-web-servers-traffic.jpg)
</Frame>

When the load balancer smartly assigns inbound requests, it may choose the server with the fewest active connections, thereby maintaining an even workload across all servers.

## Setting Up a Reverse Proxy with Nginx

Nginx is a popular solution for configuring reverse proxies due to its high performance and versatility. Although alternatives like HAProxy and Apache exist, Nginx remains a top choice for many users.

### Step 1: Install Nginx and Create the Reverse Proxy Configuration

Begin by installing Nginx and then creating a configuration file (in this example, "proxy.conf") within the `/etc/nginx/sites-available` directory.

```bash theme={null}
sudo apt install nginx
sudo vim /etc/nginx/sites-available/proxy.conf
```

Inside this configuration file, add the following settings. The server block instructs Nginx to listen on port 80, and the `location /` block specifies that requests matching the root URL should be proxied to the target web server (here, represented by IP address 1.1.1.1):

```nginx theme={null}
server {
    listen 80;
    location / {
        proxy_pass http://1.1.1.1;
    }
}
```

If you wish to proxy only specific parts of your website, such as URLs beginning with `/images`, modify the configuration accordingly:

```nginx theme={null}
server {
    listen 80;
    location /images {
        proxy_pass http://1.1.1.1;
    }
}
```

For cases where the target web server listens on a non-default port, include the port number in the `proxy_pass` directive:

```nginx theme={null}
server {
    listen 80;
    location /images {
        proxy_pass http://1.1.1.1:8081;
    }
}
```

To pass along the original request details—like the user’s IP address and protocol—the `proxy_params` file can be included:

```nginx theme={null}
server {
    listen 80;
    location /images {
        proxy_pass http://1.1.1.1;
        include proxy_params;
    }
}
```

The `/etc/nginx/proxy_params` file typically contains header definitions similar to the following:

```bash theme={null}
cat /etc/nginx/proxy_params

proxy_set_header Host $http_host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

<Callout icon="lightbulb">
  Including these header settings ensures the target server receives crucial connection details such as the client’s original IP address.
</Callout>

### Step 2: Enable the Configuration

After saving your configuration file within `/etc/nginx/sites-available`, enable it by creating a symbolic link in the `/etc/nginx/sites-enabled` directory. It is also advisable to disable the default website if it isn’t needed.

```bash theme={null}
