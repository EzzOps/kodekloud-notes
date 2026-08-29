# Demo Visual Studio Code Installation MacOS

Source: https://notes.kodekloud.com/docs/AWS-CloudFormation/Code-Editor-Setup-and-Source-Code/Demo-Visual-Studio-Code-Installation-MacOS/page

Step by step guide to download, install, and configure Visual Studio Code on macOS, enable the code command line launcher, and set useful shortcuts.

This step-by-step guide shows how to download and install Visual Studio Code (VS Code) on macOS. Follow the sequence below to get VS Code running, enable the command-line launcher, and configure a couple of handy shortcuts.

## Before you begin

* Verify your Mac is up to date and meets VS Code system requirements.
* Have an administrator account or the ability to approve app installs.
* Recommended: an internet connection for downloading the installer and extensions.

Download page:

* [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

1. Open the Visual Studio Code download page in your browser and scroll to the macOS section. Choose the installer that matches your Mac architecture (Intel x64 or Apple Silicon / Arm64).

<Frame>
  <img alt="A Visual Studio Code download page screenshot showing three columns for Windows, Linux (Tux penguin) and Mac with large OS icons and blue buttons for different installer types. Each column lists available packages and architectures (x64, Arm64, .deb, .rpm, etc.)." />
</Frame>

2. Click the macOS download button. The download is typically a .dmg or a .zip file and will be saved to your Downloads folder.

3. Open Finder → Downloads and locate the Visual Studio Code download. Double-click the file to open it. If macOS shows a security prompt saying the app was downloaded from the Internet, click Open to continue.

<Frame>
  <img alt="A macOS desktop screenshot showing the Finder Downloads folder with a security pop-up asking if you want to open &#x22;Visual Studio Code&#x22; (downloaded from the Internet) with Cancel and Open buttons. The Dock with app icons is visible along the bottom of the screen." />
</Frame>

4. Install VS Code

* If you downloaded a .dmg: open the mounted image and drag the Visual Studio Code icon into the Applications folder.
* If you downloaded a .zip: double‑click the zip to extract the .app, then move Visual Studio Code.app to Applications.

5. Launch VS Code

* Open Visual Studio Code from the Applications folder or use Spotlight (⌘Space → type “Visual Studio Code”).
* If you want easy access, right‑click the app in the Dock → Options → Keep in Dock.

> **lightbulb** Tip: After moving VS Code to your Applications folder, right-click the app and choose Options → Keep in Dock to pin it for quick access.

## Enable the command-line launcher

To open files or folders from Terminal with the convenient code command:

1. Open the Command Palette: ⇧⌘P (Shift + Command + P)
2. Type and select:

* Shell Command: Install 'code' command in PATH

After installing the shell command, open a folder from Terminal:

```bash theme={null}
