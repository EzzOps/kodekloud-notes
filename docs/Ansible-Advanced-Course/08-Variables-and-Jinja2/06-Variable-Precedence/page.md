# Variable Precedence

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Variables-and-Jinja2/Variable-Precedence/page

This article explains variable precedence in Ansible, detailing how values are determined when variables are defined in multiple locations.

This article explains how variables work in Ansible and outlines the concept of variable precedence—i.e., which value Ansible uses when the same variable is defined in multiple locations.

Ansible variables store information that might differ between hosts. They serve two main purposes:

• Configuring connectivity for Ansible itself.\
• Defining settings for your playbooks (for example, configuring DNS server IPs, NTP server IPs, firewall rules, etc.).

<Callout icon="lightbulb">
  Ansible variables are assigned to host objects during playbook execution. Initially, group variables are associated with each host, and then any host-specific variables override these values.
</Callout>

Below is an example inventory file that defines host variables for each host and includes a group variable for the DNS server:

```bash theme={null}
