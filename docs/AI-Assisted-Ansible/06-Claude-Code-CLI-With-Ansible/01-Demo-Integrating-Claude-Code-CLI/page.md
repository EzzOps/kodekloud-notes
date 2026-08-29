# inventory
[webservers]
servera ansible_host=10.0.2.4
```

3. Create a minimal ansible.cfg so you don't need to pass --inventory or --user on the command line. Save this as ansible.cfg in the project folder.

```ini theme={null}
[defaults]
inventory = inventory
remote_user = student

[privilege_escalation]
become = true
become_user = root
become_method = sudo
become_ask_pass = false
```

Files you will create

| File          | Purpose                                                           |
| ------------- | ----------------------------------------------------------------- |
| inventory     | Defines target hosts (webservers group)                           |
| ansible.cfg   | Project-local defaults (inventory, remote\_user, become settings) |
| playbook.yml  | The Ansible playbook with tasks and handlers                      |
| index.html.j2 | Jinja2 template for the web page                                  |

Write the playbook
Create playbook.yml with the content below. The playbook installs the httpd package, deploys a simple index.html template, starts the httpd service, and notifies a handler to restart httpd when the template changes.

```yaml theme={null}
# playbook.yml
- name: install httpd on servera
  hosts: webservers
  vars:
    httpd_pkg: httpd
    httpd_svc: httpd
  tasks:
    - name: Install Apache webserver
      dnf:
        name: "{{ httpd_pkg }}"
        state: latest

    - name: Deploy content
      template:
        src: index.html.j2
        dest: /var/www/html/index.html
      notify: restart httpd

    - name: Start httpd service
      service:
        name: "{{ httpd_svc }}"
        state: started

  handlers:
    - name: restart httpd
      service:
        name: "{{ httpd_svc }}"
        state: restarted
```

Create the template
Create the Jinja2 template index.html.j2 in the same project directory. This template uses an Ansible facts variable to include the host's hostname in the page.

```jinja2 theme={null}
Hello from {{ ansible_hostname }}
```

Validate and run the playbook

1. Perform a syntax check:

```bash theme={null}
student@control:~/project$ ansible-playbook playbook.yml --syntax-check
playbook: playbook.yml
```

2. Run the playbook:

```bash theme={null}
student@control:~/project$ ansible-playbook playbook.yml
```

Example (condensed) output showing the play execution:

```text theme={null}
PLAY [install httpd on servera] ****************************************************

TASK [Gathering Facts] *************************************************************
ok: [servera]

TASK [Install Apache webserver] ****************************************************
changed: [servera]

TASK [Deploy content] **************************************************************
changed: [servera]

TASK [Start httpd service] *********************************************************
changed: [servera]

RUNNING HANDLER [restart httpd] ***************************************************
changed: [servera]

PLAY RECAP ************************************************************************
servera                   : ok=5    changed=4    unreachable=0    failed=0    skipped=0
```

Verify the result on the managed host
SSH to the managed host (or use a remote check) and curl the local web server to confirm the template is served:

```bash theme={null}
student@control:~/project$ ssh servera
student@servera:~$ curl -s http://localhost
Hello from servera
```

This confirms the playbook installed httpd, deployed the index.html template, started the service, and the handler restarted httpd after the template changed.

Conclusion
You've created a minimal, reusable Ansible project that automates installing and configuring an Apache-based test page on RHEL. This covers essential Ansible concepts—inventory, configuration, variables, tasks, templates, and handlers—that form the foundation for more advanced automation.

Links and references

* [Ansible Documentation](https://docs.ansible.com/)
* [Ansible Playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)
* [Jinja2 Template Documentation](https://jinja.palletsprojects.com/)
* [RHEL System Administration Guide](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/)

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/307b5a5b-ba65-4d55-97aa-29271c722c39/lesson/927531d9-6a32-46b3-9267-0aaa3925ba6f)


# Demo Integrating Claude Code CLI

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Claude-Code-CLI-With-Ansible/Demo-Integrating-Claude-Code-CLI/page

Demo guiding DevOps engineers to install and authenticate Claude Code CLI, generate and validate Ansible ad-hoc commands and playbooks from the terminal.

In this lesson you'll add Claude Code to an Ansible workflow so you can generate ad-hoc commands and playbooks directly from the terminal. Claude Code is a lightweight CLI client for Anthropic's Claude models that connects to the Claude API and helps developers author scripts, playbooks, and commands without leaving their shell.

<Frame>
  <img alt="A presentation slide titled &#x22;Integrating Claude Code CLI&#x22; with a central circular logo and three numbered points: &#x22;Built for developers,&#x22; &#x22;Works directly from the terminal,&#x22; and &#x22;Generates Ansible playbooks.&#x22;" />
</Frame>

Target audience: systems engineers and DevOps practitioners managing Linux servers across multiple environments who want to pilot AI-assisted automation to speed up routine tasks.

<Frame>
  <img alt="The image is a presentation slide titled &#x22;Integrating Claude Code CLI&#x22; showing an illustration of a person working on a laptop with a chat/code window. To the right are three feature bullets: &#x22;Lightweight local CLI,&#x22; &#x22;Secure API connection,&#x22; and &#x22;Powered by Claude 3 models.&#x22;" />
</Frame>

What you will do in this demo:

* Verify required system packages and environment
* Install the Claude Code CLI
* Authenticate the CLI (interactive browser flow)
* Validate Claude-generated Ansible ad-hoc commands and playbooks

<Frame>
  <img alt="A dark-themed presentation slide titled &#x22;Demo&#x22; showing a two-column, numbered list of steps: verify required system packages, install Claude Code CLI, authenticate Claude Code CLI, and validate playbook and Ansible ad-hoc command generation." />
</Frame>

## 1. Prepare the VM and shell

Switch to the student virtual machine and ensure you are in the home directory:

```bash theme={null}
student@control:~/claude$ cd ~
student@control:~$ clear
```

## 2. Install Claude Code CLI

Install the CLI using the official installer script (curl piped to bash):

```bash theme={null}
student@control:~$ curl -fsSL https://claude.ai/install.sh | bash
```

Sample installer output:

```output theme={null}
Setting up Claude Code...

