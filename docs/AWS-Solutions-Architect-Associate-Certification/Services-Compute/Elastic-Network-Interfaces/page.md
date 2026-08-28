# Example SSH command from a Windows command prompt
C:\Users\sanje\Documents\scratch\aws-demo> ssh -i main.pem ec2-user@50.16.240.9
     ,#
    ,_#
     |########
   ~~~  ____
      V~->  
    ~~~  /m/'
Last login: Thu Oct 12 04:43:18 2023 from 173.73.184.248
[ec2-user@ip-10-0-5-93 ~]$
```

Once logged in, view the network interfaces on your instance with the `ip add` command:

```bash theme={null}
[ec2-user@ip-10-0-5-93 ~]$ ip add
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet6 ::1/128 scope host noprefixroute
       valid_lft forever preferred_lft forever
2: enX0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP group default qlen 1000
    link/ether 0e:c1:c6:4e:41:39 brd ff:ff:ff:ff:ff:ff
    altname eni-0f8642cda59e33e
    altname device-number-0
    inet 10.0.5.93/20 metric 512 brd 10.0.15.255 scope global dynamic enX0
       valid_lft 3291sec preferred_lft 3291sec
    inet6 fe80::cc1:c6ff:fe4e:4139/64 scope link
       valid_lft forever preferred_lft forever
3: enX1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP group default qlen 1000
    link/ether 0e:c4:fc:6e:60:3c brd ff:ff:ff:ff:ff:ff
    altname eni-014935bd661362d75
    altname device-number-1
    inet 10.0.0.17/20 metric 522 brd 10.0.15.255 scope global dynamic enX1
       valid_lft 3548sec preferred_lft 3548sec
    inet6 fe80::fcff:fe6e:603c/64 scope link
       valid_lft forever preferred_lft forever
