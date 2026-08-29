# Config Map Overview

Source: https://notes.kodekloud.com/docs/OpenShift-4/Openshift-Security/Config-Map-Overview/page

ConfigMaps are a Kubernetes resource for managing configuration data as key-value pairs, enhancing flexibility and separation of configuration from application code.

ConfigMaps are a fundamental resource in Kubernetes and, by extension, OpenShift. They offer a consistent way to manage configuration data across both platforms. If you’re already familiar with Kubernetes ConfigMaps, you’ll find that their structure, creation, and management remain unchanged in OpenShift.

## What Is a ConfigMap?

A ConfigMap is a Kubernetes API resource used to store configuration data as key-value pairs. Each key represents a configuration name, while the value holds its associated data. The primary purpose of a ConfigMap is to inject configuration details into containers, thereby separating configuration from application code.

For instance, when deploying a Pod within a Deployment, you might need to pass in parameters such as a database username or database name. ConfigMaps enable you to provide these details without hardcoding them into your Deployment manifests.

<Frame>
  ![The image illustrates a concept of injecting containers with configuration data using a ConfigMap, featuring icons and a "Deployment" label.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882714/notes-assets/images/OpenShift-4-Config-Map-Overview/configmap-injecting-containers-deployment.jpg)
</Frame>

Using ConfigMaps to pass environment variables or other configuration data at runtime enhances the flexibility of your containerized applications. This method improves code reusability and streamlines updates—if configuration changes, you update the ConfigMap rather than modifying multiple resource manifests.

<Frame>
  ![The image is a diagram illustrating a "ConfigMap" with elements like environment variables, configuration data, and parameters, alongside a gear icon. It includes red dropdown icons and text about adding environment variables and config data.](../../../../images/kodekloud.com/kk-media/image/upload/v1752882716/notes-assets/images/OpenShift-4-Config-Map-Overview/configmap-environment-variables-diagram.jpg)
</Frame>

## Working with ConfigMaps

There are multiple ways to create and manage ConfigMaps in your cluster:

1. **Using YAML Files:**\
   You can define ConfigMaps in YAML files, similar to other Kubernetes manifests including Deployments, Pods, and Services. Once defined, apply the YAML file to your cluster.

2. **Using CLI Commands:**\
   You can quickly create and manage ConfigMaps via command-line tools. For Kubernetes, you'd use `kubectl`, and for OpenShift, the equivalent CLI command is `oc`.

<Callout icon="lightbulb">
  You can inspect and troubleshoot ConfigMaps using commands like `oc describe configmap` and display all ConfigMaps with `oc get configmap`.
</Callout>

Below is an example of common commands for working with ConfigMaps:

```shell theme={null}
oc create configmap <configmap_name>
oc describe configmap <configmap_name>
oc get configmap
```

With an understanding of ConfigMaps and how to manage them, let’s dive into a demo that shows ConfigMaps in action within a real-world scenario.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/openshift-4/module/413252bb-7455-41fa-86eb-e3e9370c8f08/lesson/4c58f7aa-65e7-48c9-a199-83985f75922d" />
</CardGroup>
