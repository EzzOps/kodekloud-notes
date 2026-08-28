# Example:
# pip 23.3.2 from /usr/lib/python3.12/site-packages/pip (python 3.12)
```

Tip: use pip3 (not pip) to target the system Python 3 environment on modern RHEL systems.

## 2. Download and install Visual Studio Code (RPM)

Visit the Visual Studio Code download page and choose the RPM for Red Hat / Fedora (suitable for RHEL 10). You can install the downloaded RPM via the GUI package installer or from the terminal:

```bash theme={null}
sudo dnf install ./code-*.rpm
```

<Frame>
  <img alt="A web browser screenshot showing the Visual Studio Code documentation page, with a “Thanks for downloading VS Code!” banner at the top and &#x22;Getting started&#x22; and feature sections below. The left sidebar lists docs topics and a Download button is visible in the toolbar." />
</Frame>

Launch VS Code from the desktop menu or terminal:

```bash theme={null}
code
```

## 3. Install the Red Hat Ansible extension (and YAML support)

Open the Extensions view (Ctrl+Shift+X), search for "Ansible", and install the Red Hat Ansible extension (redhat.ansible). If you do not already have YAML language support, install the Red Hat YAML extension (redhat.vscode-yaml) — the Ansible extension relies on robust YAML parsing for many features.

<Frame>
  <img alt="A dark-themed Visual Studio Code window showing the Extensions Marketplace with Ansible-related extensions on the left and a central welcome panel titled &#x22;Create an Ansible environment&#x22; that illustrates creating an Ansible playbook and project. The right side shows a &#x22;Build with agent mode&#x22; pane and a small notification about Red Hat extension telemetry." />
</Frame>

## 4. Install Ansible development helpers (optional but recommended)

The Ansible extension delegates linting and parsing to helper tools such as ansible-core, ansible-lint, and yamllint. Install them individually with pip3:

```bash theme={null}
pip3 install --user ansible-core ansible-lint yamllint
```

Or, where available, install a meta-package like ansible-devtools:

```bash theme={null}
pip3 install --user ansible-devtools
```

Example (truncated) pip output:

```bash theme={null}
Collecting ansible-core
Collecting ansible-lint
Collecting yamllint
Collecting ruamel.yaml
...
Successfully installed ansible-core-2.20.0 ansible-lint-25.9.2 yamllint-1.37.1 ruamel.yaml-0.18.16
```

Note: The extension will also work with system-installed ansible or ansible-core; ensure ansible-core exists if you want to run playbooks locally from VS Code.

## 5. What the Ansible extension provides

After installation, the Red Hat extension exposes features like:

* Autocompletion for modules and parameters (with FQCN support).
* Linting annotations (ansible-lint, yamllint integration).
* Quick actions for running or debugging playbooks.
* Playbook and inventory detection in the workspace.

<Frame>
  <img alt="A screenshot of Visual Studio Code displaying the Ansible extension page (by Red Hat) with details, installation requirements, and a preview image. The left sidebar shows Ansible development tools and the right panel has a &#x22;Build with agent mode&#x22; prompt." />
</Frame>

## 6. Open your Ansible project folder

Open the folder that contains ansible.cfg, inventory, and playbooks. VS Code will prompt whether you trust the workspace authors — decide according to your security policy.

<Callout icon="warning">
  When prompted "Do you trust the authors of the files in this folder?", follow your organization’s security guidance. Opening untrusted workspaces can restrict some extension features until you mark the workspace as trusted.
</Callout>

<Frame>
  <img alt="A Visual Studio Code window displaying the Welcome screen with a central modal asking &#x22;Do you trust the authors of the files in this folder?&#x22; and buttons to trust or not trust. The Explorer shows a &#x22;project&#x22; folder (with ansible.cfg, inventory, playbook.yml) and an agent/agent-mode panel on the right." />
</Frame>

## 7. Validate the extension with a sample playbook

Create or open a minimal playbook (playbook.yml) to see autocompletion and linting in action. Example:

```yaml theme={null}
---
- name: My Play
  hosts: webservers
  tasks:
    - name: Show message
      ansible.builtin.debug:
        msg: "Hello, world"
