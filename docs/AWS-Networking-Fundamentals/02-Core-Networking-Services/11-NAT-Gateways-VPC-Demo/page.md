# From your local machine:
ssh -i main.pem ec2-user@<instance-public-ip>

# On the EC2 instance:
ping -c 4 8.8.8.8

# Expected output:
# 64 bytes from 8.8.8.8: icmp_seq=1 ttl=53 time=1.58 ms
# ...
# 0% packet loss
```

Your web server (if running) should also be reachable over HTTP:

```bash theme={null}
curl http://<instance-public-ip>
```

***

## 5. Restricting Inbound NACL Rules to SSH Only

Now lock down the NACL so only SSH (port 22) is allowed inbound:

1. In **VPC** → **Network ACLs**, select your ACL.
2. Edit **Inbound Rules**:
   * Change **Rule 100** to allow only SSH (TCP port 22) from `0.0.0.0/0`.
   * The default deny will now block everything else.

Test SSH and HTTP:

```bash theme={null}
# SSH should still connect:
ssh -i main.pem ec2-user@<instance-public-ip>

# HTTP now times out:
curl http://<instance-public-ip>
# (No response)
```

***

## 6. Allowing HTTP and HTTPS Traffic

To re-enable web traffic, add two inbound rules after SSH:

* **Rule 101**: Allow HTTP (TCP 80) from `0.0.0.0/0`
* **Rule 120**: Allow HTTPS (TCP 443) from `0.0.0.0/0`

![The image shows an AWS Management Console screen for editing inbound rules in a VPC, with rules for SSH, HTTP, and HTTPS traffic. The rules specify protocols, port ranges, sources, and allow/deny actions.](https://kodekloud.com/kk-media/image/upload/v1752863279/notes-assets/images/AWS-Networking-Fundamentals-NACLs-Demo/aws-management-console-vpc-inbound-rules.jpg)

Verify web access again:

```bash theme={null}
curl http://<instance-public-ip>   # Should return your web page
```

> **lightbulb** If your second server doesn’t serve HTTP yet, install and start NGINX:

  ```bash theme={null}
  sudo yum install nginx -y
  sudo systemctl enable nginx
  sudo systemctl start nginx
  ```

  Refresh your browser on both instances’ IPs to confirm HTTP works.

***

## 7. Demonstrating Stateless Behavior

NACLs are stateless, so return traffic must be explicitly allowed. Even with outbound rules open, inbound return packets for ephemeral ports are blocked:

```bash theme={null}
ping -c 4 8.8.8.8
# 100% packet loss
```

To download packages, add a temporary inbound rule:

* **Rule 130**: Allow all traffic (for the duration of your download)

After installing, remove rule 130. This illustrates that both directions require explicit rules in a stateless firewall.

![The image shows the AWS Management Console interface for editing inbound rules in a VPC network ACL. It lists rules for SSH, HTTP, HTTPS, and a custom TCP port, all set to allow traffic from any source.](https://kodekloud.com/kk-media/image/upload/v1752863280/notes-assets/images/AWS-Networking-Fundamentals-NACLs-Demo/aws-management-console-vpc-acl-rules.jpg)

***

## 8. Using Explicit Deny Rules

Unlike security groups, NACLs support explicit **Deny** entries. For example, to block SSH from a specific CIDR:

1. Create **Rule 90**: Deny TCP port 22 from `1.0.0.0/24`.
2. Keep **Rule 100**: Allow TCP port 22 from `0.0.0.0/0` (evaluated after rule 90).

Traffic evaluation:

* SSH from `1.0.0.0/24` is denied by rule 90.
* SSH from all other IPs is allowed by rule 100.

![The image shows an AWS Management Console screen displaying Network ACLs with a list of inbound rules, including SSH, HTTP, and HTTPS protocols, along with their allow or deny statuses.](https://kodekloud.com/kk-media/image/upload/v1752863281/notes-assets/images/AWS-Networking-Fundamentals-NACLs-Demo/aws-management-console-network-acls-inbound-rules.jpg)

***

## Conclusion

In this demo we covered:

* Security groups are **stateful** and instance-level.
* NACLs are **stateless** and subnet-level.
* NACLs support both **Allow** and **Deny**, evaluated in ascending order.

Use security groups for per-instance controls and NACLs for broader subnet-based traffic filtering.

## References

* [AWS Network ACLs Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
* [AWS Security Groups](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html)
* [Nginx Installation on Amazon Linux 2](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-networking-fundamentals/module/406e4440-01a6-45f6-ab45-e14485d333c3/lesson/2bde7f3d-33aa-440a-969f-48a5cbb571e4)


# NAT Gateways VPC Demo

Source: https://notes.kodekloud.com/docs/AWS-Networking-Fundamentals/Core-Networking-Services/NAT-Gateways-VPC-Demo/page

This walkthrough explains how to configure an AWS NAT Gateway for internet access in a private subnet while blocking unsolicited inbound connections.

In this walkthrough, you’ll learn how to configure an AWS NAT Gateway to enable internet access for EC2 instances in a private subnet—while preventing unsolicited inbound connections from the internet. By the end, only instances that initiate outbound requests will receive responses.

## 1. Create a New VPC

1. Open the **VPC** console and select **Create VPC**.
2. Enter a **Name tag** (e.g., `demo-vpc`) and set the **IPv4 CIDR block** to `10.0.0.0/16`.
3. Leave IPv6 settings disabled and click **Create**.

![The image shows the AWS Management Console interface for creating a VPC, with options for setting the name tag, IPv4 CIDR block, and other configurations.](https://kodekloud.com/kk-media/image/upload/v1752863282/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-management-console-create-vpc.jpg)

## 2. Create a Private Subnet

This subnet will host your EC2 instance without a public IP.

* **Name**: `private-subnet`
* **Availability Zone**: e.g., `us-east-1b`
* **IPv4 CIDR block**: `10.0.1.0/24`

![The image shows the AWS Management Console interface for creating a subnet within a VPC. It includes fields for VPC ID, subnet name, availability zone, and IPv4 CIDR block.](https://kodekloud.com/kk-media/image/upload/v1752863283/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-management-console-create-subnet-vpc.jpg)

## 3. Launch an EC2 Instance in the Private Subnet

1. Navigate to the **EC2** console → **Launch Instance**.
2. Select the **Amazon Linux 2 AMI** (or your preferred AMI).
3. Under **Network settings**:
   * Choose your **demo-vpc** and the **private-subnet**.
   * Disable **Auto-assign Public IP**.
4. Configure or select a security group (default settings are fine).
5. Review and **Launch**. Name it `private-server`.

Because there’s no public IP, the instance cannot be reached directly from the internet.

![The image shows an AWS EC2 instance launch configuration screen, detailing network settings, security group options, and a summary of the instance specifications.](https://kodekloud.com/kk-media/image/upload/v1752863284/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-ec2-instance-launch-configuration.jpg)

## 4. Create and Attach an Internet Gateway

An Internet Gateway (IGW) is required to give public subnets internet access.

1. In the VPC console, go to **Internet Gateways** → **Create Internet Gateway**.
2. Name it `my-igw` and click **Create**.
3. Select the new IGW → **Actions** → **Attach to VPC** → choose `demo-vpc`.

![The image shows an AWS Management Console screen displaying the "Internet gateways" section, with one internet gateway listed as attached to a VPC.](https://kodekloud.com/kk-media/image/upload/v1752863286/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-management-console-internet-gateways-vpc.jpg)

## 5. Create a Public Subnet

This subnet will host the NAT Gateway and must have a route to the IGW.

* **Name**: `public-subnet`
* **Availability Zone**: same or different (e.g., `us-east-1b`)
* **IPv4 CIDR block**: `10.0.2.0/24`

![The image shows an AWS VPC dashboard with a notification indicating the successful creation of a subnet. The subnet details, including its ID and availability, are displayed.](https://kodekloud.com/kk-media/image/upload/v1752863288/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-vpc-dashboard-subnet-creation.jpg)

## 6. Configure Route Tables

You need two route tables: one public and one private.

> **lightbulb** Separate route tables help isolate internet-facing and internal traffic.

| Route Table Name    | Associated Subnet | Default Route Target        |
| ------------------- | ----------------- | --------------------------- |
| public-route-table  | public-subnet     | Internet Gateway (`my-igw`) |
| private-route-table | private-subnet    | (added after NAT creation)  |

### Steps

1. **Create** `public-route-table` → select `demo-vpc` → **Create**.
2. **Edit routes** → **Add route** `0.0.0.0/0` → Target: **Internet Gateway** → choose `my-igw` → **Save**.
3. **Associate** with `public-subnet`.
4. **Create** `private-route-table` → select `demo-vpc` → **Create**.
5. **Associate** with `private-subnet` (no default route yet).

![The image shows an AWS Management Console screen displaying details of a VPC route table, including route entries and their statuses. The route table has two routes, one for internet gateway access and another for local network access, both marked as active.](https://kodekloud.com/kk-media/image/upload/v1752863289/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-vpc-route-table-details.jpg)

## 7. Deploy a NAT Gateway

In a public subnet, NAT Gateways allow private instances to access the internet securely.

1. Go to **NAT Gateways** → **Create NAT Gateway**.
2. Name it `my-nat-gateway`.
3. Subnet: **public-subnet**.
4. Allocate a new **Elastic IP**.
5. Click **Create NAT Gateway**.

![The image shows an AWS Management Console screen displaying details of a newly created NAT gateway, which is currently in a pending state.](https://kodekloud.com/kk-media/image/upload/v1752863290/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-management-console-nat-gateway-pending.jpg)

You can also use the AWS CLI:

```bash theme={null}
aws ec2 create-nat-gateway \
  --subnet-id <public-subnet-id> \
  --allocation-id <eip-allocation-id>
