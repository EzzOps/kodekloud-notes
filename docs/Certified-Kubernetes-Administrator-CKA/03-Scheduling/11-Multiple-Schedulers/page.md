# Multiple Schedulers

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Administrator-CKA/Scheduling/Multiple-Schedulers/page

This article explains how to deploy and configure multiple schedulers in a Kubernetes cluster alongside the default scheduler.

Welcome to this lesson on deploying multiple schedulers in a Kubernetes cluster. In this guide, you will learn how to deploy custom schedulers alongside the default scheduler, configure them correctly, and validate their operation.

Kubernetes' default scheduler distributes pods across nodes evenly while considering factors such as taints, tolerations, and node affinity. However, certain use cases may require a custom scheduling algorithm. For instance, when an application needs to perform extra verification before placing its components on specific nodes, a custom scheduler becomes essential. By writing your own scheduler, packaging it, and deploying it alongside the default scheduler, you can tailor pod placement to your specific needs.

> **lightbulb** Ensure that every additional scheduler has a unique name. The default scheduler is conventionally named "default-scheduler," and any custom scheduler must be registered with its own distinct name in the configuration files.

## Configuring Schedulers with YAML

Below are examples of configuration files for both the default and a custom scheduler. Each YAML file uses a profiles list to define the scheduler's name.

```yaml theme={null}
