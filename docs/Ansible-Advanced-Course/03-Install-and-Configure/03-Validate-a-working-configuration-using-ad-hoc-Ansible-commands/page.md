# This is the default Ansible 'hosts' file.
#
# Location: /etc/ansible/hosts
#
# - Comments start with the '#' character
# - Blank lines are ignored
# - Groups of hosts are defined using [group_name] headers
# - Hostnames or IP addresses can be specified
## Example 1: Ungrouped hosts (specify before any group headers).

## green.example.com
## blue.example.com
## 192.168.100.1
## 192.168.100.10

## [webservers]
## alpha.example.org
## beta.example.org
## 192.168.1.100
## 192.168.1.110
```

### Custom Inventory File Example

```ini theme={null}
/opt/my-playbook/hosts
web1 ansible_host=192.168.1.100
web2 ansible_host=192.168.1.101
```

When executing a playbook, you can specify the path to your custom inventory file with the `-i` option.

## Creating and Overriding the Configuration File

Ansible uses a default configuration file located at `/etc/ansible/ansible.cfg` when installed via a package manager. This file defines the default parameters and behaviors. You can modify these defaults directly or create a custom configuration file within your playbook directory with only the settings you wish to override.

### Default Configuration File Example

```ini theme={null}
/etc/ansible/ansible.cfg
[defaults]
inventory       = /etc/ansible/hosts
log_path        = /var/log/ansible.log
library         = /usr/share/my_modules/
roles_path      = /etc/ansible/roles
action_plugins  = /usr/share/ansible/plugins/action
gathering       = implicit
# SSH timeout
timeout         = 10
display_skipped_hosts = True
nocolor         = 1
forks           = 5
```

### Custom Configuration File Example

```ini theme={null}
/opt/my-playbook/ansible.cfg
[defaults]
gathering       = explicit
```

> **triangle-alert** When installing Ansible via pip, the default inventory and configuration files are not created automatically. You will need to create these files manually.

That’s it for this lesson. Feel free to explore installing Ansible in the hands-on labs and experiment with different configuration settings. Good luck, and see you in the next lesson!

***

## Quick Reference

| Task                              | Command Example                      |
| --------------------------------- | ------------------------------------ |
| Install Ansible on CentOS/Red Hat | `sudo yum install ansible`           |
| Install Ansible on Fedora         | `sudo dnf install ansible`           |
| Install Ansible on Ubuntu/Debian  | `sudo apt-get install ansible`       |
| Install Ansible with pip          | `sudo pip install ansible`           |
| Upgrade Ansible with pip          | `sudo pip install --upgrade ansible` |
| Install Specific Version (2.4)    | `sudo pip install ansible==2.4`      |

For further details, check out the [Ansible Documentation](https://docs.ansible.com/ansible/latest/index.html).

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/f521e68d-4c4a-4fc5-bbd7-d394df07d086/lesson/e2a722a6-a353-4910-a5a8-8a87723b4559)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/f521e68d-4c4a-4fc5-bbd7-d394df07d086/lesson/36ded66e-f98c-40c3-bfb9-c62509c553e1)


# Validate a working configuration using ad hoc Ansible commands

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Install-and-Configure/Validate-a-working-configuration-using-ad-hoc-Ansible-commands/page

Learn to run ad hoc commands with Ansible for quick testing, verifying connectivity, and gathering information from multiple servers.

In this article, you will learn how to run ad hoc commands with Ansible. Although YAML-based playbooks are the recommended method for automating tasks—enabling reusability, version control with Git, and easy sharing—ad hoc commands provide a quick and efficient alternative for testing modules, verifying connectivity, or gathering one-off information from multiple servers.

> **lightbulb** The Ansible `ping` module is used to verify SSH connectivity to target machines using the configured credentials, not for performing an ICMP ping.

## Using a YAML Playbook for Connectivity Testing

For administrators managing virtual machines, a simple playbook using the `ping` module is an excellent way to test connectivity. Below is an example playbook that pings all target servers:

```yaml theme={null}
---
- name: Ping Servers
  hosts: all
  tasks:
    - ping:
```

To run the playbook, execute the following command in your terminal:

```bash theme={null}
ansible-playbook playbook.yml
```

## Executing Ad-Hoc Commands Directly

If you prefer not to create a playbook, you can achieve the same result using an ad hoc command. Use the `-m` option to specify the module and designate the target hosts. The command below pings all servers:

```bash theme={null}
ansible -m ping all
```

When executed, the output appears in JSON format for each host, similar to the following:

```plaintext theme={null}
web2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
web1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

## Running Arbitrary Commands

To run an arbitrary command on all hosts, use the `-a` option to pass the command directly. For instance, to display the contents of the `/etc/hosts` file, run:

```bash theme={null}
ansible -a 'cat /etc/hosts' all
```

The output will be similar to this:

```plaintext theme={null}
web1 | CHANGED | rc=0 >>
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.20.1.100 web1
web2 | CHANGED | rc=0 >>
127.0.0.1 localhost
::1 localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
172.20.1.100 web1
```

## Privilege Escalation with Ad-Hoc Commands

You can also include privilege escalation options (such as `become` or `become_user`) with these ad hoc commands, just as you would when using a playbook. This flexibility makes ad hoc commands a powerful tool for managing your infrastructure on the fly.

Continue exploring additional methods to effectively utilize ad hoc commands in Ansible for efficient infrastructure management.

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/f521e68d-4c4a-4fc5-bbd7-d394df07d086/lesson/f0fbb1e8-71a9-4034-b92d-0eb449dcf703)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/f521e68d-4c4a-4fc5-bbd7-d394df07d086/lesson/582c7565-c029-463b-819d-3d009da2c66c)
