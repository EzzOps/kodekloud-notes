# Simple Ansible Playbook
- Run command1 on server1
- Run command2 on server2
- Run command3 on server3
- Run command4 on server4
- Run command5 on server5
- Run command6 on server6
- Run command7 on server7
- Run command8 on server8
- Run command9 on server9
- Restarting Server1
- Restarting Server2
- Restarting Server3
- Restarting Server4
- Restarting Server5
- Restarting Server6
- Restarting Server7

# Complex Ansible Playbook
- Deploy 50 VMs on Public Cloud
- Deploy 50 VMs on Private Cloud
- Provision Storage to all VMs
- Setup Network Configuration on Private VMs
- Setup Cluster Configuration
- Configure Web server on 20 Public VMs
- Configure DB server on 20 Private VMs
- Setup Loadbalancing between web server VMs
- Setup Monitoring components
- Install and Configure backup clients on VMs
- Update CMDB database with new VM Information
```

This diagram visually compares a simple playbook to a more complex one, illustrating tasks from basic server command execution to large-scale virtual machine deployments.

![The image shows a comparison between simple and complex Ansible playbooks, detailing tasks for server commands and virtual machine deployments.](https://kodekloud.com/kk-media/image/upload/v1752881066/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Playbooks/frame_40.jpg)

> **lightbulb** Playbooks are written in YAML format, so having a good grasp of YAML syntax is essential for writing error-free configurations.

## Anatomy of an Ansible Playbook

An Ansible playbook is a YAML file that contains a list of plays. Each play targets specific hosts defined in your inventory and comprises multiple tasks. A task represents a single action, such as executing a command, running a script, installing a package, or restarting a service.

Consider the following sample playbook:

```yaml theme={null}
- name: Play 1
  hosts: localhost
  tasks:
    - name: Execute command 'date'
      command: date

    - name: Execute script on server
      script: test_script.sh

    - name: Install httpd service
      yum:
        name: httpd
        state: present

    - name: Start web server
      service:
        name: httpd
        state: started
```

In this example, tasks execute sequentially on the specified host (localhost). The playbook prints the current date, runs a server-side script, installs the HTTP service using the yum module, and finally starts the web server.

## Multiple Plays in a Single Playbook

To further illustrate the structure, here’s an example of a playbook with two separate plays:

```yaml theme={null}
- name: Play 1
  hosts: localhost
  tasks:
    - name: Execute command 'date'
      command: date

    - name: Execute script on server
      script: test_script.sh

- name: Play 2
  hosts: localhost
  tasks:
    - name: Install web service
      yum:
        name: httpd
        state: present

    - name: Start web server
      service:
        name: httpd
        state: started
```

Each play is represented as a dictionary with keys like "name", "hosts", and "tasks". It is crucial to maintain the specified order of tasks within a play since they are executed sequentially. Changing the order may result in unexpected behavior, for example, trying to start a service before it is installed.

### Key Concepts Explained

* **Hosts Parameter:** Defines the target for the play. Although the examples here use "localhost", you can specify any host or group from your inventory. When a group is used, tasks are executed concurrently on all hosts within that group.

* **Modules:** The core building blocks of Ansible. Some common modules demonstrated above include:
  * command
  * script
  * yum
  * service

There are hundreds of modules available by default. For detailed documentation, refer to the [official Ansible documentation](https://docs.ansible.com/ansible/latest/collections/index.html) or use the `ansible-doc -l` command to list them.

## Running Your Playbook

Once your playbook is set up, you can execute it using the following command:

```bash theme={null}
ansible-playbook playbook.yml
```

For additional command options, run:

```bash theme={null}
ansible-playbook --help
```

This command-line utility provides guidance on available parameters to further customize playbook execution.

![The image explains a playbook as a YAML file defining activities (tasks) for hosts, including executing commands, running scripts, installing packages, and shutdown/restart actions.](https://kodekloud.com/kk-media/image/upload/v1752881067/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-Playbooks/frame_70.jpg)

## Complete Sample Playbook

For quick reference, here’s the complete sample playbook:

```yaml theme={null}
- name: Play 1
  hosts: localhost
  tasks:
    - name: Execute command 'date'
      command: date

    - name: Execute script on server
      script: test_script.sh

    - name: Install httpd service
      yum:
        name: httpd
        state: present

    - name: Start web server
      service:
        name: httpd
        state: started
