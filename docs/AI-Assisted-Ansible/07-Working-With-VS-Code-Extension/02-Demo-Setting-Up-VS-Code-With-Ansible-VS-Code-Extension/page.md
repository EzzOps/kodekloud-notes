# After login, check HTTP locally:
servera$ curl -s http://localhost | sed -n '1,120p'
```

Expected output includes the rendered hostname and the added paragraph:

```html theme={null}
<div class="hostname">servera</div>
<p>Created by ansible and cursor</p>
```

<Callout icon="warning">
  When testing playbooks that install or restart services, be mindful of production impact. Run first in a staging or lab environment. Confirm proper privilege escalation and inventory targeting to avoid unintended changes.
</Callout>

Summary and recommendations

* Cursor can accelerate playbook authoring by suggesting task skeletons, templates, and small refinements. Always review generated content.
* Use handlers and idempotent modules (`template`, `lineinfile`, `systemd`) to produce safe, repeatable runs.
* Validate generated playbooks with Ansible Lint and test in a controlled environment before applying to production hosts.
* Combine Cursor suggestions with human review to maintain correct security posture and operational intent.

Links and references

* [Cursor — download](https://www.cursor.com/download)
* [Ansible Documentation](https://docs.ansible.com/)
* [Ansible Lint](https://ansible-lint.readthedocs.io/en/latest/)
* [Visual Studio Code](https://code.visualstudio.com/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/d87dae2c-1617-49da-8c62-ab3435368002/lesson/91e053b8-65e5-48db-bda1-174c220b8231" />
</CardGroup>


# Demo Setting Up VS Code With Ansible VS Code Extension

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Working-With-VS-Code-Extension/Demo-Setting-Up-VS-Code-With-Ansible-VS-Code-Extension/page

Guide to configuring VS Code with the Red Hat Ansible extension on RHEL 10, adding YAML support and helper tools for linting, autocompletion, and playbook validation.

In this lesson you'll prepare a consistent Ansible development environment so each playbook you open or create in the editor receives instant validation, module suggestions, and linting feedback. We'll configure Visual Studio Code on a clean RHEL 10 system, install the Red Hat Ansible extension (plus YAML support if needed), add optional development helpers (ansible-lint, yamllint, ansible-core), and verify that the extension detects and validates playbooks.

Scenario: your team uses mixed workflows (remote editing, plain editors, local VS Code). The objective is to standardize the developer experience so everyone gets the same in-editor assistance and linting.

<Frame>
  <img alt="A dark-themed infographic titled &#x22;Standardizing the Workflow&#x22; with three laptop illustrations labeled &#x22;Uses simple text editors,&#x22; &#x22;Edits playbooks on remote servers,&#x22; and &#x22;Works locally in VS Code.&#x22; Dashed lines connect each box to a central gear icon labeled &#x22;Standardized Development Workflow.&#x22;" />
</Frame>

## Overview — what we'll do

* Ensure Python tooling (pip3) is present.
* Download and install Visual Studio Code (RPM for RHEL/Fedora).
* Install the Red Hat Ansible extension and YAML language support.
* Install optional Ansible development helpers via pip3 (ansible-core, ansible-lint, yamllint or ansible-devtools).
* Open your project in VS Code and validate extension features with a sample playbook.

| Resource                             |                                       Purpose | Example / Link                                                   |
| ------------------------------------ | --------------------------------------------: | ---------------------------------------------------------------- |
| Visual Studio Code                   |             Editor with extension marketplace | [https://code.visualstudio.com/](https://code.visualstudio.com/) |
| Red Hat Ansible extension            |       Autocomplete, linting, playbook helpers | Marketplace: redhat.ansible                                      |
| Python/pip3                          |                  Install Ansible helper tools | sudo dnf install -y python3-pip                                  |
| ansible-core, ansible-lint, yamllint | Linting and parsing support for the extension | pip3 install --user ansible-core ansible-lint yamllint           |

***

## 1. Prepare the system: confirm pip3 is available

On a minimal RHEL 10 image pip may not be present. Check with:

```bash theme={null}
student@control:~/project$ pip
bash: pip: command not found
```

If pip is missing, install the distribution package:

```bash theme={null}
sudo dnf install -y python3-pip
```

Verify pip3:

```bash theme={null}
pip3 --version
