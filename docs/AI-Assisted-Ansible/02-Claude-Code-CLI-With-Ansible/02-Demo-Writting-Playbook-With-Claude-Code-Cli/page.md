# (runs against hosts defined in inventory)
```

## 5. Interactive mode: compose playbooks with natural language

Run `claude` without flags to enter interactive mode. Use plain language or slash commands to control behavior and persist prompts:

```text theme={null}
Claude Code v2.0.37

Welcome back andrei!

Sonnet 4.5 · Claude Pro
/home/student/claude

Tips for getting started
Run /init to create a CLAUDE.md file with instructions for Claude
Run /install-github-app to tag @claude right from your Github issues and PRs

Recent activity
No recent activity

> Try "fix lint errors"

? for shortcuts                                      Thinking on (tab to toggle)
```

Ask Claude to generate a small Ansible playbook. Example prompt:

```text theme={null}
> As a DevOps engineer, generate a small Ansible playbook which creates the user test within the group webservers
```

Claude may produce a draft like this:

```yaml theme={null}
- name: Create test user in webservers group
  hosts: all
  become: yes
  tasks:
    - name: Ensure webservers group exists
      ansible.builtin.group:
        name: webservers
        state: present

    - name: Create test user and add to webservers group
      ansible.builtin.user:
        name: test
        group: webservers
        state: present
        create_home: yes
        shell: /bin/bash
```

If you intended to target the `webservers` host group (not create a system group), update the playbook to set `hosts: webservers` and remove the group-creation task. Corrected example:

```yaml theme={null}
- name: Create test user on webservers
  hosts: webservers
  become: yes
  tasks:
    - name: Create test user and add to webservers group
      ansible.builtin.user:
        name: test
        group: webservers
        state: present
        create_home: yes
        shell: /bin/bash
```

Save the playbook (for example, `create_user.yml`) and run it against your inventory:

```bash theme={null}
student@control:~$ ansible-playbook -i inventory create_user.yml
```

This demonstrates how Claude Code can draft useful Ansible content that you then review and refine before applying to your environment.

## Troubleshooting tips

* If `claude` is not found after installation, ensure `~/.local/bin` is in your PATH:
  ```bash theme={null}
  echo $PATH
  export PATH=$HOME/.local/bin:$PATH
  ```
* If browser login fails, try the alternate login method (Anthropic Console) or re-run `claude login`.
* Always review generated code for security, prompt injection, and correctness before executing.

## Helpful commands summary

| Action                  | Command                                                                         |
| ----------------------- | ------------------------------------------------------------------------------- |
| Install Claude Code     | curl -fsSL [https://claude.ai/install.sh](https://claude.ai/install.sh) \| bash |
| Authenticate CLI        | claude login                                                                    |
| Quick prompt from shell | claude -p "your prompt here"                                                    |
| Interactive mode        | claude                                                                          |
| Run playbook            | ansible-playbook -i inventory create\_user.yml                                  |

## Links and references

* [Anthropic Claude](https://claude.ai/)
* [Claude Code docs (install/login)](https://claude.ai/docs)
* [Ansible Documentation — ad-hoc commands](https://docs.ansible.com/ansible/latest/cli/ansible.html)
* [Ansible Documentation — playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)

This concludes the demo. You have installed and authenticated the Claude Code CLI, used it to generate Ansible ad-hoc commands and a playbook, and learned how to refine and run the output in your environment.

Congratulations!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/e8212b1c-d691-4db0-8c94-057594294b02/lesson/2ded7d22-d440-4f62-b709-3bbdd496561f" />
</CardGroup>


# Demo Writting Playbook With Claude Code Cli

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Claude-Code-CLI-With-Ansible/Demo-Writting-Playbook-With-Claude-Code-Cli/page

Guide to using Claude Code CLI to generate, refactor, lint, and run an Ansible playbook that installs and configures Apache httpd on RHEL hosts.

In this lesson you will use the Claude Code For Beginners CLI to generate and refine an Ansible playbook that installs and configures the Apache (httpd) web server on RHEL-based hosts. The walkthrough covers setting up a control-node workspace, generating a baseline playbook with Claude Code, refactoring to best practices (FQCNs, templates, lineinfile, handlers), validating, and running the playbook.

<Frame>
  <img alt="A presentation slide titled &#x22;Writing Playbook With Claude Code CLI&#x22; showing an illustration of a person at a computer. The slide notes testing Claude Code CLI’s ability to generate an Ansible playbook for Apache (httpd) setup." />
</Frame>

Overview — workflow

* Create a working directory and inventory
* Configure ansible.cfg
* Use Claude Code to generate site.yml (the playbook)
* Validate and refactor the playbook (use FQCNs, add template, lineinfile, handlers)
* Run ansible-lint / validate
* Execute the playbook and verify the result

For quick reference, here’s the workflow in a compact table:

| Step | Action                                 | Why                                                  |
| ---- | -------------------------------------- | ---------------------------------------------------- |
| 1    | Create workspace + inventory           | Tell Ansible which hosts to manage                   |
| 2    | Configure ansible.cfg                  | Ensure consistent behaviour and privilege escalation |
| 3    | Generate site.yml via Claude Code      | Quickly scaffold a working playbook                  |
| 4    | Refactor (FQCNs, template, lineinfile) | Improve clarity, maintainability, and idempotence    |
| 5    | Lint/validate                          | Catch issues early with ansible-lint                 |
| 6    | Run playbook and verify                | Confirm the web server is configured correctly       |

<Frame>
  <img alt="A dark-themed slide titled &#x22;Demo&#x22; listing six numbered steps. It outlines setting up a working directory, configuring the Claude Code CLI, generating and validating a playbook (site.yml), asking Claude to refactor it, and validating/executing the refactored playbook." />
</Frame>

Preparation — create the control-node workspace
Run these commands in your Claude Code workspace to create a working directory and files:

```bash theme={null}
student@control:~/claude$ pwd
/home/student/claude
student@control:~/claude$ vim inventory
student@control:~/claude$ vim ansible.cfg
student@control:~/claude$ claude
```

Example inventory (inventory)

```ini theme={null}
[webservers]
servera
```

Example ansible.cfg

```ini theme={null}
[defaults]
inventory = inventory