```

## 8. Update the Private Route Table

After the NAT Gateway becomes **available**:

1. Open `private-route-table` → **Edit routes**.
2. **Add route** `0.0.0.0/0` → Target: **NAT Gateway** → select `my-nat-gateway`.
3. **Save**.

Now, instances in `private-subnet` will send outbound traffic through the NAT Gateway while remaining inaccessible from the internet.

## 9. Plan for High Availability

NAT Gateways are zonal resources. To avoid a single point of failure:

* Deploy one NAT Gateway per Availability Zone.
* Update each private route table to point to the NAT Gateway in its own AZ.

> **triangle-alert** If the AZ with your NAT Gateway goes down, all instances using it lose internet access.

![The image shows an AWS Management Console screen displaying details of a public subnet within a Virtual Private Cloud (VPC). It includes information such as the subnet ID, state, IPv4 CIDR, and availability zone.](https://kodekloud.com/kk-media/image/upload/v1752863292/notes-assets/images/AWS-Networking-Fundamentals-NAT-Gateways-VPC-Demo/aws-management-console-public-subnet-vpc.jpg)

## Links and References

* [Amazon VPC Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
* [AWS NAT Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
* [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/index.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/aws-networking-fundamentals/module/406e4440-01a6-45f6-ab45-e14485d333c3/lesson/d29b603d-a21e-4cd3-a744-265d55acd3c2)
