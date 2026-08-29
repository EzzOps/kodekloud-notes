# User privilege specification
root    ALL=(ALL:ALL) ALL

# Members of the admin group may gain root privileges
%admin  ALL=(ALL)       ALL

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL)   ALL

# Allow mark to run any command
mark    ALL=(ALL:ALL)   ALL

# Allow sarah to reboot the system
sarah   localhost=/usr/bin/shutdown -r now

# See sudoers(5) for more information on "#include" directives:
#includedir /etc/sudoers.d
```

| Field                | Description                                           | Example                          |
| -------------------- | ----------------------------------------------------- | -------------------------------- |
| User or Group        | Username (e.g., `mark`) or group (`%sudo`)            | `%admin`                         |
| Host(s)              | Hosts where the rule applies (usually `ALL`)          | `localhost`                      |
| Run-As Specification | User and group for command execution (in `(` and `)`) | `(ALL:ALL)`                      |
| Commands             | Allowed commands or `ALL` for full rights             | `/usr/bin/shutdown -r now`       |
| Comments             | Lines beginning with `#` are ignored                  | `# User privilege specification` |

> **triangle-alert** Never edit `/etc/sudoers` with a regular text editor. Syntax errors can lock out all sudo access. Always use `visudo`.

## Best Practices for sudo Configuration

* Grant only the commands necessary for a task
* Use group-based rules to simplify management
* Avoid `NOPASSWD` unless automation requires it
* Keep custom rules in `/etc/sudoers.d/` for modularity

## Hands-On Exercises

1. Create a test user:
   ```bash theme={null}
   sudo useradd -m bob
   sudo passwd bob
   ```
2. Add the user to the `sudo` group:
   ```bash theme={null}
   sudo usermod -aG sudo bob
   ```
3. Switch to `bob` and install a package:
   ```bash theme={null}
   su - bob
   sudo apt update && sudo apt install htop
   ```
4. Customize a rule in `/etc/sudoers.d/custom_rules` to allow `bob` to restart services without a password.

## Links and References

* [sudo Manual Page](https://www.sudo.ws/man/1.8.31/sudoers.man.html)
* [Visudo Documentation](https://linux.die.net/man/8/visudo)
* [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
* [Kali Linux Privilege Escalation Guide](https://www.kali.org/docs/practice/privilege-escalation/)

- [Watch Video](https://learn.kodekloud.com/user/courses/kubernetes-and-cloud-native-security-associate-kcsa/module/6da25ade-b162-485c-b9b9-f351990e99c2/lesson/95be0e42-0b15-4321-bd4c-41508664fd26)


# Artifact Repository and Image Security

Source: https://notes.kodekloud.com/docs/Kubernetes-and-Cloud-Native-Security-Associate-KCSA/Overview-of-Cloud-Native-Security/Artifact-Repository-and-Image-Security/page

This article discusses the importance of artifact repositories and image security in containerization, highlighting risks and best practices for managing container images.

## Containerization Benefits

Team A selected containerization for their CRM application to achieve:

* Portability
* Scalability
* Consistency
* Isolation
* Enhanced security

![The image illustrates a "Team A Scenario" focusing on containerization, highlighting key benefits such as portability, scalability, consistency, isolation, and security.](https://kodekloud.com/kk-media/image/upload/v1752880835/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Artifact-Repository-and-Image-Security/team-a-scenario-containerization-benefits.jpg)

## Risk of Untrusted Base Images

In the rush to deploy, Team A used a `latest`-tagged base image from Docker Hub without verifying its origin or maintenance status. While the container spun up successfully, the CRM soon experienced performance degradation and instability.

![The image illustrates a concept of software vulnerabilities, showing a document with a bug icon under a magnifying glass, labeled "Known Vulnerabilities," and mentions that Team A assumes it is secure with the latest tag, but it is not updated.](https://kodekloud.com/kk-media/image/upload/v1752880837/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Artifact-Repository-and-Image-Security/software-vulnerabilities-known-bug.jpg)

A deep dive revealed multiple unpatched CVEs in the `latest` image, which attackers exploited to compromise data integrity and leak customer information.

![The image illustrates vulnerabilities in software, highlighting a magnifying glass over a Docker logo with a bug icon, and mentions "Latest" and "Not Always Updated or Secure."](https://kodekloud.com/kk-media/image/upload/v1752880838/notes-assets/images/Kubernetes-and-Cloud-Native-Security-Associate-KCSA-Artifact-Repository-and-Image-Security/docker-vulnerabilities-magnifying-glass.jpg)

> **triangle-alert** Relying on the `latest` tag does not ensure up-to-date security patches. Image maintainers can assign it arbitrarily, leaving you exposed to risks.

## Integrating Vulnerability Scanning

To prevent future incidents, Team A added automated scanning tools into their CI/CD pipeline:

```bash theme={null}
