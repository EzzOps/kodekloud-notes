# OpenBSD: sshd_config,v 1.103 2018/04/09 20:41:22 tj Exp $
# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.
# This sshd was compiled with PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where
# possible, but leave them commented.  Uncommented options override the
# default value.
# If you want to change the port on a SELinux system, you have to tell SELinux about this change.
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
#Port 22
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::
HostKey /etc/ssh/ssh_host_rsa_key
```

Review these comments to understand the available options.

### Changing the Listening Port

By default, the SSH daemon listens on port 22. Although this directive is commented out, you can customize it by uncommenting it and specifying a new port. For example, to change the port to 988, update the file as shown below:

```bash theme={null}
# This is the sshd server system-wide configuration file.  See
# sshd_config(5) for more information.
#
# The strategy used for options in the default sshd_config shipped with
# OpenSSH is to specify options with their default value where possible,
# but leave them commented.  Uncommented options override the default value.
#
# If you want to change the port on a SELinux system, you have to tell SELinux about this change.
# semanage port -a -t ssh_port_t -p tcp #PORTNUMBER
#
Port 988
#AddressFamily any
#ListenAddress 0.0.0.0
#ListenAddress ::
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
```

### Setting the Address Family and Listen Address

The `AddressFamily` directive determines whether the daemon will use IPv4, IPv6, or both. Here are the available options:

• any (default)\
• inet (IPv4 only)\
• inet6 (IPv6 only)

If your server has multiple IP addresses—for example, a public IP (203.0.113.1) and an internal IP (10.11.12.9)—you can restrict SSH connections to internal hosts by specifying the listen address:

```bash theme={null}
Port 988
AddressFamily inet
ListenAddress 10.11.12.9
#ListenAddress ::
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key
```

### Logging and Authentication Settings

Below the network configuration, you will find directives related to logging and authentication. For example:

```bash theme={null}
# Logging
#SyslogFacility AUTH
SyslogFacility AUTHPRIV
#LogLevel INFO

# Authentication:
#LoginGraceTime 2m
PermitRootLogin yes
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

#PubkeyAuthentication yes
# The default is to check both .ssh/authorized_keys and .ssh/authorized_keys2,
# but installations override this so that only .ssh/authorized_keys is used.
AuthorizedKeysFile .ssh/authorized_keys
#AuthorizedPrincipalsFile none
```

To prevent remote root logins, change the `PermitRootLogin` directive from `yes` to `no`:

```bash theme={null}
# Authentication:
#LoginGraceTime 2m
PermitRootLogin no
#StrictModes yes
#MaxAuthTries 6
#MaxSessions 10

#PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
```

### Enabling or Disabling Password Authentication

By default, password authentication is enabled. However, using SSH keys is recommended for stronger security. To disable password authentication, update these lines:

```bash theme={null}
PasswordAuthentication yes
ChallengeResponseAuthentication no
```

Modify them as follows:

```bash theme={null}
PasswordAuthentication no
ChallengeResponseAuthentication no
```

If you need to allow password authentication for a specific user (for example, user "aaron"), you can add a match block at the end:

```bash theme={null}
PasswordAuthentication no
Match User aaron
    PasswordAuthentication yes
```

:::note
After making changes to the SSH server configuration, always reload the SSH daemon to apply them:
:::

Reload the SSH service with:

```bash theme={null}
sudo systemctl reload sshd.service
```

──────────────────────────────────────────────

## Configuring the SSH Client

The SSH client is available by default on Windows 10, macOS, and Linux. Its configuration files are typically stored in a user's `.ssh` directory.

### Creating a Client Configuration File

If you connect to multiple servers, streamlining connection details with a client configuration file can be very beneficial. First, verify that the `.ssh` directory exists:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ ls -a
```

Then, create or modify the client configuration file located at `~/.ssh/config`:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ vim ~/.ssh/config
```

For example, you might define an alias for a server like this:

```plaintext theme={null}
Host centos
    HostName 10.11.12.9
    Port 22
    User aaron
