# Run a playbook
ansible-playbook site.yml

# Check playbook syntax without connecting to hosts
ansible-playbook --syntax-check site.yml
```

Quick command references

| Task            | Command                                    |
| --------------- | ------------------------------------------ |
| Run a playbook  | `ansible-playbook site.yml`                |
| Syntax check    | `ansible-playbook --syntax-check site.yml` |
| Check inventory | `ansible-inventory --list -i inventory/`   |

Best practices and habits
Adopt these habits to keep playbooks reliable and maintainable:

<Callout icon="lightbulb">
  * Always include a `name` for plays and for every task — it improves readability and troubleshooting.
  * Run `ansible-playbook --syntax-check` before applying changes.
  * Use handlers to avoid unnecessary service restarts when multiple tasks might trigger the same action.
  * Prefer loops and conditionals over duplicating similar tasks to keep your playbooks concise and adaptable.
</Callout>

Additional tips:

* Keep roles focused and small; one role should do one job.
* Use `check_mode` (`ansible-playbook --check`) for dry runs where appropriate.
* Store secrets in Ansible Vault and avoid committing secrets to version control.
* Keep host- and group-level variables in separate `host_vars/` and `group_vars/` directories for clarity.

Conclusion
These fundamentals — structure, modules, handlers, roles, variables, and the habit of validating before running — are the building blocks of effective Ansible automation. Once comfortable with these basics, you can expand into advanced topics like custom modules, dynamic inventories, and complex role reuse.

Further reading

* [Ansible Documentation — Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
* [YAML Official Specification](https://yaml.org/spec/)
* [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/307b5a5b-ba65-4d55-97aa-29271c722c39/lesson/ed9675d8-0f9f-4b59-8913-9381fc969290" />
</CardGroup>


# Demo Writing a Simple Playbook

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Ansible-Refresher/Demo-Writing-a-Simple-Playbook/page

Tutorial showing how to create an Ansible playbook to install and configure Apache on RHEL, deploy a template index page, and manage the service with handlers.

Now that you understand what an Ansible playbook is and how its structure works, let's build one from a real-world scenario. This tutorial converts a repetitive manual process into automation so you can deploy a basic web test environment consistently across RHEL hosts.

Imagine a small fleet of RHEL servers where developers often need a disposable web test site. Currently someone manually installs Apache (httpd), enables and starts the service, and drops a test page. We'll automate those steps with a single Ansible playbook.

<Frame>
  <img alt="A slide titled &#x22;Automating Manual Web Setup&#x22; showing a developer icon connected to a group of RHEL servers. To the right are three listed steps: Install Apache, Start service, and Deploy test page." />
</Frame>

What you'll build

* A small Ansible project that installs httpd, deploys a template-based index.html, ensures the service is running, and restarts httpd when content changes.
* The playbook demonstrates inventory, ansible.cfg defaults, variables, tasks, templates, and handlers—the core building blocks of Ansible automation.

Workflow

* Create a project folder and basic files.
* Define an inventory that targets the managed host(s).
* Add a minimal ansible.cfg so you don't need extra CLI flags.
* Write a playbook with tasks and handlers.
* Run the playbook and verify the result on the managed host.

Environment overview

| Item                 | Details                                     |
| -------------------- | ------------------------------------------- |
| Control host         | Where Ansible runs (your workstation)       |
| Managed host         | servera (RHEL)                              |
| Authentication       | SSH public-key authentication preconfigured |
| Remote user          | student (passwordless sudo configured)      |
| Privilege escalation | sudo via sudoers drop-in (no password)      |

<Callout icon="lightbulb">
  Ensure the Ansible remote user can perform privileged tasks. In this lab the sudoers entry allows the student user to use sudo without a password:
</Callout>

```text theme={null}
student ALL=(ALL) NOPASSWD: ALL
```

<Callout icon="warning">
  Be careful granting NOPASSWD sudo in production. Use the minimum required privileges and restrict commands where possible.
</Callout>

Install Ansible Core (example)

* Install Ansible on the control host. The example below uses dnf on RHEL; replace with your platform's package manager if needed.

```text theme={null}
student@control:~$ sudo dnf install -y ansible-core
...
Installed:
    ansible-core-1:2.16.14-1.el10.noarch  ...
Complete!
student@control:~$
```

Create the project directory and files

1. Create a project folder and enter it:

```bash theme={null}
student@control:~$ mkdir project
student@control:~$ cd project
```

2. Create an inventory file. This example defines a webservers group with servera. Adjust ansible\_host if you need an explicit IP.

```ini theme={null}
