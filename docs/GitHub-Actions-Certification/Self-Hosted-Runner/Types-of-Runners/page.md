# Types of Runners

Source: https://notes.kodekloud.com/docs/GitHub-Actions-Certification/Self-Hosted-Runner/Types-of-Runners/page

This article explains the types of GitHub runners, including GitHub-hosted and self-hosted options, their features, benefits, and setup instructions.

Runners are the virtual machines or servers that execute the jobs defined in your GitHub Actions workflows. Each time you trigger a workflow, GitHub either provisions a fresh VM (GitHub-hosted) or dispatches the job to one of your own machines (self-hosted). Choosing the right runner depends on your performance requirements, compliance needs, and budget.

***

## GitHub-Hosted Runners

GitHub-hosted runners give you a quick, zero-maintenance experience. They come preconfigured with common tools and support Ubuntu, Windows, and macOS environments.

### Tiers of GitHub-Hosted Runners

1. **Standard Runners**
   * 2-core CPU, \~7 GB RAM, 14 GB SSD
   * Ideal for typical CI/CD tasks with moderate resource needs
2. **Larger Managed Runners** (GitHub Team & Enterprise Cloud only)
   * 4-core CPU, \~16 GB RAM, larger SSD
   * For parallel builds, integration tests, and heavier workloads
3. **GPU-Enabled Runners (Beta)**
   * GPU resources in beta for machine learning, data processing
   * Request access via GitHub Support if on Team or Enterprise Cloud

<Callout icon="lightbulb">
  GitHub-hosted runners are fully patched and maintained by GitHub. You pay per minute of usage, with free tiers for public repositories.
</Callout>

For a quick demonstration, here’s a matrix workflow that runs tests across Linux, macOS, and Windows:

```yaml theme={null}
name: Cross-Platform Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
      - name: Run Tests
        run: npm test
```

<Frame>
  ![The image provides hardware specifications for GitHub-hosted runners, detailing CPU, RAM, and SSD requirements for different virtual machine configurations, including standard and larger runners. It also mentions GPU-enabled runners in beta and differentiates between GitHub Team and Enterprise options.](https://kodekloud.com/kk-media/image/upload/v1752876434/notes-assets/images/GitHub-Actions-Certification-Types-of-Runners/github-runners-hardware-specifications.jpg)
</Frame>

***

## Self-Hosted Runners

Self-hosted runners are machines that you own or provision in your cloud environment. They allow complete customization of OS, hardware specs, installed software, and network configuration.

<Frame>
  ![The image is an infographic titled "Self-Hosted Runner" highlighting five benefits: custom-execution environment, controlled environment for security, eliminates wait time, scalability, and reduced latency. Each benefit is represented by a numbered icon.](https://kodekloud.com/kk-media/image/upload/v1752876435/notes-assets/images/GitHub-Actions-Certification-Types-of-Runners/self-hosted-runner-infographic-benefits.jpg)
</Frame>

### Benefits of Self-Hosted Runners

* **Custom Execution Environment**: Install any dependencies, SDKs, or drivers your build needs.
* **Security & Compliance**: Run within your VPC/firewall and meet corporate policies.
* **No Queue Times**: Dedicated runners eliminate waiting for GitHub-hosted capacity.
* **Autoscaling**: Integrate with Kubernetes or autoscale groups to match workflow demand.
* **Reduced Latency**: Place runners in the same region as your artifact stores or environments.

<Callout icon="triangle-alert">
  You are responsible for updating, securing, and maintaining self-hosted runners. Always apply OS patches and rotate access tokens regularly.
</Callout>

You can register self-hosted runners at the **repository**, **organization**, or **enterprise** level. Below is how to set one up at the repository level.

***

## Setting Up a Self-Hosted Runner

### 1. Add a New Runner in GitHub

In your repository, navigate to **Settings** → **Actions** → **Runners** and click **New self-hosted runner**.

<Frame>
  ![The image shows a GitHub interface for adding a new self-hosted runner, with options to select the runner image (macOS, Linux, Windows) and architecture (x64, ARM, ARM64).](https://kodekloud.com/kk-media/image/upload/v1752876437/notes-assets/images/GitHub-Actions-Certification-Types-of-Runners/github-add-self-hosted-runner-interface.jpg)
</Frame>

Choose your OS and architecture, then follow the on-screen instructions to download the runner application.

### 2. Install and Configure the Runner

Run these commands on your machine:

```bash theme={null}
