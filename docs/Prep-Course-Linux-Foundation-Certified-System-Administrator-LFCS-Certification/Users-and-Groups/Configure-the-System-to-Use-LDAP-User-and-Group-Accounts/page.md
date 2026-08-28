#                   soft   core         0
#                   hard   rss          10000
#@student           hard   nproc        20
#@faculty           soft   nproc        20
#@faculty           hard   nproc        50
#ftp                hard   nproc        0
#@student           -      maxlogins    4
```

Each entry is composed of four fields in order:

1. **Domain:** Specifies the user or group.
2. **Type:** Indicates whether the limit is `soft`, `hard`, or both (using `-`).
3. **Item:** The resource being limited.
4. **Value:** The maximum allowed value for the resource.

### Domain Field

The domain field defines the scope of the limit:

* **Username:** For example, `trinity`.
* **Group Name:** Denoted by a prefix `@` (e.g., `@developers`).
* **Asterisk (`*`):** Sets a default limit for all users not explicitly mentioned.

In this example, an asterisk (`*`) entry is used to impose a default CPU time limit of 5 minutes for every user unless overridden by a specific user configuration.

<Callout icon="lightbulb">
  User-specific limits take precedence over global (`*`) entries. For instance, if `trinity` has a defined limit, it will override the global settings.
</Callout>

## Detailed Examples of Configuration

Below is a detailed example illustrating how to set up different resource limits:

```bash theme={null}
$ sudo vim /etc/security/limits.conf
#<domain>      <type>  <item>      <value>
**              soft    core        0
**              hard    rss         10000
#@student       hard    nproc       20
#@faculty       soft    nproc       20
#@faculty       hard    nproc       50
#ftp            hard    nproc       0
#@student       -       maxlogins   4
trinity         hard    nproc       10
@developers     soft    nproc       20
*               soft    cpu         5
```

### Explanation of Limit Types

* **Hard Limit:** The absolute maximum that cannot be exceeded.\
  *Example:* If set to 30 processes, the user cannot exceed that number.

* **Soft Limit:** The initial threshold applied at login. Users can temporarily raise the soft limit up to the hard limit as needed.\
  *Example:* A soft limit of 10 processes can be increased to a hard limit of 20 processes.

* **Combined Limit (`-`):** Applies the same limit to both soft and hard categories simultaneously.

Consider the following configuration for user `trinity`:

```bash theme={null}
$ sudo vim /etc/security/limits.conf
#<domain>          <type>   <item>         <value>
#**                soft     core           0
#**                hard     rss            10000
#@student          hard     nproc          20
#@faculty          soft     nproc          20
#@faculty          hard     nproc          50
#ftp               hard     nproc          0

