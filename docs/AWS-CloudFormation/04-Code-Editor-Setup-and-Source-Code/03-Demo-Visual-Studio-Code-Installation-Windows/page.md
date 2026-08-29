# Open the current directory in VS Code
code .
```

Use this to integrate VS Code with terminal workflows, scripts, or other tooling.

## Quick reference: macOS installer types and common actions

| Installer type | What it contains         | Installation steps                                                    |
| -------------- | ------------------------ | --------------------------------------------------------------------- |
| .dmg           | Disk image with the app  | Mount image → drag Visual Studio Code to Applications                 |
| .zip           | Compressed app bundle    | Double-click to extract → move Visual Studio Code.app to Applications |
| x64 / Arm64    | CPU architecture choices | Choose installer matching your Mac (Intel vs Apple Silicon)           |

## Useful editing shortcuts (macOS)

| Action     | Shortcut       |
| ---------- | -------------- |
| Zoom in    | ⌘ + Plus (⌘+)  |
| Zoom out   | ⌘ + Minus (⌘-) |
| Reset zoom | ⌘0             |

## Links and references

* Visual Studio Code download: [https://code.visualstudio.com/download](https://code.visualstudio.com/download)
* VS Code documentation: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)

That’s it — VS Code is now installed and ready to use on your macOS machine. If you run into permission or gatekeeper warnings, approve the app in System Preferences → Security & Privacy, or open it via the Finder Open dialog as described above.

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2e29934e-5554-4599-9f9b-5cdc229e9f2c/lesson/4981f697-ad46-421e-8105-160bc6a5851f" />
</CardGroup>


# Demo Visual Studio Code Installation Windows

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Code-Editor-Setup-and-Source-Code/Demo-Visual-Studio-Code-Installation-Windows/page

Guide to downloading installing and verifying Visual Studio Code on Windows including recommended installer options PATH setup and basic commands

In this short guide you'll download and install Visual Studio Code (VS Code) on a Windows PC. The steps are straightforward and include recommended installer options, a quick verification command, and links for further reading.

Prerequisites

* A Windows PC (Windows 10 or newer is recommended).
* Administrator privileges to run the installer (may be required for system-wide PATH changes).
* An internet connection to download the installer.

1. Open your web browser and search for "Visual Studio Code download" or go directly to the official download page:

* Visual Studio Code download: [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)
* Official documentation: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)

2. On the downloads page, choose the Windows installer to begin the .exe download. If the file does not start automatically, click the provided direct download link.

<Frame>
  <img alt="A screenshot of the Visual Studio Code download page showing big download buttons for Windows, Linux (.deb/.rpm) and Mac with their respective icons and architecture options. The browser window and Windows taskbar are also visible." />
</Frame>

3. Once the .exe file has downloaded, run it to start the Visual Studio Code Setup Wizard. If prompted for administrator permission, allow it to proceed.

4. Follow the installer prompts:
   * Accept the license agreement and click Next.
   * Choose an installation location (the default is usually fine) and click Next.
   * Select the Start Menu folder (or accept the default) and click Next.

5. On the "Select Additional Tasks" page, pick the options that suit your workflow. Common recommendations are described in the table below.

| Installer Option                                    | What it does                                             | Recommendation     |
| --------------------------------------------------- | -------------------------------------------------------- | ------------------ |
| Add "Open with Code" to file context menu           | Right-click a file to open it in VS Code                 | Recommended        |
| Add "Open with Code" to directory context menu      | Right-click a folder to open it in VS Code               | Recommended        |
| Add to PATH                                         | Makes the `code` command available from the command line | Highly recommended |
| Register as default editor for supported file types | Sets VS Code as the default app for files it supports    | Optional           |
| Create a desktop icon                               | Adds a desktop shortcut                                  | Optional           |

<Callout icon="lightbulb">
  Recommended: At minimum, check "Add to PATH" and the Explorer context menu options. These make it much easier to open files, folders, and projects from the command line or File Explorer.
</Callout>

6. Click Next, then Install. The installer will copy files and configure VS Code — this typically completes quickly.

7. When installation finishes, leave "Launch Visual Studio Code" checked if you want to open it immediately, then click Finish.

Quick verification and handy commands

* Open a new Command Prompt or PowerShell window and verify VS Code is available on your PATH and check the version:

```bash theme={null}
code --version
```

* To open the current directory in VS Code from the command line:

```bash theme={null}
code .
```

Troubleshooting and tips

* If `code` is not recognized after installation, restart your terminal or log out and log back into Windows to ensure PATH changes take effect.
* If you prefer a Stable vs. Insiders build, download the appropriate installer from the official Downloads page.

<Callout icon="warning">
  Only download installers from the official Visual Studio Code site ([https://code.visualstudio.com/](https://code.visualstudio.com/)). Avoid installing executables from untrusted sources to reduce security risk.
</Callout>

Next steps

* Explore the Command Palette (Ctrl+Shift+P) and the integrated terminal (Ctrl+\`) to become productive quickly.
* Install recommended extensions for your development stack from the Extensions view (Ctrl+Shift+X).
* Learn more with the official VS Code documentation: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)

Congratulations — Visual Studio Code is now installed and ready to use on your Windows PC!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/aws-cloud-formation/module/2e29934e-5554-4599-9f9b-5cdc229e9f2c/lesson/8b583240-7991-40a4-9f12-074c6408fb96" />
</CardGroup>
