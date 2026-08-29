# Last Modified: Mon Mar 22 11:21:42 2021
#include <tunables/global>

/root/add_data.sh {
    #include <abstractions/base>
    #include <abstractions/bash>
    #include <abstractions/consoles>

    deny owner /proc/filesystems r,
    /root/add_data.sh r,
    /usr/bin/bash ix,
    /usr/bin/date mrix,
    /usr/bin/mkdir mrix,
    /usr/bin/tee mrix,
    owner /opt/app/ rw,
    owner /opt/app/data/ w,
    owner /opt/app/data/create.log w,
}
```

## Testing the Enforced Profile

To verify that the enforced profile restricts unauthorized access, modify the script to change the log file path from `/opt/app/data` to `/opt`. Update the script as follows:

```bash theme={null}
#!/bin/bash
data_directory=/opt
mkdir -p "${data_directory}"
echo "=> File created at $(date)" | tee "${data_directory}/create.log"
```

When you run the modified script:

```bash theme={null}
./add_data.sh
```

You should see an output similar to:

```plaintext theme={null}
tee: /opt/create.log: Permission denied
=> File created at Mon 22 Mar 2021 04:04:47 PM EDT
```

This confirms that while the script can output to the terminal, the AppArmor profile restricts write access only to the `/opt/app` directory, yielding a permission denied error when attempting to write directly to `/opt`.

## Working with Existing AppArmor Profiles

To load an existing profile, use the AppArmor parser command. If no output is returned, the profile has been successfully loaded.\
To disable a profile, use the same command with the `-r` flag and create a symlink to the profile in the `/etc/apparmor.d/disable` directory.

<Callout icon="lightbulb">
  Now that you've learned how to create and enforce AppArmor profiles for a custom application, you can explore securing applications running within Kubernetes pods using AppArmor for enhanced security.
</Callout>

This concludes the lesson on creating AppArmor profiles. Next, we will explore securing an application running inside a Kubernetes pod with AppArmor profiles.

Happy securing!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/093e196c-059d-4eac-8816-af343c5e0695" />
</CardGroup>


# Identify and Disable Open Ports

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/Identify-and-Disable-Open-Ports/page

This guide explores techniques to inspect a Linux system for open ports and methods to disable unnecessary ones for enhanced security and performance.

In this guide, we explore techniques to inspect a Linux system for open ports and methods to disable those that are unnecessary. By managing open ports, you can enhance your system's security and streamline network performance.

## Understanding Open Ports

When a process starts, it often binds to a port—an addressable location in the operating system that directs network traffic between applications. For example, TCP port 22 is typically dedicated to an SSH server process. Disabling unused ports minimizes potential security vulnerabilities.

## Using netstat to Check Active Ports

To determine which ports are actively listening for connections, you can use the `netstat` command. The following example shows active ports including port 22 for SSH, port 2379 for an etcd instance, and port 6443 for the Kubernetes API server, which are common on a Kubernetes control plane node:

```bash theme={null}
netstat -an | grep -w LISTEN
tcp        0      0 127.0.0.1:10248         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:10249         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:2379          0.0.0.0:*               LISTEN
tcp        0      0 10.53.64.6:2379         0.0.0.0:*               LISTEN
tcp        0      0 10.53.64.6:2380         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:42893         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:2381          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.11:46607        0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:8080            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:10257         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:10259         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp6       0      0 :::10250                :::*                    LISTEN
tcp6       0      0 :::6443                 :::*                    LISTEN
tcp6       0      0 :::10256                :::*                    LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
tcp6       0      0 :::8888                 :::*                    LISTEN
```

The output above identifies various services bound to different ports. For instance, port 53 is conventionally reserved for the Domain Name Server (DNS) and is used for both TCP and UDP traffic.

## Determining Port Usage

A straightforward way to verify the purpose of each port is by consulting the `/etc/services` file on Ubuntu-based systems. This file catalogs service names, protocols, and associated port numbers. For example, inspecting this file will confirm that port 53 is indeed allocated for DNS services.

<Callout icon="lightbulb">
  Before installing new software, it's critical to review which ports should remain open. Always consult the official documentation of the software—such as the kubeadm documentation for Kubernetes clusters—to understand the required ports.
</Callout>

## Disabling Unnecessary Ports

After identifying the open ports your system requires, you can proceed to disable or block the unused ones. This step is essential for bolstering your system's security and ensuring only necessary network interfaces are accessible.

## Additional References

For more detailed information, consider the following resources:

* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Kubernetes Documentation](https://kubernetes.io/docs/)
* [Docker Hub](https://hub.docker.com/)
* [Terraform Registry](https://registry.terraform.io/)

By following these guidelines, you can ensure that your Linux system is not only secure but also optimized for performance through effective port management.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/certified-kubernetes-security-specialist-cks/module/d67be5ee-871d-4435-a187-382610cb6a1f/lesson/266b4f76-b359-4005-8586-05c96690941c" />
</CardGroup>
