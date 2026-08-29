# or make it executable and run
$ chmod +x hello.awk
$ ./hello.awk
Hello, World!
```

2. Bash + awk hybrid (invoke awk from a Bash script)

* Use a Bash shebang and embed an awk program string (usually single-quoted) or invoke awk with `-f` using separate files.
* Pros: Combine shell utilities and environment with awk’s text-processing power.
* Cons: Awk code is quoted inside shell; careful quoting is required.

Example (hello.sh):

```bash theme={null}
#!/usr/bin/env bash

awk 'BEGIN {
    print "Hello, World!"
}'
```

Run by making executable and using `./`:

```bash theme={null}
$ chmod +x hello.sh
$ ./hello.sh
Hello, World!
```

Why the quoting matters

Because the awk program is passed as an argument from the shell in the hybrid style, you must quote it (single quotes are typically used) to prevent the shell from interpreting awk syntax, variables, or braces.

Variable passing and declaration differences

Typically, when invoking awk from a shell (either on the command line or from a Bash script), you use `-v` to pass variables from the shell into awk. In a pure awk program you normally assign variables inside the script (for example, in `BEGIN`).

Pure awk script (hello-v1.awk):

```awk theme={null}
#!/usr/bin/env awk -f

BEGIN {
    hello = "Hello, World"
    print hello
}
```

Run:

```bash theme={null}
$ awk -f hello-v1.awk
Hello, World
```

Bash + awk hybrid (hello-v2.sh):

```bash theme={null}
#!/usr/bin/env bash

awk -v hello="Hello, World!" 'BEGIN {
    print hello
}'
```

Run:

```bash theme={null}
$ chmod +x hello-v2.sh
$ ./hello-v2.sh
Hello, World!
```

Practical reason: using `-v` lets the shell provide values to awk safely and predictably, avoiding issues with quoting and shell expansion.

<Frame>
  <img alt="A presentation slide titled &#x22;awk Programs From Files&#x22; noting that awk syntax in a bash script is equivalent to running awk commands in the terminal and that variable declaration syntax differs in pure awk programs. A footer announces an upcoming comparison of field separator syntax between awk hybrid scripts and pure awk programs." />
</Frame>

Field separator examples (two styles)

Pure awk script (separator.awk) using `BEGIN` to set `FS`:

```awk theme={null}
#!/usr/bin/env awk -f

BEGIN {
    FS = "|"
}

{
    print $2, $3
}
```

Bash + awk hybrid (separator.sh) using `-F`:

```bash theme={null}
#!/usr/bin/env bash

awk -F "|" '{
    print $2, $3
}'
```

Both scripts print the second and third fields (e.g., first and last names) when records are pipe-separated. Example output for `employees.txt`:

```bash theme={null}
$ ./separator.sh < employees.txt
Kriti Shrestha
Rajasekar Vasudevan
Debbie Miller
Enrique Rivera
Feng Lin
Andy Luscomb
Mark Crocker
Jing Ma

$ awk -f separator.awk < employees.txt
Kriti Shrestha
Rajasekar Vasudevan
Debbie Miller
Enrique Rivera
Feng Lin
Andy Luscomb
Mark Crocker
Jing Ma
```

Which style should you prefer?

* For this course and many shell-focused workflows, the Bash + awk hybrid is preferred because it shows how awk integrates with shell constructs like pipes, environment variables, command substitution, and the `set` command.
* For larger, standalone text-processing utilities or when distributing an awk tool to users who expect a single awk file, a pure awk script is often cleaner and more idiomatic.

Summary

In this lesson you learned:

* How to run awk programs from files using `awk -f script` or by making the file executable with a shebang (e.g., `#!/usr/bin/env awk -f`).
* The two main styles: pure awk scripts vs. Bash scripts that invoke awk.
* Practical differences in quoting, passing variables (`-v` vs assigning in `BEGIN`), and field-separator handling (`-F` vs `FS`).
* Which style is typically preferred in shell-focused lessons and when to choose a pure awk script instead.

Links and references

