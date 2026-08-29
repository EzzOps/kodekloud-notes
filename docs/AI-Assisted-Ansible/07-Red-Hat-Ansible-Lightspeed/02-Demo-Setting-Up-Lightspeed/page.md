# inventory
[webservers]
servera
```

Create a minimal `ansible.cfg` that points to the inventory and configures privilege escalation:

```ini theme={null}
# ansible.cfg
[defaults]
inventory = inventory

[privilege_escalation]
become_method = sudo
become = True
become_user = root
become_ask_pass = False
```

Open the `lightspeed` working directory in VS Code and use the Ansible extension / Lightspeed UI controls to generate a playbook.

<Frame>
  <img alt="A dark-themed Visual Studio Code welcome screen showing Ansible Lightspeed controls in a left sidebar, walkthroughs and start options in the center, and a &#x22;Build with agent mode&#x22; pane on the right. The UI also displays buttons for generating playbooks and roles and a feedback section." />
</Frame>

Prompt provided to Lightspeed (example):

```text theme={null}
Create a playbook which installs Apache on RHEL-based systems. Ensure Apache is started and enabled at boot. The target system is the group webservers from the inventory.
```

Lightspeed analyzes that prompt and proposes a complete playbook. After reviewing and refining the generated content for naming consistency and best practices (for example: capitalized task names, consistent module namespaces), this demo uses the following `site.yml`:

```yaml theme={null}
---
- name: Install Apache
  hosts: webservers
  become: True
  tasks:
    - name: Install Apache package
      ansible.builtin.yum:
        name: httpd
        state: present

    - name: Ensure Apache is Started
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: true

    - name: Place a template called index.html.j2 within /var/www/html/index.html
      ansible.builtin.template:
        src: templates/index.html.j2
        dest: /var/www/html/index.html
        owner: root
        group: root
        mode: '0644'
      notify: Restart Apache

  handlers:
    - name: Restart Apache
      ansible.builtin.service:
        name: httpd
        state: restarted
```

Why these choices

* ansible.builtin.yum: appropriate for RHEL-based systems (CentOS, RHEL, Alma, Rocky).
* become: True: ensures privileged operations (package install, service control) run with elevated privileges.
* Template + handler pattern: updates the site content idempotently and restarts Apache only when the template changes.

Create the template referenced by the playbook at `templates/index.html.j2`:

```jinja2 theme={null}
<!-- templates/index.html.j2 -->
<!doctype html>
<html>
  <head>
    <title>Welcome</title>
  </head>
  <body>
    <h1>Welcome to {{ ansible_facts['nodename'] }}</h1>
    <p>Managed by Ansible Lightspeed</p>
  </body>
</html>
```

Ask Lightspeed to "explain" the playbook — it will list prerequisites, describe each task and handler, and summarize expected results in plain language. For example: the playbook installs `httpd` on hosts in group `webservers`, ensures the service is running and enabled, deploys a templated `index.html`, and restarts Apache only when the template changes.

> **lightbulb** Lightspeed generates code, explains it, and suggests improvements — but always review generated playbooks for naming conventions, idempotence, and environment-specific constraints (for example SELinux context, firewall rules, or custom package sources).

Save the playbook as `site.yml` and run it from the control node:

```bash theme={null}
student@control:~/lightspeed$ ansible-playbook site.yml
```

Example (abridged) output when running the playbook:

```bash theme={null}
[WARNING]: Host 'servera' is using the discovered Python interpreter at '/usr/bin/python3.12'.
See https://docs.ansible.com/ansible-core/2.20/reference_appendices/interpreter_discovery.html

PLAY [Install Apache] *************************************************************

TASK [Gathering Facts] ************************************************************
ok: [servera]

TASK [Install Apache package] *****************************************************
ok: [servera]

TASK [Ensure Apache is Started] ***************************************************
ok: [servera]

TASK [Place a template called index.html.j2 within /var/www/html/index.html] ******
changed: [servera]

RUNNING HANDLER [Restart Apache] *************************************************
changed: [servera]

PLAY RECAP ************************************************************************
servera                   : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Artifacts you created

| File / Artifact | Purpose                                                         | Path                    |
| --------------- | --------------------------------------------------------------- | ----------------------- |
| Inventory       | Defines target group `webservers`                               | inventory               |
| ansible.cfg     | Points to inventory and configures privilege escalation         | ansible.cfg             |
| Playbook        | Installs and manages Apache, deploys template, notifies handler | site.yml                |
| Template        | Jinja2 HTML template using host facts                           | templates/index.html.j2 |

Notes on limitations and follow-ups

* Lightspeed excels at generation and explanation from natural language prompts, accelerating playbook creation.
* For larger, already-complex projects you may still need source-focused refactoring tools or manual review to enforce organization (roles, variables, testing pipelines).
* Consider adding SELinux and firewall tasks if your environment requires them, and include molecule tests for role-level validation.