```

After saving the file, secure it by restricting its permissions:

```bash theme={null}
chmod 600 ~/.ssh/config
```

Now you can connect to your server using the defined alias:

```bash theme={null}
ssh centos
```

### Generating SSH Key Pairs

To use SSH keys for authentication instead of passwords, generate a key pair on your local machine:

```bash theme={null}
[aaron@LFCS-CentOS ~]$ ssh-keygen
```

When prompted, press Enter to accept the default file location (typically `/home/aaron/.ssh/id_rsa`) and decide whether to secure the key with a passphrase. This process creates:

• A private key: `id_rsa`\
• A public key: `id_rsa.pub`

### Copying the Public Key to the Server

To enable key-based authentication, copy your public key to the server’s `authorized_keys` file. The easiest method is using the `ssh-copy-id` command:

```bash theme={null}
ssh-copy-id aaron@10.11.12.9
```

This command appends your public key to the server’s `~/.ssh/authorized_keys` file. If `ssh-copy-id` is not available, you can manually copy the public key. First, display it on your client:

```bash theme={null}
cat ~/.ssh/id_rsa.pub
```

Then, on the server, open (or create) the authorized keys file:

```bash theme={null}
[aaron@LFCS-CentOS .ssh]$ vim authorized_keys
```

Paste the public key into the file, save it, and then restrict its permissions:

```bash theme={null}
chmod 600 ~/.ssh/authorized_keys
```

### Managing Known Hosts

The first time you connect to an SSH server, its fingerprint is stored in the `known_hosts` file. If the fingerprint changes—such as after a server reinstallation—you might need to remove the outdated entry:

```bash theme={null}
ssh-keygen -R 10.11.12.9
```

To clear all stored fingerprints, simply remove the entire `known_hosts` file:

```bash theme={null}
rm ~/.ssh/known_hosts
```

──────────────────────────────────────────────

## Customizing Client Default Settings

System-wide SSH client settings are stored in `/etc/ssh/ssh_config`. For example, you might see directives like:

```bash theme={null}
# IdentityFile ~/.ssh/id_rsa
# Port 22
```

If your internal network uses an alternate port—say 229—you can modify this setting. Rather than editing the system-wide file (which may be overwritten during upgrades), create a custom configuration file in the `/etc/ssh/ssh_config.d` directory:

```bash theme={null}
sudo vim /etc/ssh/ssh_config.d/99-our-settings.conf
```

Inside this file, add your custom configurations. For instance, to change the default port:

```plaintext theme={null}
Port 229
```

With this adjustment, your SSH client will attempt connections using port 229 by default.

──────────────────────────────────────────────

## Diagrams and Manual Page Searches

For further details on configuration options, consult the manual pages. Here are some examples:

1. When reviewing the manual for the SSH daemon configuration, you can search for “AddressFamily” by typing `/Family` in the less pager. This highlights the corresponding section in the manual.

<Frame>
  ![The image shows a terminal window displaying the manual page for the sshd\_config file, which is the configuration file for the OpenSSH SSH daemon. It includes a description of how the file is used and details about specific configuration options.](https://kodekloud.com/kk-media/image/upload/v1752883589/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Configure-key-based-authentication-for-SSH/sshd-config-manual-page-terminal.jpg)
</Frame>

2. To better understand various SSH authentication methods, search for “password” in the SSHD manual page. This returns information on public key, password, and other authentication techniques.

<Frame>
  ![The image shows a terminal window displaying a manual page for SSHD configuration, focusing on authentication methods like public key and password.](https://kodekloud.com/kk-media/image/upload/v1752883590/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Configure-key-based-authentication-for-SSH/sshd-configuration-authentication-manual.jpg)
</Frame>

3. Additional details on settings such as `PasswordAuthentication` and `MaxAuthTries` are visible further down the manual page.

<Frame>
  ![The image shows a terminal window displaying a manual page for SSHD configuration settings, including options like PasswordAuthentication and MaxAuthTries.](https://kodekloud.com/kk-media/image/upload/v1752883591/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Configure-key-based-authentication-for-SSH/sshd-configuration-manual-terminal.jpg)
</Frame>

──────────────────────────────────────────────

## Conclusion

This guide has walked you through configuring both the SSH server and client on Linux with a focus on securing connections through key-based authentication. Begin by editing `/etc/ssh/sshd_config` to update your network and authentication settings. Generate SSH keys and update your client's configuration for streamlined, secure connections.

:::note
Whenever you modify the SSH server configuration, remember to reload the daemon:
:::

```bash theme={null}
sudo systemctl reload sshd.service
```

Proceed to your next lab or lecture for more advanced configurations. Happy configuring!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/5935b82f-37ac-4f4e-b619-0a6f8824088b/lesson/5c3d18b6-028f-44d8-a316-eaa8ea4b7f82" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/5935b82f-37ac-4f4e-b619-0a6f8824088b/lesson/77a2ee68-ab4a-4648-90db-ec1c58dbc6c4" />
</CardGroup>


# List and Identify SELinux file and process contexts

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Manage-Security/List-and-Identify-SELinux-file-and-process-contexts/page

This article explores how SELinux enhances security by managing file and process contexts beyond standard Linux permissions.

In this article, we'll explore how SELinux manages file and process contexts, offering an extra layer of security that goes beyond standard Linux file permissions. Traditional permissions (read, write, execute) are essential, but they may not fully protect your system against sophisticated attacks. SELinux enhances system security by confining processes and applying strict mandatory access control policies.

For example, imagine a web server running within a dedicated directory. If an attacker compromises the web server, they inherit its directory permissions, potentially exploiting system vulnerabilities. SELinux prevents this by isolating processes through detailed security contexts based on SELinux labels. On systems like CentOS Stream, SELinux is enabled by default, ensuring that even if a process is breached, its actions remain confined.

## Viewing Standard Permissions

The basic Linux command `ls -l` can be used to display the standard file and directory permissions:

```bash theme={null}
$ ls -l
-rw-rw-r--. 1 aaron aaron 160 Dec  1 18:19 archive.tar.gz
```

This output shows the read, write, and execute permissions for a file. In contrast, SELinux labels provide a more granular form of security.

## Understanding SELinux Context Labels

SELinux introduces an additional security layer by assigning each file and process a security context label. This label comprises four components in the following order: user, role, type, and level. Consider the example label below:

```text theme={null}
unconfined_u:object_r:user_home_t:s0
```

* **User**: `unconfined_u`\
  Represents the SELinux user defined within the SELinux policy, which may differ from the Linux login username.

* **Role**: `object_r`\
  Specifies the role that helps determine permitted operations.

* **Type**: `user_home_t`\
  Defines the allowed operations for the file or process and effectively serves as a security "jail."

* **Level**: `s0`\
  Often used for multi-level security in organizations, indicating the sensitivity level of the object.

When an action is initiated, SELinux evaluates it by sequentially checking the SELinux user, role, and type/domain. This layered methodology ensures that only authorized processes access specific domains, thereby denying unauthorized actions.

<Callout icon="lightbulb">
  Remember: In SELinux, only files with the correct type (e.g., `sshd_exec_t` for SSH daemon) can initiate a process that transitions into the corresponding security domain.
</Callout>

## Exploring Process Contexts

Processes also carry SELinux security contexts. You can check the SELinux labels for running processes using the `ps` command with the `-Z` option:

```bash theme={null}
$ ps axZ
system_u:system_r:accountsd_t:s0       995 ?    Ssl    0:00 /usr/libexec/accoun
system_u:system_r:NetworkManager_t:s0   1024 ?    Ssl    0:00 /usr/sbin/NetworkMa
system_u:system_r:sshd_t:s0-s0:c0.c1023 1030 ?    Ss     0:00 /usr/sbin/sshd -D
system_u:system_r:tuned_t:s0            1032 ?    Ssl    0:00 /usr/libexec/platfo
system_u:system_r:cupsd_t:s0-s0:c0.c1023 1033 ?    Ss     0:00 /usr/sbin/cupsd -l
```

In this listing, observe that the SSH daemon (`sshd`) runs within the `sshd_t` domain. Strict policies enforce that only files labeled with the correct type (in this case, often `sshd_exec_t`) can start a process that enters this domain. Conversely, processes running with the `unconfined_t` label operate with minimal restrictions.

## Viewing the Current User’s SELinux Context

To determine your current SELinux security context, use the `id` command with the `-Z` option:

```bash theme={null}
$ id -Z
unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

