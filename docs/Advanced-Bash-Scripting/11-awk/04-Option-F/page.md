# Output:
abc
jkl
stu

awk '{ print $2 }' abc.txt
# Output:
def
mno
vwx

awk '{ print $3 }' abc.txt
# Output:
ghi
pqr
yz
```

***

## 2. NR: Number of Records

`NR` tracks the current record (line) number. This is useful for adding line numbers or filtering specific lines:

```bash theme={null}
awk '{ print NR, $1, $4 }' size.txt
```

Produces:

```text theme={null}
1 Filesystem Avail
2 udev       1.8G
3 tmpfs      356M
4 /dev/sda1  9.3G
...
```

To print only the 8th line’s available space:

```bash theme={null}
awk 'NR == 8 { print $4 }' size.txt
# Output:
360G
```

***

## 3. NF: Number of Fields

`NF` contains how many fields are in the current record. It helps you spot inconsistencies in your data:

```bash theme={null}
awk '{ print NF }' size.txt
```

```text theme={null}
7
6
6
6
6
6
6
6
6
```

> **lightbulb** The header line has 7 fields because “Mounted on” is split into two separate fields.

***

## 4. Combining NR and NF

Print both the record number and its field count:

```bash theme={null}
awk '{ print NR, NF }' size.txt
```

```text theme={null}
1 7
2 6
3 6
4 6
...
```

Concatenate text with values:

```bash theme={null}
awk '{ print "Line", NR, "has", NF, "fields" }' size.txt
```

```text theme={null}
Line 1 has 7 fields
Line 2 has 6 fields
...
```

***

## 5. \$NF: The Last Field

Use `$NF` to refer directly to the last field of each record:

```bash theme={null}
awk '{ print $NF }' size.txt
```

```text theme={null}
on
/dev
/run
/
...
```

***

## 6. FILENAME: Current Filename

`FILENAME` holds the name of the file being processed (empty when reading from stdin):

```bash theme={null}
awk '{ print FILENAME, $1 }' size.txt
```

```text theme={null}
size.txt Filesystem
size.txt udev
size.txt tmpfs
...
```

When you pipe data into **awk**, `FILENAME` is empty:

```bash theme={null}
df -h | awk '{ print FILENAME, $1 }'
# Output:
 Filesystem
 udev
 tmpfs
 ...