References

* [Ansible Documentation](https://docs.ansible.com/)
* [Ansible VS Code Extension](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)
* [Ansible Playbooks — Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks.html)

Congratulations — you now have a simple, production-ready playbook generated and refined with Lightspeed, complete with a templated `index.html` and a handler to restart Apache when the template changes.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/c9159d88-f95d-4a1b-b9e9-faec8628aa03/lesson/877ca0de-0fbb-4c61-a14f-e4b033979138)


# Demo Setting Up Lightspeed

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Red-Hat-Ansible-Lightspeed/Demo-Setting-Up-Lightspeed/page

Guide to configuring and using Red Hat Ansible Lightspeed in VS Code to generate and autocomplete Ansible playbooks, authenticate, and validate suggestions

In this lesson we'll configure Red Hat Ansible Lightspeed — the AI assistant embedded in the [Red Hat Ansible extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=redhat.ansible). Lightspeed is purpose-built for Ansible: it understands Ansible modules, playbook syntax, and (optionally) your Automation Controller context so suggestions align with enterprise automation best practices.

Unlike general-purpose assistants such as [ChatGPT](https://chat.openai.com/) or [GitHub Copilot](https://github.com/features/copilot), Lightspeed is tightly coupled with the Ansible ecosystem and helps reduce YAML errors, accelerate development, and enforce consistent playbook patterns.

This demo will:

* Prepare your environment and prerequisites.
* Open the Lightspeed setup panel and authenticate to Red Hat if prompted.
* Generate a simple playbook using Lightspeed and validate autocomplete suggestions.

> **lightbulb** Ensure you have the [Red Hat Ansible extension for VS Code](https://marketplace.visualstudio.com/items?itemName=redhat.ansible) installed and that you're signed in with your Red Hat account (if prompted). Some Lightspeed features may require an active subscription or access to your Automation Controller context.

Quick demo flow

| Step                | Action                                                  | Expected result                                                 |
| ------------------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| Prepare environment | Install the Ansible extension and open VS Code          | Lightspeed UI available in the Ansible side panel               |
| Generate playbook   | Enter a natural language prompt in the Lightspeed panel | Lightspeed analyzes and creates a proposed playbook             |
| Test autocomplete   | Type natural-language task descriptions in the editor   | Lightspeed suggests Ansible tasks that can be accepted with Tab |

Now we'll generate a playbook. In the Lightspeed panel I type a natural-language prompt such as:

Create a playbook which installs Apache on [RHEL](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux) servers.

<Frame>
  <img alt="A dark-themed Visual Studio Code window displaying the Ansible Lightspeed &#x22;Create a playbook&#x22; panel, with the text &#x22;Create a playbook which installs apache&#x22; entered and an &#x22;Analyze&#x22; button. Sidebars show Ansible development tools on the left and a &#x22;Build with agent mode&#x22; pane on the right." />
</Frame>

I click Analyze. Lightspeed parses the request and summarizes the intended tasks. For this example the analysis shows:

```text theme={null}
1. Install apache

No problems have been detected in the workspace.
```

Click Continue to let Lightspeed create a new playbook file. The generated YAML appears in the editor. To test Lightspeed’s autocomplete, add another task by typing a natural description in the editor (for example: "Create a user called test") and press Enter. Lightspeed will present a suggestion for the corresponding Ansible task — accept it with Tab to insert the task into your playbook.

Resulting playbook (with become set to escalate privileges where needed):

```yaml theme={null}
---
- name: Install apache on rhel
  hosts: rhel
  become: true
  tasks:
    - name: Install apache
      ansible.builtin.package:
        name: httpd
        state: present

    - name: Create a user called test
      ansible.builtin.user:
        name: test
        state: present
```

What to expect

* Generated suggestions appear inline in the editor and can be accepted or edited.
* You can refine prompts, add variables, or extend tasks to match your organization's requirements.
* If you provide Automation Controller context or inventories, Lightspeed can generate suggestions that better match your environment.

> **warning** If Lightspeed does not produce suggestions, verify you are signed in to the Red Hat Ansible extension, your extension is up to date, and any required subscription or Automation Controller access is available.

Links and references

* [Red Hat Ansible extension for VS Code](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)
* [Ansible documentation — modules and playbooks](https://docs.ansible.com/ansible/latest/)
* [Automation Controller (Ansible Tower) documentation](https://docs.ansible.com/automation-controller/latest/)
* [Red Hat Enterprise Linux (RHEL)](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)

Troubleshooting tips

* Ensure VS Code and the Ansible extension are updated.
* Restart VS Code if the Lightspeed panel does not load.
* Check extension logs (View → Output → Ansible) for authentication or connectivity issues.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/c9159d88-f95d-4a1b-b9e9-faec8628aa03/lesson/6a15f706-251d-4e42-bd5a-1daa9dc6e12e)