This output indicates how your login maps into the SELinux policy. To see how Linux users are mapped to SELinux users, execute:

```bash theme={null}
$ sudo semanage login -l
Login Name    SELinux User      MLS/MCS Range    Service
__default__   unconfined_u      s0-s0:c0.c1023   *
root          unconfined_u      s0-s0:c0.c1023   *
```

<Callout icon="lightbulb">
  The default mapping assigns non-root users to the `unconfined_u` SELinux user, ensuring that even root processes are subject to the same security policies.
</Callout>

## Checking SELinux Enforcement Status

To check if SELinux is actively enforcing its security policies, use the `getenforce` command:

```bash theme={null}
$ getenforce
Enforcing
```

The possible outputs are:

* **Enforcing**: SELinux policies are enforced, and unauthorized actions are blocked.
* **Permissive**: SELinux is not actively enforcing policies but logs actions that would have been denied.
* **Disabled**: SELinux is turned off, and no access control is performed.

## Summary

This article has outlined how SELinux uses security context labels to provide robust access control for both files and processes. By examining the SELinux user, role, and type/domain—and considering the security level—SELinux creates a comprehensive security framework that limits potential damage from compromised processes. This granular approach is essential for maintaining the integrity of your system in the face of modern cyber threats.

For further details and practical exercises to strengthen your understanding of SELinux and its use in securing Linux systems, continue exploring related documentation and hands-on tutorials.

## Further Reading

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [SELinux Project Wiki](https://selinuxproject.org/page/Main_Page)
* [Linux Security Modules Documentation](https://www.kernel.org/doc/html/latest/security/LSM.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/5935b82f-37ac-4f4e-b619-0a6f8824088b/lesson/6d5cd666-0642-4f1b-9c7a-7c97afaba6b6" />
</CardGroup>
