# chgrp group_name file/directory
$ chgrp wheel family_dog.jpg
```

After running the command, verify the change:

```bash theme={null}
$ ls -l
-rw-r-----  1 aaron wheel 49 Oct 27 14:41 family_dog.jpg
```

<Callout icon="lightbulb">
  You may only change the group to one that your user belongs to. To check your group memberships, run:

  ```bash theme={null}
  $ groups
  aaron wheel family
  ```

  This output shows that you can change the file group to "aaron", "wheel", or "family" if those groups are associated with your account.
</Callout>

## Changing File Owner

To change the owner of a file or directory, use the `chown` command with the following syntax:

```bash theme={null}
$ sudo chown new_owner file/directory
```

For example, to change the file's owner from "aaron" to "jane" (which requires root privileges):

```bash theme={null}
$ sudo chown jane family_dog.jpg
```

The change is reflected with:

```bash theme={null}
$ ls -l
-rw-r----- 1 jane family 49 Oct 27 14:41 family_dog.jpg
```

You can also change both the owner and the group simultaneously by specifying them separated by a colon. For example, to revert the file's ownership back to "aaron" with the group "family":

```bash theme={null}
$ sudo chown aaron:family family_dog.jpg
```

Verifying with:

```bash theme={null}
$ ls -l
-rw-r-----  1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

## Understanding the Permission String

The first character of the output produced by `ls -l` indicates the file type:

* A dash (-) for a regular file
* "d" for a directory
* "l" for a symbolic link

Following this, the next nine characters represent permissions divided into three distinct groups:

* **User (owner) permissions**
* **Group permissions**
* **Others (everyone else)**

For regular files, permissions are represented as:

* "r" for read
* "w" for write
* "x" for execute

In the case of directories:

* "r" allows listing of the directory's contents,
* "w" permits creating or deleting files,
* "x" enables entering the directory (via the `cd` command).

The diagram below visually explains how file and directory permissions work:

<Frame>
  ![The image illustrates file and directory permissions in a Unix-like system, showing "rwxrwxrwx" for owner, group, and others, with a key explaining the meaning of each permission bit.](https://kodekloud.com/kk-media/image/upload/v1752883624/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-List-set-and-change-standard-ugorwx-permissions/unix-file-permissions-diagram.jpg)
</Frame>

Consider the following example where the file "family\_dog.jpg" has permissions set to read-only for the owner, read-write for the group, and no permissions for others:

```bash theme={null}
$ ls -l
-r--rw---- 1 aaron family 49 family_dog.jpg
```

Even though user “aaron” is part of the "family" group (which has write permissions), the system applies the owner's permissions first. Since the owner is limited to read-only, write operations are denied. For instance, attempting to append text as the owner results in:

```bash theme={null}
(aaron)$ echo "Add this content to file" >> family_dog.jpg
bash: family_dog.jpg: Permission denied
```

If another user, such as "jane" (also a member of the "family" group), accesses the file, group permissions are applied:

```bash theme={null}
(aaron)$ su jane
(jane)$ echo "Add this content to file" >> family_dog.jpg
```

After this operation, verifying the file contents shows that Jane was able to write to it:

```bash theme={null}
(jane)$ cat family_dog.jpg
Picture of Milo the dog
```

For users who are neither the owner nor members of the file's group, the "others" permissions will determine the level of access.

## Changing Permissions with chmod

The `chmod` command is used to modify file or directory permissions. Its basic syntax is:

```bash theme={null}
chmod [who][+|-|=][permissions] file/directory
```

Where:

* "who" can be:
  * u for user (owner)
  * g for group
  * o for others
* The operators:
  * * to add permissions
  * * to remove permissions
  * \= to set permissions exactly

### Adding Permissions

For example, if the user "aaron" needs write permission added to his current read-only state, run:

```bash theme={null}
$ chmod u+w family_dog.jpg
```

After execution, the owner’s permissions change from read-only (r--) to read and write (rw-):

```bash theme={null}
$ ls -l
-rw-rw----. 1 aaron family 49 Oct 27 14:41 family_dog.jpg
```

### Removing Permissions

To remove permissions—for instance, to remove the read permission for others:

```bash theme={null}
$ chmod o-r family_dog.jpg
```

Only the owner and group will have read access after this change.

### Setting Exact Permissions

Using the equals operator allows you to define permissions exactly. For example, to set the group’s permissions to read-only (r--):

```bash theme={null}
$ chmod g=r family_dog.jpg
```

To remove all permissions from the group, you can either omit all letters with the equals operator:

```bash theme={null}
$ chmod g= family_dog.jpg
```

Or use the minus operator to remove read, write, and execute permissions:

```bash theme={null}
$ chmod g-rwx family_dog.jpg
```

### Multiple Changes in a Single Command

To specify multiple permission changes, separate them with commas. For example:

```bash theme={null}
$ chmod u+rw,g=r,o= family_dog.jpg
```

Alternatively, if you want to ensure that the user has exactly read and write permissions and remove write permission from the group without altering other group settings:

```bash theme={null}
$ chmod u=rw,g-w family_dog.jpg
```

## Using Octal Values for Permissions

Another method for setting permissions is by using octal values. The `stat` command displays file permissions in both symbolic and octal formats:

```bash theme={null}
$ stat family_dog.jpg
  File: family_dog.jpg
  Size: 49             Blocks: 8          IO Block: 4096   regular file
Device: fd00h/64768d   Inode: 52946177    Links: 1
Access: (0640/-rw-r-----)  Uid: ( 1000/ aaron)   Gid: (  10/ wheel)
```

In this output, the octal value "640" corresponds to:

* 6 (4+2) for the user (read and write)
* 4 for the group (read-only)
* 0 for others (no permissions)

To calculate these values:

* Read (r) = 4
* Write (w) = 2
* Execute (x) = 1

For example:

* rw- equals 4+2 = 6
* r-- equals 4
* \--- equals 0

Other common permission sets include 755 (rwx, r-x, r-x) and 777 (full permissions for everyone).

Once the desired octal value is determined, set the permissions with:

```bash theme={null}
$ chmod 640 family_dog.jpg
```

Now, "family\_dog.jpg" is set to:

* Owner: rw-
* Group: r--
* Others: no permissions

The diagram below illustrates how read, write, and execute permissions translate to their corresponding octal values:

<Frame>
  ![The image explains octal permissions in a Unix-like system, showing how read, write, and execute permissions translate to numerical values. It includes examples of permission strings and their corresponding octal values.](https://kodekloud.com/kk-media/image/upload/v1752883625/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-List-set-and-change-standard-ugorwx-permissions/octal-permissions-unix-explained.jpg)
</Frame>

## Summary

This article covered the fundamentals of listing file details, changing ownership, and modifying file permissions using both symbolic and octal notations. Understanding the Linux permission model is key to maintaining secure file management practices.

Well done, and see you in the next article!

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/4557bfb4-ed24-4bde-b55f-bda4a4979b05" />
</CardGroup>


# Locate read and use system documentation including man info and files in usrsharedoc

Source: https://notes.kodekloud.com/docs/Red-Hat-Certified-System-AdministratorRHCSA/Understand-and-Use-Essential-Tools/Locate-read-and-use-system-documentation-including-man-info-and-files-in-usrsharedoc/page

This guide explores essential Linux documentation sources, including the info system and the /usr/share/doc directory, to enhance understanding of commands and system features.

In this guide, we explore two essential sources of Linux documentation that provide in-depth explanations of commands and system features. Whether you're troubleshooting an issue or preparing for a certification exam, leveraging these resources can significantly enhance your understanding.

## The Info System

The info documentation system is a hypertext-based alternative to traditional man pages. It offers multi-page documentation that allows you to navigate seamlessly through interconnected sections. For example, to view detailed information about the Bash shell, execute:

```bash theme={null}
info bash
```

Here are some key navigation tips for using the info system effectively:

* Press the **Space** bar to scroll down within the current node or move to the next node when you reach the end.
* Press **Backspace** to return to the previous node.
* Use the **Close Bracket (])** key to jump to the next node.

<Frame>
  ![The image shows a terminal window displaying a section of the GNU Bash Reference Manual, specifically describing Bash features and their origins.](https://kodekloud.com/kk-media/image/upload/v1752883626/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Locate-read-and-use-system-documentation-including-man-info-and-files-in-usrsharedoc/bash-reference-manual-features.jpg)
</Frame>

* Press the **Open Bracket (\[)** key to navigate to the previous node.
* Press **n** to move to the next node on the same level.
* Press **p** (as in "papa") to go to the previous node on the same level (if available).
* Press **u** to jump up to the parent node.
* Press **l** (as in "lima") to return to the last visited node.
* Press **q** to exit the info system.

In the info pages, links are marked with asterisks. For a quick navigation, simply hover over a link and press **Enter**. The **Tab** key can help you move the cursor to the nearest link. Keep in mind that while the info system is comprehensive, not every command has an associated info page.

<Frame>
  ![The image shows a terminal window displaying a text-based menu with options for an introduction to Bash and shells. The interface includes typical menu options like File, Edit, and View.](https://kodekloud.com/kk-media/image/upload/v1752883627/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Locate-read-and-use-system-documentation-including-man-info-and-files-in-usrsharedoc/bash-shells-terminal-menu-options.jpg)
</Frame>

<Frame>
  ![The image shows a terminal window displaying text related to Bash definitions, including terms like 'name', 'operator', and 'process group'.](https://kodekloud.com/kk-media/image/upload/v1752883629/notes-assets/images/Red-Hat-Certified-System-AdministratorRHCSA-Locate-read-and-use-system-documentation-including-man-info-and-files-in-usrsharedoc/bash-definitions-terminal-window.jpg)
</Frame>

<Callout icon="lightbulb">
  If you get stuck while browsing, simply use the command `info <command>` to retrieve detailed documentation for the command you're working with.
</Callout>

## Documentation in /usr/share/doc

Another valuable resource is the `/usr/share/doc` directory, which contains documentation for many of the software packages installed on your system. This directory typically holds FAQs, README files, introductory notes, and sometimes HTML-formatted guides.

To begin exploring the documentation, change to the directory:

```bash theme={null}
cd /usr/share/doc
```

You will notice a variety of subdirectories, each corresponding to an installed package. To view these directories, run:

```bash theme={null}
ls | less
```

For instance, to inspect documentation for Bash, navigate to its directory:

```bash theme={null}
cd /usr/share/doc/bash
ls
```

Within the Bash documentation directory, you might find files such as `bash.html`, `bashref.html`, `FAQ`, `INTRO`, `RBASH`, and `README`. To read the introductory documentation, you can use a pager like `less`:

```bash theme={null}
less INTRO
```

Alternatively, you can open the file with an editor such as `vi`:

```bash theme={null}
vi INTRO
```

Or use `grep` to search for specific terms in the document, for example:

```bash theme={null}
grep "comma" INTRO
```

These commands and tools (less, vi, grep) allow you to navigate and search the content efficiently, ensuring you can quickly access the information you need.

When you're finished, clear your terminal screen by running:

```bash theme={null}
clear
```

<Callout icon="lightbulb">
  Both the info system and the `/usr/share/doc` directory are comprehensive resources. By mastering their navigation and search functionalities, you can easily find detailed documentation and enhance your expertise in using Linux commands.
</Callout>

<CardGroup>
  <Card title="Watch Video" icon="video" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/2849c94f-2fc5-4df5-b386-dc7ccaebba6c" />

  <Card title="Practice Lab" icon="installation" href="https://learn.kodekloud.com/user/courses/red-hat-certified-system-administrator-rhcsa/module/c3d8eded-b1dc-479c-a51a-c4f468ba6da3/lesson/9a1f1e9b-2be5-4492-925e-3943d065d7c7" />
</CardGroup>