```

As you edit:

* Autocomplete suggestions appear for modules and parameters.
* ansible-lint/yamllint (if installed) will surface warnings or rule violations.
* The extension recommends using fully-qualified collection names (FQCN), e.g., ansible.builtin.debug.

<Callout icon="lightbulb">
  Using fully-qualified module names (for example `ansible.builtin.debug`) makes playbooks unambiguous about which collection provides a module. Short names (like `debug`) still work but can trigger linter warnings depending on your ruleset.
</Callout>

## 8. Run the playbook

Run the playbook from VS Code's integrated terminal or use quick run actions from the extension. A standard command:

```bash theme={null}
ansible-playbook -i inventory playbook.yml
```

If you prefer to run within VS Code, use the integrated terminal (View → Terminal) or the extension’s run actions.

## Troubleshooting — common issues

* No hosts matched / host unreachable:
  * Verify inventory group names and host entries.
  * Ensure SSH connectivity and correct credentials.
* Linter warnings you disagree with:
  * Configure ansible-lint rules via a .ansible-lint or configuration file in your project, or disable specific checks.
* Extension not recognizing playbooks:
  * Confirm the workspace contains typical Ansible files (ansible.cfg, inventory, playbook.yml) and that workspace trust is enabled if necessary.

If a host (e.g., host1) is marked unreachable:

* Confirm the host exists in the inventory and is assigned to the correct group (e.g., webservers).
* Verify network connectivity, SSH keys, and user settings.

## Links and references

* Visual Studio Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)
* Red Hat Ansible extension (VS Code Marketplace): [https://marketplace.visualstudio.com/items?itemName=redhat.ansible](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)
* Red Hat YAML extension (VS Code Marketplace): [https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
* Ansible core & community tools (PyPI): [https://pypi.org/project/ansible-core/](https://pypi.org/project/ansible-core/) and [https://pypi.org/project/ansible-lint/](https://pypi.org/project/ansible-lint/)
* ansible-devtools meta-package: [https://pypi.org/project/ansible-devtools/](https://pypi.org/project/ansible-devtools/)

With VS Code, the Red Hat Ansible extension, and the optional helper tools installed, you’ll have consistent in-editor completion, linting, and the ability to run playbooks — improving collaboration and code quality across your team.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/d87dae2c-1617-49da-8c62-ab3435368002/lesson/af7d07b5-f663-4cba-83df-055277a144ba" />
</CardGroup>


# Demo Using Linting and Validation

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Working-With-VS-Code-Extension/Demo-Using-Linting-and-Validation/page

Demonstrates using the VS Code Ansible extension and ansible-lint to lint, validate, and fix playbooks for consistency and reliability before execution.

In this lesson we'll demonstrate how to use the VS Code Ansible extension together with ansible-lint to validate syntax, indentation, and common logic issues before running playbooks. Treat this workflow as a final quality gate that improves reliability and maintainability of automation code.

What you'll learn:

* How the VS Code Ansible extension provides real-time diagnostics and autocompletion.
* How ansible-lint enforces best practices (FQCNs, naming, etc.).
* A typical edit → lint → fix → run cycle for a small playbook.

<Frame>
  <img alt="A presentation slide titled &#x22;Agenda.&#x22; It lists four steps for improving Ansible playbooks: use the VS Code Ansible extension and ansible-lint; check syntax, indentation, and logic; run a final quality gate before deployment; and turn a good playbook into a great one." />
</Frame>

Scenario
Imagine joining a DevOps automation team that has accumulated many playbooks written by different engineers. Your objective is to restore consistency, avoid regressions, and make playbooks easier to review. The combination of the [Red Hat Ansible extension for VS Code](https://marketplace.visualstudio.com/items?itemName=redhat.ansible) and [ansible-lint](https://ansible-lint.readthedocs.io/en/stable/) helps enforce those standards with minimal friction.

This demo follows a straightforward workflow:

1. Create a working folder and a sample inventory/playbook.
2. Observe real-time validation in VS Code.
3. Introduce an intentional error to see diagnostic feedback.
4. Run ansible-lint and apply its suggestions.
5. Execute the validated playbook.

<Frame>
  <img alt="A presentation slide titled &#x22;Demo&#x22; showing six numbered steps for creating and validating a sample playbook in VS Code. The steps list creating a working folder and sample playbook, checking real-time validation, introducing a deliberate error to observe feedback, reviewing linting results, fixing detected issues, and executing the validated playbook." />
</Frame>

Getting started — create the project folder and files

```bash theme={null}
student@control:~$ mkdir validation
student@control:~$ cd validation/
student@control:~/validation$ vim inventory
student@control:~/validation$ vim ansible.cfg
```

Example minimal inventory (one host named `servera`):

```ini theme={null}
servera
```

Minimal `ansible.cfg` to use the local inventory and enable privilege escalation:

```ini theme={null}
[defaults]
inventory = inventory

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False
```

Open the `validation` folder in VS Code and create `playbook.yml`.

<Frame>
  <img alt="A dark-themed Visual Studio Code welcome screen with the Explorer sidebar showing project files. A &#x22;New File&#x22; dialog suggesting &#x22;playbook.yml&#x22; is open, with walkthroughs and a &#x22;Build with agent mode&#x22; panel on the right." />
</Frame>

Authoring the initial playbook
The Ansible extension in VS Code will provide autocompletion for hosts (from your inventory), modules, and module parameters. Below is a small playbook with a deliberate mistake in the `debug` task to trigger diagnostics.

```yaml theme={null}
---
- name: validation
  hosts: servera
  tasks:
    - name: install httpd
      dnf:
        name: httpd
        state: latest
    - name: start httpd
      ansible.builtin.service:
        name: httpd
        state: started
    - name: show message
      debug: dsada
      msg: "itsworked"
