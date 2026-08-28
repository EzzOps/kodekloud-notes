# Demo Starting the Consul Process Using Dev Mode

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Deploy-a-Single-Datacenter/Demo-Starting-the-Consul-Process-Using-Dev-Mode/page

This article covers starting a Consul server in dev mode and bootstrapping AWS EC2 instances into a Consul cluster.

Welcome to the first lab of this course. In this lesson, we’ll cover two main tasks:

1. Starting a Consul server in **dev mode** on your local machine
2. Bootstrapping two AWS EC2 instances into a Consul cluster

Throughout the course, we’ll reuse these servers so you can follow along and observe how the cluster evolves.

***

## 1. Running Consul in Dev Mode

<Callout icon="lightbulb">
  Running Consul in **dev mode** is intended for local testing only. Data is ephemeral and not suitable for production.
</Callout>

### Start the Dev Agent

Open PowerShell (or your preferred shell) and launch the Consul agent:

```bash theme={null}
consul agent -dev
```

You should see output similar to:

```text theme={null}
2021-02-10T16:03:43.762-0500 [INFO]  agent.leader: started routine: routine="federation state anti-entropy"
2021-02-10T16:03:43.763-0500 [DEBUG] agent.server: successfully established leadership: duration=19.001ms
2021-02-10T16:03:43.817-0500 [INFO]  agent: Synced node info
2021-02-10T16:03:45.177-0500 [DEBUG] agent: Node info in sync
```

### Verify the Local Agent

In a new shell, confirm the agent is running:

```bash theme={null}
consul members
```

You’ll see a single-node entry. Then open your browser to explore the Consul UI:

[http://127.0.0.1:8500](http://127.0.0.1:8500)

<Frame>
  ![The image shows a web interface for Consul, displaying a list of services with one instance labeled "consul." The interface includes options for searching and filtering by health status and service type.](https://kodekloud.com/kk-media/image/upload/v1752877809/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Starting-the-Consul-Process-Using-Dev-Mode/consul-web-interface-services-list.jpg)
</Frame>

To stop the agent, press `Ctrl+C` in the shell where it’s running.

***

## 2. Preparing AWS EC2 Instances

I’ve provisioned two EC2 instances and used Packer to install Consul under `/usr/local/bin`. Let’s verify everything:

```bash theme={null}
