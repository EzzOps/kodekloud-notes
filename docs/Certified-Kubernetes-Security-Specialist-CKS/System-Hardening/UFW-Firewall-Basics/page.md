# UFW Firewall Basics

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Security-Specialist-CKS/System-Hardening/UFW-Firewall-Basics/page

This article introduces UFW, a user-friendly firewall interface for managing Linux firewall rules on an Ubuntu server.

In this lesson, we introduce UFW (Uncomplicated Firewall), a user-friendly interface designed to simplify managing Linux firewall rules. We'll walk through configuring UFW on an Ubuntu server (app01) to restrict network access and secure your environment.

Imagine a setup where access to app01 must be limited. In this scenario, only the jump server with IP address 172.16.238.5 is allowed to establish SSH connections. This jump server is the primary access point for system administrators. Additionally, app01 hosts a web server on port 80, which needs to be accessible not only from the jump server but also from internal clients within the IP range 172.16.100.0/28.

<Frame>
  ![The image illustrates a network setup with an Admin Jump Server and Internal Users accessing an application server (app01) via SSH, HTTP, and TCP protocols.](https://kodekloud.com/kk-media/image/upload/v1752871753/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-UFW-Firewall-Basics/frame_40.jpg)
</Frame>

All other ports on app01 must remain closed to inbound traffic. To achieve this, we leverage Netfilter, the Linux kernel's internal packet filtering system. Although IPTables is a common command-line tool for managing firewall rules, its complexity often demands a simpler solution. UFW serves as an intuitive front-end for configuring IPTables.

<Frame>
  ![The image shows a comparison between "iptables" and "ufw (Uncomplicated Firewall)" under the title "Install UFW."](https://kodekloud.com/kk-media/image/upload/v1752871754/notes-assets/images/Certified-Kubernetes-Security-Specialist-CKS-UFW-Firewall-Basics/frame_80.jpg)
</Frame>

## Inspecting Active Ports

Before configuring UFW, log in via SSH to app01 and inspect the active listening ports using the netstat utility. Run the following command to confirm that SSH (port 22) and HTTP (port 80) are active, along with port 8080 which should be blocked from inbound connections:

```bash theme={null}
netstat -an | grep -w LISTEN
```

Expected output:

```plaintext theme={null}
tcp        0      0 0.0.0.0:22          0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:80           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:8080         0.0.0.0:*               LISTEN
```

## Installing UFW

To install UFW on app01, start by updating your package list and then installing UFW:

```bash theme={null}
apt-get update
