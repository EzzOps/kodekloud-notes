# ConfigMaps

Source: https://notes.kodekloud.com/docs/Certified-Kubernetes-Application-Developer-CKAD/Configuration/ConfigMaps/page

This guide explains managing application configuration data in Kubernetes using ConfigMaps to streamline environment-specific data management across multiple Pods.

In this guide, you'll learn how to manage application configuration data in Kubernetes using ConfigMaps. ConfigMaps help decouple configuration artifacts from container images, streamlining the management of environment-specific data across multiple Pod definitions.

## Overview

Traditionally, environment variables were defined directly within Pod definition files. For example, a basic Pod configuration might look like this:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
spec:
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports:
        - containerPort: 80
      env:
        - name: APP_COLOR
          value: blue
        - name: APP_MODE
          value: prod
```

When you need to manage configuration data across many Pods, hardcoding environment variables quickly becomes unwieldy. By extracting these settings into a ConfigMap, you centralize the configuration, making it easier to maintain and update.

> **lightbulb** ConfigMaps store configuration data as key-value pairs. When a Pod is created, this data can be injected either as environment variables or as mounted files, giving your application easy access to the configuration.

There are two main steps when working with ConfigMaps:

1. Creating the ConfigMap.
2. Injecting the ConfigMap into the Pod.

## Creating a ConfigMap

There are two approaches to create ConfigMaps: imperative (command line) and declarative (YAML file).

### Imperative Approach

The imperative method allows you to create a ConfigMap directly from the command line. For instance, to create a ConfigMap named `app-config` with key-value pairs for `APP_COLOR` and `APP_MODE`, run:

```bash theme={null}
kubectl create configmap app-config --from-literal=APP_COLOR=blue --from-literal=APP_MODE=prod
```

If you have configuration data stored in a file (e.g., `app_config.properties`), you can create a ConfigMap from that file:

```bash theme={null}
kubectl create configmap app-config --from-file=app_config.properties
```

### Declarative Approach

For the declarative method, define a ConfigMap in a YAML file and apply it using `kubectl create -f`. Below is an example YAML file (`config-map.yaml`):

```yaml theme={null}
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_COLOR: blue
  APP_MODE: prod
```

Deploy the ConfigMap with the following command:

```bash theme={null}
kubectl create -f config-map.yaml
```

> **lightbulb** When creating multiple ConfigMaps (such as for your application, MySQL, or Redis), use descriptive names. This ensures easier reference within Pod definitions.

## Viewing ConfigMaps

To list all available ConfigMaps, you can run:

```bash theme={null}
kubectl get configmaps
```

The output looks similar to:

```bash theme={null}
NAME         DATA   AGE
app-config   2      3s
```

For a detailed view of a specific ConfigMap, use:

```bash theme={null}
kubectl describe configmaps app-config
```

This command displays comprehensive details, including the stored key-value pairs:

```yaml theme={null}
Name:         app-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
APP_COLOR:
----
blue
APP_MODE:
----
prod
Events: <none>
```

## Injecting a ConfigMap into a Pod

After creating a ConfigMap, you can inject the configuration data into a Pod. A common method is using the `envFrom` property within the Pod’s container specification, as shown below:

```yaml theme={null}
apiVersion: v1
kind: Pod
metadata:
  name: simple-webapp-color
  labels:
    name: simple-webapp-color
spec:
  containers:
    - name: simple-webapp-color
      image: simple-webapp-color
      ports:
        - containerPort: 8080
      envFrom:
        - configMapRef:
            name: app-config
```

In this configuration, all key-value pairs from the `app-config` ConfigMap are injected as environment variables into the container.

## Alternative Methods for Configuration Injection

There are additional ways to inject configuration data into your Pods:

| Method                               | Description                                                             | Example Code Snippet                                                                                                                        |
| ------------------------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Individual Environment Variables** | Reference specific keys from the ConfigMap using `env` and `valueFrom`. | `yaml<br>env:<br>  - name: APP_COLOR<br>    valueFrom:<br>      configMapKeyRef:<br>        name: app-config<br>        key: APP_COLOR<br>` |
| **Mounting as a Volume**             | Mount the ConfigMap as a volume to provide configuration as files.      | `yaml<br>volumes:<br>  - name: app-config-volume<br>    configMap:<br>      name: app-config<br>`                                           |

Choose the method that best fits your application's requirements.

> **lightbulb** Now that you understand how to create and inject ConfigMaps, try experimenting with live Kubernetes clusters to practice configuring, viewing, and troubleshooting environment variables.

This guide provides a structured approach to managing configuration data in Kubernetes, empowering you to build more maintainable and scalable applications. For further reading, please visit the [Kubernetes Documentation](https://kubernetes.io/docs/).

- [Watch Video](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/1ca88380-3de9-4a78-a64f-0e2a5ee5560e)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/certified-kubernetes-application-developer-ckad/module/a2ce8bef-967b-48a9-9f58-253035a96c98/lesson/4bc76d3a-e06a-48b4-85c6-8b5d647fd5f4)
