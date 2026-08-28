# Script to add a user to a Linux system
if [ "$(id -u)" -eq 0 ]; then
    username="johndoe"
    read -s -p "Enter password: " password
    useradd "$username" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "User has been added"
    else
        echo "Failed to add the user!"
    fi
else
    echo "This script must be run as root."
fi
```

### Equivalent Ansible Playbook

Ansible simplifies the process dramatically. The playbook below performs the same operation on the localhost with just a few lines:

```yaml theme={null}
- hosts: localhost
  tasks:
    - name: Add the user johndoe
      user:
        name: johndoe
```

***

## Example 2: Enhanced Script with Validation and Targeted Execution

### Improved Shell Script with User Existence Check

This enhanced shell script checks if the user already exists before attempting to add them:

```bash theme={null}
#!/bin/bash
# Script to add a user to a Linux system with validation
if [ "$(id -u)" -eq 0 ]; then
    username="johndoe"
    read -s -p "Enter password: " password
    grep -q "^$username:" /etc/passwd
    if [ $? -ne 0 ]; then
        useradd "$username"
        echo "$password" | passwd --stdin "$username"
        echo "User has been added"
    else
        echo "User '$username' already exists!"
    fi
else
    echo "This script must be run as root."
fi
```

### Ansible Playbook Targeting Specific Servers

Changing the execution target in Ansible is as simple as modifying one line. For instance, to perform the same task on a specific group of web servers in a disaster recovery environment, use this playbook:

```yaml theme={null}
- hosts: all_my_web_servers_in_DR
  tasks:
    - name: Add the user johndoe
      user:
        name: johndoe
```

<Callout icon="lightbulb">
  Using Ansible, you can easily shift focus from a single host to multiple servers by updating the target hosts. This provides flexibility in managing both local and remote environments.
</Callout>

***

## Real-World Use Cases

Imagine needing to restart several hosts in a specific order. For instance, you may need to shut down your web servers first, followed by database servers, then reboot and restart them in reverse order. With Ansible, creating such a playbook is straightforward and can be executed whenever necessary.

Another common scenario involves provisioning a complex infrastructure that spans both public and private clouds, managing hundreds of virtual machines. Ansible can provision VMs on platforms like Amazon AWS and private environments such as VMware. It then configures applications, updates configuration files, installs necessary software packages, and modifies firewall rules. Moreover, its extensive library of built-in modules facilitates integration with other systems—such as pulling data from your CMDB or triggering automated workflows via ServiceNow.

<Frame>
  ![The image illustrates a complex use case involving ServiceNow, databases, cloud, and multiple servers, with a person presenting the diagram.](https://kodekloud.com/kk-media/image/upload/v1752881106/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Introduction/frame_190.jpg)
</Frame>

Explore the extensive guides and hundreds of playbook examples available in the [Ansible Documentation](https://docs.ansible.com) to deepen your understanding and broaden your automation skills.

<Frame>
  ![The image shows a webpage of Ansible Documentation with a person standing in front, wearing a navy and orange sweater.](https://kodekloud.com/kk-media/image/upload/v1752881108/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Introduction/frame_200.jpg)
</Frame>

***

This article provided an overview of Ansible, showcasing its benefits and advantages over traditional scripting. In the upcoming lessons, we will guide you through setting up an Ansible hands-on lab environment and delve into more advanced playbook configurations. Stay tuned for the next lesson!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/1b3f113a-1512-4858-a794-1b74c3541725/lesson/1d3be0a0-a3f5-489c-98c3-8f04b428ecbe" />
</CardGroup>


# Introduction

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Introduction/Introduction/page

This course teaches Ansible through engaging lectures, hands-on labs, and real-world scenarios for absolute beginners without prior coding experience.

Welcome to the [Ansible for the Absolute Beginners](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course) course! I’m Mumshad Mannambeth, your instructor and a seasoned DevOps trainer at KodeKloud.com with over 13 years of industry experience. Throughout my career, I’ve guided hundreds of thousands of students in mastering technology through interactive, hands-on learning.

In this course, you will learn Ansible by following a series of engaging lectures enhanced with animations and illustrations, which simplify complex concepts. We complement these lectures with demos to help you install and get started with Ansible, as well as browser-accessible hands-on labs. These labs are designed to run on any system without needing cloud platforms or high-end hardware since they use dedicated lab environments and challenges.

<Callout icon="lightbulb">
  Each lab is customized to the topic at hand so that you work through real-world scenarios, rather than following static instructions.
</Callout>

## Course Objectives

At the end of this course, you will deploy the KodeKloud e-commerce application using simple Ansible playbooks. This course is specifically designed for absolute beginners—no prior coding or scripting experience is needed.

We cover:

* A clear explanation of what Ansible is and its capabilities.
* Step-by-step instructions on setting up Ansible on your environment using a VirtualBox-deployed virtual machine.
* An introduction to YAML, the language used for writing Ansible playbooks.
* Interactive coding exercises that help you confidently automate tasks with Ansible.

To reinforce your learning, you can access hands-on labs and a browser-based quiz portal. The portal presents a range of questions and includes an editor for you to create and test your YAML files and playbooks. If you run into any challenges, hints and solutions are available, and our Q\&A section is always open for support.

I'm excited to embark on this automation journey with you. Let’s get started!

## Further Learning

* Explore the fundamentals of Ansible and other DevOps tools by visiting our detailed [Ansible documentation](https://docs.ansible.com/).
* Learn more about best practices in automation and configuration management at [KodeKloud](https://kodekloud.com).

Happy automating!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/1b3f113a-1512-4858-a794-1b74c3541725/lesson/7741ee47-6c45-4d99-a099-29257b769fb3" />
</CardGroup>
