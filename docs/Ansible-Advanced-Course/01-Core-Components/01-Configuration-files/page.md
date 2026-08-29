# Configuration files

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Core-Components/Configuration-files/page

This lesson explores Ansible configuration files and their impact on Ansible's behavior, including overriding settings and using environment variables.

In this lesson, we will explore configuration files in Ansible and understand how they influence Ansible's behavior. When you install Ansible, a default configuration file is generated. On Windows, for example, it might be located at `C:\ansible\ansible.cfg`, while on Linux the default file is commonly found at `/etc/ansible/ansible.cfg`. This file regulates Ansible's default behavior by splitting settings into several sections. The primary section is usually at the top (commonly named `[defaults]`), followed by sections for inventory, privilege escalation, SSH connection, colors, and others. Each section contains various options with corresponding values.

For example, a typical configuration file may appear as follows:

```ini theme={null}
/etc/ansible/ansible.cfg
[default]
[inventory]
[privilege_escalation]
[paramiko_connection]
[ssh_connection]
[persistent_connection]
[colors]
```

These sections define settings such as the default inventory file location, log file path, directories for modules, roles, or plugins, as well as options like fact gathering and SSH connection timeouts. Consider the following sample configuration:

```ini theme={null}
[defaults]
inventory          = /etc/ansible/hosts
log_path           = /var/log/ansible.log
library            = /usr/share/my_modules/
roles_path         = /etc/ansible/roles
action_plugins     = /usr/share/ansible/plugins/action
gathering          = implicit
