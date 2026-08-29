# Creating Backstage Instance

Source: https://notes.kodekloud.com/docs/Prep-Course-Certified-Backstage-Associate-CBA-Certification/Backstage-Basics/Creating-Backstage-Instance/page

Guide to install, configure, and run a Backstage instance on a remote server, covering prerequisites, scaffolding, troubleshooting, configuration, and remote access tips

This guide walks through creating a Backstage instance on a remote server. It preserves the original sequence of steps and examples while improving flow, troubleshooting guidance, and configuration notes for running Backstage in a remote environment.

> Note: terminal prompts like
>
> ```
> user1 in 🌐 kodekloud in ~
> ❯
> ```
>
> indicate a shell connected to a remote server (not your local workstation). When running Backstage on a remote server you may need to update host/IP/base URLs so the UI is reachable from your workstation.

<Callout icon="lightbulb">
  Before you begin, ensure you have shell access to the target server and permission to install Node.js, Yarn, and other developer tools. You can scaffold a Backstage app on your server and then expose it to your workstation via SSH tunneling, a reverse proxy, or by binding services to 0.0.0.0 and opening firewall ports.
</Callout>

## Prerequisites

| Requirement | Purpose                                       | Example / Notes                  |
| ----------- | --------------------------------------------- | -------------------------------- |
| Node.js     | Runtime for Backstage (>= 18.12 recommended)  | Use `nvm` to manage versions     |
| Yarn        | Backstage uses Yarn for dependency management | `npm install -g yarn` if missing |
| npx         | Runs the Backstage scaffolder CLI             | Comes with Node/npm              |

## Install Node.js (recommended via nvm)

Using nvm (Node Version Manager) is recommended because it makes switching Node versions simple and avoids system-wide package issues.

Follow the nvm install directions from the project README and run the install script. For reference, the README "Install & Update Script" section looks like this:

<Frame>
  <img alt="A screenshot of a GitHub README page for &#x22;Node Version Manager (nvm)&#x22; showing the project header, badges, and a Table of Contents with a mouse cursor hovering over the &#x22;Install & Update Script&#x22; link. The page layout and repository sidebar are visible in a browser window." />
</Frame>

After installing nvm, install Node 18 (or a later 18.x/20.x release). Example:

```bash theme={null}
