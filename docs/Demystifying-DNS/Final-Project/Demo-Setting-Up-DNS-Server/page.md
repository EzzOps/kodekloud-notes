# Demo Setting Up DNS Server

Source: https://notes.kodekloud.com/docs/Demystifying-DNS/Final-Project/Demo-Setting-Up-DNS-Server/page

This guide demonstrates how to configure a multi-node DNS setup with two nameservers and one webserver acting as a client.

In this guide, we will demonstrate how to configure a multi-node DNS setup consisting of two nameservers and one webserver that also acts as a client. The configuration details are as follows:

• node-01: Primary nameserver\
• node-02: Secondary nameserver\
• node-03: Webserver running an application (and acting as a client)

Below is an illustration of the multi-node DNS setup:

<Frame>
  ![The image illustrates a multi-node DNS setup with three nodes: a primary nameserver, a secondary nameserver, and a web nameserver, along with a client icon.](https://kodekloud.com/kk-media/image/upload/v1752873237/notes-assets/images/Demystifying-DNS-Demo-Setting-Up-DNS-Server/multi-node-dns-setup-illustration.jpg)
</Frame>

***

## Primary Nameserver Setup (node-01)

Begin by installing and configuring BIND9 on node-01, which will serve as the primary nameserver.

### 1. Install and Start BIND9

Start the BIND9 service:

```bash theme={null}
sudo systemctl start bind9
```

### 2. Configure the Zone File

Edit the zone configuration file (typically `named.conf.local`) to specify the zone information. In this example, our domain is `multinode.kodekloud.lab` and its zone file is stored in `/etc/bind`. The configuration should indicate that node-01 is the primary (master) server for the zone:

```plaintext theme={null}
zone "multinode.kodekloud.lab" {
    type master;
    file "/etc/bind/db.multinode.kodekloud.lab";
};
```

<Callout icon="lightbulb">
  Gather the IP addresses for node-01 and node-02 before updating the zone file. These IP addresses will be used within the zone file.
</Callout>

### 3. Verify IP Addresses

Run the following commands to check the IP addresses of node-01 and node-02:

```bash theme={null}
