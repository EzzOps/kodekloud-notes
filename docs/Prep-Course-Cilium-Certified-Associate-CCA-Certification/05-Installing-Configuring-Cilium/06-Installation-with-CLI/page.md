# Installation with CLI

Source: https://notes.kodekloud.com/docs/Prep-Course-Cilium-Certified-Associate-CCA-Certification/Installing-Configuring-Cilium/Installation-with-CLI/page

Guide to installing and configuring Cilium using the cilium CLI, including download, installation, dry-run previews, Helm value configuration, status checks, and best practices.

In this lesson we will go over how to install Cilium using the Cilium CLI.

<Frame>
  <img alt="A presentation title slide with the text &#x22;Installing Cilium With CLI&#x22; on a blue-green gradient background. A small &#x22;© Copyright KodeKloud&#x22; appears in the lower-left corner." />
</Frame>

## Download and install the Cilium CLI

First, download the Cilium CLI binary appropriate for your platform and install it into your PATH. The example below targets Linux; macOS and Windows users can find platform-specific binaries on the Cilium releases page.

Recommended links:

* Cilium CLI releases: [https://github.com/cilium/cilium-cli/releases](https://github.com/cilium/cilium-cli/releases)
* Cilium docs: [https://cilium.io/docs/](https://cilium.io/docs/)

Example (Linux):

```bash theme={null}
