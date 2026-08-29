# Restore build artifacts if they exist
if [ "$(ls /tmp/s2i/artifacts/ 2>/dev/null)" ]; then
  mv /tmp/s2i/artifacts/* $HOME/.
fi

# Move the application source
mv /tmp/s2i/src $HOME/src

# Build application artifacts
pushd ${HOME}
make all

# Install the artifacts
make install
popd
```

In this script, all contents are initially unpacked into the default directory. The source code is then relocated, the build artifacts are created using `make`, and finally, the artifacts are installed. This basic process demonstrates the powerful automation capabilities of S2I for container image creation.

## Conclusion

S2I streamlines the container image build process by allowing you to focus on your source code while the system handles the heavy lifting. This approach provides a secure, efficient, and standardized method for creating container images ready for modern orchestration platforms.

For more detailed information, refer to the [OpenShift Container Platform documentation](https://docs.openshift.com/container-platform/latest/), which provides extensive details on S2I scripts and configuration.

![The image shows a section of the Red Hat OpenShift documentation, specifically focusing on S2I (Source-to-Image) requirements, with a table listing scripts and their descriptions.](https://kodekloud.com/kk-media/image/upload/v1752882615/notes-assets/images/OpenShift-4-S2I/openshift-s2i-requirements-table.jpg)

> **lightbulb** Leveraging S2I enables developers and DevOps engineers to integrate code changes seamlessly into production-ready container images, benefiting from automated processes, enhanced security, and optimized build times.

- [Watch Video](https://learn.kodekloud.com/user/courses/openshift-4/module/3200131b-dec7-4422-9e05-68c751bc4213/lesson/dc1da82f-2958-45af-bb9f-a6a6782ecc13)


# Demo Install Single Node using CRC

Source: https://notes.kodekloud.com/docs/OpenShift-4/Getting-Started-with-Openshift/Demo-Install-Single-Node-using-CRC/page

This article provides a step-by-step guide to installing CodeReady Containers for local OpenShift development on a single node.

After configuring your Red Hat account, navigate to [Red Hat OpenShift](https://console.redhat.com/openshift). You should see a page similar to the one below:

![The image shows the Red Hat Hybrid Cloud Console interface with a message indicating no OpenShift clusters are currently displayed, and options to create or register a cluster.](https://kodekloud.com/kk-media/image/upload/v1752882630/notes-assets/images/OpenShift-4-Demo-Install-Single-Node-using-CRC/red-hat-hybrid-cloud-console-no-clusters.jpg)

In this lesson, we will install CodeReady Containers (CRC), a tool that functions similarly to Docker Desktop by running a local OpenShift cluster. Once launched from your taskbar, CRC lets you use OpenShift for local development—comparable to Docker Desktop or Minikube.

## Create a Local Cluster

Begin by clicking on **Create Cluster** and select **Local** as your deployment option:

![The image shows a Red Hat Hybrid Cloud Console interface for creating an OpenShift cluster, with options for cloud, datacenter, and local setups. It displays active subscriptions and managed services, with a focus on Red Hat OpenShift Dedicated Trial.](https://kodekloud.com/kk-media/image/upload/v1752882631/notes-assets/images/OpenShift-4-Demo-Install-Single-Node-using-CRC/red-hat-hybrid-cloud-openshift-cluster.jpg)

You will now see the "Red Hat OpenShift Local" page with a download button. Depending on your operating system (Linux, macOS, or Windows), click the appropriate download button:

![The image shows a webpage from the Red Hat Hybrid Cloud Console, specifically the section for downloading and setting up Red Hat OpenShift Local. It includes options for selecting the operating system and downloading the necessary files.](https://kodekloud.com/kk-media/image/upload/v1752882632/notes-assets/images/OpenShift-4-Demo-Install-Single-Node-using-CRC/red-hat-openshift-local-setup.jpg)

## Installing CRC on Windows

For Windows users, click **Download OpenShift Local** and run the installer. Follow the installation prompts by clicking **Next** until you reach the **Install** button. After installation, you will be prompted to restart your computer:

![The image shows a computer screen with a Red Hat OpenShift setup process, including a file explorer window displaying a downloaded installer and a prompt to restart the system.](https://kodekloud.com/kk-media/image/upload/v1752882633/notes-assets/images/OpenShift-4-Demo-Install-Single-Node-using-CRC/red-hat-openshift-setup-process.jpg)

Click **Yes** to restart your system. After restarting, open PowerShell and maximize the window. You should see a prompt similar to the following:

```powershell theme={null}
PS C:\Users\mike>
```

## Set Up CRC Prerequisites

Verify that the CRC CLI is installed by typing `crc`. Then, run the setup command to install all prerequisites:

```powershell theme={null}
crc setup
```

When prompted for anonymous usage statistics, type **N** to decline:

```plaintext theme={null}
CRC is constantly improving and we would like to know more about usage (more details at https://developers.redhat.com/article/tool-data-collection)
Your preference can be changed manually if desired using 'crc config set consent-telemetry <yes/no>'
Would you like to contribute anonymous usage statistics? [y/N]: N
```

During the setup process, CRC configures several prerequisites. On Windows, CRC leverages Hyper-V for virtualization (similar to how Docker Desktop runs a virtual machine in the background). This process may download a large bundle (approximately 14 GiB) and configure multiple components, including:

* Hyper-V settings (ensuring Hyper-V is enabled and that your user is in the required groups).
* The CRC bundle for Hyper-V.
* The daemon task (which installs and runs as needed).

The output will resemble the example below:

```plaintext theme={null}
PS C:\Users\mike> crc setup
INFO  Using bundle path C:\Users\mike\.crc\cache\crc_hyperv_4.11.1_amd64.crcbundle
INFO  Checking if current user is in Hyper-V Admins group
INFO  Checking if C:\Users\mike\.crc\cache\crc_hyperv_4.11.1_amd64.crcbundle exists
INFO  Getting bundle for the CRC executable
INFO  Downloading crc_hyperv_4.11.1_amd64.crcbundle
3.24 GiB / 3.24 GiB [-------------------------------------] 100.00% 11.08 MiB p/s
INFO  Uncompressing C:\Users\mike\.crc\cache\crc_hyperv_4.11.1_amd64.crcbundle
crc.vhdx: 14.01 GiB / 14.01 GiB [-------------------------------------] 100.00%
INFO  Checking if the daemon task is installed
INFO  Installing the daemon task
INFO  Checking if the daemon task is running
INFO  Running the daemon task
INFO  Checking admin helper service is running
Your system is correctly setup for using CRC. Use 'crc start' to start the instance
```

> **lightbulb** Ensure that Hyper-V is enabled on your Windows machine before running the setup command.

## Starting the CRC Cluster

Clear your screen and start the CRC cluster with:

```powershell theme={null}
crc start
```

Starting the cluster may take around 15 minutes as the virtual machine fully initializes. Once the cluster is running, the CRC icon will appear in your Windows taskbar. Right-click the icon and select **Open Console** to view your CRC console credentials.

Open a terminal and execute the command provided by the console to reveal your credentials. You might see output similar to this:

```plaintext theme={null}
PowerShell 7.1.3
Copyright (c) Microsoft Corporation.

https://aka.ms/powershell
Type 'help' to get help.

A new PowerShell stable release is available: v7.2.6
Upgrade now, or check out the release page at:
https://aka.ms/PowerShell-Release?tag=v7.2.6
```

The output displays credentials for both the administrator and developer users. For example:

```plaintext theme={null}
INFO 2 operators are progressing: kube-apiserver, openshift-controller-manager
INFO 2 operators are progressing: authentication, openshift-controller-manager
...
Started the OpenShift cluster.
The server is accessible via web console at:
https://console-openshift-console.apps-crc.testing/
Log in as administrator:
Username: kubeadmin
Password: IxAvf-CKLZp-aqT8d-niTJV
Log in as user:
Username: developer
Password: developer
Use the 'oc' command line interface:
PS> & crc oc-env | Invoke-Expression
PS> oc login -u developer https://api.crc.testing:6443
PS C:\Users\mleva>
```

Copy the password provided for the "kubeadmin" account to log in as the administrator.

![The image shows a login page for the Red Hat OpenShift Container Platform, prompting for a username and password. The username field is filled with "kubeadmin."](https://kodekloud.com/kk-media/image/upload/v1752882636/notes-assets/images/OpenShift-4-Demo-Install-Single-Node-using-CRC/openshift-login-page-kubeadmin.jpg)

## Verifying Your Installation

After logging in, the OpenShift dashboard will be displayed, confirming your successful connection to the local OpenShift cluster.

![The image shows the dashboard of the Red Hat OpenShift Container Platform, displaying an overview of cluster details and getting started resources. It includes navigation options on the left and a warning banner at the top indicating the cluster is for development and testing purposes only.](https://kodekloud.com/kk-media/image/upload/v1752882637/notes-assets/images/OpenShift-4-Demo-Install-Single-Node-using-CRC/openshift-dashboard-cluster-overview.jpg)

This completes the setup of CRC on your local machine. You are now ready to develop and test locally with OpenShift.

Happy Coding!

- [Watch Video](https://learn.kodekloud.com/user/courses/openshift-4/module/7ba3dd10-68d9-414d-b26b-8e9109a4a3d3/lesson/0b597f99-f0b0-487d-bccc-a58648d9a35e)