[ec2-user@ip-10-0-5-93 ~]$
```

The output lists the loopback interface and the two attached network interfaces. Notice that only private IP addresses are present because AWS uses network address translation (NAT) to map the public Elastic IPs—thus keeping the public IPs hidden from the instance itself.

<Callout icon="lightbulb">
  Network interfaces can be detached from a running instance via the instance's actions menu. Detached interfaces retain their IP addresses and security configurations, allowing you to attach them to another instance without reconfiguration. This is especially useful for maintenance and scaling.
</Callout>

This separation between EC2 instances and their network configurations offers a robust and scalable method for managing your AWS cloud networking resources.

That concludes our demonstration. We hope this lesson on AWS network interfaces has been both informative and practical for managing your EC2 networking setup.

## Additional Resources

* [AWS EC2 Documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/)
* [AWS Networking Concepts](https://aws.amazon.com/networking/)

Happy networking!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/3a08896e-0be8-4f42-8ea8-ef51193c1757" />
</CardGroup>


# Elastic Network Interfaces

Source: https://notes.kodekloud.com/docs/AWS-Solutions-Architect-Associate-Certification/Services-Compute/Elastic-Network-Interfaces/page

This article explores Elastic Network Interfaces in Amazon EC2, detailing their properties, benefits, and configurations for flexible network management.

In this article, we delve into Elastic Network Interfaces (ENIs) in [Amazon EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2). An ENI is a virtual network interface that can be attached to EC2 instances within a VPC. It decouples network configurations from the compute instances, enabling you to seamlessly move an interface—with all its associated settings such as IP addresses, security groups, and more—across different instances.

## Key Properties of ENIs

An ENI represents a logical version of a physical network card in a VPC. Its main properties include:

* A primary private IPv4 address automatically selected from the subnet's CIDR block.
* Optionally, a primary IPv6 address.
* Secondary private IPv4 addresses.
* The ability to associate an Elastic IP address.
* Public IP address allocation when enabled.
* A unique MAC address.
* Configurable flags like the source/destination check.

<Frame>
  ![The image illustrates a network architecture diagram showing an Elastic Network Interface within a VPC, including a public and private IP, a subnet, and security components.](https://kodekloud.com/kk-media/image/upload/v1752864957/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Elastic-Network-Interfaces/network-architecture-diagram-vpc.jpg)
</Frame>

## Primary vs. Secondary ENIs

When you launch an [Amazon EC2](https://learn.kodekloud.com/user/courses/amazon-elastic-compute-cloud-ec2) instance, it automatically receives a primary ENI, typically named Ethernet0. This primary ENI comes with a primary private IPv4 address sourced from the associated subnet. It remains attached to the instance for its lifetime and cannot be detached—even during instance stops or restarts—and is deleted when the instance is terminated. Additionally, if your subnet configuration auto-assigns public IP addresses, this ENI will obtain a public IP address as well.

<Callout icon="lightbulb">
  The primary ENI is permanently linked to its instance. Secondary ENIs, however, can be detached and reattached, making them ideal for scenarios like network appliances or management networks.
</Callout>

Secondary ENIs offer enhanced flexibility:

* They can be attached to or detached from EC2 instances as needed.
* They can host a primary private IP along with multiple secondary private IP addresses.
* They may have different security groups compared to the primary ENI, allowing for distinct network and security configurations.

<Frame>
  ![The image compares primary and secondary Elastic Network Interfaces (ENI), showing their associated public and private IP addresses. The primary ENI (eth0) has IPs 34.191.162.238 (public) and 10.0.0.35 (private), while the secondary ENI (eth1) has IPs 54.35.215.118 (public) and 10.0.1.69 (private).](https://kodekloud.com/kk-media/image/upload/v1752864958/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Elastic-Network-Interfaces/eni-ip-addresses-comparison.jpg)
</Frame>

Remember, while the primary ENI is immovable, secondary ENIs persist even when an instance is stopped or restarted, offering the ability to transfer them between instances when necessary.

<Frame>
  ![The image illustrates the concept of Elastic Network Interfaces (ENI) in Amazon EC2, showing a central EC2 instance connected to one primary and two secondary ENIs.](https://kodekloud.com/kk-media/image/upload/v1752864959/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Elastic-Network-Interfaces/elastic-network-interfaces-ec2-diagram.jpg)
</Frame>

## Elastic IP Addresses and Security Groups

You can associate an Elastic IP address with an ENI, which guarantees that the IP remains constant even if the ENI is detached and later reattached to a different instance. Moreover, security groups can be directly linked to an ENI, allowing granular control over the traffic at the interface level.

## Benefits of Using ENIs

ENIs offer several powerful features for designing flexible and secure network architectures on AWS:

| Feature                      | Benefit                                                                    |
| ---------------------------- | -------------------------------------------------------------------------- |
| Multiple IP Addresses        | Support for both primary and secondary private IPv4 addresses              |
| Elastic IP Association       | Maintain static IP configurations regardless of instance changes           |
| Enhanced Security            | Assign different security groups directly at the interface level           |
| Hot Attach/Detach Capability | Attach or detach ENIs without stopping or restarting the instance          |
| Flow Logs Configuration      | Capture detailed IP traffic information for monitoring and troubleshooting |

<Frame>
  ![The image lists five features: Multiple IP Addresses, Elastic IP Addresses, Security, Hot Attach and Detach, and Network Flow Logs, each with an icon.](https://kodekloud.com/kk-media/image/upload/v1752864959/notes-assets/images/AWS-Solutions-Architect-Associate-Certification-Elastic-Network-Interfaces/features-multiple-ip-elastic-security.jpg)
</Frame>

## Summary

ENIs are robust and versatile components of Amazon EC2 that help you:

* Decouple network configurations from compute instances.
* Leverage multiple IP addressing schemes.
* Configure static IP addresses through Elastic IP associations.
* Implement specialized security configurations using dedicated security groups.
* Enhance operational flexibility by allowing dynamic attachment and detachment of network interfaces.

For more detailed guidance and best practices on AWS networking, explore the [Amazon EC2 documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-solutions-architect-associate-certification/module/afe0c951-fe76-47f2-9fc4-18858721be70/lesson/0b43e510-b3b3-4f09-8ebb-fceb9b6c92b9" />
</CardGroup>
