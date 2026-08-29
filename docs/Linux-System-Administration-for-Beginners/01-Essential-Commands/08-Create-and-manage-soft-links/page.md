# Applies to /home/jane/Pictures/family_dog.jpg as well
```

Ensure users have the appropriate permissions in the target directory before creating a hard link.

***

## Further Reading

* [Linux Inodes and Hard Links](https://www.kernel.org/doc/html/latest/filesystems/index.html)
* [Filesystem Fundamentals](https://www.linuxfoundation.org/)
* [GNU Coreutils: ln Manual](https://www.gnu.org/software/coreutils/manual/html_node/ln-invocation.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-system-administration-for-beginners/module/cc1949d1-8171-4c8c-b69f-86f96cad0bbe/lesson/03bf8733-1baa-419c-808c-6e9f9a9829c6)


# Create and manage soft links

Source: https://notes.kodekloud.com/docs/Linux-System-Administration-for-Beginners/Essential-Commands/Create-and-manage-soft-links/page

Learn how to create and manage soft links in Linux to reference files or directories without duplicating data.

In this lesson, you’ll learn how Linux handles soft links (symbolic links), allowing you to reference files or directories from convenient locations without duplicating data.

## Soft Links Explained

When you install an application on Windows, you often get a desktop shortcut pointing to the actual program in `C:\Program Files\MyCoolApp\application.exe`. Double-clicking the shortcut launches the app even though its files reside elsewhere. A Linux soft link works the same way: it’s a special file containing the path to another file or directory.

![The image shows a diagram illustrating a soft link from a Brave browser icon to a file path "C:\Program Files\MyCoolApp\application.exe" with a browser window open in private mode.](https://kodekloud.com/kk-media/image/upload/v1752881471/notes-assets/images/Linux-System-Administration-for-Beginners-Create-and-manage-soft-links/brave-browser-soft-link-diagram.jpg)

## Creating a Symbolic Link

Use the `ln` command with the `-s` option:

```bash theme={null}
ln -s <path_to_target> <path_to_link>
```

* `<path_to_target>`: the existing file or directory.
* `<path_to_link>`: name of the new symlink.

Example:

```bash theme={null}
ln -s /home/aaron/Pictures/family_dog.jpg family_dog_shortcut.jpg
```

## Verifying a Soft Link

List files in long format to see symlinks marked with an `l` and showing their targets:

```bash theme={null}
ls -l