```

***

## 7. Summary Table of Built-in Variables

| Variable   | Description                                 | Example                             |
| ---------- | ------------------------------------------- | ----------------------------------- |
| `$1`, `$2` | Positional fields (first, second, etc.)     | `awk '{ print $2 }' file.txt`       |
| `NR`       | Current record (line) number                | `awk '{ print NR }' file.txt`       |
| `NF`       | Number of fields in the current record      | `awk '{ print NF }' file.txt`       |
| `$NF`      | The last field in the current record        | `awk '{ print $NF }' file.txt`      |
| `FILENAME` | Name of the file being processed (or empty) | `awk '{ print FILENAME }' file.txt` |

***

## 8. Custom Field Separators

If your data uses a delimiter other than whitespace, set the `-F` option:

```bash theme={null}
awk -F, '{ print $1, $NF }' data.csv
```

> **triangle-alert** Always quote the `-F` argument when it contains special characters, e.g., `awk -F'|' '...' file.txt`.

***

## Links and References

* [GNU awk Manual](https://www.gnu.org/software/gawk/manual/)
* [awk User’s Guide](https://www.cs.princeton.edu/~bwk/btl.mirror/)
* [Korn Shell: awk Built-in Variables](https://docstore.mik.ua/orelly/unix3/awk/ch02_01.htm)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0cddb337-89d3-4068-a878-37a0a342c22f/lesson/814d3d28-834a-4ccb-bbe3-8cde6a0721d2)


# Option F

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/awk/Option-F/page

Learn to use the -F option in awk to customize field separators for processing structured text.

Learn how to use the **-F** option in `awk` to customize the field separator when processing structured text. By default, `awk` splits records on whitespace, but **-F** lets you define any character or regular expression as the delimiter.

```bash theme={null}
usage: awk [-F fs] [-v var=value] [-f progfile | 'prog'] [file ...]
```

## 1. Default Field Splitting

By default, `awk` treats any whitespace as the field separator:

```bash theme={null}
$ df -h
```

```text theme={null}
Filesystem      Size  Used Avail Use% Mounted on
udev            1.8G     0  1.8G   0% /dev
tmpfs           366M  9.7M  356M   3% /run
...
```

When your data uses a different delimiter—such as commas, colons, or pipes—you must override this behavior.

## 2. Changing the Field Separator with -F

To use a colon (`:`) as the separator:

```bash theme={null}
$ awk -F ":" '{ print $1 }' sizeV1.txt
```

```text theme={null}
Filesystem
udev
tmpfs
/dev/sda1
...
```

Print the second field:

```bash theme={null}
$ awk -F ":" '{ print $2 }' sizeV1.txt
```

```text theme={null}
Size
1.8G
366M
...
```

Combine fields 1 and 5:

```bash theme={null}
$ awk -F ":" '{ print $1, $5 }' sizeV1.txt
```

```text theme={null}
Filesystem Use%
udev 0%
tmpfs 3%
...
```

You can also pipe data into `awk`:

```bash theme={null}
$ cat sizeV1.txt | awk -F ":" '{ print $2 }'
```

## 3. Why Quote or Escape the Separator

Certain characters (for example, `|`, `&`, `*`, `<`, `>`) have special meanings to the shell.

> **triangle-alert** Always quote or escape the field separator to prevent shell interpretation.

  Incorrect:

  ```bash theme={null}
  awk -F | '{ print $1 }' employees.txt
  ```

  This fails because `|` is seen as a pipe.

  Correct:

  ```bash theme={null}
  awk -F "|" '{ print $1 }' employees.txt
  # or
  awk -F \| '{ print $1 }' employees.txt
  ```

![The image shows a tip about using the awk command with a field separator, suggesting to enclose the character in double quotes for literal values. There's also a lightbulb icon and a checkmark.](../../../../images/kodekloud.com/kk-media/image/upload/v1752868665/notes-assets/images/Advanced-Bash-Scripting-Option-F/awk-command-field-separator-tip.jpg)

## 4. Common Field Separators

| Separator | Shell Meaning       | Example Use Case  |
| --------- | ------------------- | ----------------- |
| :         | None                | `/etc/passwd`     |
| ,         | None                | CSV export        |
| \|        | Pipe (must escape)  | Database output   |
| \t        | Tab (escape \t)     | TSV files         |
| =         | Assignment (escape) | Key-value configs |

![The image shows a list of special characters separated by dotted lines, under the heading "awk -F - Field Separator."](../../../../images/kodekloud.com/kk-media/image/upload/v1752868666/notes-assets/images/Advanced-Bash-Scripting-Option-F/awk-field-separator-special-characters.jpg)

## 5. Example: Processing Database Output

Here’s a Bash script (`db.sh`) that runs a PostgreSQL query inside Docker, trimming each field:

```bash theme={null}
#!/usr/bin/env bash
docker_run() {
  docker exec -i employees_db psql -U postgres -d employees -tAQ <<EOF
SELECT
  trim(id_employee::text),
  trim(first_name),
  trim(last_name),
  trim(area),
  trim(job_title),
  trim(email),
  trim(salary::text)
FROM "employee";
EOF
}
docker_run > employees.txt
exit 0
```

View the output:

```bash theme={null}
$ cat employees.txt
```

```text theme={null}
1|Kriti|Shreshtha|Finance|Financial Analyst|kriti.shreshtha@company.com|60000
...
```

Extract first names (field 2):

```bash theme={null}
$ awk -F "|" '{ print $2 }' employees.txt
```

```text theme={null}
Kriti
Rajasekar
Debbie
...
```

> **lightbulb** See the [GNU Awk User’s Guide](https://www.gnu.org/software/gawk/manual/html_node/Options.html) for more `awk` options.

## Next Steps

Next, we’ll explore the **-v** option to declare variables within `awk`:

```bash theme={null}
usage: awk [-F fs] [-v var=value] [-f progfile | 'prog'] [file ...]
```

## References

* [GNU Awk Manual](https://www.gnu.org/software/gawk/manual/)
* [awk(1) — Linux manual page](https://man7.org/linux/man-pages/man1/awk.1.html)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0cddb337-89d3-4068-a878-37a0a342c22f/lesson/b0829d7f-bdad-408b-a726-7f2299926b5b)
