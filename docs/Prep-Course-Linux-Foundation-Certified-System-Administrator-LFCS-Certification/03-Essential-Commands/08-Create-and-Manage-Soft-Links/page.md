# Create and Manage Soft Links

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Essential-Commands/Create-and-Manage-Soft-Links/page

This article explores how to create and manage soft links in Linux, detailing their functionality and usage.

In this article, we explore how Linux handles soft links (also known as symbolic links). Soft links in Linux work similarly to the shortcuts you might find on a Windows desktop. For instance, when you install a program on Windows, a shortcut is added to your desktop that points to the actual executable stored elsewhere (such as "C:\Program Files\MyCoolApp\application.exe"). When you double-click the shortcut, it launches the program even though the executable is not directly stored on your desktop.

```text theme={null}
C:\Program Files\MyCoolApp\application.exe
```

Unlike hard links, which directly reference an inode, soft links are files that contain a path to another file or directory. Essentially, they are text files holding the address where the target file or directory is located.

To create a soft link, you add the `-s` option to the `ln` command. The basic syntax is:

```text theme={null}
