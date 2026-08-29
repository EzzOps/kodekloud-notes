# SSH timeout
timeout            = 10
forks              = 5

[inventory]
enable_plugins     = host_list, virtualbox, yaml, constructed
```

This configuration sets essential parameters:

* Inventory location
* Log file location
* Module library and roles path
* Behavior controlling fact gathering
* Connection timeout and the number of hosts to target simultaneously when executing playbooks

Under the `[inventory]` section, options are provided to enable specific inventory plugins.

<Callout icon="lightbulb">
  For more detailed configuration options and explanations, refer to the [Ansible Configuration Documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_configuration.html).
</Callout>

***

## Overriding Configuration Settings

The values used in the default configuration file apply whenever you run playbooks from any location on your control machine. For instance, if you have multiple playbooks—each for web, database, or network tasks—you might require tailored settings for each. Examples include:

* **Web playbooks:** Disable fact gathering.
* **Database playbooks:** Enable fact gathering but disable colored output.
* **Network playbooks:** Extend the SSH timeout to 20 seconds.

To handle these scenarios, you can copy the default configuration file into each playbook's directory and modify only the necessary parameters. When running a playbook, Ansible first searches for an `ansible.cfg` in the current directory; if it is found, that file is used. Otherwise, Ansible defaults to `/etc/ansible/ansible.cfg`.

What if you want to use a configuration file stored in an alternative location (e.g., `/opt/ansible-web.cfg`) for multiple playbooks? You can specify the location of this configuration file through the `ANSIBLE_CONFIG` environment variable before running your playbook. For example:

```bash theme={null}
ANSIBLE_CONFIG=/opt/ansible-web.cfg
```

Ansible determines which configuration file to use based on the following order of precedence:

| Priority | Configuration File Source                                        |
| -------- | ---------------------------------------------------------------- |
| 1        | The file specified by the `ANSIBLE_CONFIG` environment variable. |
| 2        | The `ansible.cfg` file in the current directory.                 |
| 3        | The `ansible.cfg` file in the user's home directory.             |
| 4        | The default `ansible.cfg` file in `/etc/ansible/`.               |

*Note:* These files do not have to include every parameter; only the parameters you wish to override need to be specified. Parameters not defined in the highest-priority file will inherit their values from the next available file in the priority chain.

For example, if your storage playbooks should use the default configuration except for modifying the fact-gathering behavior, you don't need to copy the entire file. Instead, you can override just the necessary parameter. If the default configuration has:

```ini theme={null}
/etc/ansible/ansible.cfg
gathering = implicit
```

You can change it to explicit by setting:

```bash theme={null}
ANSIBLE_GATHERING=explicit
```

***

## Setting Environment Variables

Ansible supports determining configuration parameters based on environment variables. Generally, you can convert the parameter name to uppercase and prefix it with `ANSIBLE_`. In this case, `gathering` becomes `ANSIBLE_GATHERING`.

There are various ways to set this environment variable:

* **Inline with the playbook command:**

  ```bash theme={null}
  ANSIBLE_GATHERING=explicit ansible-playbook playbook.yml
  ```

* **Export for the duration of a shell session:**

  ```bash theme={null}
  export ANSIBLE_GATHERING=explicit
  ansible-playbook playbook.yml
  ```

If you require persistent configuration across sessions or for multiple users, it is recommended to create a local copy of the configuration file within your playbook directory, update the necessary parameter, and check this file into your version control system.

<Callout icon="triangle-alert">
  Avoid modifying environment variables without verifying their impact on other playbooks. Always test configuration changes in a controlled environment.
</Callout>

***

## Exploring Configuration Options

To explore the available configuration options and view their corresponding environment variables, you can utilize the following commands:

```bash theme={null}
$ ansible-config list  # Lists all configurations and their default values
$ ansible-config view  # Shows the configuration file currently active
```

If you are unsure which setting is active, the `ansible-config dump` command can help you. It displays a comprehensive list of all settings that Ansible has picked up, along with their source:

```bash theme={null}
$ ansible-config dump  # Shows the current settings
$ export ANSIBLE_GATHERING=explicit
$ ansible-config dump | grep GATHERING
DEFAULT_GATHERING(env: ANSIBLE_GATHERING) = explicit
```

The output above confirms that the `gathering` parameter is set to explicit and shows that it was derived from the environment variable `ANSIBLE_GATHERING`. This feature is particularly useful for troubleshooting configuration issues.

***

That’s it for this lesson. You can now apply your knowledge by practicing with Ansible configuration files and enhancing your skills. The configuration file is well documented and self-explanatory, allowing you to identify and modify the necessary options. We will be testing some of these configuration skills during future challenges. Happy configuring!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/a8141931-256e-4d6a-8534-d83e82ae27c8/lesson/00961e6e-a6a9-4a56-a95c-633457fe398e" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/a8141931-256e-4d6a-8534-d83e82ae27c8/lesson/2228aacd-a348-4ca4-9d74-7cac0ad238ea" />
</CardGroup>


# Core Components Introduction

Source: https://notes.kodekloud.com/docs/Ansible-Advanced-Course/Core-Components/Core-Components-Introduction/page

This article explores the core components of our system, focusing on facts and configuration files.

In this article, we take a deep dive into the core components of our system. In our previous discussions, we covered topics such as inventories, modules, variables, plays, and playbooks. This time, our focus shifts to exploring facts and configuration files.

<Callout icon="lightbulb">
  Before you begin, please be aware that the code examples provided throughout this article are designed to illustrate playbook syntax and structure. Some examples have been simplified for clarity. For the complete versions used in our labs, please refer to the GitHub repository or the lab instructions.
</Callout>

Happy learning!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/ansible-advanced-course/module/a8141931-256e-4d6a-8534-d83e82ae27c8/lesson/910d99ab-9ffd-4f1b-a1b1-4e15f9b37480" />
</CardGroup>