* GNU Awk Manual: [https://www.gnu.org/software/gawk/manual/](https://www.gnu.org/software/gawk/manual/)
* awk (Wikipedia): [https://en.wikipedia.org/wiki/Awk](https://en.wikipedia.org/wiki/Awk)
* env command (GNU coreutils): [https://www.gnu.org/software/coreutils/manual/html\_node/env-invocation.html](https://www.gnu.org/software/coreutils/manual/html_node/env-invocation.html)

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0cddb337-89d3-4068-a878-37a0a342c22f/lesson/41130575-a66f-44a7-a358-c07d27c09e3f)


# Option v

Source: https://notes.kodekloud.com/docs/Advanced-Bash-Scripting/awk/Option-v/page

Explains using awk -v to set variables before execution with examples, best practices, and filtering demos using a sample employees dataset

The -v option in awk sets variables before the awk program or action block runs. Declaring variables this way keeps configuration separate from program logic, makes one-liners easier to read, and improves reusability for scripts and pipelines.

<Frame>
  <img alt="A presentation slide titled &#x22;awk -v Variables&#x22; with a large &#x22;$ awk&#x22; logo in the center. Below it is the subtitle &#x22;Domain-Specific Language&#x22; inside a dotted rounded rectangle." />
</Frame>

## Simple example: use -v with a BEGIN block

This example sets a variable named `var` before the program executes and prints it from a `BEGIN` block. `BEGIN` runs before awk reads any input.

```bash theme={null}
$ awk -v var="Hello, World!" 'BEGIN { print var }'
Hello, World!
```

## Notes on placement and behavior

* The `-v` flag is an option to the `awk` command and is typically placed among other options.
* For portability and clarity, place `-F` (custom field separator) before `-v` when both are used.
* `BEGIN` runs before any input is processed — use it for initialization, printing headers, or other tasks that don't require input data.
* If you omit `BEGIN` and use an action like `{ print var }`, awk reads input (files or stdin) and executes the action for every input record. End interactive stdin with Ctrl+D on Unix-like systems.

> **lightbulb** When you need configuration values that may change (thresholds, prefixes, file names), pass them with `-v` instead of hard-coding them in the awk program — it improves readability and allows reusing the same script with different settings.

## Example — printing a variable for each input line (stdin)

```bash theme={null}
$ awk -v var="Hello, World!" '{ print var }'
passing input ........................
Hello, World!
passing input again ........................
Hello, World!
^D
```

(Press Ctrl+D to finish interactive stdin input.)

## Practical dataset: employees.txt

Use this sample data for the following examples. It's pipe-delimited with fields:

1. ID
2. First name
3. Last name
4. Department
5. Job title
6. Email
7. Salary

```bash theme={null}
$ cat employees.txt
1|Kriti|Shreshtha|Finance|Financial Analyst|kriti.shreshtha@company.com|60000
2|Rajasekar|Vasudevan|Finance|Senior Accountant|rajasekar.vasudevan@company.com|75000
3|Debbie|Miller|IT|Software Developer|debbie.miller@company.com|80000
4|Enrique|Rivera|Marketing|Marketing Specialist|enrique.rivera@company.com|65000
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
7|Mark|Crocker|HR|HR Manager|mark.crocker@company.com|85000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

## Example — prefix first names with a descriptive variable

Use `-F "|" -v prefix="..."` to set the field separator and a descriptive prefix that will print before the first name field (`$2`):

```bash theme={null}
$ awk -F "|" -v prefix="Employee's First Name: " '{ print prefix, $2 }' employees.txt
Employee's First Name: Kriti
Employee's First Name: Rajasekar
Employee's First Name: Debbie
Employee's First Name: Enrique
Employee's First Name: Feng
Employee's First Name: Andy
Employee's First Name: Mark
Employee's First Name: Jing
```

Observations:

* `-v prefix="..."` defines a variable available inside the awk program.
* `-F "|" ` splits records on the pipe character; `$2` is the first name.
* The variable `prefix` is expanded inside the action block for each input record.

## Filtering by numeric field (salary)

Print employees earning 90,000 or more (salary is field `$7`):

```bash theme={null}
$ awk -F "|" '$7 >= 90000' employees.txt
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

### Parameterize the threshold with -v

Use `-v` to pass the salary threshold, making the command reusable without editing the awk program:

```bash theme={null}
$ awk -F "|" -v high_salary="90000" '$7 >= high_salary' employees.txt
5|Feng|Lin|Sales|Sales Manager|feng.lin@company.com|90000
6|Andy|Luscomb|IT|IT Manager|andy.luscomb@company.com|95000
8|Jing|Ma|Engineering|Engineering Manager|jing.ma@company.com|100000
```

Print only the first names of high earners:

```bash theme={null}
$ awk -F "|" -v high_salary="90000" '$7 >= high_salary { print $2 }' employees.txt
Feng
Andy
Jing
```

## Example — benchmark with two variables

Declare multiple variables by using multiple `-v` flags. This example finds employees earning \<= 65000 or >= 90000:

```bash theme={null}
$ awk -F "|" -v high_salary="90000" -v low_salary="65000" \
    '$7 >= high_salary || $7 <= low_salary { print $2 }' employees.txt
Kriti
Enrique
Feng
Andy
Jing
```

<Frame>
  <img alt="A dark-themed slide titled &#x22;awk -v Variables&#x22; showing a central &#x22;-v&#x22; icon and text advising to create meaningful variable names because they help quickly identify the program's purpose." />
</Frame>

## Summary and best practices

| Topic                | Recommendation                                                                     | Example                     |                  |
| -------------------- | ---------------------------------------------------------------------------------- | --------------------------- | ---------------- |
| Variable declaration | Use `-v name=value` to set variables before awk runs                               | `awk -v threshold=100 file` |                  |
| Field separator      | Place `-F` before `-v` for portability                                             | \`awk -F "                  | " -v n=1 '...'\` |
| Multiple variables   | Use one `-v` per variable                                                          | `-v a=1 -v b=2`             |                  |
| Numeric comparisons  | Quoted numeric strings work; awk converts strings to numbers when used numerically | `-v n="90000"`              |                  |
| Initialization       | Use `BEGIN` for startup tasks; omit `BEGIN` to process input records               | `BEGIN { print "Header" }`  |                  |

> **warning** Each `-v` sets a variable before awk begins. If you pass a variable name that matches an awk built-in or field name, you can shadow it — choose meaningful names (e.g., `high_salary`, `prefix`) to avoid collisions and improve maintainability.

Key takeaways:

* `-v` separates configuration from logic and improves clarity for one-liners and scripts.
* Place `-F` before `-v` for consistent behavior across awk implementations.
* Use clear variable names and pass numeric thresholds via `-v` to make scripts configurable.
* `BEGIN` executes prior to record processing; normal action blocks execute per input record.

## Links and references

* [GNU Awk User’s Guide](https://www.gnu.org/software/gawk/manual/gawk.html) — comprehensive reference for awk options and behavior
* [KornShell & awk examples](https://www.grymoire.com/Unix/Awk.html) — practical awk one-liners and tutorials

This lesson covered declaring and using variables in awk with `-v`, how they interact with `BEGIN` blocks and regular action blocks, and practical examples using a sample employees file.

- [Watch Video](https://learn.kodekloud.com/user/courses/advanced-bash-scripting/module/0cddb337-89d3-4068-a878-37a0a342c22f/lesson/3465090f-e249-4c9c-ab09-3fc1702fc617)
