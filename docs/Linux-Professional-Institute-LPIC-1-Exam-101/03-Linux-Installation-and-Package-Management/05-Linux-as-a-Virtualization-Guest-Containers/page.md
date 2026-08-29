# For BIOS-based systems
grub2-mkconfig -o /boot/grub2/grub.cfg

# For UEFI-based systems
grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
```

***

## 5. Install GRUB to the Disk (BIOS Mode)

1. Identify your disks:

   ```bash theme={null}
   lsblk
   ```

   Example output:

   ```plain theme={null}
   NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
   sda      8:0    0   20G  0 disk
   ├─sda1   8:1    0    1G  0 part /boot
   ├─sda2   8:2    0    2G  0 part [SWAP]
   └─sda3   8:3    0   17G  0 part /
   ```

   Here, `/dev/sda` is our target disk.

2. Install GRUB to the MBR:

   ```bash theme={null}
   grub2-install /dev/sda
   ```

You should see:

```plain theme={null}
Installing for i386-pc platform.
Installation finished. No error reported.
```

<Callout icon="triangle-alert">
  Ensure you specify the correct disk (e.g., `/dev/sda`). Installing GRUB to the wrong device can overwrite another OS or data.
</Callout>

***

## 6. Exit Rescue Mode and Reboot

Exit the chroot environment and reboot the system:

```bash theme={null}
exit     # leaves chroot
exit     # leaves rescue shell
```

Remove the installation media when prompted so the machine boots from the hard drive.

***

## 7. Customize GRUB Settings

Once back in your CentOS Stream system, you can fine-tune GRUB by editing `/etc/default/grub`:

```bash theme={null}
sudo vi /etc/default/grub
```

A typical configuration:

```ini theme={null}
GRUB_TIMEOUT=5
GRUB_DISTRIBUTOR="$(sed 's, release .*$,,g' /etc/system-release)"
GRUB_DEFAULT=saved
GRUB_DISABLE_SUBMENU=true
GRUB_TERMINAL_OUTPUT="console"
GRUB_CMDLINE_LINUX="crashkernel=auto resume=UUID=… rhgb quiet"
GRUB_DISABLE_RECOVERY="true"
GRUB_ENABLE_BLSCFG=true
```

### Change the Boot Timeout

To reduce the wait time:

```diff theme={null}
-GRUB_TIMEOUT=5
+GRUB_TIMEOUT=1
```

Save and exit (`:wq` in `vi`).

***

## 8. Regenerate Configuration After Edits

Apply your changes by regenerating `grub.cfg`:

```bash theme={null}
# BIOS
sudo grub2-mkconfig -o /boot/grub2/grub.cfg

# UEFI
sudo grub2-mkconfig -o /boot/efi/EFI/centos/grub.cfg
```

Look for:

```plain theme={null}
Generating grub configuration file ...
done
```

***

## 9. Verify and Test

Reboot one final time:

```bash theme={null}
sudo reboot
```

You should see the GRUB menu for the new timeout duration, and your kernel options will reflect any changes made in `/etc/default/grub`.

***

## References

* [CentOS Stream Documentation](https://docs.centos.org/)
* [GNU GRUB Manual](https://www.gnu.org/software/grub/manual/)
* [Red Hat Enterprise Linux Booting](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/04c4f60d-8cda-4174-a12d-7147437ee42d" />
</CardGroup>


# Linux as a Virtualization Guest Containers

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Linux-as-a-Virtualization-Guest-Containers/page

Hands-on guide to container management using Podman and Docker compatible CLI commands covering installation, pulling images, running and naming containers, port mapping, stopping and cleaning images.

Hello — this lesson demonstrates practical container management and configuration using Docker-compatible tooling (Podman on RHEL-based systems). We'll cover why containers are useful, how to install and configure Podman, and basic workflows: pulling images, running containers, mapping ports, stopping/removing containers, and cleaning up images.

<Frame>
  <img alt="A dark presentation slide reading &#x22;Demo — Manage and configure containers&#x22; with a small film-camera icon in the center-right and a &#x22;KodeKloud&#x22; logo in the top-right corner." />
</Frame>

Why use containers?

* Containers package an application and everything it needs (binaries, libraries, configuration, logs, and data) together. This eliminates fragmented configurations across /etc, /var/lib, /var/log, etc., and makes migration or replication to other hosts predictable and repeatable.
* Example: A MariaDB server inside a container keeps the daemon, configuration files, databases, and logs together. Copy or pull that container on another host and it behaves the same way.

Installing Docker-compatible tooling

* On modern RHEL-based distributions (CentOS Stream, RHEL) Docker packages may not be available; Podman is the recommended replacement. Podman is daemonless, OCI-compliant, and provides Docker-compatible CLI behavior via the podman-docker wrapper.

Install Podman with dnf:

```bash theme={null}
sudo dnf install podman
```

The podman-docker package provides docker CLI compatibility so many existing Docker commands (docker pull, docker run, docker ps, etc.) work unchanged.

<Callout icon="lightbulb">
  Podman includes a Docker-CLI compatibility wrapper (podman-docker). You can use `docker ...` commands, or call `podman` directly. Podman is daemonless and integrates with systemd and rootless workflows.
</Callout>

Configuring default registries (optional)

* Container tools consult /etc/containers/registries.conf to determine search registries for unqualified image names. To prefer docker.io only, set the unqualified-search-registries array to \["docker.io"].

Example excerpt from /etc/containers/registries.conf:

```toml theme={null}
