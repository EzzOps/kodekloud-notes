# Demo Using Consul Template to monitor Changes to Consul KV

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Access-the-Consul-KeyValue-KV/Demo-Using-Consul-Template-to-monitor-Changes-to-Consul-KV/page

Step-by-step guide to pull dynamic configuration from Consul K/V store using Consul Template.

***

title: "Using Consul Template to Monitor Changes in Consul K/V"
description: "Step-by-step guide to pull dynamic configuration from Consul K/V store using Consul Template."
------------------------------------------------------------------------------------------------------------

In this tutorial, you'll learn how to leverage Consul Template to dynamically fetch configuration values from a Consul K/V store and generate application configuration files automatically. This approach ensures your application configs stay in sync with the latest Consul K/V entries.

## 1. Populate Consul K/V Store

First, add the required key-value pairs for our eCommerce application. You can verify these entries in Consul UI or via CLI.

| Key                           | Value        | Description                       |
| ----------------------------- | ------------ | --------------------------------- |
| apps/eCommerce/version        | 4.5          | Current application version       |
| apps/eCommerce/environment    | production   | Deployment environment            |
| apps/eCommerce/database\_host | customer\_db | Hostname of the customer database |
| apps/eCommerce/database       | billing      | Database name for billing service |

Run the following commands:

```bash theme={null}
consul kv put apps/eCommerce/version 4.5
consul kv put apps/eCommerce/environment production
consul kv put apps/eCommerce/database_host customer_db
consul kv put apps/eCommerce/database billing
```

## 2. Download and Install Consul Template

Head over to the [Consul Template releases](https://releases.hashicorp.com/consul-template/) page and copy the link for your platform.

<Frame>
  ![The image shows a terminal window and a browser displaying a list of downloadable files for different operating systems from the HashiCorp Consul Template release page.](https://kodekloud.com/kk-media/image/upload/v1752877774/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Using-Consul-Template-to-monitor-Changes-to-Consul-KV/hashicorp-consul-template-downloads-terminal-browser.jpg)
</Frame>

<Callout icon="lightbulb">
  Make sure to choose the correct architecture (e.g., linux\_amd64) from the release page.
</Callout>

Install and verify:

```bash theme={null}
curl -sLo /tmp/consul-template.zip \
  https://releases.hashicorp.com/consul-template/0.25.1/consul-template_0.25.1_linux_amd64.zip

unzip /tmp/consul-template.zip -d /tmp
sudo mv /tmp/consul-template /usr/local/bin/

consul-template -v
