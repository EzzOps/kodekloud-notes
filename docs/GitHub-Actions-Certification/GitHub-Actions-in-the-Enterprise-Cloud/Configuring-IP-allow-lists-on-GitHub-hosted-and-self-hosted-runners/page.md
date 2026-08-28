# Example if using a systemd service
systemctl restart actions.runner.your-repo.service
```

***

## Verifying Proxy Usage in Your Workflow

Update your workflow to print proxy variables and make an HTTPS request:

```yaml theme={null}
name: Verify Proxy Usage  
on: workflow_dispatch

jobs:
  verify_proxy:
    runs-on: self-hosted
    steps:
      - name: Show Proxy Environment
        run: |
          echo "HTTPS_PROXY: $HTTPS_PROXY"
          echo "HTTP_PROXY:  $HTTP_PROXY"
          echo "NO_PROXY:    $NO_PROXY"

      - name: External Call via Proxy
        run: curl -v https://httpbin.org/ip
```

<Frame>
  ![The image shows a GitHub Actions interface with a completed workflow run named "demo\_job," which includes steps like setting up the job, making an external call using cURL, and verifying proxy settings.](https://kodekloud.com/kk-media/image/upload/v1752876216/notes-assets/images/GitHub-Actions-Certification-Configure-self-hosted-runners-with-proxies/github-actions-demo-job-workflow-run.jpg)
</Frame>

Once the run completes:

<Frame>
  ![The image shows a GitHub Actions interface with a completed workflow run titled "Exploring Github Enterprise Action Features/Policies." The workflow includes steps like "Set up job," "Hello," "External Call using cURL," "Verify Proxy Settings," and "Complete job," all marked as successful.](https://kodekloud.com/kk-media/image/upload/v1752876217/notes-assets/images/GitHub-Actions-Certification-Configure-self-hosted-runners-with-proxies/github-actions-workflow-completed-steps.jpg)
</Frame>

### Logs: Proxy in Action

```bash theme={null}
* Uses proxy env variable HTTP_PROXY = 'localhost:3128'
* Connected to localhost (127.0.0.1) port 3128 (#0)
> GET https://httpbin.org/ip HTTP/1.1
> Proxy-Authorization: Basic e2VjaGF0ZXpzOnBhc3N3b3JkMQ== 
< HTTP/1.1 200 OK
{"origin": "127.0.0.1, 35.188.139.128"}
```

The runner picks up the proxy variables automatically, authenticates with your proxy (e.g., Squid), and successfully forwards requests.

***

Thank you for following this tutorial on setting up proxies for your self-hosted GitHub Actions runners! For more details, see the [GitHub Actions documentation](https://docs.github.com/actions/hosting-your-own-runners/configuring-the-proxy-for-self-hosted-runners).

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/9b181319-216b-42b5-8069-9d56650f2d53/lesson/a0c1daa6-6a6b-452b-87c3-d03e6b253fd0" />
</CardGroup>


# Configuring IP allow lists on GitHub hosted and self hosted runners

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/GitHub-Actions-in-the-Enterprise-Cloud/Configuring-IP-allow-lists-on-GitHub-hosted-and-self-hosted-runners/page

This guide explains how to secure GitHub resources by restricting access to specific IP addresses through IP allow lists.

In this guide, we’ll show you how to secure your GitHub Organization or Enterprise by restricting access to private resources to specific IP addresses. By default, authorized users can connect from any IP. Enforcing an IP allow list limits access to trusted networks or hosts, reducing your attack surface and ensuring compliance.

<Frame>
  ![The image shows a GitHub documentation page about managing allowed IP addresses for an organization, with navigation links on the left and article sections on the right.](https://kodekloud.com/kk-media/image/upload/v1752876218/notes-assets/images/GitHub-Actions-Certification-Configuring-IP-allow-lists-on-GitHub-hosted-and-self-hosted-runners/github-managing-allowed-ip-addresses-docs.jpg)
</Frame>

This documentation covers:

* Adding and managing allowed IP addresses or CIDR ranges
* Enabling allow lists for GitHub Apps, GitHub Actions, and GitHub Pages
* Verifying whether an IP is permitted before enforcement

## Using IP allow lists with GitHub Actions

To ensure your workflows run only on known IPs, choose runners with static addresses. You have two options:

| Runner Type           | IP Stability        | Use Case                                                             |
| --------------------- | ------------------- | -------------------------------------------------------------------- |
| Self-hosted runners   | Static or dynamic   | You manage the environment and networking                            |
| GitHub-hosted “large” | Static IP available | Enhanced VMs with more RAM, CPU, disk, auto-scaling, and defined IPs |

<Callout icon="lightbulb">
  Workflows on static-IP runners won’t fail due to IP restrictions.\
  Consider [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) or GitHub-hosted “large” runners if you need fixed IPs.
</Callout>

## Configuring IP allow lists at the enterprise level

When you enable an IP allow list at the Enterprise level, it applies to all member organizations. The steps mirror the organization-level process:

1. Navigate to **Enterprise Settings**
2. Select **Authentication security**
3. Under **IP allow list**, click **Add IP** or **Add CIDR range**
4. Use the built-in checker to validate an IP before enforcement
5. Toggle **IP allow list** to **Enabled** and select services (Apps, Actions, Pages)

<Frame>
  ![The image shows a GitHub security settings page for managing IP allow lists, with an option to check if an IP address is permitted. An IP address "1.2.3.4" is entered, and a message indicates it is not permitted by the IP allow list.](https://kodekloud.com/kk-media/image/upload/v1752876219/notes-assets/images/GitHub-Actions-Certification-Configuring-IP-allow-lists-on-GitHub-hosted-and-self-hosted-runners/github-security-ip-allow-list-check.jpg)
</Frame>

Once enforced, only users, apps, and runners originating from your approved IP addresses can access private enterprise resources.

<Frame>
  ![The image shows a GitHub settings page focused on authentication security, including options for SAML single sign-on, SSH certificate authorities, and IP allow lists.](https://kodekloud.com/kk-media/image/upload/v1752876220/notes-assets/images/GitHub-Actions-Certification-Configuring-IP-allow-lists-on-GitHub-hosted-and-self-hosted-runners/github-settings-authentication-security-options.jpg)
</Frame>

### Handling dynamic IP addresses

If your self-hosted runners use dynamic IPs, automate updates to the allow list via a scheduled script or CI job that calls the [GitHub REST API](https://docs.github.com/rest). This prevents runner lockouts when IPs change.

<Callout icon="triangle-alert">
  Failing to refresh dynamic IP addresses can block your self-hosted runners and halt CI/CD pipelines.
</Callout>

## Configuring IP allow lists at the organization level

The organization-level workflow is identical to the enterprise process:

1. Navigate to **Organization Settings**
2. Select **Authentication security**
3. Add and verify IP addresses or CIDR ranges
4. Enable the IP allow list and choose applicable services (Apps, Actions, Pages)

With these settings enforced, only traffic from your specified IPs—including GitHub Actions workflows on static-IP runners—can reach your private repositories and organization resources.

***

## Links and References

* [Using IP allow lists to restrict access](https://docs.github.com/en/organizations/managing-security-settings-for-your-organization/using-ip-allow-lists-to-restrict-access-to-your-organization)
* [About self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
* [GitHub REST API documentation](https://docs.github.com/rest)

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/github-actions-certification/module/9b181319-216b-42b5-8069-9d56650f2d53/lesson/8873d075-e523-403c-933f-5bdf0620af09" />
</CardGroup>