trinity           hard     nproc          10
@developers       soft     nproc          20
*                 soft     cpu            5
```

In this setup, the global asterisk provides default limits, while `trinity` has a dedicated process limit, ensuring her settings override the defaults.

Now, explore a further example that demonstrates both soft and hard limits:

```bash theme={null}
$ sudo vim /etc/security/limits.conf
#<domain>     <type>     <item>          <value>
#**            soft       core            0
#**            hard       rss             10000
#@student     hard       nproc           20
#@faculty     soft       nproc           20
#@faculty     hard       nproc           50
#ftp          hard       nproc           0
#@student     -          maxlogins       4
trinity       hard       nproc           30
trinity       hard       nproc           20
trinity       soft       nproc           10
trinity       -          nproc           20
```

Here, `trinity` initially has a soft limit of 10 processes but can temporarily raise it to 20. However, the combined limit (`-`) enforces a strict maximum of 20 processes upon login.

## Common Resource Items

Some common items you might limit include:

* **nproc:** Maximum number of concurrent processes.
* **fsize:** Maximum file size (in kilobytes). For example, 1024 KB equals 1 MB.
* **cpu:** CPU time limit in minutes. Note that a process running for 1 second at 100% CPU uses 1 second from the allocated CPU time, while 50% usage deducts 0.5 seconds.

For a complete list of options, refer to the limits.conf manual page:

```bash theme={null}
$ man limits.conf
```

## Example Combined Configuration

The following YAML snippet represents a combined configuration example:

```yaml theme={null}
#<domain>          <type>  <item>          <value>
#                   #
#**                soft    core            0
#**                hard    rss             10000
#@student          hard    nproc           20
#@faculty          soft    nproc           20
#@faculty          hard    nproc           50
#ftp               hard    nproc           0
#@student          -       maxlogins       4
trinity           hard    nproc           30
trinity           hard    fsize           1024
trinity           hard    cpu             1
```

## Setting a Custom Limit Example

To restrict `trinity` to a maximum of 3 concurrent processes, find the following line in your configuration:

```bash theme={null}
#@student   -       maxlogins      4
```

Immediately after that line, add the new limit (make sure not to comment it out):

```conf theme={null}
#@student   -       maxlogins      4
trinity    -       nproc          3
```

After saving the file, log in as `trinity` using:

```bash theme={null}
$ sudo -iu trinity
```

Once logged in, you should see only the bash shell process running by default:

```bash theme={null}
$ ps | less
PID TTY      TIME CMD
6314 pts/0  00:00:00 bash
6348 pts/0  00:00:00 ps
6349 pts/0  00:00:00 less
```

Now, with the updated configuration:

```conf theme={null}
#@student   -       maxlogins      4
trinity    -       nproc          3
```

`trinity` is limited to 3 concurrent processes. Attempting to spawn a fourth process will trigger errors similar to:

```bash theme={null}
$ ls -a | grep bash | less
bash: fork: retry: Resource temporarily unavailable.
bash: fork: retry: Resource temporarily unavailable.
bash: fork: retry: Resource temporarily unavailable.
bash: fork: retry: Resource temporarily unavailable.
bash: fork: retry: Resource temporarily unavailable.
```

These errors confirm that the 3-process limit is enforced correctly.

To exit `trinity`'s session, simply type:

```bash theme={null}
$ logout
```

## Viewing and Adjusting Current Resource Limits

You can check your current resource limits using the `ulimit -a` command, which displays all settings along with their units:

```bash theme={null}
$ ulimit -a
core file size         (blocks, -c)          0
data seg size          (kbytes, -d)    unlimited
scheduling priority    (-e)                  0
file size              (blocks, -f)    unlimited
pending signals        (-i)              14722
max locked memory      (kbytes, -l)         64
max memory size        (kbytes, -m)    unlimited
open files             (-n)              1024
pipe size              (512 bytes, -p)       8
POSIX message queues   (bytes, -q)      819200
real-time priority     (-r)                  0
stack size             (kbytes, -s)       8192
cpu time               (seconds, -t)    unlimited
max user processes     (-u)              14722
virtual memory         (kbytes, -v)    unlimited
file locks             (-x)           unlimited
```

For example, the `-u` flag shows the maximum number of processes a user can run. To lower this limit (e.g., to 5000 processes), execute:

```bash theme={null}
$ ulimit -u 5000
```

<Callout icon="lightbulb">
  By default, a user can only decrease their limits. If both hard and soft limits exist, the soft limit can be increased up to the hard limit only once per session.
</Callout>

After adjusting the limit, verify the changes with another `ulimit -a`. Remember, any future commands can only lower the limit further unless restarted.

## Conclusion

In this lesson, you have learned how to configure and enforce user resource limits in Linux through the `/etc/security/limits.conf` file. Properly managing these limits ensures balanced resource distribution among multiple users and maintains system stability.

For more information, refer to the [Linux man pages](https://linux.die.net/man/5/limits.conf) and additional resources on system administration.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/b36d272b-24e2-44e1-82cb-20a5cfa93635/lesson/d1ff1109-94fb-4ee8-9c41-6aaa85250142" />
</CardGroup>


# Configure the System to Use LDAP User and Group Accounts

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Users-and-Groups/Configure-the-System-to-Use-LDAP-User-and-Group-Accounts/page

This article explains how to configure a Linux system to use an LDAP server for centralized user and group account management.

Linux systems typically store user account and group information locally. For example, user details are maintained in the /etc/passwd file—not to be confused with actual password storage. This file holds important account details such as username, UID, home directory, and the preferred shell. Consider the following example from /etc/passwd:

***

man:x:6:12:man:/var/cache/man:/usr/sbin/nologin\
lp:x:7:7:lp\:/var/spool/lpd:/usr/sbin/nologin\
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin\
news:x:9:9:news\:/var/spool/news\:/usr/sbin/nologin\
uucp:x:10:10:uucp\:/var/spool/uucp\:/usr/sbin/nologin\
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin\
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin\
backup:x:34:34:backup\:/var/backups\:/usr/sbin/nologin\
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin\
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin\
\_apt:x:42:65534:65534:nonexistent:/usr/sbin/nologin\
nobody:x:65534:65534:nobody:/usr/sbin/nologin\
systemd-network:x:998:998:systemd Network Management:/usr/sbin/nologin\
systemd-timesync:x:997:997:systemd Time Synchronization:/usr/sbin/nologin\
dhcpd:x:100:65534:DHCP Client Daemon,,,:/usr/lib/dhcpcd:/bin/false\
messagebus:x:101:102:nonexistent:/usr/sbin/nologin\
systemd-resolve:x:992:992:systemd Resolver:/usr/sbin/nologin\
pollinate:x:102:1:/var/cache/pollinate:/bin/false\
polkitd:x:991:991:User for polkitd:/usr/sbin/nologin\
syslog:x:103:104:nonexistent:/usr/sbin/nologin\
uuidd:x:104:104:nonexistent:/var/uuid:/usr/sbin/nologin\
tcpdump:x:105:107:nonexistent:/usr/sbin/nologin\
tss:x:106:108:TPM software stack,,/var/lib/tpm:/bin/false\
landscape:x:107:109:/var/lib/landscape:/usr/sbin/nologin\
fwupd-refresh:x:989:989:Firmware update daemon:/var/lib/fwupd:/usr/sbin/nologin\
usbmux:x:108:46:usbmux daemon,,/var/lib/usbmux:/usr/sbin/nologin\
sshd:x:109:65534:/run/sshd:/usr/sbin/nologin\
jeremy:x:1000:1000:Jeremy Morgan:/home/jeremy:/bin/bash\
jeremy\@kodekloud:\~\$
----------------------

Managing user accounts and groups individually across hundreds of servers can be challenging—even when using automation tools like Chef, Ansible, or Puppet. To simplify this, you can use a centralized LDAP (Lightweight Directory Access Protocol) server as the primary source for account data. This approach enables you to add, remove, or modify user and group information centrally; those updates then propagate automatically to all Linux clients configured to use LDAP.

For better understanding, the remainder of this guide walks you through a practical exercise to implement this setup.

***

## Initial Verification of Local Users

Before integrating LDAP, confirm that certain user accounts (such as john and jane) are not present locally:

```bash theme={null}
jeremy@kodekloud:~$ id john
id: ‘john’: no such user
jeremy@kodekloud:~$ id jane
id: ‘jane’: no such user
jeremy@kodekloud:~$
```

Later in this guide, you will see how the LDAP server supplies these accounts.

***

## Setting Up an LDAP Server Using LXC Containers

In production environments, the LDAP server might be hosted on dedicated hardware or cloud platforms (such as Microsoft Azure or Windows Server). For this exercise, we will use a pre-configured LDAP server housed within an LXC container. LXC containers offer a lightweight virtualization approach, similar to Docker, but run full operating systems.

### Step 1: Initialize LXD

First, initialize LXD, the hypervisor managing your LXC containers:

```bash theme={null}
jeremy@kodekloud:~$ lxd init
Installing LXD snap, please be patient.
Would you like to use LXD clustering? (yes/no) [default=no]:
```

If prompted for the loop device size, ensure it is at least 5GB (the default value) and press Enter.

### Step 2: Confirm the LDAP Server Archive

A pre-configured LDAP server has been archived as ldap-server.tar.xz. Confirm its existence:

```bash theme={null}
jeremy@kodekloud:~$ ls -la
total 444860
drwxr-x--- 5 jeremy jeremy  4096 May 22 22:02 .
drwxr-xr-x 3 root   root    4096 May 22 21:51 ..
-rw-r--r-- 1 jeremy jeremy   220 Mar 31 08:41 .bash_logout
-rw-r--r-- 1 jeremy jeremy  3771 Mar 31 08:41 .bashrc
drwx------ 2 jeremy jeremy  4096 May 22 21:52 .cache
-rwxr-xr-x 1 jeremy jeremy 455502300 May 22 21:51 ldap-server.tar.xz
-rw-r--r-- 1 jeremy jeremy   807 Mar 31 08:41 .profile
drwx------ 3 jeremy jeremy  4096 May 22 22:02 snap
drwx------ 2 jeremy jeremy  4096 May 22 21:51 .ssh
jeremy@kodekloud:~$
```

### Step 3: Import and Start the Container

Import the container image:

```bash theme={null}
jeremy@kodekloud:~$ lxc import ldap-server.tar.xz
```

Wait until the import completes and then list your containers:

```bash theme={null}
jeremy@kodekloud:~$ lxc list
+---------------+---------+-----------+---------+-------------+
|     NAME      |  STATE  |   IPV4    |   IPV6  |   TYPE      |
+---------------+---------+-----------+---------+-------------+
|  ldap-server  |  STOPPED|           |         |  CONTAINER  |
+---------------+---------+-----------+---------+-------------+
jeremy@kodekloud:~$
```

Start the container:

```bash theme={null}
jeremy@kodekloud:~$ lxc start ldap-server
```

Next, verify that the container is running and note its IPv4 address:

```bash theme={null}
jeremy@kodekloud:~$ lxc list
+---------------+---------+-------------------------------+-------------------------------------------------------------+-------------+
|     NAME      |  STATE  |            IPV4               |                           IPV6                              |   TYPE      |
+---------------+---------+-------------------------------+-------------------------------------------------------------+-------------+
|  ldap-server  | RUNNING | 10.0.142.218 (eth0)           | fd42:f1ca:1ed:230d:216:3eff:fe88:50e8 (eth0)                  | CONTAINER  |
+---------------+---------+-------------------------------+-------------------------------------------------------------+-------------+
jeremy@kodekloud:~$
```

At this point, your LDAP server is operational. Note that for simplicity, every password on this server is set to "password." Both the LDAP admin and the Linux accounts (John and Jane) have the password "password."

***

## Configuring the Linux System to Use LDAP for Account Management

To enable your Linux system to query LDAP for user and group information, you must install the package libnss-ldapd. This package enhances the Name Service Switch (NSS), allowing the system to retrieve data from sources such as LDAP.

### Installing libnss-ldapd

Run the following commands to update your package lists and install libnss-ldapd:

```bash theme={null}
jeremy@kodekloud:~$ sudo apt update && sudo apt install libnss-ldapd
[sudo] password for jeremy:
```

A configuration wizard will appear to assist you in setting up libnss-ldapd.

<Callout icon="lightbulb">
  When prompted for the NSLCD URL, replace the default "ldap\://127.0.0.1/" with the actual IP address of your LDAP server (e.g., "ldap\://10.0.142.218/") and ensure you include the trailing slash.
</Callout>

Next, provide the distinguished name (DN) for the LDAP search base. Although an example like "dc=hsd1,dc=or,dc=comcast,dc=net" might be shown, our pre-configured server uses the domain "kodekloud.com." Therefore, enter:

```plaintext theme={null}
dc=kodekloud,dc=com
```

When choosing the services to use LDAP lookups, ensure that you select passwd (users), group, and shadow (passwords). Confirm these selections and complete the wizard.

Below is the relevant image of the LDAP configuration interface (do not modify the image link or description):

<Frame>
  ![The image shows a configuration screen for "libnss-ldapd," where users can select services for LDAP lookups, such as passwd, group, and shadow.](https://kodekloud.com/kk-media/image/upload/v1752881371/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Configure-the-System-to-Use-LDAP-User-and-Group-Accounts/libnss-ldapd-configuration-screen.jpg)
</Frame>

Press Enter to complete the configuration. The wizard updates files such as /etc/nsswitch.conf and sets up the NSLCD service.

### Verifying /etc/nsswitch.conf

The updated /etc/nsswitch.conf file should now include LDAP as a source for passwd, group, and shadow data:

```plaintext theme={null}
passwd:         files systemd ldap
group:          files systemd ldap
shadow:         files systemd ldap
gshadow:        files systemd
...
```

This informs the system to fetch user information from local files, systemd, and the LDAP server. The Name Service Switch uses the NSLCD daemon to perform LDAP queries; its configuration is stored in /etc/nslcd.conf. To view the NSLCD configuration, run:

```bash theme={null}
sudo cat /etc/nslcd.conf
```

A typical configuration may appear as follows:

```plaintext theme={null}
