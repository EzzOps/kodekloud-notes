# Demo Remote Development

Source: https://notes.kodekloud.com/docs/Cursor-AI/Understanding-and-Customizing-Cursor/Demo-Remote-Development/page

Guide to using Cursor Remote SSH for developing on remote machines, setting up SSH hosts, installing the VS Code server, and running code, terminals, and debuggers remotely

This guide shows how to use Cursor (a fork of Visual Studio Code) to develop on a remote machine over SSH. This workflow is ideal when your development machine (laptop, macOS, or Windows) is different from the remote host (for example, a Linux server with a GPU). Using the Remote - SSH flow, Cursor runs the editor UI locally while executing terminals, debuggers, and processes on the remote host.

Cursor supports Windows, macOS, and Linux. The Remote - SSH extension used here is the same extension available for Visual Studio Code, so the workflow will feel familiar if you’ve used VS Code remotely.

Ensure the Remote - SSH extension is available in your Cursor extensions list.

<Frame>
  <img alt="A screenshot of Visual Studio Code showing the Extensions view open to the &#x22;Remote - SSH&#x22; extension page, with details, install/disable buttons, and a preview of using VS Code to connect to a remote server. The left sidebar lists other remote-related extensions and the right pane shows marketplace metadata." />
</Frame>

<Callout icon="lightbulb">
  Aside from Remote - SSH, Cursor also supports Dev Containers and other remote extensions. Choose the remote method that best fits your workflow — e.g., Dev Containers for reproducible dev environments, Remote - SSH for direct access to a specific host.
</Callout>

Example workload to run remotely

* Below is a simple Python example (SVM cross-validation) that demonstrates a CPU/GPU-bound task you might run on a remote machine.

```python theme={null}
