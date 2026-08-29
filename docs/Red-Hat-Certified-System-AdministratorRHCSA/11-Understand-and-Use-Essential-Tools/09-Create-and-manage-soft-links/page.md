# Create and manage soft links

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Create-and-manage-soft-links/page

This article explores the creation and management of soft links in Linux, providing explanations and examples for effective implementation.

In this article, we explore the creation and management of soft links (symbolic links) in Linux. Soft links operate similarly to Windows shortcuts, enabling you to access files and directories located elsewhere on your system. This guide provides detailed explanations and examples to help you understand and implement soft links effectively.

When you install a program on Windows, a shortcut is commonly added to the desktop. This shortcut points to the executable file, even if the actual application files reside in a different directory (for example, C:\Program Files\MyCoolApp\application.exe). In Linux, soft links serve a similar purpose by referencing the target file or directory.

Unlike hard links, which point directly to file inodes, a soft link is a separate file containing the path to another file or directory. To create a soft link, use the ln command with the -s (or --symbolic) option. The general syntax is:

ln -s \[path\_to\_target\_file\_or\_directory] \[path\_to\_link]

## Creating a Soft Link

For instance, to create a symbolic link that points to the file /home/aaron/Pictures/family\_dog.jpg, run:

```bash theme={null}
