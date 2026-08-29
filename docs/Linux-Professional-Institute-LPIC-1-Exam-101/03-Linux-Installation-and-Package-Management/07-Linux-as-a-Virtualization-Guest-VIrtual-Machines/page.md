# Update and upgrade packages on first boot
apt_update: true
apt_upgrade: true
# Install Nginx web server
packages:
  - nginx
```

<Callout icon="triangle-alert">
  The line `#cloud-config` must begin at the very start of the file with no leading whitespace.
</Callout>

## References

* [Xen Project](https://xenproject.org/)
* [Linux KVM](https://www.linux-kvm.org/)
* [Oracle VM VirtualBox](https://www.virtualbox.org/)
* [cloud-init Documentation](https://cloud-init.io/)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/linux-professional-institute-lpic-1-exam-101/module/78ca0fa8-2083-408a-bf8a-2775b09fbf1d/lesson/8aa0f6ec-d0f5-4318-a577-d65a23a7440c" />
</CardGroup>


# Linux as a Virtualization Guest VIrtual Machines

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/Linux-Installation-and-Package-Management/Linux-as-a-Virtualization-Guest-VIrtual-Machines/page

Learn to manage virtual machines on Linux using QEMU-KVM and Libvirt’s virsh CLI for virtualization and cloud platform support.

In this guide, you’ll learn how to manage virtual machines (VMs) on Linux using QEMU-KVM and Libvirt’s `virsh` CLI. By the end, you will be able to install dependencies, define VM domains via XML, control VM lifecycle, adjust resources, and clean up definitions—all from the command line. This workflow is fundamental for self-hosted virtualization and supports major cloud platforms like [AWS](https://aws.amazon.com), [DigitalOcean](https://www.digitalocean.com), and [Google Cloud](https://cloud.google.com).

Example: A single Linux server with 64 CPU cores and 1 TiB RAM can host dozens of isolated VMs, each with its own dedicated vCPU and memory allocation.

***

## 1. Installing Dependencies

Install QEMU, KVM, and Libvirt tools:

```bash theme={null}
sudo dnf install -y qemu-kvm libvirt
```

* **qemu-kvm**: Hardware-accelerated virtualization
* **libvirt**: API and utilities for managing VMs

<Callout icon="lightbulb">
  You may also need to start and enable the libvirtd service:

  ```bash theme={null}
  sudo systemctl enable --now libvirtd
  ```
</Callout>

***

## 2. Defining a Virtual Machine Domain

Libvirt uses XML to describe VM configurations (called *domains*). Create a file named `testmachine.xml`:

```bash theme={null}
vim testmachine.xml
```

Paste this minimal configuration:

```xml theme={null}
<domain type="kvm">
  <name>TestMachine</name>
  <memory unit="GiB">1</memory>
  <vcpu>1</vcpu>
  <os>
    <type arch="x86_64">hvm</type>
  </os>
</domain>
```

This sets:

* **Name**: TestMachine
* **Memory**: 1 GiB
* **vCPUs**: 1
* **OS**: Hardware VM on x86\_64

Save and exit.

***

## 3. Defining and Listing Domains

Register the domain with Libvirt:

```bash theme={null}
virsh define testmachine.xml
```

Expected output:

```text theme={null}
Domain 'TestMachine' defined from testmachine.xml
```

List all domains, including inactive:

```bash theme={null}
virsh list --all
```

Sample:

| Id | Name        | State    |
| -- | ----------- | -------- |
| -  | TestMachine | shut off |

<Callout icon="lightbulb">
  Omit `--all` to list only running domains.
</Callout>

***

## 4. VM Lifecycle Management

Use the following commands to control the VM. See the quick reference table below.

| Action            | Command                      |
| ----------------- | ---------------------------- |
| Start             | `virsh start TestMachine`    |
| Graceful reboot   | `virsh reboot TestMachine`   |
| Forced reset      | `virsh reset TestMachine`    |
| Graceful shutdown | `virsh shutdown TestMachine` |
| Forced power-off  | `virsh destroy TestMachine`  |

```bash theme={null}
