# Use Remote Filesystems NFS

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Storage/Use-Remote-Filesystems-NFS/page

This article explains how to use the Network File System (NFS) protocol for sharing remote file systems between Linux computers.

In previous lessons, we explored working with local file systems and local block storage devices—data stored on the same system where you are logged in. In this lesson, we focus on using remote file systems by leveraging the Network File System (NFS) protocol, a popular method for sharing data between Linux computers.

<Frame>
  ![The image illustrates the Network Filesystem Protocol (NFS) with two computers running Linux, connected by a file-sharing icon, emphasizing that protocols act as a "language."](https://kodekloud.com/kk-media/image/upload/v1752881369/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Use-Remote-Filesystems-NFS/nfs-network-filesystem-protocol.jpg)
</Frame>

NFS operates based on a two-step process:

1. Configuring an NFS server to share a file system with remote machines.
2. Setting up an NFS client to mount the remote file system.

<Frame>
  ![The image illustrates the Network Filesystem Protocol (NFS) with a diagram showing an NFS server and NFS clients connected through the protocol.](https://kodekloud.com/kk-media/image/upload/v1752881369/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Use-Remote-Filesystems-NFS/nfs-protocol-server-clients-diagram.jpg)
</Frame>

<Callout icon="lightbulb">
  The NFS protocol simplifies remote file sharing by standardizing communication between the server and client. This allows Linux systems to seamlessly share and access files over the network.
</Callout>

## Configuring the NFS Server

Begin by setting up the NFS server—the system that shares data with clients.

### Step 1: Install the NFS Server Package

Install the necessary package using the following command:

```bash theme={null}
sudo apt install nfs-kernel-server
```

### Step 2: Define File System Shares

Specify which directories to share by editing the `/etc/exports` file. Open the file with your preferred text editor:

```bash theme={null}
sudo vim /etc/exports
```

Inside this file, you will see commented examples that illustrate the basic syntax. The general format for an export declaration is:

1. The directory to be shared (e.g., `/nfs/disk1/backups` or `/srv/homes`).
2. One or more allowed NFS clients (specified as hostnames, fully qualified domain names, or IP addresses).
3. Optionally, a range of IP addresses can be allowed using CIDR notation (e.g., `10.0.16.0/24`).
4. Export options enclosed in parentheses, such as `(rw,sync,no_subtree_check)` for read/write access or `(ro,sync,no_subtree_check)` for read-only access.

Here’s an example configuration in `/etc/exports`:

```bash theme={null}
