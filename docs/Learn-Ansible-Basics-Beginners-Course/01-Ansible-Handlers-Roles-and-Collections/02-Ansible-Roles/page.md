# Ansible Roles

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Handlers-Roles-and-Collections/Ansible-Roles/page

This article explores the concept of roles in Ansible for configuring servers and promoting code reusability across projects.

In this article, we explore the concept of roles in Ansible. Just like individuals have specific roles in society—such as doctors, engineers, police officers, or chefs—servers in your infrastructure can be designated with particular roles. A server might function as a database server, web server, Redis messaging server, or even a backup server based on the assigned role.

Assigning a role involves executing every necessary step to configure a server for its intended purpose. For example, becoming a doctor involves attending medical school, completing a residency, and obtaining a license. Likewise, transforming a server into a MySQL database server entails installing prerequisites, adding MySQL packages, configuring the MySQL service, and setting up databases or users. Similarly, setting up a web server using Nginx includes installing prerequisites for Nginx, adding the necessary packages, configuring its service, and establishing custom web pages.

<Frame>
  ![The image compares career paths for doctors and engineers with steps for setting up MySQL and Nginx, using icons and bullet points.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881040/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Roles/frame_80.jpg)
</Frame>

By now, you are familiar with how to perform these tasks using Ansible playbooks. Consider the following simple playbook that installs and configures MySQL:

```yaml theme={null}
- name: Install and Configure MySQL
  hosts: db-server
  tasks:
    - name: Install Pre-Requisites
      yum:
        name: pre-req-packages
        state: present

    - name: Install MySQL Packages
      yum:
        name: mysql
        state: present

    - name: Start MySQL Service
      service:
        name: mysql
        state: started

    - name: Configure Database
      mysql_db:
        name: db1
        state: present
```

Once you develop such a playbook, it can be reused by anyone who needs to install MySQL. Instead of rewriting the same code repeatedly, you can package these tasks into a role. Your playbook can then simply reference the role. For example, whether you are configuring one server or scaling to hundreds, your playbook might look like this:

```yaml theme={null}
- name: Install and Configure MySQL
  hosts: db-server1,...,db-server100
  roles:
    - mysql
```

<Callout icon="lightbulb">
  Roles promote code reusability across projects, encourage best practices by organizing files into directories such as tasks, vars, defaults, handlers, and templates, and simplify code sharing within the community.
</Callout>

Below is an example structure inside a role:

```yaml theme={null}
tasks:
  - name: Install Pre-Requisites
    yum:
      name: pre-req-packages
      state: present

  - name: Install MySQL Packages
    yum:
      name: mysql
      state: present

  - name: Start MySQL Service
    service:
      name: mysql
      state: started

  - name: Configure Database
    mysql_db:
      name: db1
      state: present

vars:
  mysql_packages:
    - mysql
    - mysql-server
  db_config:
    db_name: db1

defaults:
  mysql_user_name: root
  mysql_user_password: root
```

Roles not only simplify local development but also enable you to share your solutions with the broader Ansible community. [Ansible Galaxy](https://galaxy.ansible.com/) is a widely used hub where you can find thousands of roles for diverse tasks like setting up web servers, database servers, automation tools, monitoring systems, packaging tools, and security software.

<Frame>
  ![The image shows a webpage interface for "Galaxy" with navigation options like Home, Search, and Community, featuring categories such as System, Development, and Security.](../../../../images/kodekloud.com/kk-media/image/upload/v1752881041/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Roles/frame_210.jpg)
</Frame>

Before writing your own playbooks, it is worthwhile to explore Ansible Galaxy; someone may have already created the role you need.

## Getting Started with Roles

Creating a role is straightforward. Although you can manually create the required directory structure, Ansible Galaxy offers a convenient command-line tool to generate a role skeleton. To initialize a new role, run:

```bash theme={null}
$ ansible-galaxy init mysql
```

After initializing, move your code into the appropriate directories (e.g., tasks, vars, defaults, handlers, templates) as needed. To ensure your playbook can locate the role, place it in a directory named "roles" within your playbook’s folder or in a common path (by default, /etc/ansible/roles) defined in your Ansible configuration.

For example:

```yaml theme={null}
- name: Install and Configure MySQL
  hosts: db-server
  roles:
    - mysql
```

Your Ansible configuration file (typically at /etc/ansible/ansible.cfg) might include the following setting to designate the default roles path:

```ini theme={null}
/etc/ansible/ansible.cfg
roles_path = /etc/ansible/roles
```

## Using Roles from Ansible Galaxy

If you prefer using an existing role from Ansible Galaxy, you can search for and install one via the command line. For instance, to install the community-provided MySQL role, run:

```bash theme={null}
$ ansible-galaxy install geerlingguy.mysql
```

During installation, you might see output similar to this:

```bash theme={null}
- downloading role 'mysql', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-mysql/archive/2.9.5.tar.gz
- extracting geerlingguy.mysql to /etc/ansible/roles/geerlingguy.mysql
- geerlingguy.mysql (2.9.5) was installed successfully
```

You can reference the installed role in your playbook as follows:

```yaml theme={null}
- name: Install and Configure MySQL
  hosts: db-server
  roles:
    - geerlingguy.mysql
```

Roles can also be declared as dictionaries if you need to pass additional options such as privilege escalation or extra parameters. For example, to assign roles for both MySQL and Nginx, your playbook might include:

```yaml theme={null}
- name: Install and Configure MySQL and Nginx
  hosts: db-and-webserver
  roles:
    - geerlingguy.mysql
    - nginx
```

## Managing and Locating Roles

To view a list of roles installed on your system, use the following command:

```bash theme={null}
$ ansible-galaxy list
- geerlingguy.mysql
- kodekloud1.mysql
```

Additionally, you can check your Ansible configuration for roles settings with:

```bash theme={null}
$ ansible-config dump | grep ROLE
DEFAULT_PRIVATE_ROLE_VARS(default) = False
DEFAULT_ROLES_PATH(default) = [u'/root/.ansible/roles', u'/usr/share/ansible/roles', u'/etc/ansible/roles']
GALAXY_ROLE_SKELETON(default) = None
GALAXY_ROLE_SKELETON_IGNORE(default) = ['^.git$', '.*/.git_keep$']
```

To install roles into a specific directory, use the -p option:

```bash theme={null}
$ ansible-galaxy install geerlingguy.mysql -p ./roles
```

## Summary

By leveraging roles, you can simplify the development, reuse, and sharing of your Ansible playbooks—whether you’re configuring a single server or managing setups across hundreds of servers.

<Callout icon="lightbulb">
  * Learn more about [Ansible Roles Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html).
  * Explore more on [Ansible Galaxy](https://galaxy.ansible.com/).
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/e98a2ff3-ee65-4cf3-9bf3-b91507d617e3/lesson/52317fb0-2d32-4015-bf28-fcc54881314c" />
</CardGroup>
