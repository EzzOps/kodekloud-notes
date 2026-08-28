# Ansible File Separation

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Include-and-Roles/Ansible-File-Separation/page

Learn to separate variables from Ansible inventory files for better maintenance and organization using dedicated YAML files for host-specific and group variables.

In this lesson, you will learn how to separate variables from your Ansible inventory file to simplify maintenance and improve organization. When dealing with numerous inventory items, embedding variables within the inventory file itself can quickly become cumbersome. A more efficient approach is to define host-specific variables in dedicated YAML files.

For each server (for example, web1, web2, and web3), create a YAML file with the same name as the host inside the **host\_vars** directory. Then, move the corresponding variables from the inventory file into these new files. When transferring the variables, make sure to replace the equal sign (`=`) with a colon followed by a space (`: `) to adhere to proper YAML syntax. Ansible automatically processes these files during playbook execution, matching them with the corresponding host based on the file name.

Below is an example of an inventory file entry before variables are separated:

```ini theme={null}
[web_servers]
web1 ansible_host=172.20.1.100 dns_server=10.1.1.5
web2 ansible_host=172.20.1.101 dns_server=10.1.1.5
web3 ansible_host=172.20.1.102 dns_server=10.1.1.5
```

Since the DNS server detail is common across all the servers in the group, you can also move this variable into a group variable file. Group variables should reside in the **group\_vars** directory and the file must be named after the group. The recommended folder structure is as follows:

* For host variables, use a folder named **host\_vars**.
* For group variables, use a folder named **group\_vars**.

It is a best practice to place the inventory file along with the **host\_vars** and **group\_vars** directories inside a single **inventory** directory to keep all related information centralized.

***

<Callout icon="lightbulb">
  If your variable file is not located in one of Ansible’s default directories, you can still load external variables by using the `include_vars` module within your playbook.
</Callout>

Consider a scenario where you store a set of variables in a central repository (for example, in `/opt/apps/common-data/email`) that is shared across multiple playbooks. Below is a simplified file structure:

```ini theme={null}
