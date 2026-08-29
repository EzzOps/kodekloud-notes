# Ansible Inventory

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Inventory/Ansible-Inventory/page

This article explores configuring an inventory in Ansible for managing multiple systems using native protocols without requiring additional software.

In this article, we explore how to configure an inventory in Ansible. By managing one or multiple systems simultaneously, Ansible establishes connections to target servers using protocols built into modern infrastructures. For Linux hosts, it relies on SSH, and for Windows systems, it uses PowerShell remoting. This agentless design eliminates the need for installing additional software on target machines—SSH connectivity alone is enough. Unlike many other orchestration tools that require agents, Ansible leverages native protocols to interact with your infrastructure.

Information about these target systems is stored in an inventory file. By default, Ansible uses the inventory file located at `/etc/ansible/hosts` unless you specify a custom file.

An inventory file is written in an INI-like format. It can list servers sequentially or group them by placing the group name in square brackets, followed by the list of servers. For example:

<Callout icon="lightbulb">
  The example below demonstrates a basic inventory file structure that lists and groups servers without relying on any additional diagrams or images.
</Callout>

Consider the following inventory file which defines groups such as `[inventory]`, `[mail]`, `[db]`, and `[web]`:

```ini theme={null}
[inventory]
server1.company.com
server2.company.com

[mail]
server3.company.com
server4.company.com

[db]
server5.company.com
server6.company.com

[web]
server7.company.com
server8.company.com
```

In many practical scenarios, you may want to refer to servers using friendly aliases (e.g., web server or database server). You can set an alias by specifying the `ansible_host` parameter, which defines the FQDN or IP address of the server. Other useful inventory parameters include:

* **ansible\_connection:** Defines the connection method Ansible uses (e.g., `ssh` for Linux or `winrm` for Windows). Setting it to `localhost` means no remote connection is required.
* **ansible\_port:** Specifies the port for the connection (default is 22 for SSH).
* **ansible\_user:** Specifies the username for remote connections (for instance, `root` for Linux by default).
* **ansible\_ssh\_pass:** Specifies the SSH password. *Note:* Storing passwords in plain text is strongly discouraged. It is best practice to configure key-based authentication, especially in production environments.

Below is a sample inventory configuration that includes these parameters. This setup works well for introductory lessons on Ansible as it focuses on fundamentals without delving deeply into intricate security configurations:

```ini theme={null}
