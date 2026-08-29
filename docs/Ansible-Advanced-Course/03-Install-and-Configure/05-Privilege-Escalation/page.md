# Privilege Escalation

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Install-and-Configure/Privilege-Escalation/page

Learn to configure privilege escalation on managed nodes using Ansible for elevated permissions to perform system tasks.

In this guide, you'll learn how to configure privilege escalation on managed nodes using Ansible. Privilege escalation is the process of temporarily obtaining elevated permissions (typically root or administrative privileges) to perform system tasks that a regular user cannot.

![The image features the text "Ansible Privilege Escalation" on a red and dark background, possibly indicating a topic related to Ansible's security features.](https://kodekloud.com/kk-media/image/upload/v1752869400/notes-assets/images/Ansible-Advanced-Course-Privilege-Escalation/frame_10.jpg)

## Understanding User Privileges

Every user on a system is assigned a set of permissions. Consider a development server for a web application where various user accounts exist:

* **root:** Full system privileges (often locked for direct login).
* **Administrator/Developer:** Limited privileges necessary for everyday tasks.
* **Dedicated Users:** Specific accounts for tools or applications like Nginx, databases, and monitoring tools.

A typical workflow in such an environment involves an administrator logging in (using a password or SSH key), installing packages that require elevated privileges, and then configuring applications under designated user accounts.

![The image displays a hierarchy of user roles, with "root" at the top, followed by "admin," "developer," "nginx," "monitor," and "mysql" users.](https://kodekloud.com/kk-media/image/upload/v1752869401/notes-assets/images/Ansible-Advanced-Course-Privilege-Escalation/frame_60.jpg)

### Example: Installing a Package Without Escalation

For instance, if an administrator logs in to install a package:

```bash theme={null}
ssh -i id_ras admin@server1
su
yum install nginx
