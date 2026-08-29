# Search Text Files Using Regular Expressions Part 1 Create simple regular expressions containing several notational elements

Source: https://notes.kodekloud.com/docs/Linux-Professional-Institute-LPIC-1-Exam-101/GNU-and-Unix-Commands/Search-Text-Files-Using-Regular-Expressions-Part-1-Create-simple-regular-expressions-containing-several-notational-elements/page

Learn to use basic regex operators in Linux to effectively search and filter text in files with `grep`.

In Linux, regular expressions (regex) empower you to locate and filter text in files far beyond simple string matching. In this first part of our series, you will learn basic regex operators and how to craft simple yet powerful patterns with `grep`.

Imagine you need to extract every IPv4 address (e.g., `203.102.3.5`) from hundreds of configuration files. A naive approach that searches for “digit–dot–digit” (`[0-9]\.[0-9]`) would also match incomplete fragments like `1.2`. By combining regex operators, you can define precise constraints and avoid false positives:

![The image shows a grid of ten dark-themed code editor windows displaying configuration files with highlighted IP addresses. The text appears to be related to system or network configurations.](https://kodekloud.com/kk-media/image/upload/v1752881407/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Search-Text-Files-Using-Regular-Expressions-Part-1-Create-simple-regular-expressions-containing-several-notational-elements/dark-themed-code-editor-grid-ip-configs.jpg)

In mathematics, we often define a variable *x* by specifying its domain and constraints:

> Let *x* be an integer, *x* > 3, and *x* \< 8.\
> Then *x* ∈ .

![The image shows a mathematical puzzle with conditions for an integer ( x ) where ( x > 3 ) and ( x \< 8 ), with a sequence of numbers starting at 3 and ending at 8.](https://kodekloud.com/kk-media/image/upload/v1752881408/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Search-Text-Files-Using-Regular-Expressions-Part-1-Create-simple-regular-expressions-containing-several-notational-elements/mathematical-puzzle-integer-conditions.jpg)

Regular expressions use a similar principle: you combine operators to specify exactly what a match should look like. Below is a quick reference of common regex metacharacters:

| Metacharacter | Meaning                               |                  |
| ------------- | ------------------------------------- | ---------------- |
| `^`           | Anchor to the start of a line         |                  |
| `$`           | Anchor to the end of a line           |                  |
| `.`           | Any single character                  |                  |
| `*`           | Zero or more of the preceding element |                  |
| `+`           | One or more of the preceding element  |                  |
| `{n,m}`       | Between *n* and *m* occurrences       |                  |
| `?`           | Zero or one occurrence                |                  |
| \`            | \`                                    | Alternation (OR) |
| `[]`          | Character class                       |                  |
| `()`          | Grouping                              |                  |
| `[^ ]`        | Negated character class               |                  |

<Frame>
  ![The image displays a set of regex operators, including symbols like ^, \$, ., \*, +, \{}, ?, |, \[\], (), and \[^\].](https://kodekloud.com/kk-media/image/upload/v1752881408/notes-assets/images/Linux-Professional-Institute-LPIC-1-Exam-101-Search-Text-Files-Using-Regular-Expressions-Part-1-Create-simple-regular-expressions-containing-several-notational-elements/regex-operators-symbols-set.jpg)
</Frame>

## 1. Matching at the Beginning of a Line (`^`)

Consider a file `names.txt` containing:

```bash theme={null}
$ cat names.txt
adam
adnan
basam
samad
samuel
sheela
ravi
mausami
```

A plain search for `sam` returns any line with that substring:

```bash theme={null}
$ grep 'sam' names.txt
basam
samad
samuel
mausami
```

To match only lines that **start** with `sam`, prefix your pattern with `^`:

```bash theme={null}
$ grep '^sam' names.txt
samad
samuel
```

## 2. Matching at the End of a Line (`$`)

Similarly, to find entries ending in `sam`, append `$` to the pattern:

```bash theme={null}
$ grep 'sam$' names.txt
basam
```

You can also apply this to system files, for example, looking for lines in `/etc/login.defs` that end with the digit `7`:

```bash theme={null}
$ grep '7' /etc/login.defs
