# Types of Runners

Source: https://notes.kodekloud.com/docs/GitHub-Actions/Self-Hosted-Runner/Types-of-Runners/page

This article explores different types of GitHub Actions runners for workflows, including GitHub-hosted and self-hosted options.

In this article, we’ll explore the different types of GitHub Actions runners available for your workflows. GitHub Actions runners execute jobs by automatically cloning your repository, installing dependencies, and running your specified commands. You can choose between GitHub-hosted runners or self-hosted runners depending on your needs.

## GitHub-Hosted Runners

GitHub-hosted runners are virtual machines maintained by GitHub. Each time a workflow is triggered, you get a fresh environment with pre-installed tools, reducing setup time and maintenance overhead.

### Supported Environments

* Ubuntu (ubuntu-latest, ubuntu-22.04, ubuntu-20.04)
* Windows (windows-latest, windows-2019)
* macOS (macos-latest, macos-11)

### Example: Matrix Build Workflow

The following workflow runs unit tests across multiple OS environments using [job matrices][job-matrices]:

```yaml theme={null}
name: Cross-Platform Tests
on: [push, pull_request]

jobs:
  unit-tests:
    name: Unit Tests on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Node.js on ${{ matrix.os }}
        uses: actions/setup-node@v3
        with:
          node-version: '16'

      - name: Run Tests
        run: npm test
```

GitHub-hosted runners are available in two performance tiers:

* **Standard runners**: Suitable for most CI/CD tasks with moderate CPU, memory, and SSD.
* **Larger runners**: (GitHub Teams and Enterprise Cloud) Offer more CPU cores, RAM, and disk space.

> **lightbulb** GPU-enabled GitHub-hosted runners are currently in beta. [Apply for the beta program][gpu-beta] if you require GPU resources.

![The image provides hardware specifications for GitHub-hosted runners, detailing CPU, RAM, and SSD configurations for standard and larger virtual machines, along with supported operating systems. It also mentions GitHub Team, GPU-enabled runners in beta, and GitHub Enterprise.](https://kodekloud.com/kk-media/image/upload/v1752876778/notes-assets/images/GitHub-Actions-Types-of-Runners/github-runners-hardware-specifications.jpg)

## Self-Hosted Runners

Self-hosted runners run on machines that you provision and manage. They provide full control over hardware, operating system, and installed software—ideal for custom requirements or compliance needs.

### Key Benefits

* Custom OS and software configurations
* Compliance with strict security policies
* Dedicated compute resources (no shared queue delays)
* Horizontal scaling and autoscaling
* Geographic placement for low-latency or data residency

Self-hosted runners can be registered at the repository, organization, or enterprise level. To add a runner at the repository level:

1. Navigate to **Settings → Actions → Runners**.
2. Click **Add runner**, then select your operating system and architecture.

![The image shows a GitHub interface for adding a new self-hosted runner, with options to select the operating system and architecture.](https://kodekloud.com/kk-media/image/upload/v1752876779/notes-assets/images/GitHub-Actions-Types-of-Runners/github-add-self-hosted-runner-interface.jpg)

### Installation and Configuration

Follow these steps to install and configure a self-hosted runner:

```bash theme={null}
