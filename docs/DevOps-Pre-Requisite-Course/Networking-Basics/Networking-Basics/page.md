# Networking Basics

Source: https://notes.kodekloud.com/docs/DevOps-Pre-Requisite-Course/Networking-Basics/Networking-Basics/page

This lesson explores fundamental networking concepts including switching, routing, gateways, and DNS configurations on Linux for device communication.

In this lesson, we explore the fundamental concepts of networking, including switching, routing, gateways, and DNS configurations on Linux. These core topics form the building blocks for understanding how devices communicate over a network.

<Frame>
  ![The image lists networking prerequisites: Switching, Routing, Default Gateway, and DNS Configurations on Linux.](https://kodekloud.com/kk-media/image/upload/v1752873508/notes-assets/images/DevOps-Pre-Requisite-Course-Networking-Basics/frame_10.jpg)
</Frame>

Imagine you have two computers (or VMs) that need to communicate. Both systems are connected to a switch, and each host requires an interface—either physical or virtual—to establish that connection. To view the available interfaces on a Linux host, run:

```bash theme={null}
ip link
