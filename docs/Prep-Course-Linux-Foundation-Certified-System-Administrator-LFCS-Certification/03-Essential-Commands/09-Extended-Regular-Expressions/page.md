# ln -s path_to_target_file path_to_link_file
```

* "path\_to\_target\_file" is the location of the file or directory that the soft link will reference.
* "path\_to\_link\_file" is the name (and optionally, the location) of the new soft link.

For example, to create a symbolic link for a family dog picture, use the following commands:

```bash theme={null}
$ ln -s /home/aaron/Pictures/family_dog.jpg family_dog_shortcut.jpg
$ ls -l
lrwxrwxrwx. 1 aaron aaron family_dog_shortcut.jpg -> /home/aaron/Pictures/family_dog.jpg
```

In the output of `ls -l`, the leading "l" indicates that the file is a soft link. It also displays the path that the soft link points to. If the target path is lengthy, `ls -l` might not show the entire path. In these cases, you can use the `readlink` command to view the complete link destination:

```bash theme={null}
$ readlink family_dog_shortcut.jpg
/home/aaron/Pictures/family_dog.jpg
```

> **lightbulb** Although the soft link appears to have full permission bits (rwx), these permissions are not actually enforced. Instead, the permissions of the destination file or directory determine access rights.

For example, if you attempt to redirect output to a soft link that points to a protected file (such as `/etc/fstab`), the operation will be denied:

```bash theme={null}
$ ln -s /home/aaron/Pictures/family_dog.jpg family_dog_shortcut.jpg
$ ls -l
lrwxrwxrwx. 1 aaron aaron family_dog_shortcut.jpg -> /home/aaron/Pictures/family_dog.jpg
$ readlink family_dog_shortcut.jpg
/home/aaron/Pictures/family_dog.jpg
$ echo "Test" >> fstab_shortcut
bash: fstab_shortcut: Permission denied
```

Using an absolute path in a soft link (e.g., `/home/aaron/Pictures/family_dog.jpg`) means that if the directory name (like "aaron") changes in the future, the link will break. A broken link is typically displayed in red when you use `ls -l`.

To prevent this issue, consider creating a soft link with a relative path if you are working within the same directory structure. This method ensures that when the soft link is accessed, it correctly redirects to the intended file relative to the current directory.

Soft links can also be created for directories or for files and directories located on different file systems.

![The image is a diagram explaining soft links, showing how they can link to files and folders, including across different filesystems. It includes visual representations of files and folders with arrows indicating the links.](https://kodekloud.com/kk-media/image/upload/v1752881236/notes-assets/images/Linux-Foundation-Certified-System-Administrator-LFCS-Create-and-Manage-Soft-Links/soft-links-diagram-files-folders.jpg)

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/115b1db7-7970-4cc8-91d4-0ac4892fed9f/lesson/a4c5ddb8-e9dc-41f4-865c-51f49e995f33)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/115b1db7-7970-4cc8-91d4-0ac4892fed9f/lesson/495e559c-1315-45d4-9f65-48c4cdf39d15)


# Extended Regular Expressions

Source: https://notes.kodekloud.com/docs/Prep-Course-Linux-Foundation-Certified-System-Administrator-LFCS-Certification/Essential-Commands/Extended-Regular-Expressions/page

This article explains how to use extended regular expressions with grep to simplify pattern matching and avoid escaping special characters.

Extended regular expressions (ERE) simplify pattern matching by reducing the need for escaping special characters. When using ERE with grep (via the -E option or its alias, egrep), most special characters are interpreted as regex operators by default. You only need to escape them when you want them treated as literal characters.

> **lightbulb** Use ERE with grep by using the uppercase -E flag or the egrep command to simplify your regular expressions and avoid common pitfalls with escaping characters.

## Basic Usage with grep

Consider a command that searches for one or more occurrences of the digit zero in files under the `/etc/` directory:

```bash theme={null}
$ grep -Er '0+' /etc/
```

This command uses the `+` operator to match one or more zeros. Equivalently, you could use:

```bash theme={null}
$ egrep -r '0+' /etc/
```

In both cases, the command highlights lines in various `/etc/` files where the pattern is found.

## Matching Specific Repetitions

To find strings containing at least three consecutive zeros, you can use the curly bracket syntax:

```bash theme={null}
$ egrep -r '0{3,}' /etc/
```

Here, `{3,}` specifies a minimum repetition of three, with no upper limit.

If you want to search for a string beginning with `1` followed by up to three zeros, the pattern is:

```bash theme={null}
$ egrep -r '10{,3}' /etc/
```

This regex also matches the case where no zero follows the digit `1`. To match exactly three zeros, omit the comma and second number:

```bash theme={null}
$ egrep -r '0{3}' /etc/
```

## Optional Characters with the Question Mark

The question mark operator (`?`) makes the preceding element optional (i.e., it can appear once or not at all). For example, to find lines containing either "disable" or "disabled," you might use:

```bash theme={null}
$ egrep -r 'disable?d?' /etc/
```

Be cautious—this expression may also match portions of longer words (like "disables"). To match whole words exactly, consider using the `-w` option with grep or an alternation operator:

```bash theme={null}
$ egrep -r 'enabled|disabled' /etc/
```

For broader matching that handles case variations, add the `-i` option for a case-insensitive search.

## Ranges and Sets

Ranges allow you to specify a set of characters between two endpoints. For example:

* `[a-z]` matches any lowercase letter.
* `[0-9]` matches any digit.

Sets allow matching one character from a list. To search for either "cat" or "cut":

```bash theme={null}
$ egrep -r 'c[au]t' /etc/
```

This pattern checks for the letters `a` or `u` in the middle of "c?t," effectively matching both "cat" and "cut."

## Combining Regex Patterns: Matching Device Files

When matching configuration entries for device files (e.g., `/dev/sda1` or `/dev/twa0`), the naive use of `.*` might be too broad:

```bash theme={null}
$ egrep -r '/dev/.*' /etc/
```

Instead, you can be more specific by matching a forward slash followed by any number of lowercase letters:

```bash theme={null}
$ egrep -r '/dev/[a-z]*' /etc/
```

To include trailing digits, adjust the pattern:

```bash theme={null}
$ egrep -r '/dev/[a-z]*[0-9]' /etc/
```

This matches only device names ending in a digit. To accommodate both cases (with or without a trailing digit):

```bash theme={null}
$ egrep -r '/dev/[a-z]*[0-9]?' /etc/
```

For multi-segment device names (like `/dev/tty0p0`), group the pattern for letters and an optional digit, then allow repetition:

```bash theme={null}
$ egrep -r '/dev/([a-z]*[0-9]?)+'
```

If uppercase letters are also possible in device names, extend the character class:

```bash theme={null}
$ egrep -r '/dev/(([a-zA-Z])*[0-9]?)+' /etc/
```

This pattern effectively matches various formats, including `/dev/ttyS0`.

## Using the Negation Operator

Inside square brackets, the caret (^) negates a set. For example, to search for the string "https" that is not immediately followed by a colon:

```bash theme={null}
$ egrep -r 'https[^:]' /etc/
```

Similarly, you can refine your pattern to match "http" not followed by certain characters by excluding them in the character set.

For example, to find lines where a forward slash is immediately followed by a character that is not a lowercase letter:

```bash theme={null}
$ egrep -r '/[^a-z]' /etc/
```

This command will return lines where the character following `/` does not fall within the lowercase alphabet.

## Practical Considerations and Further Resources

Regular expressions provide a powerful, precise method for text searching and manipulation. By mastering regex operators, ranges, sets, and grouping, you can craft expressions tailored to your needs.

> **lightbulb** Explore online tools such as [regexr.com](https://regexr.com) to experiment with and validate your regular expressions. Additionally, refer to the [grep documentation](https://www.gnu.org/software/grep/manual/grep.html) for more detailed information.

Happy grepping!

- [Watch Video](https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/115b1db7-7970-4cc8-91d4-0ac4892fed9f/lesson/45ca77f0-79a8-430e-97bd-9558d6f2d640)

  - [Practice Lab](https://learn.kodekloud.com/user/courses/linux-foundation-certified-system-administrator-lfcs/module/115b1db7-7970-4cc8-91d4-0ac4892fed9f/lesson/2f83b86d-f3a9-405f-baf1-7ee6d12b1267)
