# Backup all KV data
consul snapshot save backup.snap

# Restore KV data from a snapshot
consul snapshot restore backup.snap
```

In Consul Enterprise, the **Consul Snapshot Agent** provides automated, policy-driven backups.

<Callout icon="lightbulb">
  See the [Consul Backup and Restore guide](https://www.consul.io/docs/enterprise/snapshots) for advanced options.
</Callout>

## Designing the KV Structure

Collaborate with your teams to plan a KV hierarchy that meets current requirements and future growth.

<Frame>
  ![The image is a slide titled "Designing the K/V Structure," providing guidelines on designing a key/value structure, emphasizing collaboration, alignment with teams, and consideration of current and future use cases. It features colorful text and a pixelated design on the right side.](https://kodekloud.com/kk-media/image/upload/v1752877780/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Consul-KV-Store/designing-kv-structure-guidelines-slide.jpg)
</Frame>

### Example 1: SDLC-Based Structure

Organize keys by environment:

* k8s/
  * dev/
  * qa/
  * staging/
  * production/

Example keys:

* `k8s/staging/app3/api-key`
* `k8s/staging/app3/certificate`

### Example 2: Team-Based Structure

Group keys by team and service:

<Frame>
  ![The image is a diagram illustrating the design of a key/value (K/V) structure based on teams, with categories like cloud, automation, data, and apps, and subcategories such as chef, aws, TFE, and app1-3. It includes specific parameters like account numbers and API keys.](https://kodekloud.com/kk-media/image/upload/v1752877782/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Introduction-to-Consul-KV-Store/kv-structure-diagram-teams-categories.jpg)
</Frame>

* **cloud/**
  * `cloud/aws/account-number`
  * `cloud/aws/account-name`
* **apps/**
  * `apps/app1/param1`
  * `apps/app2/param2`

Tailor your structure to align with application teams and infrastructure needs.

## Links and References

* [Consul Documentation](https://www.consul.io/docs)
* [Vault Documentation](https://www.vaultproject.io/docs)
* [Kubernetes Basics](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)
* [Terraform Registry](https://registry.terraform.io/)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/31a5f0ad-8329-4870-b4ae-c4fd116e3a31" />
</CardGroup>


# Objective 4 Section Overview

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Access-the-Consul-KeyValue-KV/Objective-4-Section-Overview/page

Exploring the Consul Key/Value Store, its capabilities, interaction methods, HTTP API access, and monitoring changes using various tools.

In this lesson, you’ll explore the Consul Key/Value (K/V) Store—its core capabilities, interaction methods, HTTP API access, and how to monitor changes using Consul Watch, Envconsul, and Consul Template.

<Callout icon="lightbulb">
  Ensure you have a running Consul cluster and basic familiarity with [Consul installation](https://www.consul.io/docs/install).
</Callout>

## Topics Covered

1. Capabilities and limitations of the Consul Key/Value Store

<Frame>
  ![The image outlines objectives for accessing the Consul Key/Value store, including understanding its capabilities, interacting with it via CLI and UI, and monitoring changes. It also indicates a difficulty level of 2.](https://kodekloud.com/kk-media/image/upload/v1752877783/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Objective-4-Section-Overview/consul-key-value-store-objectives.jpg)
</Frame>

2. Interacting with the K/V Store using the Consul CLI and Web UI
3. Accessing the K/V Store via the HTTP API
4. Monitoring key-value changes with Consul Watch and integrating external tools:
   * [Envconsul](https://github.com/hashicorp/envconsul)
   * [Consul Template](https://github.com/hashicorp/consul-template)

Let’s dive in and start querying, storing, and watching key/value pairs within Consul!

## Links and References

* [Consul Key/Value Store Concepts](https://www.consul.io/docs/agent/key-value)
* [Consul HTTP API: KV Endpoints](https://www.consul.io/api-docs/kv)
* [Envconsul GitHub Repository](https://github.com/hashicorp/envconsul)
* [Consul Template GitHub Repository](https://github.com/hashicorp/consul-template)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/70a7eb0f-aec7-41aa-b417-398c341698b6/lesson/0bb7db97-a1fc-4219-b2c6-b84362f46767" />
</CardGroup>