✔ Claude Code successfully installed!

Version: 2.0.37
Location: ~/.local/bin/claude

Next: Run claude --help to get started

✅ Installation complete!
student@control:~$
```

## 3. Authenticate the CLI

Start the interactive login flow:

```bash theme={null}
student@control:~$ claude login
```

The CLI presents the login options:

```output theme={null}
Claude Code can be used with your Claude subscription or billed based on API usage through your Console account.

Select login method:

› 1. Claude account with subscription · Pro, Max, Team, or Enterprise
  2. Anthropic Console account · API usage billing
```

Choose the appropriate method. In this demo the user selects a Claude account and authenticates via Google; a browser window opens for the OAuth flow.

<Frame>
  <img alt="A computer desktop screenshot showing a Firefox browser open to the Claude.ai login page with a Google sign-in popup window loading. A smaller dialog on the page prompts the user to connect using a Google account (the prompt text appears in Romanian)." />
</Frame>

After completing the browser-based login, the CLI displays security notes describing model limitations and guidance.

<Frame>
  <img alt="A dark terminal-style screen displaying &#x22;Security notes&#x22; about Claude — warning that Claude can make mistakes and advising caution with code and prompt injection, plus a link to documentation. An orange ASCII-art character appears at the top left and a &#x22;Press Enter to continue…&#x22; prompt is shown." />
</Frame>

> **lightbulb** Claude models can make mistakes and prompts might include unsafe instructions. Be cautious when executing generated code or granting filesystem access.

Allow the CLI the requested workspace permissions, complete the flow, and return to the shell. If the process is interrupted you may see:

```text theme={null}
> /login
└ Login interrupted

student@control:~$
```

Re-run `claude login` to retry if needed.

## 4. Quick verification: ask Claude for Ansible ad-hoc commands

Try a simple prompt to generate an Ansible ad-hoc ping command for your inventory:

```bash theme={null}
student@control:~$ claude -p "Ansible ad-hoc command to ping all hosts within inventory"
```

Claude typically returns several valid variations. Common examples include:

|                           Use case | Command                                        |
| ---------------------------------: | ---------------------------------------------- |
| Ping all hosts (default inventory) | ansible all -m ping                            |
| Ping all hosts using become (sudo) | ansible all -m ping --become                   |
| Ping a specific group (webservers) | ansible webservers -m ping                     |
|            Ping as a specific user | ansible all -m ping -u username                |
|           Ping with verbose output | ansible all -m ping -v                         |
|            Prompt for SSH password | ansible all -m ping --ask-pass                 |
|         Prompt for become password | ansible all -m ping --become --ask-become-pass |

Note on the Ansible ping module:

* The `ping` module does not send ICMP packets; it executes a small Python task on the remote and returns "pong" on success. It verifies:
  * SSH connectivity
  * SSH authentication
  * Python availability on the remote host

If your inventory doesn't match Claude's suggested pattern, Ansible will warn that the host pattern couldn't be matched:

```bash theme={null}
student@control:~$ ansible webservers -m ping
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'
[WARNING]: Could not match supplied host pattern, ignoring: webservers
```

Inspect your workspace inventory to confirm host groups:

```bash theme={null}
student@control:~$ cd claude/
student@control:~/claude$ ls
ansible.cfg  inventory  site.yml
student@control:~/claude$ ansible webservers -m ping
