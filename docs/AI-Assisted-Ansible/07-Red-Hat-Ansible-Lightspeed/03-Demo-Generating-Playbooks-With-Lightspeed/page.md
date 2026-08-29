# Demo Generating Playbooks With Lightspeed

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Red-Hat-Ansible-Lightspeed/Demo-Generating-Playbooks-With-Lightspeed/page

Using Red Hat Ansible Lightspeed in VS Code to generate, refine, validate, and run an Ansible playbook that installs and manages Apache with a templated index and restart handler

In this lesson you'll use Red Hat Ansible Lightspeed (within the VS Code Ansible extension) to generate a complete, production-ready Ansible playbook from a natural-language prompt such as "install and start httpd". Lightspeed will propose tasks, modules, parameters, and proper indentation. You will create a workspace, generate and refine a playbook named `site.yml`, add a templated page and a handler, ask Lightspeed to explain the result, and validate and run the playbook.

<Frame>
  <img alt="A slide titled &#x22;Lightspeed Playbook Test&#x22; showing a DevOps team on the left and a flow on the right from the Red Hat Ansible Lightspeed logo to the VS Code logo, with the caption &#x22;Prompts to playbooks.&#x22;" />
</Frame>

Scenario: your team has connected Red Hat Ansible Lightspeed to VS Code and wants to evaluate how effectively Lightspeed converts plain-English prompts into playbooks that follow best practices for RHEL-based targets. The goal: a working playbook that installs and starts Apache (httpd), deploys a simple templated index page, and restarts the service when the template changes.

<Frame>
  <img alt="A dark-themed slide titled &#x22;Demo&#x22; showing a six-step checklist split into two columns. Steps include creating a new workspace, creating a playbook file called site.yml using Lightspeed, reviewing generated code, adding a templating task and handler, explaining the playbook, and validating." />
</Frame>

Quick checklist (what you'll do)

* Create a workspace and inventory
* Create a playbook file `site.yml` using Lightspeed
* Review and refine generated tasks and naming
* Add a templated `index.html` and a handler to restart Apache
* Ask Lightspeed to explain the playbook
* Validate and run the playbook

Step-by-step: create the workspace and basic configuration on your control node.

Create the workspace directory:

```bash theme={null}
student@control:~$ mkdir lightspeed
student@control:~$ cd lightspeed
```

Create a minimal inventory file that defines the `webservers` group:

```ini theme={null}
