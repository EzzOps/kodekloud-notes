# EC2 Storage

Source: https://notes.kodekloud.com/docs/Amazon-Elastic-Compute-Cloud-EC2/Basics-of-EC2/EC2-Storage/page

Amazon EC2 offers various storage solutions with unique performance, durability, and cost characteristics to meet application requirements.

Amazon EC2 provides flexible, cost-effective, and easy-to-use storage solutions for your compute instances. Each option offers a unique combination of performance, durability, and cost. You can mix and match these storage types to meet your application’s requirements.

Common EC2 storage options:

* Instance Store
* Amazon Elastic Block Store (EBS)
* Amazon Elastic File System (EFS)

***

## 1. Instance Store

Instance Store volumes are temporary, high-performance disks physically attached to the host server. They deliver very low-latency I/O but are **ephemeral**.

> **triangle-alert** Data on an Instance Store is lost if the instance stops, hibernates, or terminates. Use it only for non-persistent workloads.

Key characteristics:

* Ephemeral storage tied to instance lifecycle
* Ideal for scratch data, buffers, and caches
* Automatic deletion on stop/terminate (reboot retains data)

Use cases:

* Temporary caches (e.g., in-memory databases, processing buffers)
* Scratch disks for big data workloads
* High-speed swap or buffer space

***

## 2. Amazon Elastic File System (EFS)

Amazon EFS is a fully managed, elastic NFS file system that can be mounted concurrently by multiple EC2 instances across Availability Zones.

> **lightbulb** EFS scales automatically—you pay only for the storage you consume.

Features:

* Elastic capacity: grows and shrinks as you add or remove files
* Shared access: mount the same file system on multiple instances
* Fully managed: AWS handles provisioning, patching, and maintenance
* Supports NFSv4.1 and NFSv4.2 protocols

Common commands:

```bash theme={null}