```

## Example Inventory Configuration

Below is an example inventory file that categorizes various hosts into groups:

```plaintext theme={null}
localhost

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

## Final Thoughts

Modules, tasks, and play definitions work in unison to create an orderly and efficient automation workflow. As you grow more comfortable with Ansible, you’ll discover advanced modules and strategies to manage configurations across a diverse range of environments.

Happy automating!

- [Watch Video](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/f7bcdbad-4792-4e82-beaa-b799773214fd/lesson/d35aa43c-c3ca-4a09-952e-19163dbd6241)


# Ansible lint

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Ansible-Playbooks/Ansible-lint/page

This article discusses how Ansible Lint enhances the quality of Ansible playbooks by identifying errors, bugs, and stylistic issues.

Verifying your Ansible playbooks using check mode and diff mode is a crucial step to ensure your configurations behave as expected. Now, let's explore how you can take your quality assurance to the next level using Ansible Lint.

![The image is a flowchart about verifying Ansible playbooks, highlighting "Check mode" and "Diff mode" under the topic "Introduction."](https://kodekloud.com/kk-media/image/upload/v1752881068/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-lint/frame_10.jpg)

Imagine you are a DevOps engineer at a busy software company. As you automate your infrastructure with Ansible, your growing collection of playbooks can become increasingly complex. Over time, this complexity might lead to challenges in understanding and maintaining your configurations. This is where Ansible Lint becomes essential.

Ansible Lint is a command-line tool designed for linting playbooks, roles, and collections. It meticulously scans your Ansible code for potential errors, bugs, stylistic issues, and suspicious constructs. Think of it as having an experienced mentor by your side offering valuable insights and catching issues that might go unnoticed.

![The image explains the need for ansible-lint, highlighting its role in checking Ansible playbooks for errors, bugs, and stylistic issues, akin to having a mentor.](https://kodekloud.com/kk-media/image/upload/v1752881069/notes-assets/images/Learn-Ansible-Basics-Beginners-Course-Ansible-lint/frame_60.jpg)

***

## Example: Linting a Sample Playbook

Consider a sample playbook named `style-example.yaml` that installs and configures Nginx. The playbook contains some style-related issues such as inconsistent indentation and non-uniform naming conventions for tasks.

```yaml theme={null}
- name: Style Example Playbook
  hosts: localhost
  tasks:
    - name: Ensure nginx is installed and started
      apt:
        name: nginx
        state: latest
        update_cache: yes

    - name: Enable nginx service at boot
      service:
        name: nginx
        enabled: yes
        state: started

    - name: Copy nginx configuration file
      copy:
        src: /path/to/nginx.conf
        dest: /etc/nginx/nginx.conf
        notify:
          - Restart nginx service

handlers:
  - name: Restart nginx service
    service:
      name: nginx
      state: restarted
```

When you run Ansible Lint on this playbook, you might see warnings like the following:

```bash theme={null}
$ ansible-lint style_example.yml
[WARNING]: incorrect indentation: expected 2 but found 4 (syntax/indentation)
style_example.yml:6
[WARNING]: command should not contain whitespace (blacklisted: ['apt']) (commands)
style_example.yml:6
[WARNING]: Use shell only when shell functionality is required (deprecated in favor of 'cmd') (commands)
style_example.yml:6
[WARNING]: command should not contain whitespace (blacklisted: ['service']) (commands)
style_example.yml:12
[WARNING]: 'name' should be present for all tasks (task-name-missing) (tasks)
style_example.yml:14
```

> **lightbulb** If Ansible Lint completes without any output, it means your playbook is free of linting issues.

This detailed feedback helps you pinpoint and address issues such as inconsistent indentation, incorrect module usage, and non-uniform task naming. Regularly integrating Ansible Lint into your workflow can help maintain the quality and reliability of your automation scripts.

***

This concludes our discussion on Ansible Lint. By incorporating this tool into your continuous integration processes, you can ensure that your Ansible playbooks are both efficient and error-free. For more detailed information, refer to the official [Ansible Documentation](https://docs.ansible.com/) and explore advanced linting practices.

Happy automating!

- [Watch Video](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/f7bcdbad-4792-4e82-beaa-b799773214fd/lesson/a179014f-17c5-41ee-9a66-89c125e9595e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course/module/f7bcdbad-4792-4e82-beaa-b799773214fd/lesson/0431ba24-9b8e-48d6-947b-48218e3e8508)
