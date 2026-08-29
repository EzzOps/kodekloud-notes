# Install apache on webservers within this playbook.
- hosts: webservers
  become: yes
  tasks:
    - name: Install Apache
      apt:
        name: apache2
        state: present
        update_cache: yes

    - name: Ensure Apache is running
      service:
        name: apache2
        state: started
        enabled: yes
```

Refine the target platform

* If your managed hosts are RHEL-family (RHEL, CentOS, Rocky, Fedora), update your prompt to indicate that. Copilot will adapt package/module choices (yum/dnf and systemd). Example RHEL-style suggestion:

```yaml theme={null}
# Install apache on webservers within this playbook. The target is RHEL.
- name: Install and start Apache on webservers
  hosts: webservers
  become: yes

  tasks:
    - name: Install Apache
      yum:
        name: httpd
        state: present

    - name: Start and enable Apache service
      systemd:
        name: httpd
        state: started
        enabled: yes
```

Prefer the service module and FQCNs

* When refining prompts, ask Copilot to:
  * Use ansible.builtin.service for broader compatibility across init systems.
  * Use fully-qualified collection names (FQCN) like ansible.builtin.yum and ansible.builtin.template to avoid ambiguity.
  * Add variables for package name, service name, document root, and template names.
  * Notify a handler to restart the service after template changes.

> **lightbulb** Using FQCNs (for example, ansible.builtin.yum and ansible.builtin.template) is recommended to avoid ambiguity and make your playbooks explicit about which modules they use.

Caveat: always review Copilot output

> **warning** Copilot can produce a helpful scaffold but may generate incorrect assumptions (wrong package names, missing variables, or security issues). Validate generated tasks, run ansible-lint, and test in a safe environment before using in production.

Consolidated final playbook

* After iterating with Copilot and refining prompts (service module, FQCN, handler, vars, enable/start service, append a footer line), a consolidated site.yaml can look like this:

```yaml theme={null}
---
# Install apache on webservers within this playbook. The target is RHEL. Use the service for service management. Deploy a template.
# Use the fqcn of modules. Restart the httpd service on a change using handlers. Add a variable which creates the content within the template.
- name: Install and configure Apache on webservers
  hosts: webservers
  become: yes

  vars:
    apache_package: httpd
    apache_service: httpd
    apache_document_root: /var/www/html
    apache_index_template: index.html.j2
    apache_index_destination: "{{ apache_document_root }}/index.html"
    page_content: "Welcome to the Apache Web Server!"

  tasks:
    - name: Install Apache package
      ansible.builtin.yum:
        name: "{{ apache_package }}"
        state: present

    - name: Deploy index.html from template
      ansible.builtin.template:
        src: "{{ apache_index_template }}"
        dest: "{{ apache_index_destination }}"
      notify: Restart Apache

    - name: Ensure httpd service is enabled and started
      ansible.builtin.service:
        name: "{{ apache_service }}"
        state: started
        enabled: yes

    - name: Add a footer line to index.html
      ansible.builtin.lineinfile:
        path: "{{ apache_index_destination }}"
        line: "Created by ansible and copilot"
        state: present
        insertafter: EOF

  handlers:
    - name: Restart Apache
      ansible.builtin.service:
        name: "{{ apache_service }}"
        state: restarted
