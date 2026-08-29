# Search for files

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Search-for-files/page

This article explores how to search for files on a Linux system using the find command and its various options.

In this article, we explore how to search for files on a Linux system using the versatile and powerful find command. Familiarity with your system’s directory structure is essential—for example, SSH configuration files are typically found in /etc/ssh, while system logs reside in /var/log.

![The image shows a directory structure diagram with a root directory ("/") branching into "usr," "var," and "etc," with further subdirectories "share," "log," and "ssh."](https://kodekloud.com/kk-media/image/upload/v1752883638/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Search-for-files/directory-structure-diagram-root.jpg)

Most of the time, you have a good idea of where your files are located. However, certain scenarios require more specific searches:

* **Website Maintenance:** If your website files are stored in /usr/share, and you need to list all image files (e.g., with a .jpg extension), you can run:

  ```bash theme={null}
  $ find /usr/share/ -name '*.jpg'
  # Example output:
  # 1.jpg
  # 2.jpg
  # 3.jpg
  ```

* **Disk Space Management:** When hosting virtual machines, you might encounter low disk space situations. Since most VM files are usually under 20 GB, filtering out unusually large files is critical. For example, to find files larger than 10 megabytes, execute:

  ```bash theme={null}
  $ find /lib64/ -size +10M
  # Example output:
  # large_file.txt
  ```

* **Monitoring File Changes:** After deploying an application, you may want to verify which files have been modified recently. To list files modified within the last minute, use the mmin parameter:

  ```bash theme={null}
  $ find /path/to/directory -mmin -1
  ```

These examples illustrate the find command’s versatility when handling various search requirements.

## Find Command Syntax

The basic syntax for the find command is:

```bash theme={null}