```

What VS Code/extension reports

* The editor will highlight the incorrect `debug: dsada` usage and show a diagnostic explaining that the module call and parameter structure are invalid.
* Hovering the module name or using Peek Definition shows inline module docs and expected parameters.

Fix the debug task to use the module properly:

```yaml theme={null}
---
- name: validation
  hosts: servera
  tasks:
    - name: install httpd
      dnf:
        name: httpd
        state: latest

    - name: start httpd
      ansible.builtin.service:
        name: httpd
        state: started

    - name: show message
      debug:
        msg: "it worked"
```

Running ansible-lint from the editor
If you configure ansible-lint integration in VS Code (or run it from the terminal), linting will recommend best practices that don’t necessarily stop execution but improve consistency and readability—e.g., using fully qualified collection names (FQCNs) and consistent task naming.

Apply simple lint feedback: use FQCNs and consistent task naming

```yaml theme={null}
---
- name: validation
  hosts: servera
  tasks:
    - name: install_httpd
      ansible.builtin.dnf:
        name: httpd
        state: latest

    - name: start_httpd
      ansible.builtin.service:
        name: httpd
        state: started

    - name: show_message
      ansible.builtin.debug:
        msg: "it worked"
```

Detecting misspelled modules
Introduce an intentional module-name typo to see how the extension reports unknown modules:

```yaml theme={null}
---
- name: validation
  hosts: servera
  tasks:
    - name: install_httpd
      dnff:
        name: httpd
        state: latest

    - name: start_httpd
      ansible.builtin.service:
        name: httpd
        state: started

    - name: show_message
      ansible.builtin.debug:
        msg: "it worked"
```

The extension and ansible-lint will warn that `dnff` is not a known module—this usually indicates a misspelling or a missing collection. Correct it back to `ansible.builtin.dnf`.

Final lint-clean playbook
After applying corrections and following lint suggestions (task names, FQCNs, newline at EOF), your playbook should be clean and readable:

```yaml theme={null}
---
- name: Validation
  hosts: servera
  tasks:
    - name: Install httpd
      ansible.builtin.dnf:
        name: httpd
        state: latest

    - name: Start httpd
      ansible.builtin.service:
        name: httpd
        state: started

    - name: Show message
      ansible.builtin.debug:
        msg: "it worked"
```

Run the playbook from the terminal:

```bash theme={null}
student@control:~/validation$ ansible-playbook /home/student/validation/playbook.yml
```

Example successful output (trimmed):

```console theme={null}
TASK [Show message] ****************************************************************
ok: [servera] => {
    "msg": "it worked"
}

PLAY RECAP ************************************************************************
servera                   : ok=4    changed=2    unreachable=0    failed=0
```

Common ansible-lint suggestions and example fixes

| Lint Recommendation                      | Why it matters                                             | Example fix                                        |
| ---------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------- |
| Use FQCN (ansible.builtin.module)        | Avoids ambiguity when multiple collections provide modules | Change `dnf:` to `ansible.builtin.dnf:`            |
| Consistent task naming                   | Improves readability in logs and reports                   | Use `Install httpd` instead of mixed styles        |
| Avoid unused vars or misleading messages | Prevents confusion and accidental errors                   | Ensure `debug:` uses `msg:` correctly              |
| Ensure YAML structure is correct         | Prevents runtime errors and invalid playbooks              | Use proper indentation and module parameter blocks |

<Callout icon="lightbulb">
  Use the extension to jump to [module documentation](https://docs.ansible.com/ansible/[AWS_SECRET_ACCESS_KEY].html) or use "Peek Definition" in VS Code—this gives immediate access to module options and examples without leaving the editor.
</Callout>

Tips and references

* Click module names in VS Code to open module docs or press Peek Definition for inline summaries.
* Hover over parameters to read short descriptions and expected types.
* If you run ansible-lint locally, ensure it's installed in the environment that VS Code uses (e.g., same Python interpreter or virtualenv).

Further reading

* [VS Code — Ansible extension (Marketplace)](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)
* [ansible-lint documentation](https://ansible-lint.readthedocs.io/en/stable/)
* [Ansible collections & builtin modules](https://docs.ansible.com/ansible/[AWS_SECRET_ACCESS_KEY].html)

This concludes the demo showing how real-time diagnostics in VS Code and ansible-lint together raise playbook quality and reduce deployment risk.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/d87dae2c-1617-49da-8c62-ab3435368002/lesson/d4cd9bc6-27e7-497e-81a4-84dfe7abeb23" />
</CardGroup>
