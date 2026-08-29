# Introduction to Shell

Source: https://notes.kodekloud.com/docs/Learning-Linux-Basics-Course-Labs/Working-with-Shell-I/Introduction-to-Shell/page

This guide provides a solid foundation for navigating directories, managing files, and executing commands using the Linux Bash Shell.

In this lesson, we dive deep into the Linux shell and learn how to navigate directories, manage files, and execute commands using the Bash Shell. Whether you’re new to Linux or looking to sharpen your command-line skills, this guide provides a solid foundation.

![The image outlines a course module titled "Working with the Shell - I," featuring topics on Linux commands and Bash Shell, including labs for practical learning.](https://kodekloud.com/kk-media/image/upload/v1752881156/notes-assets/images/Learning-Linux-Basics-Course-Labs-Introduction-to-Shell/frame_20.jpg)

## Getting Started with the Command Line

The first chapter, "Working with the Shell, Part 1," introduces the command line interface. Although graphical user interfaces (GUIs) can be visually appealing, the command-line shell offers enhanced functionality and flexibility—an essential tool for any Linux system administrator.

![The image shows a PDF labeled "Linux Basics" and a computer screen displaying the Ubuntu desktop graphical view, with text referencing the Linux shell.](https://kodekloud.com/kk-media/image/upload/v1752881157/notes-assets/images/Learning-Linux-Basics-Course-Labs-Introduction-to-Shell/frame_60.jpg)

The Linux shell acts as a mediator between you and the operating system. Commands entered into the shell are executed immediately, and the results are returned in the same window. Upon logging in, you are placed in your home directory, typically located under /home. For example:

* A user named Michael will have a home directory at `/home/Michael`.
* Another user, Alan, will have a home directory at `/home/Alan`.

Your home directory serves as your personal workspace—a dedicated area for storing, retrieving, and managing your files and folders.

![The image illustrates a directory structure for users Allen and Michael, showing their respective home directories and subdirectories with files.](https://kodekloud.com/kk-media/image/upload/v1752881158/notes-assets/images/Learning-Linux-Basics-Course-Labs-Introduction-to-Shell/frame_170.jpg)

In the command line, your home directory is represented by the tilde symbol (`~`). When you see `~` in your prompt, it indicates that you are currently in your home directory.

```bash theme={null}
