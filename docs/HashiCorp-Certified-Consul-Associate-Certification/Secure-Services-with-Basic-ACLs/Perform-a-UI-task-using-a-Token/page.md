# Perform a UI task using a Token

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Consul-Associate-Certification/Secure-Services-with-Basic-ACLs/Perform-a-UI-task-using-a-Token/page

This guide explains managing operations in the Consul UI with ACLs enabled, requiring a valid ACL token for changes.

This guide shows how to manage operations in the Consul UI when ACLs are enabled with a default deny-all policy. With ACL enforcement active, read-only views remain accessible, but any change—such as modifying services, nodes, or KV pairs—requires a valid ACL token.

<Callout icon="triangle-alert">
  Ensure you have the correct ACL token (Secret ID) before continuing. Without it, all management actions in the UI will be blocked.
</Callout>

## Prerequisites

* A running Consul cluster or single server with ACL enforcement enabled
* Your ACL bootstrap token or another token with sufficient privileges
* Access to the Consul UI (node IP, load balancer, or `localhost`)

## Authenticating in the UI

1. Open the Consul UI and click the **ACL** tab (highlighted in yellow).
2. Paste your ACL Secret ID into the token field.
3. Click **Save**.

After successful authentication, two sub-tabs appear under **Access Controls**:

| Sub-Tab  | Purpose                                                                                               |
| -------- | ----------------------------------------------------------------------------------------------------- |
| Tokens   | View default tokens (`bootstrap`, `anonymous`) and create new tokens bound to policies.               |
| Policies | Define, edit, or delete ACL policies. Then return to **Tokens** to issue tokens using those policies. |

## Managing Tokens and Policies

<Frame>
  ![The image is a tutorial on performing a UI task using a token, showing steps to enter a valid token in the Access Controls section and manage tokens and policies. It includes labeled screenshots of a user interface with instructions.](https://kodekloud.com/kk-media/image/upload/v1752877962/notes-assets/images/HashiCorp-Certified-Consul-Associate-Certification-Perform-a-UI-task-using-a-Token/ui-task-token-management-tutorial.jpg)
</Frame>

1. **Tokens**
   * Click **Create Token** to issue a new token and bind it to one or more policies.
   * Provide a name and select the policies that define its permissions.

2. **Policies**
   * Click **Create Policy** to open the policy editor.
   * Define rules using [HCL syntax](https://www.consul.io/docs/security/acl/policies#policy-rules).
   * Save the policy, then switch back to **Tokens** to issue tokens using your new policy.

## Next Steps

* Explore the **Services**, **Nodes**, and **KV** tabs to verify your permissions.
* Automate workflows by using your token with the [Consul CLI](https://www.consul.io/docs/commands) or API.

<Callout icon="lightbulb">
  For complete ACL configuration and best practices, see the [Consul ACL documentation](https://www.consul.io/docs/security/acl).
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/hashicorp-certified-consul-associate-certification/module/77c34744-e0fe-450e-82ea-c699ae223d45/lesson/5f7f2a32-f236-4747-8266-0830d94a8a87" />
</CardGroup>