[privilege_escalation]
become = true
become_user = root
become_method = sudo
become_ask_pass = false
```

Generate an initial playbook with Claude Code
Start an interactive Claude Code session and ask it to create a playbook named site.yml that installs httpd on hosts in the webservers group (RHEL-based systems). Example CLI snippet:

```bash theme={null}
student@control:~/claude$ claude

Claude Code v2.0.37

Welcome back andrei!
/home/student/claude

> Create an ansible playbook file called site.yml which installs httpd on the group of hosts called webservers which are RHEL-based systems.
```

Claude Code will typically generate a simple playbook like this. Open site.yml in your editor to inspect it.

Initial generated site.yml

```yaml theme={null}
---
- name: Install and configure httpd on webservers
  hosts: webservers
  become: yes

  tasks:
    - name: Install httpd package
      yum:
        name: httpd
        state: present

    - name: Start and enable httpd service
      service:
        name: httpd
        state: started
        enabled: yes
```

Refactor to use Fully Qualified Collection Names (FQCNs)
Best practice: use FQCNs such as ansible.builtin.yum and ansible.builtin.service to avoid ambiguity and ensure the intended module is executed. Ask Claude Code to refactor the playbook to FQCNs or update it yourself.

site.yml with FQCNs

```yaml theme={null}
---
- name: Install and configure httpd on webservers
  hosts: webservers
  become: yes

  tasks:
    - name: Install httpd package
      ansible.builtin.yum:
        name: httpd
        state: present

    - name: Start and enable httpd service
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: yes
```

Add a Jinja2 template to serve host facts
Create a template that renders host-specific facts (hostname and fqdn) to /var/www/html/index.html. Example template (index.html.j2):

index.html.j2

```html theme={null}
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome to {{ ansible_hostname }}</h1>
    <p>This page is served from host: {{ ansible_fqdn }}</p>
