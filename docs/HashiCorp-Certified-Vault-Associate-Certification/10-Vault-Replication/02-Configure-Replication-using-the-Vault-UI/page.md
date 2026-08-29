# On Primary Cluster
$ vault write -f sys/replication/dr/primary/enable
Success! DR replication primary enabled.

$ vault write sys/replication/dr/primary/secondary-token id="us-east2-dr"
Key    Value
---    -----
token  s.XXXXXXXXXXXXXX

# On Secondary Cluster
$ vault write sys/replication/dr/secondary/enable token="s.XXXXXXXXXXXXXX"
Success! DR replication secondary enabled.
```

## Troubleshooting

| Issue                            | Resolution                                     |
| -------------------------------- | ---------------------------------------------- |
| Network connectivity issues      | Open TCP port `8200` between Vault clusters    |
| DNS or endpoint misconfiguration | Verify DNS records or update `VAULT_ADDR`      |
| Vault API not reachable          | Ensure Vault service is running and accessible |

> \[!note]
> After setup, the secondary cluster continuously receives data. In a primary outage, promote the secondary to minimize downtime.

## Links and References

* [Vault DR Replication Documentation](https://www.vaultproject.io/docs/enterprise/replication/dr)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)
* [Vault Networking Guide](https://www.vaultproject.io/docs/concepts/operations/networking)

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/cfd009a3-718e-46c1-b509-a1354fc1e2a6/lesson/3e9172c7-564e-4180-8f4f-55a30b46bd1a)


# Configure Replication using the Vault UI

Source: https://notes.kodekloud.com/docs/HashiCorp-Certified-Vault-Associate-Certification/Vault-Replication/Configure-Replication-using-the-Vault-UI/page

Learn to set up Disaster Recovery replication using HashiCorp Vault’s web interface for robust disaster recovery between primary and secondary clusters.

In this guide, you’ll learn how to set up Disaster Recovery (DR) replication using HashiCorp Vault’s web interface. While you can configure replication via the CLI or API, the UI offers an intuitive workflow for most users. By the end, you’ll have a primary cluster replicating to a secondary for robust disaster recovery.

> **lightbulb** * Vault Enterprise license (1.5+)
  * Admin-level token with `replication` capabilities
  * Two Vault clusters (primary and secondary) with network connectivity

## 1. Enable DR Replication on the Primary Cluster

1. Log in to your **primary** Vault cluster through the UI.
2. In the sidebar, click **Status**, then select **Replication**.
3. Click **Enable Replication**.
4. From the **Type** dropdown, choose **Disaster Recovery (DR) Replication**.
5. Set **Cluster Mode** to **Primary**, then confirm by clicking **Enable Replication**.

![The image is a screenshot of a user interface for configuring replication, specifically selecting Disaster Recovery (DR) replication and setting the cluster mode to primary. It includes instructional text and graphics to guide the user.](https://kodekloud.com/kk-media/image/upload/v1752878260/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configure-Replication-using-the-Vault-UI/dr-replication-cluster-mode-configuration.jpg)

Vault will initialize DR replication in seconds and show the status panel, which initially displays **No known secondaries**.

## 2. Register a Secondary Cluster

1. In the **Replication** panel, click **Add a Secondary**.
2. Provide a descriptive **Name** for your secondary cluster.
3. (Optional) Adjust the **Token TTL** to control how long the secondary activation token remains valid.
4. Click **Generate Token** and **Copy** the output.

![The image shows a user interface for configuring disaster recovery replication in Vault, with a section to name a secondary ID and generate a token. There's also a badge indicating a Vault Certified Operations Professional.](https://kodekloud.com/kk-media/image/upload/v1752878262/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configure-Replication-using-the-Vault-UI/disaster-recovery-replication-vault-ui.jpg)

```text theme={null}
eyJhbGciOiJFUzUxMlsInR5c6IkpXVCJ9.eyJhY2Nlc3Nlc3NfdHlwZSI6ImFkZGl0aW9uIiwic2Vjb25kYXJ5X3Rva2VuIjoiJodHRwOitYrR1hY2J2stcHJgyMDAiLCJleHBpcmF0aW9uIjoxMjM0NTY3ODkwMH19
```

> **triangle-alert** Keep the generated token secure. It grants replication activation rights on the secondary cluster.

## 3. Activate DR Replication on the Secondary Cluster

1. Log in to your **secondary** Vault cluster.
2. Navigate to **Status** → **Replication** → **Enable Replication**.
3. Select **Disaster Recovery (DR) Replication**.
4. Choose **Secondary** for **Cluster Mode**.
5. Paste the token you copied from the primary.
6. Click **Enable Replication** to start synchronization.

![The image is a guide for configuring replication using a user interface, specifically for setting up a secondary cluster for disaster recovery. It includes instructions to select disaster recovery replication, choose secondary mode, and paste a secondary activation token.](https://kodekloud.com/kk-media/image/upload/v1752878263/notes-assets/images/HashiCorp-Certified-Vault-Associate-Certification-Configure-Replication-using-the-Vault-UI/disaster-recovery-replication-guide-ui.jpg)

Vault will now synchronize changes from the primary to the secondary, completing your DR setup.

## DR vs. Performance Replication

| Replication Type        | Use Case                          | Data Direction      |
| ----------------------- | --------------------------------- | ------------------- |
| Disaster Recovery (DR)  | Failover during outages           | Primary → Secondary |
| Performance Replication | Read-scaling and geo-distribution | Bidirectional       |

## Next Steps & References

* [Vault Replication Overview](https://www.vaultproject.io/docs/enterprise/replication)
* [Vault UI Guide](https://www.vaultproject.io/docs/platform/ui)
* [Vault CLI Commands](https://www.vaultproject.io/docs/commands)

Your Vault clusters are now configured for DR replication via the UI. Regularly monitor the **Replication** status page to ensure health and sync progress.

- [Watch Video](https://learn.kodekloud.com/user/courses/hashicorp-certified-vault-associate-certification/module/cfd009a3-718e-46c1-b509-a1354fc1e2a6/lesson/b7f697dc-5dff-473a-a306-9f4641a89ba6)
