# find [/path/to/directory] [search_parameters]
```

For instance, to locate a file named file1.txt in the /bin directory, use:

```bash theme={null}
$ find /bin -name file1.txt
```

If you don’t specify a directory path, the command searches from your current working directory. Always specify the search location first, followed by the desired search parameters.

<Callout icon="lightbulb">
  If no directory is specified, remember that find will perform a recursive search starting in the current directory.
</Callout>

## Common Search Parameters

### Name and Wildcards

The -name option allows you to search for files by their name. Note that this search is case sensitive:

```bash theme={null}
$ find -name felix
```

To perform a case-insensitive search, utilize the -iname option:

```bash theme={null}
$ find -iname felix
```

Wildcards can also be used. For example, to find all files beginning with the letter "f":

```bash theme={null}
$ find -name "f*"
```

Here, the asterisk (\*) serves as a wildcard, matching any number of characters.

### Time-Based Searches

The -mmin option lets you find files based on their modification time in minutes. For example, to list files modified exactly 5 minutes ago:

```bash theme={null}
$ find -mmin 5
```

For files modified within the last 5 minutes, apply a negative value:

```bash theme={null}
$ find -mmin -5
```

Similarly, the -mtime option works with 24-hour periods. For instance:

* -mtime 0 returns files modified within the past 24 hours.
* -mtime 1 returns files modified between 24 and 48 hours ago.
* To find files modified between 48 and 72 hours ago, you would use:

  ```bash theme={null}
  $ find -mtime 2
  ```

### Size-Based Searches

The -size parameter allows searching for files based on file size. For example, to find files that are exactly 512 kilobytes in size:

```bash theme={null}
$ find -size 512k
```

Use a plus sign (+) to search for files larger than the specified size, or a minus sign (–) for files smaller than that size. The following suffixes denote size units:

| Size Suffix | Unit      |
| ----------- | --------- |
| C           | Bytes     |
| K           | Kilobytes |
| M           | Megabytes |
| G           | Gigabytes |

### Combining Search Parameters

Multiple search conditions can be combined to refine your results. For example, to search for files that start with the letter "f" and are exactly 512K in size:

```bash theme={null}
$ find -name "f*" -size 512k
```

For OR expressions (files that either start with "f" or are 512K in size), use the -o flag:

```bash theme={null}
$ find \( -name "f*" -o -size 512k \)
```

To exclude a particular pattern, use the NOT operator with -not or an escaped exclamation mark. For example, to omit files that start with a capital "F", you can run:

```bash theme={null}
$ find -not -name "f*"
```

Alternatively:

```bash theme={null}
$ find \! -name "f*"
```

### Permission-Based Searches

The -perm option finds files based on their permission settings. Here are several examples:

* **Exact permissions:** To search for files with precisely 664 permissions (read and write permissions for the user and group; read permission for others):

  ```bash theme={null}
  $ find -perm 664
  ```

* **At least these permissions:** To find files having at least these permissions, prefix the mode with a hyphen:

  ```bash theme={null}
  $ find -perm -664
  ```

* **Any of the specified permissions:** To search for files where any one of the specified permissions is present, use a slash:

  ```bash theme={null}
  $ find -perm /u=r,g=r,o=r
  ```

Additional permission examples include:

* To find files that only the owner can read and write:

  ```bash theme={null}
  $ find -perm 600
  ```

* To find files that the owner can execute (regardless of additional permissions):

  ```bash theme={null}
  $ find -perm -100
  ```

* To ensure that others do not have read permission, combine conditions with the NOT operator:

  ```bash theme={null}
  $ find \! -perm -o=r
  ```

## Conclusion

The find command is an indispensable tool in Linux for locating files based on name, size, modification time, and permissions. With its extensive set of options, you can efficiently tailor your searches to meet various system administration needs.

Now that you have a deeper understanding of how to leverage the find command, it’s time to practice these techniques and sharpen your Linux file management skills.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/0e6594ac-243a-4549-85b9-fc5d38ad635d" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/c37f6f1c-ab04-4201-9586-4da2577f8041" />
</CardGroup>


# Securely transfer files between systems

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Securely-transfer-files-between-systems/page

This guide explains how to securely transfer files between systems using SCP and SFTP protocols leveraging SSH for authentication and encryption.

In this guide, you'll discover how to securely transfer files between systems using two popular protocols: SCP and SFTP. Both of these tools leverage SSH (Secure Shell) for authentication and encryption, ensuring that your file transfers remain secure during transmission.

***

## Using SCP for Secure File Transfer

SCP (Secure Copy) is a command-line utility designed for quick and secure file transfers between hosts. By relying on SSH, SCP guarantees that your data is encrypted throughout the transfer process. Below is the basic syntax and usage examples.

### Basic SCP Syntax

1. Specify the username and remote host using the format:\
   `username@remote_host`
2. Provide the remote file path prefixed with a colon and a slash (`:/`).
3. Define the local destination path where the file will be saved.

For example, to copy a file from a remote machine with IP `192.168.1.27` using the username `aaron`, execute:

```bash theme={null}
$ scp aaron@192.168.1.27:/home/aaron/myfile.tgz /home/aaron/myfile.tgz
```

Similarly, to transfer a file from your local machine to a remote server, use:

```bash theme={null}
$ scp /home/aaron/my_archive.tar aaron@192.168.1.27:/home/aaron/my_archive.tar
```

You can also transfer files directly between two remote systems. In that case, specify both remote locations:

```bash theme={null}
$ scp aaron@192.168.1.27:/home/aaron/familyphoto.jpg aaron@192.168.1.59:/home/aaron/familyphoto.jpg
```

<Callout icon="lightbulb">
  When using SCP without explicitly specifying a username, the current local user will be assumed for the remote host.
</Callout>

To explore more options and learn about additional flags, refer to the SCP manual:

```bash theme={null}
$ man scp
```

***

## Using SFTP for Interactive File Transfers

SFTP (Secure File Transfer Protocol) offers a more user-friendly, interactive interface for managing and transferring files securely. The connection command resembles that of SCP, providing an easy transition if you're familiar with secure shell protocols.

### Establishing an SFTP Connection

To connect to a remote host using the SFTP protocol, run:

```bash theme={null}
$ sftp aaron@192.168.1.27
```

Once connected, you will be greeted with an `sftp>` prompt. From here, you can execute a range of commands to navigate and manage files.

### Common SFTP Commands

* **ls** – Lists files and directories on the remote system.
* **cd** – Changes directories on the remote host.
* **lls** or **lcd** – Lists files or changes directories locally (note the `l` prefix).

For instance, to navigate to the `Pictures` directory on the remote host, type:

```bash theme={null}
sftp> cd Pictures
```

Switching to a local directory is just as simple:

```bash theme={null}
sftp> lcd /local/path
```

To download a file from the remote system, use the `get` command:

```bash theme={null}
sftp> get familypicture.jpg
```

If you need to download an entire directory recursively, add the `-r` flag:

```bash theme={null}
sftp> get -r Pictures/
```

For uploading a file to the remote host, use the `put` command:

```bash theme={null}
sftp> put myarchive.tgz
```

When you are finished with your SFTP session, exit by typing:

```bash theme={null}
sftp> bye
```

For more detailed usage of SFTP and its commands, consult the manual page:

```bash theme={null}
$ man sftp
```

<Callout icon="triangle-alert">
  Always ensure that you have the necessary permissions on both the local and remote systems to transfer files securely.
</Callout>

***

## Conclusion

Both SCP and SFTP provide robust solutions for secure file transfers. Choose SCP when you need a quick, one-off file copy, and opt for SFTP when you require a more interactive environment to navigate and transfer multiple files or directories.

For further insights, consider exploring additional resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/30ef7b0d-8b9f-4209-8b6c-e2991539a2bd" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/90f18e8f-3edc-4cb5-b7d4-1f8cd2d7750f" />
</CardGroup>
