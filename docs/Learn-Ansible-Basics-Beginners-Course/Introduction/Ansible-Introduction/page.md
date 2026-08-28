# Ansible Introduction

Source: https://notes.kodekloud.com/docs/Learn-Ansible-Basics-Beginners-Course/Introduction/Ansible-Introduction/page

This article introduces Ansible, a tool for IT automation that simplifies tasks through easy-to-learn playbooks, replacing complex scripts.

In this article, we introduce Ansible—a tool that revolutionizes IT automation by reducing repetitive manual tasks. Whether you're a systems engineer, IT administrator, or any IT specialist, you likely encounter tasks like provisioning new hosts, configuring systems, patching dozens of servers, performing migrations, deploying applications, or executing security and compliance audits. Traditionally, these operations required complex custom scripts, significant coding expertise, and time-consuming maintenance.

Ansible streamlines IT automation with an easy-to-learn framework that replaces lengthy scripts with concise playbooks. Below, we compare traditional shell scripting with simple Ansible playbooks to illustrate how you can automate tasks effortlessly.

***

## Example 1: Adding a User

### Traditional Shell Script

Consider this shell script that adds a user to a Linux system:

```bash theme={null}
#!/bin/bash
