# Demo Adding and Removing Consul Agents

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Deploy-a-Single-Datacenter/Demo-Adding-and-Removing-Consul-Agents/page

This tutorial covers viewing a Consul cluster, adding a client agent, and removing an agent to maintain a healthy service mesh.

<Frame>
  ![The image is mostly black with a small, dark purple rectangle in the bottom right corner.](../../../../images/kodekloud.com/kk-media/image/upload/v1752877806/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Demo-Adding-and-Removing-Consul-Agents/black-background-purple-rectangle-image.jpg)
</Frame>

In this tutorial, you'll learn how to view your current Consul cluster, add a new client agent, and remove an agent—either gracefully or forcefully. This ensures your service mesh remains healthy and up to date.

## Viewing the Current Cluster

On your server node (`consul-node-a`), verify the existing members and Raft peers:

```bash theme={null}