</body>
</html>
```

Deploy the template and use lineinfile for attribution
Rather than embedding the attribution directly into the template, demonstrate combining modules: deploy the template using ansible.builtin.template, then add an attribution line using ansible.builtin.lineinfile. Notify a handler to reload httpd when the file changes.

Tasks to add

```yaml theme={null}
- name: Deploy index.html from template
  ansible.builtin.template:
    src: index.html.j2
    dest: /var/www/html/index.html
    owner: root
    group: root
    mode: '0644'
  notify: Reload httpd

- name: Add attribution line to index.html
  ansible.builtin.lineinfile:
    path: /var/www/html/index.html
    line: "This was created by ansible and claude"
    insertbefore: '</body>'
  notify: Reload httpd
```

Add the handler

```yaml theme={null}
handlers:
  - name: Reload httpd
    ansible.builtin.service:
      name: httpd
      state: reloaded
```

Consolidated site.yml
Below is the full playbook that combines installation, service management, template deployment, line insertion, and the handler.

```yaml theme={null}
---
- name: Install and configure httpd on webservers
  hosts: webservers
  become: yes

  tasks:
    - name: Install httpd package
      ansible.builtin.yum:
        name: httpd
        state: present

    - name: Start and enable httpd service
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: yes

    - name: Deploy index.html from template
      ansible.builtin.template:
        src: index.html.j2
        dest: /var/www/html/index.html
        owner: root
        group: root
        mode: '0644'
      notify: Reload httpd

    - name: Add attribution line to index.html
      ansible.builtin.lineinfile:
        path: /var/www/html/index.html
        line: "This was created by ansible and claude"
        insertbefore: '</body>'
      notify: Reload httpd

  handlers:
    - name: Reload httpd
      ansible.builtin.service:
        name: httpd
        state: reloaded
```

Linting and validation
Before running the playbook in production, consider running ansible-lint to catch common issues:

```bash theme={null}
ansible-lint site.yml
```

Execute the playbook
Run the playbook from your control node:

```bash theme={null}
student@control:~/claude$ ansible-playbook /home/student/claude/site.yml
```

Example playbook execution (trimmed)

```text theme={null}
PLAY [Install and configure httpd on webservers] ********************************

TASK [Gathering Facts] *********************************************************
ok: [servera]

TASK [Install httpd package] ***************************************************
changed: [servera]

TASK [Start and enable httpd service] ******************************************
changed: [servera]

TASK [Deploy index.html from template] *****************************************
changed: [servera]

TASK [Add attribution line to index.html] **************************************
changed: [servera]

RUNNING HANDLER [Reload httpd] *************************************************
changed: [servera]
```

Verify on the managed host
Confirm the web page is served and contains the expected facts and attribution.

```bash theme={null}
student@servera:~$ curl localhost:80
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>

</head>
<body>
    <h1>Welcome to servera</h1>
    <p>This page is served from host: servera</p>
This was created by ansible and claude
</body>
</html>
student@servera:~$
```

Wrapping up
You have used Claude Code For Beginners to scaffold an Ansible playbook, refactored it to follow best practices (FQCNs, templates, handlers), and executed it against a managed RHEL-based host. This pattern—generate, inspect, refactor, and validate—helps you move quickly while keeping playbooks maintainable and predictable.

Links and references

* Claude Code For Beginners course: [https://learn.kodekloud.com/user/courses/claude-code-for-beginners](https://learn.kodekloud.com/user/courses/claude-code-for-beginners)
* Jinja2 Basics (Mini Course): [https://learn.kodekloud.com/user/courses/jinja2-basics-mini-course](https://learn.kodekloud.com/user/courses/jinja2-basics-mini-course)
* Ansible documentation: [https://docs.ansible.com/](https://docs.ansible.com/)
* ansible-lint: [https://ansible-lint.readthedocs.io/](https://ansible-lint.readthedocs.io/)

<Callout icon="lightbulb">
  Use FQCNs (ansible.builtin.\*) in playbooks to avoid ambiguity and ensure the intended module is executed.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/e8212b1c-d691-4db0-8c94-057594294b02/lesson/ebc8fcf2-2916-4c2a-883d-e77a774c5c82" />
</CardGroup>
