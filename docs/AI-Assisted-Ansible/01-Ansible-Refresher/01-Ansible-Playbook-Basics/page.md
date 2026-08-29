# Ansible Playbook Basics

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Ansible-Refresher/Ansible-Playbook-Basics/page

Overview of Ansible playbooks covering structure, components, execution, and best practices for automating system configuration and application deployment

In this lesson we focus on one of the most important parts of Ansible: playbooks. Understanding how playbooks are structured and how they execute gives you a reliable foundation to automate system configuration, application deployment, and operational tasks.

What is a playbook?
Think of a playbook as an automation blueprint: a human-readable, declarative description of the desired end state for one or more hosts. Ansible evaluates the declaration and makes the remote systems match that state. Playbooks use YAML for readability and maintainability so teams can review, share, and version control automation easily.

<Frame>
  <img alt="A slide titled &#x22;What Is a Playbook?&#x22; showing four numbered cards labeled 01 Blueprint, 02 Desired state, 03 YAML file, and 04 Human-readable and repeatable, each with a small icon." />
</Frame>

Key benefits of using playbooks

* Consistency: Running the same playbook produces the same result every time.
* Scale: Apply the same configuration across many hosts in a single run.
* Idempotence: Re-running a playbook leaves systems unchanged when they already match the desired state.
* Readability: Playbooks double as documentation for what your automation does.

<Frame>
  <img alt="A presentation slide titled &#x22;Playbooks – Benefits&#x22; with four turquoise circular icons across the top. The icons are labeled &#x22;Consistency,&#x22; &#x22;Saves time,&#x22; &#x22;Safe and idempotent,&#x22; and &#x22;Readable.&#x22;" />
</Frame>

Basic skeleton of a playbook
A playbook is one or more plays, and a play targets one or more hosts. At minimum, a play typically contains:

* `name`: a descriptive label for the play
* `hosts`: the inventory group or host pattern to target
* `become`: whether to use privilege escalation (e.g., sudo)
* `tasks`: a list of steps (each task calls a module)

Every playbook begins with the YAML document marker `---`.

Example minimal playbook:

```yaml theme={null}
---
- name: My play
  hosts: all
  become: true
  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
```

Everything else — variables, handlers, roles, loops, and conditionals — builds on this same foundation.

Playbook components explained
Below is a quick reference for the main building blocks you’ll use in playbooks.

| Component            | Purpose                                                       | Common examples                                  |
| -------------------- | ------------------------------------------------------------- | ------------------------------------------------ |
| Tasks                | Ordered steps executed on target hosts                        | Use modules like `apt`, `yum`, `file`, `service` |
| Modules              | Idempotent units that perform actions                         | `apt`, `copy`, `template`, `uri`                 |
| Handlers             | Tasks triggered only when notified (useful for restarts)      | `notify: Restart nginx`                          |
| Roles                | Directory layout for reusable code and separation of concerns | `roles/nginx/tasks/main.yml`                     |
| Variables            | Parameterize values across environments                       | Inventory vars, `vars_files`, `host_vars`        |
| Loops & Conditionals | Iterate or run tasks conditionally to avoid duplication       | `loop`, `when`                                   |

<Frame>
  <img alt="A slide titled &#x22;Playbook Components&#x22; showing six labeled cards in two columns—left: Tasks, Modules, Handlers; right: Roles, Variables, Loops & Conditionals—each paired with a simple icon. The layout uses a dark blue background with teal accents." />
</Frame>

Running and validating playbooks
Use `ansible-playbook` to execute playbooks. Before applying changes to real systems, validate syntax and structure.

Commands:

```bash theme={null}
