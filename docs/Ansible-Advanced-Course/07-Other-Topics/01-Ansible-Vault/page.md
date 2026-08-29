# Permission Denied
```

The command fails because installing packages requires root privileges. By configuring the admin user to use the sudo utility (or a similar mechanism), the admin can escalate privileges and perform the installation successfully.

### Example: Switching User Accounts

The process of switching to another user to configure an application is also a form of privilege escalation. For example:

```bash theme={null}
ssh -i id_ras admin@server1
sudo yum install nginx
su nginx
su mysql
# Configure MySQL
```

In scenarios like this, privilege escalation is essential for transitioning between different user roles during the configuration process.

## Configuring Privilege Escalation in Ansible

Ansible allows you to replicate the behavior of privilege escalation that you manually perform on the command line.

### Basic Inventory and Playbook Without Privilege Escalation

Consider an inventory file that connects to a lamp server with the admin user. Although it's often a good practice to create a dedicated user for Ansible tasks, this example uses the admin user:

```yaml theme={null}
# inventory file
lamp-dev1 ansible_host=172.20.1.100 ansible_user=admin

# playbook file
---
- name: Install nginx
  hosts: all
  tasks:
    - yum:
        name: nginx
        state: latest
```

Running the playbook without privilege escalation will fail because the admin user lacks the required permissions.

### Enabling Privilege Escalation with the become Directive

To fix the issue, add the "become" directive to the playbook. This instructs Ansible to perform tasks with elevated privileges, similar to using the sudo command:

```yaml theme={null}
# inventory file
lamp-dev1 ansible_host=172.20.1.100 ansible_user=admin

# playbook file
---
- name: Install nginx
  become: yes
  hosts: all
  tasks:
    - yum:
        name: nginx
        state: latest
```

With the "become" directive, Ansible runs the tasks with elevated permissions, successfully installing Nginx.

### Using Alternative Privilege Escalation Methods

By default, Ansible uses sudo for privilege escalation. However, if you prefer another method such as "doas" or "pfexec," you can specify it using the "become\_method" option:

```yaml theme={null}
# inventory file
lamp-dev1 ansible_host=172.20.1.100 ansible_user=admin

# playbook file
---
- name: Install nginx
  become: yes
  become_method: doas
  hosts: all
  tasks:
    - yum:
        name: nginx
        state: latest
```

### Targeting a Specific User With become\_user

You can also designate a specific target user (e.g., the nginx user) using the "become\_user" directive. This tells Ansible to switch to a particular user before executing tasks. You can define these settings in multiple locations:

* In the Ansible configuration file (/etc/ansible/ansible.cfg)
* In the inventory file as host parameters (prefixed with "ansible\_")
* Directly in the playbook
* Via command-line arguments

#### In the Ansible Configuration File

```ini theme={null}
# /etc/ansible/ansible.cfg
become              = True
become_method       = doas
become_user         = nginx
```

#### In the Inventory File

```ini theme={null}
# inventory file
lamp-dev1 ansible_host=172.20.1.100 ansible_user=admin ansible_become=yes ansible_become_user=nginx
```

#### In the Playbook

```yaml theme={null}
# playbook file
---
- name: Install nginx
  hosts: all
  tasks:
    - yum:
        name: nginx
        state: latest
```

Keep in mind that any values specified directly in the playbook override those in the inventory file, and command-line parameters have the highest precedence, while settings in the default configuration file have the lowest.

> **lightbulb** For complex environments, consider consolidating privilege escalation settings in the Ansible configuration file to simplify management.

### Prompting for a Privilege Escalation Password

Sometimes, escalating privileges may require a password (similar to using sudo). Ansible can prompt you for this password by using the "--ask-become-pass" option on the command line:

```plaintext theme={null}
$ ansible-playbook --become --become-method=doas --become-user=nginx --ask-become-pass
```

When you run the playbook with this option, Ansible will prompt you to enter the appropriate password for privilege escalation.

## Summary

This article covered how to configure privilege escalation in Ansible by:

* Understanding different user roles and privileges.
* Using the "become" directive to execute tasks with elevated permissions.
* Configuring alternative methods with "become\_method" and targeting specific users with "become\_user."
* Overriding settings in the inventory file, playbook, and command-line.
* Prompting for privilege escalation passwords when needed.

Review the available practice exercises to apply and further solidify your understanding of these concepts. For more detailed information, refer to the [Ansible Documentation](https://docs.ansible.com/).

Happy automating!

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/f521e68d-4c4a-4fc5-bbd7-d394df07d086/lesson/ee54bc41-4847-484b-8014-e206253caafe)


# Ansible Vault

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Other-Topics/Ansible-Vault/page

This guide explains how to protect sensitive data in Ansible projects using Ansible Vault for encryption.

In this guide, we explain how to protect sensitive data in your Ansible projects by using Ansible Vault. Traditionally, plain-text credentials—such as passwords and API keys—have been stored in inventory files, posing a significant security risk. With Ansible Vault, you can encrypt this sensitive information, ensuring it remains secure and only accessible when the correct password is provided.

## Encrypting an Existing Inventory File

Let's assume you have an inventory file with the following content:

```bash theme={null}
inventory
web1 ansible_host=172.20.1.100 ansible_ssh_pass=Passw0rd
web2 ansible_host=172.20.1.101 ansible_ssh_pass=Passw0rd
```

To encrypt this file, run:

```bash theme={null}
ansible-vault encrypt inventory
```

Once executed, you will be prompted to enter a new vault password. After encryption, the file’s content is no longer human-readable without the correct password.

## Running Playbooks with Encrypted Inventory

If you attempt to run a playbook that references an encrypted inventory file without providing the vault password, Ansible will return an error. To execute the playbook successfully, include the `--ask-vault-pass` option so Ansible can prompt for the vault password, as shown below:

```bash theme={null}
ansible-playbook playbook.yml -i inventory --ask-vault-pass
```

After entering the correct vault password, your playbook will run as expected.

> **lightbulb** For improved security, avoid running playbooks without providing the vault password. Always use the `--ask-vault-pass` option or a secure method to supply the password.

## Alternative Approach: Storing the Vault Password in a File

An alternative method is to store the vault password in a file and reference it with your command. However, keep in mind that saving the vault password in plain text is not recommended. A more secure approach is to use a Python script (with a `.py` extension) that dynamically retrieves the vault password—possibly via an API call, a database, or another secure source.

> **triangle-alert** Storing the vault password in plain text poses security risks. Always consider using a dynamic retrieval method to ensure your credentials remain secure.

## Viewing and Creating Encrypted Files

To inspect the contents of an encrypted file, use the following command:

```bash theme={null}
ansible-vault view inventory
```

Similarly, to create a new encrypted file, run:

```bash theme={null}
ansible-vault create new_file.yml
```

## Conclusion

By encrypting your inventory files and other sensitive data using Ansible Vault, you significantly enhance the security of your automation workflows. For further practice, try experimenting with these vault commands in your Ansible environment.

For more information on Ansible Vault and securing your infrastructure, consider exploring the [Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/vault.html).

- [Watch Video](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/5ce7e345-0c21-4fba-8735-a4d9f3302e0e/lesson/6fa9fcb9-2536-4737-ab2f-759752b9959d)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/5ce7e345-0c21-4fba-8735-a4d9f3302e0e/lesson/00354234-d22c-4fb7-b546-f74b732cedeb)
