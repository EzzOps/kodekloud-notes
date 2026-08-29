# lpic-1
# office-hours-with
# open-source
```

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/48f719ae-cce4-4f68-8711-68cbe8a28ed0/lesson/5f00290b-a66b-4eae-9d12-2a2ef18e526e)


# Prerequisites

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/Prerequisites/Prerequisites/page

Lists knowledge, lab environment, and account prerequisites plus checklist and next steps for running AI-assisted Ansible labs on RHEL 10.

This lesson briefly reviews the prerequisites needed for the course — both the knowledge you should already have and the lab resources you'll need to complete the exercises.

## Knowledge prerequisites

You should be comfortable with the following fundamentals before proceeding:

| Skill                   | Why it matters                                                                                                       | Example / What to practice                                    |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Linux basics            | You'll administer the control and managed nodes (install packages, manage services, work with files and permissions) | Install packages with `dnf`, manage systemd services          |
| YAML syntax             | Ansible playbooks are written in YAML                                                                                | Practice indentation, lists, and mapping structures           |
| Ansible fundamentals    | Helps you focus on AI-assisted workflows rather than relearning concepts                                             | Understand playbooks, plays, tasks, handlers, and inventories |
| Command-line navigation | We'll run and validate playbooks from a terminal                                                                     | Use `ssh`, `scp`, and basic shell commands                    |

<Frame>
  <img alt="A presentation slide titled &#x22;Knowledge Prerequisites&#x22; showing a left panel of required skills with icons: Linux Basics, YAML Syntax, Ansible Fundamentals, and Command-Line Skills. To the right is a note saying &#x22;Navigate and run playbooks in RHEL.&#x22;" />
</Frame>

## Lab environment requirements

For hands-on labs you will need an environment with the following components. This setup mirrors typical enterprise RHEL deployment scenarios and ensures the examples work as shown.

| Resource                  | Purpose                                                            | Recommendation                                      |
| ------------------------- | ------------------------------------------------------------------ | --------------------------------------------------- |
| Control node (RHEL 10)    | Install Ansible and run playbooks from a central location          | RHEL 10 VM or physical host                         |
| Managed node(s) (RHEL 10) | Targets where Ansible applies configurations                       | At least one RHEL 10 VM                             |
| Network connectivity      | Ansible uses SSH to connect to managed nodes                       | Ensure SSH access and routing between nodes         |
| Internet access           | Required for cloud-authenticated AI tools and downloading packages | Required for Copilot, Lightspeed, and package repos |

<Frame>
  <img alt="A presentation slide titled &#x22;Lab Environment Prerequisites&#x22; showing four requirement cards: 01 Control Node (RHEL 10) to install Ansible and run playbooks, 02 Managed Node (RHEL 10) to execute configurations, 03 Network Connection to ensure SSH between systems, and 04 Internet Access required for Copilot and Lightspeed." />
</Frame>

## Account and access requirements

You will need the following accounts and access configured before starting the labs:

| Account / Service                | Purpose                                                                                                                                             |                                                                     |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Red Hat Developer account        | Access RHEL packages and developer resources                                                                                                        |                                                                     |
| GitHub Copilot trial             | AI-assisted code suggestions while authoring playbooks ([GitHub Copilot course](https://learn.kodekloud.com/user/courses/github-copilot-in-action)) |                                                                     |
| Red Hat Ansible Lightspeed trial | AI-enhanced Ansible content and recommendations                                                                                                     |                                                                     |
| Cursor trial account             | Optional: for additional AI coding tools ([Cursor course](https://learn.kodekloud.com/user/courses/cursor-ai))                                      |                                                                     |
| Cloud account (optional)         | Host lab VMs if you are not using local VMs                                                                                                         | Note: cloud service free-tier availability varies; plan accordingly |

> **lightbulb** Configure SSH key-based authentication between the control node and managed node(s) before running playbooks. SSH keys prevent repeated password prompts and are the recommended practice for secure, automated Ansible runs.

## Quick checklist

* [ ] Install RHEL 10 on control node and managed node(s).
* [ ] Ensure network connectivity and SSH reachability.
* [ ] Create and distribute SSH keys for key-based authentication.
* [ ] Sign up for required trials (GitHub Copilot, Red Hat Ansible Lightspeed, Cursor if needed).
* [ ] Confirm internet access from your control node for downloads and AI auth.

## Next steps

With prerequisites satisfied, proceed to:

1. Install Ansible on the control node.
2. Configure SSH key-based access to managed node(s).
3. Run a first, simple playbook to verify connectivity and apply a basic configuration.

## Links and references

* [Ansible Documentation](https://docs.ansible.com/)
* [Red Hat Enterprise Linux Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/)
* [GitHub Copilot information](https://learn.kodekloud.com/user/courses/github-copilot-in-action)
* [Cursor AI course](https://learn.kodekloud.com/user/courses/cursor-ai)
* [Red Hat Ansible Lightspeed](https://www.redhat.com/en/technologies/management/ansible)

This setup ensures you have a stable environment for learning AI-assisted Ansible workflows and follow-up labs.

- [Watch Video](https://learn.kodekloud.com/user/courses/ai-assisted-ansible/module/48f719ae-cce4-4f68-8711-68cbe8a28ed0/lesson/7b2cd967-68af-42e9-9d7f-e1c243ed63ca)
