# Demo Installing and Enabling Copilot

Source: https://notes.kodekloud.com/docs/AI-Assisted-Ansible/GitHub-Copilot/Demo-Installing-and-Enabling-Copilot/page

Guide to install and enable GitHub Copilot in VS Code on a RHEL VM to author and test Ansible playbooks including Copilot Chat setup and authorization

In this lesson we'll set up GitHub Copilot inside Visual Studio Code (VS Code) on a RHEL virtual machine so you can use an AI assistant to write Ansible playbooks faster and with fewer mistakes. After completing the steps below you'll have the Copilot extension installed, authorized with your GitHub account, and verified that both inline completions and Copilot Chat are working in your Ansible environment.

This guide assumes:

* You have a RHEL VM with a GUI and network access to GitHub.
* VS Code is installed on the VM (or you can install it before starting).
* You have a GitHub account (Copilot may require a subscription or access entitlement).

<Frame>
  <img alt="The image is a slide titled &#x22;AI-Assisted Workflow&#x22; showing a DevOps team on the left, a stack of Ansible playbooks in the center labeled &#x22;Dozens of Ansible playbooks per week&#x22; with a GitHub Copilot icon beneath. On the right a manager icon has a speech bubble asking, &#x22;Can GitHub Copilot replace manual work?&#x22;" />
</Frame>

Overview — what we'll do

* Confirm VS Code is installed and the VM can reach GitHub.
* Install the GitHub Copilot extension in VS Code (and Copilot Chat if you want conversational assistance).
* Sign in to GitHub from VS Code and authorize the Copilot extension.
* Validate Copilot status and test inline completions and Copilot Chat.
* Create a sample Ansible playbook and run it against a simple inventory to confirm end-to-end flow.

Quick step table

| Step | Action                  | Where / Command                                   |
| ---- | ----------------------- | ------------------------------------------------- |
| 1    | Open VS Code            | GUI on the RHEL VM                                |
| 2    | Open Extensions view    | Ctrl+Shift+X in VS Code                           |
| 3    | Install Copilot         | Search "GitHub Copilot" in Extensions             |
| 4    | Sign in and authorize   | Browser-based GitHub OAuth flow                   |
| 5    | Verify running status   | VS Code status bar shows Copilot signed in        |
| 6    | Create project and test | Create folder, add playbook, run ansible-playbook |

High-level step-by-step

1. Launch VS Code on the VM.
2. Open the Extensions view (Ctrl+Shift+X).
3. Search for "Copilot" and install the official "GitHub Copilot" extension. For conversational chat, also install "GitHub Copilot Chat" and ensure your GitHub account has Chat access.
4. After installing, sign in with your GitHub account and authorize the extension via the browser prompt.
5. Confirm Copilot is running (status appears in the VS Code status bar).
6. Create a project folder, add a playbook file, and test inline suggestions and Copilot Chat.

I'll switch over to my virtual machine and open VS Code to demonstrate the steps.

<Frame>
  <img alt="A presentation slide titled &#x22;Demo&#x22; showing six numbered steps for installing and configuring GitHub Copilot in VS Code. Steps include preparing the environment, ensuring VS Code/GitHub reachability, installing and authorizing the Copilot extension, signing in to GitHub, and checking Copilot status." />
</Frame>

Detailed walkthrough

1. Open VS Code on the RHEL VM.
2. Go to the Extensions view (Ctrl+Shift+X).
3. Search for "GitHub Copilot" and click Install on the official extension. If you want natural-language, conversational assistance, also install "GitHub Copilot Chat" (the chat extension is separate).
4. After installation VS Code will prompt you to sign in. If you see a Copilot sign-in button in the status bar, click it to launch the browser-based GitHub OAuth flow. Approve the requested permissions to authorize the extension.
   * After completing the browser flow, return to VS Code and confirm the status bar shows Copilot as signed in and active.
5. Verify inline completions by editing a file: Copilot will show context-aware suggestions as you type. Accept with Tab (or Enter/right-arrow depending on your editor keybindings).
6. If you installed Copilot Chat and your account has access, open the Copilot Chat pane to ask questions in natural language and get code snippets, explanations, and examples.

<Callout icon="warning">
  Make sure your VM has network access to GitHub and that you are signed in. Copilot requires connectivity to GitHub’s services and a Copilot-enabled account or subscription—without these, suggestions and chat will not work.
</Callout>

Now create a project folder and a playbook to test Copilot.

* Create a folder named Copilot and open it in VS Code.
* Inside that folder create a new file named playbook.yml.

<Frame>
  <img alt="A dark-themed code editor window with a centered file browser dialog showing a large &#x22;Folder is Empty&#x22; message. The dialog sidebar lists folders like Home, Recent, and Starred, and a filename &#x22;playbook.yml&#x22; with a &#x22;Create File&#x22; button is visible." />
</Frame>

Type the playbook header and a task description. Copilot will propose completions inline; accept suggestions with Tab.

Example playbook (suggested by Copilot and suitable for creating a user named test on a RHEL system):

```yaml theme={null}
- name: Setup a user called test on a rhel system
  hosts: rhel_systems
  become: yes
  tasks:
    - name: Ensure user 'test' exists
      user:
        name: test
        state: present
        shell: /bin/bash
        create_home: yes
        uid: 1500
```

Example inventory and command to run the playbook:

```ini theme={null}
