# Ansible Modules

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Modules-Plugins/Ansible-Modules/page

This article explores various Ansible modules categorized by functionality for tasks like system management, command execution, file handling, and cloud interactions.

In this article, we explore a variety of Ansible modules categorized by their functionality. Each module group is tailored for specific tasks such as system management, command execution, file handling, database operations, cloud interactions, and Windows management.

![The image lists various modules, including System, Commands, Files, Database, Cloud, and Windows, with specific items like User, Group, Hostname, and Service highlighted.](https://kodekloud.com/kk-media/image/upload/v1752881051/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_20.jpg)

Modules are grouped as follows:

* **System Modules:** Perform actions at the operating system level, such as managing users and groups, configuring IP tables and firewalls, handling logical volumes, managing mount operations, and controlling services (start, stop, restart).
* **Command Modules:** Allow execution of commands or scripts on a host. Use the `command` module for simple commands or the `expect` module for interactive commands. The `script` module lets you run local scripts on remote hosts.
* **File Modules:** Facilitate operations on files, including setting file permissions with ACL, compression with `archive`/`unarchive`, and file content modifications using modules like `find`, `lineinfile`, and `replace`.
* **Database Modules:** Manage database operations for systems such as MongoDB, MySQL, MS SQL, and PostgreSQL, allowing you to add, remove, or update configurations.
* **Cloud Modules:** Offer robust functionalities for various cloud providers including Amazon, Azure, Docker, Google, OpenStack, and VMware. They help manage tasks like instance creation/destruction, networking, security configurations, container management, and data center operations.
* **Windows Modules:** Optimize management of Windows environments. Modules like `win_copy`, `win_command`, `win_service`, and others help with tasks ranging from file transfer to installing software and managing Windows services.

![The image lists various modules like System, Commands, Files, and more, with specific file-related functions such as Copy, Find, and Template highlighted.](https://kodekloud.com/kk-media/image/upload/v1752881052/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_70.jpg)

![The image lists modules like System, Commands, Files, Database, Cloud, Windows, and more, with a focus on databases such as MongoDB, MySQL, and PostgreSQL.](https://kodekloud.com/kk-media/image/upload/v1752881053/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_80.jpg)

![The image lists various modules like System, Commands, and Cloud, with cloud providers such as Amazon, Azure, and Google mentioned.](https://kodekloud.com/kk-media/image/upload/v1752881054/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_100.jpg)

![The image lists various modules related to system, commands, files, database, cloud, and Windows, including specific Windows commands like Win\_copy and Win\_service.](https://kodekloud.com/kk-media/image/upload/v1752881056/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_130.jpg)

For a complete reference and detailed documentation, please visit the [Ansible Documentation](https://docs.ansible.com).

Let's delve into some specific modules to understand how to utilize them and read their documentation pages.

***

## The Command Module

The command module executes a command on a remote node using key-value pair parameters. Below is an example playbook that runs the `date` command and displays the contents of `/etc/resolv.conf`:

```yaml theme={null}
- name: Play 1
  hosts: localhost
  tasks:
    - name: Execute command 'date'
      command: date

    - name: Display resolv.conf contents using full path
      command: cat /etc/resolv.conf

    - name: Display resolv.conf contents using change directory
      command: cat resolv.conf chdir=/etc

    - name: Create folder if it does not exist
      command: mkdir /folder creates=/folder
```

Notice how parameters such as `chdir` and `creates` modify the execution behavior. The `chdir` parameter changes the working directory before executing the command, while the `creates` parameter prevents command execution if a specific file or directory already exists.

One important concept is "free form" input. In the command module, the command itself (e.g., `cat /etc/resolv.conf` or `mkdir /folder`) is provided as a free form string. In contrast, modules like the copy module require explicit parameter names:

```yaml theme={null}
- name: Play 1
  hosts: localhost
  tasks:
    - name: Copy file from source to destination
      copy:
        src: /source_file
        dest: /destination
```

> **lightbulb** The command module accepts free form commands, making it ideal for straightforward executions, while modules such as copy require a structured key=value syntax.

***

## The Script Module

The script module facilitates executing a local script on remote nodes. When invoked, Ansible automatically transfers the script from the controller machine to the target nodes and then runs it. This automation simplifies tasks that require script execution across multiple machines.

Simply specify the local path of the script and include any necessary arguments.

![The image illustrates running a local script on remote nodes by transferring it, showing a network of computers and steps for copying and executing scripts remotely.](https://kodekloud.com/kk-media/image/upload/v1752881057/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_350.jpg)

***

## The Service Module

The service module manages system services, enabling you to start, stop, or restart them. Below is an example playbook to start a database service:

```yaml theme={null}
- name: Start Services in order
  hosts: localhost
  tasks:
    - name: Start the database service using key-value format
      service: name=postgresql state=started
```

You can also express the same logic using a dictionary format for enhanced readability:

```yaml theme={null}
- name: Start Services in order
  hosts: localhost
  tasks:
    - name: Start the database service using a map
      service:
        name: postgresql
        state: started
```

In these examples, the `name` parameter identifies the service (in this case, PostgreSQL), and the `state` parameter declares the desired state. The use of "started" instead of "start" ensures that if the service is already running, Ansible performs no extra action, promoting idempotency.

> **lightbulb** Idempotency ensures that running the same playbook multiple times results in a consistent state without unintended side effects.

![The image explains the difference between "start" and "started" for the httpd service, emphasizing ensuring it's running and actions based on its current state.](https://kodekloud.com/kk-media/image/upload/v1752881057/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Modules/frame_480.jpg)

***

## The Lineinfile Module

The lineinfile module is essential for managing file content. It ensures that a specific line is present in a file by adding or replacing it as needed, making it highly useful for configuration management. For example, to add a new DNS server entry to `/etc/resolv.conf`:

```yaml theme={null}
- name: Add DNS server to resolv.conf
  hosts: localhost
  tasks:
    - name: Ensure the correct nameserver is present in resolv.conf
      lineinfile:
        path: /etc/resolv.conf
        line: 'nameserver 10.1.250.10'
```

In contrast, a shell script appending text to a file might create duplicate entries over multiple executions:

```sh theme={null}
