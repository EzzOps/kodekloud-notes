# Auto Lock

Source: https://notes.kodekloud.com/docs/Docker-Certified-Associate-Exam-Course/Docker-Swarm/Auto-Lock/page

This article explains how to secure a Docker Swarm cluster using auto-lock for key management.

Docker Swarm automatically stores two critical keys in the manager’s in-memory keystore by default:

* **Raft Encryption Key**: Encrypts on-disk Raft logs
* **TLS Key**: Secures communication between Swarm nodes

Enabling **auto-lock** moves key management out of the daemon’s memory. This lets you store keys in a hardware security module (HSM) or a dedicated key management service (KMS).

> **triangle-alert** When you enable auto-lock, Swarm generates a one-time unlock key. Store it in a secure password manager—without it, you cannot unlock your manager after a restart.

## Enable Auto-Lock

You can turn on auto-lock either during cluster initialization or on an existing Swarm:

```bash theme={null}
