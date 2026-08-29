# Facts

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Core-Components/Facts/page

This article provides an overview of Ansible facts, detailing how they are collected and utilized during playbook execution.

In this article, we explore Ansible facts—vital details automatically collected during playbook execution. When Ansible connects to a target machine, it gathers a wide range of system and network information. This data, including system architecture, OS version, processor details, memory statistics, network interfaces, IP addresses, FQDN, MAC addresses, disks, volumes, mounts, and even date/time settings, is stored in a collective variable called “facts.”

Ansible leverages the setup module to gather these facts. This module runs automatically before any playbook tasks, even if it is not explicitly specified.

> **lightbulb** Even if you do not include the setup module in your playbook, facts are gathered by default.

## Basic Playbook Example

Below is a simple playbook that prints a hello message. Notice that besides displaying the message, Ansible first collects facts using the setup module:

```yaml theme={null}
- name: Print hello message
  hosts: all
  tasks:
    - debug:
        msg: "Hello from Ansible!"
```

When you run this playbook, the output includes two tasks—the fact gathering task and the debug message display. An example output is:

```plaintext theme={null}
PLAY [Print hello message] ***************************************************

TASK [Gathering Facts] *******************************************************
ok: [web2]
ok: [web1]

TASK [debug] *****************************************************************
ok: [web1] => {
    "msg": "Hello from Ansible!"
}
ok: [web2] => {
    "msg": "Hello from Ansible!"
}
```

## Displaying Gathered Facts

All the system details gathered by Ansible are stored in a variable named `ansible_facts`. To display these facts, modify your playbook as shown below:

```yaml theme={null}
- name: Print all gathered facts
  hosts: all
  tasks:
    - debug:
        var: ansible_facts
```

The resulting output contains a comprehensive list of system information, including IP addresses, system architecture, operating system details, DNS configurations, network interfaces, memory allocation, processor information, and more:

```plaintext theme={null}
PLAY [Print all gathered facts] ********************************************

TASK [Gathering Facts] **************************************************
ok: [web2]
ok: [web1]

TASK [debug] **************************************************************
ok: [web1] => {
    "ansible_facts": {
        "all_ipv4_addresses": [
            "172.20.1.100"
        ],
        "architecture": "x86_64",
        "date_time": {
            "date": "2019-09-07"
        },
        "distribution": "Ubuntu",
        "distribution_file_variety": "Debian",
        "distribution_major_version": "16",
        "distribution_release": "xenial",
        "distribution_version": "16.04",
        "dns": {
            "nameservers": [
                "127.0.0.11"
            ]
        },
        "fqdn": "web1",
        "hostname": "web1",
        "interfaces": [
            "lo",
            "eth0"
        ],
        "machine": "x86_64",
        "memfree_mb": 72,
        "memory_mb": {
            "real": {
                "free": 72,
                "total": 985,
                "used": 913
            }
        }
    }
}
```

This information can be particularly useful when configuring devices, managing logical volumes, or making decisions based on disk space or system resources.

## Disabling Fact Gathering

There are scenarios where fact gathering may be unnecessary or even undesired. You can disable automatic fact gathering by setting the `gather_facts` parameter to `no` in your playbook:

```yaml theme={null}
- name: Print hello message without gathering facts
  hosts: all
  gather_facts: no
  tasks:
    - debug:
        msg: "Hello from Ansible!"
```

When fact gathering is disabled, only the explicitly defined tasks run. Keep in mind that the Ansible configuration file (typically found at `/etc/ansible/ansible.cfg`) also controls this behavior. The `gathering` setting in the configuration file can be specified as follows:

* **smart**: Gathers facts by default, but avoids re-gathering if the data already exists.
* **implicit**: Automatically gathers facts; you can disable this with `gather_facts: False` in your playbook.
* **explicit**: Does not gather facts by default; you must explicitly set `gather_facts: True` in the playbook when needed.

An example snippet from the configuration file is:

```plaintext theme={null}
/etc/ansible/ansible.cfg
