# Backup Jenkins

Source: https://notes.kodekloud.com/docs/Jenkins/Systems-Administration-with-Jenkins/Backup-Jenkins/page

This article explores strategies for backing up Jenkins instances, including file system snapshots, backup plugins, and custom shell scripts.

In this article, we explore various strategies for backing up your Jenkins instance. Since Jenkins does not include a dedicated backup solution, it's essential to choose an approach that aligns with your operational requirements—whether it's through file system snapshots, backup plugins, or custom shell scripts.

## Backup Options

One method is to use file system snapshots. Although snapshots can provide daily or incremental protection, they are not true backups and should not be relied upon as a long-term solution.

![The image shows a Jenkins documentation page about creating backups, highlighting filesystem snapshots, backup plugins, and shell scripts for Jenkins instance backup.](https://kodekloud.com/kk-media/image/upload/v1752880139/notes-assets/images/Jenkins-Backup-Jenkins/frame_20.jpg)

Another option is to leverage backup plugins. Git-backed for flexibility, Jenkins supports a wide variety of plugins to extend its functionality. Alternatively, you might consider crafting a shell script to automate your backup process.

> **lightbulb** Both plugin-based and script-based backups offer unique benefits. Choose the approach that best suits your environment and backup objectives.

Below is an excerpt from a custom Jenkins backup shell script available on GitHub:

```bash theme={null}
#!/bin/bash -xe
