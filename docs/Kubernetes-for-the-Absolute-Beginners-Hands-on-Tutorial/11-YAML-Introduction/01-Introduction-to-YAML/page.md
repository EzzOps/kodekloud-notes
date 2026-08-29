# Introduction to YAML

Source: https://notes.kodekloud.com/docs/Kubernetes-for-the-Absolute-Beginners-Hands-on-Tutorial/YAML-Introduction/Introduction-to-YAML/page

This article provides an introduction to YAML, covering its syntax,

Welcome to this comprehensive lesson on YAML. In this guide, you'll learn about YAML files, how to define configuration data, and why YAML is preferred for its human-readable format. If you're already comfortable with YAML, feel free to skip ahead. Otherwise, it’s highly recommended to follow along because the remainder of this course relies on a solid understanding of YAML. If you’re experienced with XML or JSON, you'll find learning YAML to be a smooth transition.

Below is a simple YAML example that defines a list of servers:

```yaml theme={null}
Servers:
  - name: Server1
    owner: John
    created: 12232012
    status: active
```

YAML is a popular format used to represent configuration data in a clear and readable way. To illustrate its readability and structure, consider the following comparison of XML, JSON, and YAML representations. Taking a moment to observe these differences can help you appreciate YAML's simplicity.

Let’s delve deeper into the YAML syntax.

## Key-Value Pairs and Arrays

At its core, YAML uses key-value pairs. For example, you can define basic items like this:

```yaml theme={null}