```

Create the Jinja2 template

* Save the following as index.html.j2 (project root or role/templates). This minimal Jinja2 template renders the page\_content variable.

```html theme={null}
{# A minimal HTML page showing the content of the variable page_content in jinja2 syntax #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Content</title>
</head>
<body>
    {{ page_content }}
</body>
</html>
```

Linting and editor feedback

* Use the Ansible VS Code extension and ansible-lint for style and correctness suggestions:
  * ansible-lint may flag quote style, variable usage, or package pinning.
  * The extension highlights syntax, YAML indentation, and module FQCN recommendations.
* Treat linter output as guidance; resolve critical issues and decide which stylistic rules match your project.

Running the playbook and verifying the result

* From your control host, run:

```bash theme={null}
student@control:~/copilot$ ansible-playbook -i inventory site.yaml
```

* On the managed host (serverA) verify the web page:

```bash theme={null}
student@servera:~$ curl localhost:80
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Content</title>
</head>
<body>
    Welcome to the Apache Web Server!
</body>
</html>
Created by ansible and copilot
student@servera:~$
```

Summary — best practices when using Copilot with Ansible

* Use short, descriptive comments as prompts (e.g., include target OS and desired behavior).
* Iterate: ask Copilot to change modules (yum vs apt), add variables, enable handlers, and use FQCNs.
* Validate all generated code with ansible-lint and functional testing.
* Keep templates, handlers, and service management explicit and well-documented.
* Let Copilot scaffold repetitive tasks but perform manual review for security and correctness.

Next steps and ideas

* Extend the playbook with SSL configuration, virtual hosts, or more advanced Jinja2 templates.
* Add role separation (tasks, handlers, templates) and ask Copilot to scaffold role structure.
* Integrate CI checks that run ansible-lint and a dry-run to catch regressions early.

Links and references

* [GitHub Copilot in Action (course)](https://learn.kodekloud.com/user/courses/github-copilot-in-action)
* [VS Code](https://code.visualstudio.com/)
* [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
* [Ansible basics (course)](https://learn.kodekloud.com/user/courses/learn-ansible-basics-beginners-course)
* [Jinja2 Basics (Mini Course)](https://learn.kodekloud.com/user/courses/jinja2-basics-mini-course)
* [Ansible Documentation](https://docs.ansible.com/)
* [ansible-lint](https://ansible-lint.readthedocs.io/en/latest/)
* [Ansible VS Code extension](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)

Final prompt/example location:

```bash theme={null}
student@control:~/copilot$
```

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/879a564d-fe0d-47ff-85d8-610adeddf6a2/lesson/a878f3bc-7335-4384-9731-20bdf3a42ff7)


# Course Introduction

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Prerequisites/Course-Introduction/page

A practical course teaching how to combine AI tools with Ansible to rapidly author, validate, and secure playbooks using VS Code, linters, ChatGPT, Copilot, Claude Code and Ansible Lightspeed.

Welcome — and thanks for joining the AI-Assisted Ansible course. This demonstration-driven program shows how top engineering teams combine Ansible automation with AI to build playbooks faster, reduce human error, and troubleshoot infrastructure with greater confidence. I'm Andrei Balint, your instructor.

As infrastructure grows more distributed and complex, traditional automation practices can become slow to author and brittle to maintain. This course teaches practical techniques for integrating AI into your Ansible workflow so you can:

* Generate and iterate playbooks quickly
* Validate code automatically using linters and language servers
* Reduce repetitive authoring with intelligent code suggestions
* Produce secure, production-ready automation aligned with best practices

You’ll revisit Ansible fundamentals (YAML basics, playbook structure, tasks, modules) and then learn how to use modern AI tooling to accelerate development and improve reliability.

<Frame>
  <img alt="A presentation slide titled &#x22;Playbook Components&#x22; listing two items — &#x22;Tasks&#x22; and &#x22;Modules&#x22; — each with an icon. There's also a small circular video inset of a presenter in the bottom-right corner." />
</Frame>

What you'll learn

* How to author clear, maintainable Ansible playbooks (YAML structure, tasks, modules)
* How to use VS Code’s Ansible extension plus ansible-lint and ansible-language-server to catch issues early
* How to prompt and iterate with ChatGPT to generate and refine playbooks
* How to use GitHub Copilot inside VS Code to speed routine tasks and parameter suggestions
* How to run Claude Code from the CLI to produce reproducible, templated playbooks
* How Red Hat Ansible Lightspeed helps generate secure, Ansible-aware automation

Tools covered (quick reference)

| Tool                                   | Use Case                                               |
| -------------------------------------- | ------------------------------------------------------ |
| VS Code Ansible extension              | Linting, autocompletion, validation                    |
| ansible-lint / ansible-language-server | Enforce style and surface problems early               |
| ChatGPT                                | Conversational prompt-driven playbook generation       |
| GitHub Copilot                         | Inline suggestions and context-aware completions       |
| Claude Code CLI                        | Scripted prompt templates and terminal-first workflows |
| Red Hat Ansible Lightspeed             | Enterprise-grade, Ansible-aware AI assistance          |

> **lightbulb** Tip: Combine linters and language servers in your editor to get immediate feedback as you author. This reduces iteration time when using AI-generated output.

Editor integrations: VS Code and linting
You’ll set up the VS Code Ansible extension and learn how editor tooling improves authoring speed and playbook quality. The extension, together with ansible-lint and the ansible-language-server, provides autocompletion, validation, and inline diagnostics so you can detect common issues during development instead of in CI.

<Frame>
  <img alt="A presentation slide titled &#x22;Using Linting and Validation&#x22; showing a DevOps Engineer icon and three steps: &#x22;Use VS Code&#x22;, &#x22;Add Ansible extension&#x22;, and &#x22;Validate with Ansible Lint.&#x22; A small circular video inset of the presenter appears in the lower-right corner." />
</Frame>

AI-assisted authoring: ChatGPT, Copilot, and Claude Code
We compare multiple AI approaches and show when to use each:

* ChatGPT: Best for iterative, conversational playbook generation and debugging. Learn how to craft prompts that produce usable playbooks and how to validate the output against best practices.
* GitHub Copilot: Works inside VS Code to suggest tasks, modules, and parameter values based on surrounding context — ideal for boosting day-to-day productivity.
* Claude Code CLI: Generates playbooks from the terminal using structured prompts, which is useful for reproducible prompt templates and automated pipelines.

You’ll see side-by-side examples of how each tool behaves and the trade-offs between conversational refinement (ChatGPT), inline completion (Copilot), and CLI-driven reproducibility (Claude Code).

<Frame>
  <img alt="A presenter wearing a KodeKloud shirt sits at a desk with a laptop and several clocks on the wall behind him. Beside him is a slide titled &#x22;AI Assisted Ansible Curriculum&#x22; listing topics like Using ChatGPT with Ansible, GitHub Copilot, and VS Code extension." />
</Frame>

Red Hat Ansible Lightspeed
We’ll explain what Ansible Lightspeed is, how to integrate it into your workflow, and why it’s valuable for generating secure, production-ready playbooks aligned with Red Hat best practices. Expect demos showing context-aware suggestions and how Lightspeed applies Ansible-aware intelligence to reduce manual rework.

<Frame>
  <img alt="A presentation slide titled &#x22;Ansible Lightspeed Features&#x22; showing three feature icons around an Ansible logo, with a small circular presenter video thumbnail in the lower-right. The features listed are Context Understanding, Seamless Integration, and Ansible‑Aware Intelligence." />
</Frame>

Who should take this course

* DevOps engineers, SREs, system administrators, and platform teams
* Engineers who maintain large infrastructure, CI/CD pipelines, or multi-cloud deployments
* Anyone looking to add AI-driven authoring and validation to their Ansible workflows

> **warning** Warning: AI-generated automation should always be reviewed and validated. Use linters, testing playbooks in staging environments, and code review practices to ensure safe, idempotent operations.

Community and next steps
At KodeKloud you’ll join an active learning community — ask questions, share your work, and learn with others. By the end of this course you’ll have practical, repeatable skills to integrate AI into your automation lifecycle and accelerate how you build and maintain Ansible playbooks.

```text theme={null}
