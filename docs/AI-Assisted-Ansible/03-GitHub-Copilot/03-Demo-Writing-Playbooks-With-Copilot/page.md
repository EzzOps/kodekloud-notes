# inventory.ini
[rhel_systems]
serverA ansible_host=192.0.2.10 ansible_user=ec2-user
```

Run the playbook with:

```bash theme={null}
ansible-playbook -i inventory.ini playbook.yml
```

Copilot Chat usage

* If you installed the Copilot Chat extension and have access, open the chat pane and ask plain-language questions like:
  * "How do I create a user using Ansible on a server called Server A?"
* Copilot Chat will typically return a sample playbook (similar to the example above), the inventory snippet, and the ansible-playbook command — ready to copy and run.

References and further reading

* GitHub Copilot extension (VS Code Marketplace): [https://marketplace.visualstudio.com/items?itemName=GitHub.copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
* GitHub Copilot Chat (VS Code Marketplace): [https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
* VS Code documentation: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)
* Ansible documentation: [https://docs.ansible.com/](https://docs.ansible.com/)

<Callout icon="lightbulb">
  You must be signed in to GitHub and have network access to GitHub for Copilot to provide suggestions. A Copilot subscription or access entitlement may be required depending on your account.
</Callout>

This completes the demo setup and verification. Once Copilot is signed in and running in VS Code, you should be able to use inline completions and Copilot Chat (if enabled for your account) to speed up writing and iterating on Ansible playbooks.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/879a564d-fe0d-47ff-85d8-610adeddf6a2/lesson/c6fe5d8a-bcb3-448c-aef1-c6e11dd8f232" />
</CardGroup>


# Demo Writing Playbooks With Copilot

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/GitHub-Copilot/Demo-Writing-Playbooks-With-Copilot/page

Demonstrating how to use GitHub Copilot in VS Code to generate, refine, and test Ansible playbooks including templating, handlers, and best practices.

In this lesson we'll use GitHub Copilot inside VS Code to generate a complete Ansible playbook from a short comment such as "install and start Apache". Copilot can infer context (hosts, modules, parameters, indentation) and propose full YAML tasks. We'll walk through accepting, refining, and extending Copilot suggestions, add a minimal Jinja2 template, and demonstrate iterative edits and handlers.

This demo focuses on common, repetitive playbooks (package installation, service management, templating) to see whether Copilot speeds authoring while keeping playbooks accurate, readable, and maintainable.

Prerequisites

* VS Code with the [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) installed and signed in.
* An Ansible project directory with ansible.cfg and an inventory file.
* Ansible installed on your control host.
* Optionally: the [Ansible VS Code extension](https://marketplace.visualstudio.com/items?itemName=redhat.ansible) and [ansible-lint](https://ansible-lint.readthedocs.io/en/latest/) for editor feedback.

<Frame>
  <img alt="A slide titled &#x22;Testing Copilot&#x22; showing a stylized monitor with the VS Code logo and GitHub Copilot icon inside, and a gradient user-with-code icon to the left on a dark background." />
</Frame>

Working directory (example)

```bash theme={null}
student@control:~/copilot$
```

Quick workflow

| Step | Action                                                                      |
| ---- | --------------------------------------------------------------------------- |
| 1    | Create site.yaml                                                            |
| 2    | Type a short comment (e.g., "write a playbook to install and start Apache") |
| 3    | Review and refine Copilot's suggestions                                     |
| 4    | Add a templating file (index.html.j2)                                       |
| 5    | Test contextual prompts and iterative edits; run the playbook               |

<Frame>
  <img alt="A slide titled &#x22;Demo&#x22; showing a six-step workflow for using Copilot with Ansible, including creating a site.yml playbook, asking Copilot to write a playbook to install/start Apache, reviewing generated code, adding a templating file, and testing contextual understanding and iterative editing." />
</Frame>

Initial Copilot guess

* When you prompt Copilot with a generic comment, its first suggestion will often target Debian/Ubuntu systems and use apt. Example suggestion:

```yaml theme={null}
