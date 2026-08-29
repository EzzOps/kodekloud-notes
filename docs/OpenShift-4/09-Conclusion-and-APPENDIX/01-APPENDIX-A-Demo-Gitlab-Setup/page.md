# APPENDIX A Demo Gitlab Setup

Source: https://notes.kodekloud.com/docs/OpenShift-4/Conclusion-and-APPENDIX/APPENDIX-A-Demo-Gitlab-Setup/page

This article provides a step-by-step guide to setting up a local GitLab instance on a CentOS virtual machine using Oracle VirtualBox and Docker.

Welcome to this comprehensive guide on setting up a local GitLab instance on your laptop. In this article, you'll learn how to deploy a CentOS-based virtual machine using Oracle VirtualBox, configure a static IP address, and install GitLab through Docker. This step-by-step guide is perfect for developers looking to create a local development environment.

***

## Deploying the CentOS Virtual Machine

Begin by downloading the CentOS VirtualBox image from [osboxes.org](http://www.osboxes.org). Browse the list of available operating systems and select the 64-bit CentOS VirtualBox image. After downloading the VDI file, extract it to a folder on your computer.

<Frame>
  ![The image shows a webpage from osboxes.org offering CentOS VM images for download, with options for VirtualBox and VMware. It includes download links, file sizes, and SHA256 checksums, along with advertisements and recent posts.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882617/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/centos-vm-images-download-osboxes.jpg)
</Frame>

Next, open Oracle VirtualBox and click the "New" button to create a new virtual machine. Choose "Other Linux (64-bit)" as the operating system and allocate at least 2 GB of memory. When prompted for the hard disk, select the "Use existing" option and locate the extracted VDI file.

<Frame>
  ![The image shows the Oracle VM VirtualBox Manager interface with a virtual machine named "minishift" running, and a "Create Virtual Machine" window open, where a user is selecting the operating system type and version.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882618/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/oracle-vm-virtualbox-minishift-interface.jpg)
</Frame>

Before starting the virtual machine, you need to configure the networking settings to enable a static IP address. Since VirtualBox uses DHCP by default, create a host-only network adapter without DHCP support. Open the global settings, navigate to the Host Network Manager, add a new adapter, and uncheck the "Enable DHCP Server" option. Take note of the configured IP address and range.

<Frame>
  ![The image shows the Oracle VM VirtualBox Manager interface, specifically the Host Network Manager window, displaying details of two host-only Ethernet adapters with their respective IP addresses and DHCP server status.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882619/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/oracle-vm-virtualbox-host-network-manager.jpg)
</Frame>

Then, adjust the CentOS template settings:

* Increase the CPU count to two.
* Set the first network adapter to "Bridged Adapter" to access the Internet through your wireless router.
* Attach the second adapter to the previously created host-only network to allow for a static IP assignment.

<Frame>
  ![The image shows the network settings of a virtual machine in VirtualBox, with the network adapter set to a bridged adapter using an Intel Dual Band Wireless-AC 7265.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882621/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/virtualbox-network-settings-bridged-adapter.jpg)
</Frame>

Power on the CentOS template. During boot-up, you’ll be prompted to accept the license agreement. Log in for the first time using the credentials provided on osboxes.org (the default password is "osboxes.org").

<Frame>
  ![The image shows the Oracle VM VirtualBox Manager with a CentOS 7 Linux virtual machine running, displaying a license agreement window.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882622/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/oracle-vm-virtualbox-centos7-license.jpg)
</Frame>

Once the initial configuration is complete, shut down the virtual machine. Right-click on the CentOS template and select "Clone" to create a new linked clone named "GitLab." Ensure you check the "Reset MAC address" option so that the clone receives a unique MAC address. Power on the cloned "GitLab" VM and log in again using the "osboxes.org" password.

<Frame>
  ![The image shows a VirtualBox interface with a dialog box for cloning a virtual machine, offering options for a full or linked clone.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882624/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/virtualbox-clone-dialog-box.jpg)
</Frame>

***

## Configuring a Static IP Address

After logging into the GitLab VM, open a terminal and run the command `ifconfig` to view the network interfaces. You might observe that the host-only adapter (commonly named enp0s8) does not have an IP address assigned. To assign a static IP, create a new network script for that interface.

1. Navigate to the network scripts directory:

   ```bash theme={null}
   cd /etc/sysconfig/network-scripts
   ```

2. Copy the default loopback script as a template for the host-only adapter:

   ```bash theme={null}
   sudo cp ifcfg-lo ifcfg-enp0s8
   sudo vi ifcfg-enp0s8
   ```

3. Update the file with the following configuration (replace IP values as desired):

   ```bash theme={null}
   DEVICE=enp0s8
   IPADDR=192.168.56.150
   NETMASK=255.255.255.0
   NETWORK=192.168.56.0
   BROADCAST=192.168.56.255
   ONBOOT=yes
   NAME=enp0s8
   ```

4. Save the file and restart the network service:

   ```bash theme={null}
   sudo service network restart
   ifconfig enp0s8
   ```

The output should now display an IP address similar to:

```plaintext theme={null}
inet 192.168.56.150  netmask 255.255.255.0  broadcast 192.168.56.255
```

<Callout icon="lightbulb">
  Assigning a static IP address ensures reliable connectivity and proper network routing for your GitLab setup.
</Callout>

***

## Installing GitLab

To install GitLab, start by preparing your system with the necessary packages. For additional details, refer to the [GitLab installation guide](https://about.gitlab.com/install/).

1. Install required packages:

   ```bash theme={null}
   sudo yum install -y curl policycoreutils-python openssh-server
   sudo systemctl enable sshd
   sudo systemctl start sshd
   sudo firewall-cmd --permanent --add-service=http
   sudo systemctl reload firewalld
   ```

2. Install Postfix to handle email notifications:

   ```bash theme={null}
   sudo yum install postfix
   sudo systemctl enable postfix
   sudo systemctl start postfix
   ```

3. Deploy GitLab using Docker. If Docker is not installed, use the official Docker installation script:

   ```bash theme={null}
   curl -fsSL get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

4. Once Docker is installed, start the Docker service and deploy the GitLab container using one of the following commands. Use the first command for standard systems or the second if SELinux is enabled.

   Standard deployment:

   ```bash theme={null}
   sudo docker run --detach \
     --hostname gitlab.example.com \
     --publish 443:443 --publish 80:80 --publish 22:22 \
     --name gitlab \
     --restart always \
     --volume /srv/gitlab/config:/etc/gitlab \
     --volume /srv/gitlab/logs:/var/log/gitlab \
     --volume /srv/gitlab/data:/var/opt/gitlab \
     gitlab/gitlab-ce:latest
   ```

   For systems with SELinux enabled:

   ```bash theme={null}
   sudo docker run --detach \
     --hostname gitlab.example.com \
     --publish 443:443 --publish 80:80 --publish 22:22 \
     --name gitlab \
     --restart always \
     --volume /srv/gitlab/config:/etc/gitlab:Z \
     --volume /srv/gitlab/logs:/var/log/gitlab \
     --volume /srv/gitlab/data:/var/opt/gitlab \
     gitlab/gitlab-ce:latest
   ```

Make sure that the hostname reflects the fully qualified domain name (FQDN) or the static IP address of your CentOS virtual machine.

Allow a few minutes for GitLab to initialize. You can monitor the initialization process using:

```bash theme={null}
sudo docker logs -f gitlab
```

When GitLab prompts you to change the default password at first login, update it to secure your access. Log in with the username "root" and your new secure password.

<Frame>
  ![The image shows a GitLab Community Edition sign-in page with a prompt asking if the user wants to save their password using Google Smart Lock.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882625/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/gitlab-sign-in-google-smart-lock.jpg)
</Frame>

After successful configuration, the GitLab dashboard will be displayed, allowing you to create projects, manage groups, and configure additional settings.

<Frame>
  ![The image shows a GitLab dashboard with options to create a project, create a group, add people, and configure GitLab. It includes a navigation bar with links to projects, groups, activity, milestones, and snippets.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882626/notes-assets/images/OpenShift-4-APPENDIX-A-Demo-Gitlab-Setup/gitlab-dashboard-projects-groups-navigation.jpg)
</Frame>

<Callout icon="lightbulb">
  Be sure to update the default credentials as soon as you log in to enhance the security of your GitLab installation.
</Callout>

***

Congratulations! You have now set up a fully functional local GitLab environment on your laptop. Enjoy your new development setup and happy coding!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/openshift-4/module/d84e1350-21eb-421e-87d0-2d7bf019360f/lesson/90d6cdc7-a86a-48d6-baa1-3081b4d3ecc1" />
</CardGroup>
