# Configure and Explore JCasC

Source: https://notes.kodekloud.com/docs/Advanced-Jenkins/Backup-and-Configuration-Management/Configure-and-Explore-JCasC/page

Guide to Jenkins Configuration as Code plugin, exporting and managing Jenkins configuration via declarative YAML for reproducible, version controlled setups, including installation, locations, validation, and best practices.

Jenkins Configuration as Code (JCasC) lets you express a Jenkins instance and many plugin settings as human-readable YAML. Using JCasC makes Jenkins configuration repeatable, auditable, and suitable for version control — ideal for infrastructure-as-code workflows and CI/CD pipelines.

This guide shows how to install the JCasC plugin, inspect the auto-generated YAML for a running instance, and apply changes from a YAML file stored on the controller or an external source.

## What you'll learn

* Installing the Configuration as Code plugin
* Where JCasC looks for configuration files and environment variables
* Viewing the auto-generated YAML export
* Editing and applying JCasC YAML on the controller
* Best practices, validation, and troubleshooting

## Installation and official docs

Install the plugin from Manage Jenkins → Manage Plugins → Available → *Configuration as Code*.

Official resources:

* Plugin page: [https://plugins.jenkins.io/configuration-as-code/](https://plugins.jenkins.io/configuration-as-code/)
* Examples & repo: [https://github.com/jenkinsci/configuration-as-code-plugin](https://github.com/jenkinsci/configuration-as-code-plugin)

## Common configuration locations and environment variables

| Purpose                                                 | Examples / Notes                                                              |
| ------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Environment variable to point at JCasC config directory | `CASC_JENKINS_CONFIG: /var/jenkins_home/casc_configs`                         |
| JVM option alternative                                  | `JENKINS_JAVA_OPTIONS: "-Dcasc.jenkins.config=/jenkins/casc_configs"`         |
| Typical file locations the plugin can load              | `/var/jenkins_home/casc_config/jenkins.yaml`, `https://acme.org/jenkins.yaml` |
| Supported extensions                                    | `.yml`, `.yaml`, `.YAML`                                                      |
| Default fallback                                        | `$JENKINS_HOME/jenkins.yaml`                                                  |

Example environment snippet (for clarity):

```yaml theme={null}
CASC_JENKINS_CONFIG: /var/jenkins_home/casc_configs
