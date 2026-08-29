# Demo Install Buildpack

Source: https://notes.kodekloud.com/docs/Cloud-Native-Buildpacks/Buildpacks-Basics/Demo-Install-Buildpack/page

Learn to set up the Pack CLI on Ubuntu with similar steps for other Linux distributions.

In this lesson, you'll learn how to set up the Pack CLI on Ubuntu. Although this demonstration uses Ubuntu, the installation steps are quite similar for other Linux distributions and platforms.

> **lightbulb** Before proceeding, ensure that Docker is installed on your system. The Pack CLI relies on Docker. If Docker isn't installed, please follow the appropriate installation instructions for your Ubuntu system.

## Installing Pack CLI on macOS or Systems Using Homebrew

If you're using Homebrew, use the following command to install the Pack CLI:

```bash theme={null}
brew install buildpacks/tap/pack
```

## Installing Pack CLI on Ubuntu

For Ubuntu users, the installation process involves adding the buildpack repository and installing the CLI. Open your terminal and execute these commands one after the other:

```bash theme={null}
sudo add-apt-repository ppa:cncf-buildpacks/pack-cli
sudo apt-get update
sudo apt-get install pack-cli
```

## Verifying the Installation

After installation, verify that the Pack CLI is correctly installed by checking its version. Note that the correct flag is `--version`. Run the command below:

```bash theme={null}
pack --version
